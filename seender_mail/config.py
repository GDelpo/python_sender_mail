import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Environment configuration
ENV = os.getenv("ENV", "development")

# EMAIL SMTP CONFIGURATION
HOST = os.getenv("MAIL_HOST")
USERNAME = os.getenv("MAIL_USERNAME")
PASSWORD = os.getenv("MAIL_PASSWORD")
PORT = os.getenv("MAIL_PORT", 465)

# LOGGING CONFIGURATION TOKEN, service into cloud
TOKEN_LOGGER = os.getenv("TOKEN_LOGGER")

# JWT CONFIGURATION
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# PATHS CONFIGURATION
PUBLIC_FOLDER = os.path.join(os.getcwd(), "public")

# DATABASE CONFIGURATION
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# File upload configuration
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB


