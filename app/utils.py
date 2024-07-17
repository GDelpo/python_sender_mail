from passlib.context import CryptContext
from typing import Union, List, Optional

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
