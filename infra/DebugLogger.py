import logging
import sys
import os



#  CLASS

class DebugLogger:
  
  #  CONSTRUCTOR
  
  def __init__(self):
    print("[DebugLogger] initialised sucessfully.")
    
  
  #  METHODS
  
  #  leanrt: reusable solution for logger
  def setup_app_logger(self, logger_name="APPLICATION", file_name=None):
    
    #  1. setup logger and customised format
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    """
    DEBUG: for diagnosing potential issues for development stage
    INFO: for normal workflow records
    WARNING: for identifying strange behaviors while keep running
    ERROR: for raising errors reminder while keep running
    CRITICAL: for system crash
    **  the levels refers to the barrier:
        as DEBUG the most tightest, while CRITICAL the least
    """
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    """
    asctime: time
    name: logger's name
    levelname: the level of logging
    message: logging messages
    """
    
    #  2. the handler adopt the format
    stream_handler = logging.StreamHandler(sys.stdout)
    """
    Here, sys.stdout is the conduit for communication
    stdin: receive input
    stdout: response
    stderr: warning with error messages
    """
    #  learnt: the handler will use the customised msg style for its logs
    stream_handler.setFormatter(formatter)
    
    #  3. the logger adopt the handler
    logger.handlers.clear()
    logger.addHandler(stream_handler)
    
    #  4. if prev log existed, assign the file handler for update
    if file_name:
      #  learnt: required to regulate the location in infra/
      base_directory = os.path.dirname(os.path.abspath(__file__))
      log_path = os.path.join(base_directory, file_name)
      #  leant: after got the log_path, put it into FileHandler
      file_handler = logging.FileHandler(log_path, encoding='utf-8')
      file_handler.setFormatter(formatter)
      #  the logger finally adopt the handler
      logger.addHandler(file_handler)
    
    #  5. output
    return logger
      
      

   
    