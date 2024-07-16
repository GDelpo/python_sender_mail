import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# EMAIL SMTP CONFIGURATION
HOST = os.environ.get("MAIL_HOST")
USERNAME = os.environ.get("MAIL_USERNAME")
PASSWORD = os.environ.get("MAIL_PASSWORD")
PORT = os.environ.get("MAIL_PORT", 465)
# LOGGING CONFIGURATION TOKEN, service into cloud
TOKEN_LOGGER = os.environ.get("TOKEN_LOGGER")
# JWT CONFIGURATION
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))