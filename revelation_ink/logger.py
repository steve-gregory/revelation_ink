"""
Logging for django applications
Provides two separate log levels. One for dependencies and one for the application.

django's settings.py:
  ## logging imports
  import logging
  import django_app_name.logger
  ## logging
  DEBUG = True
  TEMPLATE_DEBUG = DEBUG
  LOGGING_LEVEL = logging.DEBUG
  DEP_LOGGING_LEVEL = logging.WARN#Logging level for dependencies.
  revelation_ink.logger.initialize(LOGGING_LEVEL, DEP_LOGGING_LEVEL)
example use:
  from django_app_name.logging import logger
  # ...
  logger.debug('debugorz')
  logger.info('infoz')

"""

from __future__ import absolute_import
import logging
import os.path
try:
  import json
except:
  import simplejson as json

logger = None

def logger_initialize(logger):
    """
    Customize the application logger.
    Examples of customization: Set formatter or change, add, remove handlers.
    """
    pass

def initialize(app_log_level, dep_log_level):
    """
    Initialize the root and application logger.
    """
    format = "%(asctime)s %(name)s-%(levelname)s [%(pathname)s %(funcName)s %(lineno)d] %(message)s"
    formatter = logging.Formatter(format)
    import revelation_ink
    log_file = os.path.join(revelation_ink.__file__,
			'..',
			'..',
			'logs/app.log')

    # Setup the root logging for dependencies, etc.
    logging.basicConfig(
        level = dep_log_level,
        format = format,
        filename = log_file,
        filemode = 'a+')

    # Setup and add separate application logging.
    global logger
    logger = logging.getLogger('revelation_ink')
    logger_initialize(logger)
    logger.setLevel(app_log_level) # required to get level to apply.

