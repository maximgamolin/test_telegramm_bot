import time

import schedule

from models import User
from server import get_test


def job():
    users = User.select()
    for user in users:
        get_test(None, user)


if __name__ == '__main__':
    schedule.every(30).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
