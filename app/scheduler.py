from apscheduler.schedulers.background import BackgroundScheduler
from .crud import get_emails_by_status, update_email_status
from .mailer import send_mail
from .db_manager import get_session
from .models.email import EmailStatus

scheduler = BackgroundScheduler()

def send_pending_emails():
    session = next(get_session())
    try:
        emails = get_emails_by_status(session, EmailStatus.PENDING)
        for email in emails:
            data = email.model_dump()
            success = send_mail(data)
            status = EmailStatus.SENT if success else EmailStatus.FAILED
            update_email_status(session, email.id, status)
    finally:
        session.close()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(send_pending_emails, 'interval', minutes=1)
        scheduler.start()
        print("Scheduler started")
    else:
        print("Scheduler is already running")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("Scheduler stopped")
    else:
        print("Scheduler is not running")
