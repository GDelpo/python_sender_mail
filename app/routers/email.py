import os
from typing import Annotated, Optional
import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status, File, UploadFile
from sqlmodel import Session
from app.logger import logger

from ..utils import normalize_email
from ..crud import create_email, get_all_emails_by_service, get_email_by_id, get_emails_by_status_and_service, update_email_status
from ..db_manager import get_session
from ..mailer import send_mail
from ..models.user import UserModel
from ..models.email import EmailModel, EmailSchemaRequest, EmailSchemaResponse, EmailStatus
from ..security import get_current_active_user
from ..config import PUBLIC_FOLDER

router = APIRouter(
    prefix='/emails',
    tags=["emails"],
)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB

def validate_file(file: UploadFile):
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File type not allowed")
    if len(file.file.read()) > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large")
    file.file.seek(0)

def send_email_task(email_id: int, user_id: uuid.UUID):
    session = next(get_session())
    try:
        email = get_email_by_id(session, email_id, user_id)
        if email and email.status == EmailStatus.PENDING:
            success = send_mail(email.model_dump())
            status = EmailStatus.SENT if success else EmailStatus.FAILED
            update_email_status(session, email_id, user_id, status)
    except Exception as e:
        logger.error(f"Error sending email: {e}")
    finally:
        session.close()

@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_description="Email scheduled for sending")
def schedule_mail(
    request: EmailSchemaRequest, 
    background_tasks: BackgroundTasks,
    #file: UploadFile = File(None), 
    session: Session = Depends(get_session), 
    current_user: UserModel = Depends(get_current_active_user)
):
    email = EmailModel(
        from_email=normalize_email(request.from_email),
        to_email=normalize_email(request.to_email),
        to_cc_email=normalize_email(request.to_cc_email),
        to_cco_email=normalize_email(request.to_cco_email),
        subject=request.subject.strip(),
        body=request.body,
        status=EmailStatus.PENDING,
        owner_id=current_user.id
    )

    # if file:
    #     validate_file(file)
    #     try:
    #         service_dir = os.path.join(PUBLIC_FOLDER, current_user.service_name)
    #         os.makedirs(service_dir, exist_ok=True)
    #         file_path = os.path.join(service_dir, file.filename)
    #         with open(file_path, "wb") as f:
    #             f.write(file.file.read())
    #         email.attachment = file_path
    #     except Exception as e:
    #         logger.error(f"Error saving attachment: {e}")
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save attachment")

    email = create_email(session, email)
    background_tasks.add_task(send_email_task, email.id, email.owner_id)
    return {"id": email.id, "message": "Email scheduled for sending"}

@router.get("/", response_model=list[EmailSchemaResponse])
def list_emails(
    status: Annotated[Optional[str], Query(description="Status of the emails to filter by", regex="^(sent|pending)$")] = None,
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_active_user)
):
    if status:
        status_enum = EmailStatus.SENT if status == "sent" else EmailStatus.PENDING
        emails = get_emails_by_status_and_service(session, status_enum, current_user.id)
    else:
        emails = get_all_emails_by_service(session, current_user.id)
    return emails

@router.get("/{email_id}", response_model=EmailSchemaResponse)
def email_status(email_id: int, session: Session = Depends(get_session), current_user: UserModel = Depends(get_current_active_user)):
    email = get_email_by_id(session, email_id, current_user.id)
    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    return email
