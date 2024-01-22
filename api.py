from flask import Flask
from ai import execute
from datetime import datetime
app = Flask(__name__)


@app.route('/execute')
def post_linkedin():
    execute()
    return 'Hello, World!'


@app.route('/')
def hello():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"Current Time = {current_time}"