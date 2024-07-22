import json
from typing import Annotated, Optional
import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, Query, status, File, UploadFile
from sqlmodel import Session
from seender_mail.logger import logger

from ..utils import normalize_email, save_attachment
from ..crud import create_email, get_all_emails_by_service, get_email_by_id, get_emails_by_status_and_service, update_email_status
from ..db_manager import get_session
from ..mailer import send_mail
from ..models.user import UserModel
from ..models.email import EmailModel, EmailSchemaRequest, EmailSchemaResponse, EmailStatus
from ..security import get_current_active_user

router = APIRouter(
    prefix='/emails',
    tags=["emails"],
)
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
async def schedule_mail(
    background_tasks: BackgroundTasks,
    payload: str = Form(..., description="JSON payload containing the email details"),
    file: UploadFile = File(None, description="Optional file to be attached"),
    session: Session = Depends(get_session), 
    current_user: UserModel = Depends(get_current_active_user)
):
    try:
        # Check if the payload is a valid JSON
        email_request = EmailSchemaRequest.model_validate_json(payload)
        # Create the email object with the data from the request validated
        email = EmailModel(
            from_email=normalize_email(email_request.from_email),
            to_email=normalize_email(email_request.to_email),
            to_cc_email=normalize_email(email_request.to_cc_email),
            to_cco_email=normalize_email(email_request.to_cco_email),
            subject=email_request.subject.strip(),
            html_body=email_request.html_body,
            status=EmailStatus.PENDING,
            owner_id=current_user.id
        )
        # Save the attachment if it exists
        if file:
            file_path = await save_attachment(file, current_user)
            if file_path is None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save attachment")
            email.attachment = file_path

        # Create the email in the database
        email = create_email(session, email)
        # Schedule the email for sending
        background_tasks.add_task(send_email_task, email.id, email.owner_id)
        # Return the response with the email id and a message
        return {"id": email.id, "message": "Email scheduled for sending"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format", "status_code": status.HTTP_400_BAD_REQUEST}
    except ValueError as e:
        return {"error": str(e), "status_code": status.HTTP_400_BAD_REQUEST}

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
