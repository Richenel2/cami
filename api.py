from flask import Flask
from ai import execute
from datetime import datetime

from flask_apscheduler import APScheduler

app = Flask(__name__)

scheduler = APScheduler()

@app.route('/execute')
def post_linkedin():
    execute()
    return 'Hello, World!'


@app.route('/')
def hello():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"Current Time = {current_time}"

@scheduler.task('interval', id='my_job', minute=40, hour = 18)
def my_job():
    execute()
    print('This job is executed every 10 seconds.')


if __name__ == '__main__':

    scheduler.init_app(app)

    scheduler.start()

    app.run()
