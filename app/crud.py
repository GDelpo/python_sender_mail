from datetime import datetime, timezone
import uuid
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from .utils import get_password_hash
from .models.email import EmailModel, EmailStatus
from .models.user import UserModel, UserSchemaRequest
from app.logger import logger

# CRUD operations for UserModel - Service authentication
def get_user_by_id(session: Session, user_id: uuid.UUID):
    try:
        return session.get(UserModel, user_id)
    except SQLAlchemyError as e:
        logger.error(f"Error fetching user by ID: {e}")
        return None

def get_user_by_service_name(session: Session, service_name: str):
    statement = select(UserModel).where(UserModel.service_name == service_name)
    try:
        return session.exec(statement).first()
    except SQLAlchemyError as e:
        logger.error(f"Error fetching user by service name: {e}")
        return None

def create_service(session: Session, user: UserSchemaRequest):
    if get_user_by_service_name(session, user.service_name):
        return None
    db_user = UserModel(
        service_name=user.service_name,
        hashed_password=get_password_hash(user.password),
        is_active=True,
    )
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        logger.error(f"Error creating service: {e}")
        session.rollback()
        return None

# CRUD operations for EmailModel
def create_email(session: Session, email_data: EmailModel):
    try:
        session.add(email_data)
        session.commit()
        session.refresh(email_data)
        return email_data
    except SQLAlchemyError as e:
        logger.error(f"Error creating email: {e}")
        session.rollback()
        return None

def update_email_status(session: Session, email_id: int, user_id: uuid.UUID, status: EmailStatus):
    email = get_email_by_id(session, email_id, user_id)
    if email:
        email.status = status
        email.sent_at = datetime.now(timezone.utc)
        try:
            session.commit()
            session.refresh(email)
            return email
        except SQLAlchemyError as e:
            logger.error(f"Error updating email status: {e}")
            session.rollback()
            return None
    return None

def get_email_by_id(session: Session, email_id: int, user_id: uuid.UUID):
    statement = select(EmailModel).where(EmailModel.id == email_id).where(EmailModel.owner_id == user_id)
    try:
        return session.exec(statement).first()
    except SQLAlchemyError as e:
        logger.error(f"Error fetching email by ID: {e}")
        return None

def get_all_emails_by_service(session: Session, user_id: uuid.UUID):
    statement = select(EmailModel).where(EmailModel.owner_id == user_id)
    try:
        return session.exec(statement).all()
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all emails by service: {e}")
        return None

def get_emails_by_status_and_service(session: Session, status: EmailStatus, user_id: uuid.UUID):
    statement = select(EmailModel).where(EmailModel.status == status.value).where(EmailModel.owner_id == user_id)
    try:
        return session.exec(statement).all()
    except SQLAlchemyError as e:
        logger.error(f"Error fetching emails by status and service: {e}")
        return None
