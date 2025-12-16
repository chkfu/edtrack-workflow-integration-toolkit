import logging
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
import pandas as pd
from pandas.api.types import is_numeric_dtype
from models import DataManager
from states import CleanState, CleanDataState


#  LOGGING

logger = logging.getLogger("MERGE_CONTROLLER")


# CLASS

class MergeController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    self.manage_model = DataManager()
    logger.info("initialised sucessfully.")