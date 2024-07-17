from apscheduler.schedulers.background import BackgroundScheduler
from .crud import get_emails_by_status_and_service, update_email_status
from .mailer import send_mail
from .db_manager import get_session
from .models.email import EmailStatus
from app.logger import logger
import os

scheduler = BackgroundScheduler()

def send_pending_emails():
    session = next(get_session())
    try:
        emails = get_emails_by_status_and_service(session, EmailStatus.PENDING)
        for email in emails:
            data = email.model_dump()
            try:
                success = send_mail(data)
                status = EmailStatus.SENT if success else EmailStatus.FAILED
                update_email_status(session, email.id, status)
            except Exception as e:
                logger.error(f"Error processing email ID {email.id}: {e}")
                update_email_status(session, email.id, EmailStatus.FAILED)
        session.commit()
    except Exception as e:
        logger.error(f"Error in send_pending_emails: {e}")
        session.rollback()
    finally:
        session.close()

def start_scheduler():
    if not scheduler.running:
        interval_minutes = int(os.environ.get("SCHEDULER_INTERVAL_MINUTES", 1))
        scheduler.add_job(send_pending_emails, 'interval', minutes=interval_minutes)
        scheduler.start()
        logger.info("Scheduler started")
    else:
        logger.info("Scheduler is already running")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")
    else:
        logger.info("Scheduler is not running")
