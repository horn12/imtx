import logging
from imtx.settings import *

def debug(msg):
    if not DEBUG:
        return
    logging.debug(msg)
