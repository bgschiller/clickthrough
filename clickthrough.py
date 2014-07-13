import importlib
import sys

import click

from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

class ClickthroughError(Exception):
    pass

def get_command(command_location):
    '''Given a module name, find and return a command.
    '''
    try: #first, try module.command case
        module_name, command_name = command_location.rsplit('.', 1)
        module = importlib.import_module(module_name)
        command = getattr(module, command_name)
        assert isinstance(command, click.Command)
        return command
    except (AttributeError, ValueError): #Go searching for a command
        module = importlib.import_module(command_location)
        return find_command_in_module(module)
    except ImportError as e:
        raise ClickthroughError(e.message)

def find_command_in_module(module):
    commands = [getattr(module, a) for a in dir(module)
                    if not a.startswith('_') and
                    isinstance(getattr(module, a), click.Command)]
    if len(commands) > 1:
        raise ClickthroughError(
            "More than one command in that module (please be specific)")
    if len(commands) == 0:
        raise ClickthroughError(
            "No commands were found in that module")
    return commands.pop()

@click.command()
@click.argument('command')
def clickthrough(command):    
    app.command = get_command(command)
    app.run() 

@app.route('/')
def hello():
    return render_template('default.html',
        command=app.command,
        ctx=click.Context(app.command,info_name=app.command.name))

if __name__ == '__main__':
    clickthrough()
