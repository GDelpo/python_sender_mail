from datetime import datetime
import uuid
from sqlmodel import Session, select

from .utils import get_password_hash
from .models.email import EmailModel, EmailStatus
from .models.user import UserModel, UserSchemaRequest

# CRUD operations for UserModel
def get_user_by_id(session: Session, user_id: uuid.UUID):
    return session.get(UserModel, user_id)

def get_user_by_service_name(session: Session, service_name: str):
    statement = select(UserModel).where(UserModel.service_name == service_name)
    return session.exec(statement).first()

def create_service(session: Session, user: UserSchemaRequest):
    if get_user_by_service_name(session, user.service_name):
        return None
    db_user = UserModel(
        service_name=user.service_name,
        hashed_password=get_password_hash(user.password),
        is_active=True,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# CRUD operations for EmailModel
def create_email(session: Session, email_data: EmailModel):
    session.add(email_data)
    session.commit()
    session.refresh(email_data)
    return email_data

def update_email_status(session: Session, email_id: int, status: EmailStatus):
    email = get_email_by_id(session, email_id)
    if email:
        email.status = status
        email.sent_at = datetime.now()
        session.commit()
        session.refresh(email)
        return email
    return None

def get_email_by_id(session: Session, email_id: int):
    return session.get(EmailModel, email_id)

def get_sent_emails(session: Session):
    statement = select(EmailModel).where(EmailModel.status == EmailStatus.SENT.value)
    return session.exec(statement).all()

def get_pending_emails(session: Session):
    statement = select(EmailModel).where(EmailModel.status == EmailStatus.PENDING.value)
    return session.exec(statement).all()