from apscheduler.schedulers.background import BackgroundScheduler

from api.jobs.approve_question import approve_question
from api.jobs.approve_reply import approve_reply
from api.jobs.approver_answer import approve_answer

def scheduler():
    """
    This function used schedule all jobs.

    Parameters: None
    Returns: None
    """

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        approve_question,
        'interval',
        seconds=15
    )
    scheduler.add_job(
        approve_answer,
        'interval',
        seconds=15
    )
    scheduler.add_job(
        approve_reply,
        'interval',
        seconds=15
    )
    scheduler.start()