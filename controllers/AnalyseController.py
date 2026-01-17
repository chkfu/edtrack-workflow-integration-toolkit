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

  #  Remarks: for updating analyse options into analyse state
  def analyse_dd_pivot_event(self, target_col: str, selected_text: str) -> None:
    if selected_text == "--- Please Select ---":
      return
    if target_col == "pivots_col_01":
      self.app.analyse_state.pivots_col_01 = selected_text
    elif target_col == "pivots_col_02":
      self.app.analyse_state.pivots_col_02 = selected_text
    elif target_col == "pivots_row_01":
      self.app.analyse_state.pivots_row_01 = selected_text
    elif target_col == "pivots_row_02":
      self.app.analyse_state.pivots_row_02 = selected_text
    elif target_col == "pivots_val_01":
      self.app.analyse_state.pivots_val_01 = selected_text
    else:
      return
    
    
  # Remarks: generate list for dropdown options
  def deliver_col_opts(self, target_tab: str) -> list:
    include_list: list = [col for col in self.app.merge_state.merge_proc.columns]
    return ["--- Please Select ---", *include_list]
  
  
  
