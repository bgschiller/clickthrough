from flask import Flask
import example

app = Flask(__name__)
app.DEBUG = True

@app.route('/')
def hello():
    return ('<pre>' +
        '\n'.join('{p.name} : {p.help}, defaults to {p.default}'.format(p=p)
            for p in example.hello.params)
        +'</pre>')

if __name__ == '__main__':
    app.run()
