from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import os
from .logger import logger
from .models.email import EmailModel
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP,SMTPException

from .config import HOST, PORT

def send_mail(data: dict | None = None):
    # Check if data is empty
    if not data:
        return False
    # Create an EmailModel instance
    msg = EmailModel(**data)
    # Create a MIMEMultipart message
    message = MIMEMultipart()
    # Set the message headers
    message["From"] = msg.from_email
    message["To"] = msg.to_email
    message["Cc"] = msg.to_cc_email
    message["Bcc"] = msg.to_cco_email
    message["Subject"] = msg.subject
    # Attach the message body
    message.attach(MIMEText(msg.html_body, "html"))
    # Attach the attachment if it exists
    attachment_path = msg.attachment
    if attachment_path:
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            filename = os.path.basename(attachment_path)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={filename}",
            )
            message.attach(part)
        except IOError as e:
            logger.error(f"Error opening attachment file {attachment_path}: {e}")
            return False

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