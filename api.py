from flask import Flask
from ai import execute

app = Flask(__name__)


@app.route('/execute')
def hello():
    execute()
    return 'Hello, World!'


@app.route('/')
def hello():
    return 'Hello, World!'