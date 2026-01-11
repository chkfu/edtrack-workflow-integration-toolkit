import logging
import pandas as pd
from controllers.ValidController import ValidController
from models.DataManager import DataManager
from views.components.config.views_config import MERGE_METHOD_OPT


#  LOGGING

logger = logging.getLogger("ANALYSE_CONTROLLER")


# CLASS

class AnalyseController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    logger.info("initialised sucessfully.")
    
    
  #  METHODS 
  
