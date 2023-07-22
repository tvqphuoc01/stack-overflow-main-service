#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import datetime as dt
import time
from scheduler import Scheduler


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_service.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    from api.jobs.job import approve_question_auto, approve_answer_auto, approve_reply_auto
    schedule = Scheduler()
    schedule.cyclic(dt.timedelta(seconds=15), approve_question_auto)
    schedule.cyclic(dt.timedelta(seconds=15), approve_answer_auto)
    schedule.cyclic(dt.timedelta(seconds=15), approve_reply_auto)

    while True:
        schedule.exec_jobs()
        time.sleep(1)


if __name__ == '__main__':
    main()
