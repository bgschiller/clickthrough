import clickthrough

import os
import shutil

from nose.tools import with_setup, assert_raises

def test_find_command():
    clickthrough.get_command('hello')
    clickthrough.get_command('hello.hello')

def test_find_on_bad_command():
    assert_raises(Exception, #should be more specific...
        clickthrough.get_command,
        'nonexistent')
    assert_raises(Exception,
        clickthrough.get_command,
        'hello.nonexistent')

def create_deep_module():
    os.mkdir('deeper_module')
    open('deeper_module/__init__.py','a').close()
    shutil.copy('hello.py','deeper_module/hello.py')

def destroy_deep_module():
    shutil.rmtree('deeper_module')

@with_setup(create_deep_module, destroy_deep_module)
def test_deeper_find_command():
    clickthrough.get_command('deeper_module.hello')
    clickthrough.get_command('deeper_module.hello.hello')

