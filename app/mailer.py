from .logger import logger
from .models.email import EmailModel
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP,SMTPException

from .config import HOST, PORT

def send_mail(data: dict | None = None):
    msg = EmailModel(**data)
    message = MIMEText(msg.body, "html")
    message["From"] = msg.from_email
    message["To"] = msg.to_email
    message["Cc"] = msg.to_cc_email
    message["Bcc"] = msg.to_cco_email
    message["Subject"] = msg.subject

    context = create_default_context()

    try:
        with SMTP(HOST, PORT) as server:
            server.send_message(message)
            server.quit()
        return True
    except SMTPException as e:
        logger.error(f"SMTP error while sending email: {e}")
        return False
    except Exception as e:
        logger.error(f"General error while sending email: {e}")
        return False


# VER COMO HACCER CON SMTP_SSL
# with SMTP_SSL(HOST, PORT, context=context) as server:
#             server.login(USERNAME, PASSWORD)