from main import app, db
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import requests

scheduler = BackgroundScheduler()
scheduler.start()


def call_update_room_status():
    url = 'http://localhost:5000/update_room_status'
    response = requests.get(url)
    if response.status_code == 200:
        print(f'Successfully called the API at {datetime.now()}')
    else:
        print(f'Failed to call the API at {datetime.now()}')


scheduler.add_job(
    call_update_room_status,
    IntervalTrigger(minutes=1)
)

try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
