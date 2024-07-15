import logging
import sys
from logtail import LogtailHandler

from app.config import TOKEN_LOGGER

# get token from config
token = TOKEN_LOGGER

# get logger
logger = logging.getLogger()

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create handlers
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')
better_stack_handler = LogtailHandler(source_token=token)

# set formatters
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add handlers to logger
logger.handlers = [stream_handler, file_handler, better_stack_handler]

# set log level
logger.setLevel(logging.INFO)
