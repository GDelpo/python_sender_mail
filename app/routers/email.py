from typing import Annotated, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlmodel import Session

from ..utils import normalize_email
from ..crud import create_email, get_all_emails, get_email_by_id, get_emails_by_status, update_email_status
from ..db_manager import get_session
from ..mailer import send_mail
from ..models.user import UserModel
from ..models.email import EmailModel, EmailSchemaRequest, EmailSchemaResponse, EmailStatus
from ..security import get_current_active_user

router = APIRouter(
    prefix='/emails',
    tags=["emails"],
)

def send_email_task(email_id: int):
    session = next(get_session())
    try:
        email = get_email_by_id(session, email_id)
        if email and email.status == EmailStatus.PENDING:
            success = send_mail(email.model_dump())
            status = EmailStatus.SENT if success else EmailStatus.FAILED
            update_email_status(session, email_id, status)
    finally:
        session.close()

@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_description="Email scheduled for sending")
def schedule_mail(request: EmailSchemaRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session), current_user: UserModel = Depends(get_current_active_user)):
    email = EmailModel(
        from_email=normalize_email(request.from_email),
        to_email=normalize_email(request.to_email),
        to_cc_email=normalize_email(request.to_cc_email),
        to_cco_email=normalize_email(request.to_cco_email),
        subject=request.subject,
        body=request.body,
        status=EmailStatus.PENDING.value
    )
    email = create_email(session, email)
    background_tasks.add_task(send_email_task, email.id)
    return {"id": email.id, "message": "Email scheduled for sending"}

@router.get("/", response_model=list[EmailSchemaResponse])
def list_emails(
    status: Annotated[Optional[str], Query(description="Status of the emails to filter by", regex="^(sent|pending)$")] = None,
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_active_user)
):
    if status:
        status_enum = EmailStatus.SENT if status == "sent" else EmailStatus.PENDING
        emails = get_emails_by_status(session, status_enum)
    else:
        emails = get_all_emails(session)
    return emails

@router.get("/{email_id}", response_model=EmailSchemaResponse)
def email_status(email_id: int, session: Session = Depends(get_session), current_user: UserModel = Depends(get_current_active_user)):
    email = get_email_by_id(session, email_id)
    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    return email




