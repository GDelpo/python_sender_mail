import os
from fastapi import HTTPException, UploadFile, status
from passlib.context import CryptContext
from typing import Union, List, Optional

from .config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, PUBLIC_FOLDER
from .models.user import UserModel
from .logger import logger

# Bcrypt hashing algorithm and methods for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Email normalization
def normalize_email(email: Union[str, List[str], None]) -> Optional[str]:
    if email:
        if isinstance(email, list):
            return ",".join(email).strip().lower()
        return email.strip().lower()
    return None    

# File upload functions
import aiofiles
import aiofiles.os as async_os

async def validate_file(file: UploadFile):
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="File type not allowed")
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")
    file.file.seek(0)  # Esta operación podría no ser necesaria dependiendo de cómo manejas el archivo después
    return content  # Devuelve el contenido para no tener que leer el archivo de nuevo

async def save_attachment(file: UploadFile, current_user: UserModel) -> Optional[str]:
    try:
        content = await validate_file(file)  # Asegúrate de leer el archivo una sola vez
        service_dir = os.path.join(PUBLIC_FOLDER, current_user.service_name)
        await async_os.makedirs(service_dir, exist_ok=True)
        file_path = os.path.join(service_dir, file.filename)
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)
        return file_path
    except Exception as e:
        logger.error(f"Error saving attachment: {e}")