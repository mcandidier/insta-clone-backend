from celery.decorators import task
from celery.utils.log import get_task_logger

from .emails import send_reset_password

logger = get_task_logger(__name__)


@task(name="send_reset_password_email")
def send_feedback_email_task(email, token):
    """sends an email when reset password form is filled successfully"""
    logger.info("Sent reset password email")
    return send_reset_password(email, token)
