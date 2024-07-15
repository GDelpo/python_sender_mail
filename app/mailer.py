from app.logger import logger
from .models.email import EmailModel
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP

from .config import HOST, PORT, USERNAME, PASSWORD

def send_mail(data: dict | None = None):
    msg = EmailModel(**data)
    message = MIMEText(msg.body, "html")
    message["From"] = msg.from_email
    message["To"] = msg.to_email
    message["Cc"] = msg.to_cc_email
    message["Bcc"] = msg.to_cco_email
    message["Subject"] = msg.subject.strip()

    #ctx = create_default_context()

    try:
        with SMTP(HOST, PORT) as server:
            # server.starttls(context=ctx)
            # server.login(USERNAME, PASSWORD)
            server.send_message(message)
            server.quit()
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False
