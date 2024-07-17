import logging
import sys
from logtail import LogtailHandler
from .config import TOKEN_LOGGER, ENV

# Get logger
logger = logging.getLogger()

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create handlers
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')
#logtail_handler = LogtailHandler(source_token=TOKEN_LOGGER)

# Set formatters
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
#logtail_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
#logger.addHandler(logtail_handler)

# Set log level
logger.setLevel(logging.DEBUG if ENV == "development" else logging.INFO)
