from passlib.context import CryptContext

# Configuración de bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def normalize_email(email: str) -> str:
    if email:
        if isinstance(email, list):
            return ",".join(email).strip().lower()
        return email.strip().lower()
    return None