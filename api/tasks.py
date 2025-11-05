import time

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3)
def process_data(self, data):
    """
    Example task that processes data
    """
    try:
        logger.info(f"Processing data: {data}")
        # Simulate long-running task
        time.sleep(5)
        result = {"status": "success", "data": data, "processed": True}
        logger.info(f"Data processed successfully: {result}")
        return result
    except Exception as exc:
        logger.error(f"Error processing data: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task
def send_email(email, subject, message):
    """
    Example task to send email
    """
    logger.info(f"Sending email to {email}")
    # Simulate email sending
    time.sleep(2)
    logger.info(f"Email sent to {email}")
    return {"email": email, "sent": True}


@shared_task
def send_daily_report():
    """
    Scheduled task that runs daily
    """
    logger.info("Generating daily report...")
    # Add your report generation logic here
    time.sleep(3)
    logger.info("Daily report sent successfully")
    return {"report": "daily", "status": "sent"}


@shared_task
def cleanup_old_data():
    """
    Scheduled task to cleanup old data
    """
    logger.info("Cleaning up old data...")
    # Add your cleanup logic here
    time.sleep(2)
    logger.info("Old data cleaned up")
    return {"cleaned": True, "count": 0}


@shared_task
def health_check():
    """
    Periodic health check task
    """
    logger.info("Running health check...")
    return {"status": "healthy", "timestamp": time.time()}
