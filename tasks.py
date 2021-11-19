import time
import logging
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
        try:
            schedule.run_pending()
        except Exception as e:
            logging.exception("Не удалось отправить плановый тест")
            pass
        time.sleep(1)
