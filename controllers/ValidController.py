"""
This controller manages UI navigation with the changes of steps.
It bridges the UI events and the application's state changes, applying
preferred logic into user workflow.
"""

from views.components.config.views_config import RAW_COL_SCHEMA
from views.components.config.views_config import STEP_NAME_LIST
import logging
import pandas as pd

#  LOGGING

logger = logging.getLogger("VALID_CONTROLLER")


#  CLASS

class ValidController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    logger.info("initialised sucessfully.")
    
  
  #  METHODS
  
  def validate_col(self, 
                   target_df: pd.DataFrame, 
                   target_col: str) -> str:
    
    #  for index
    if target_col.strip().lower() == "index":
      return "index"
    #  for columns
    output = next((col for col in target_df.columns if col.strip().lower() == target_col.strip().lower()), None)
    if output is None:
      raise ValueError("target column is not found.")
    return output.strip()
  

  def validate_preview_df(self,
                          lb_text: str,
                          target_state: pd.DataFrame,
                          target_schema: dict) -> bool:
    expectation: str = target_schema[lb_text]
    
    # if schema not found, unable to match, failed
    if expectation is None:
        err_msg = f"{lb_text} is not in the target schema."
        logger.error(err_msg, exc_info=True)
        self.app.comp_fact.build_reminder_box("Error", err_msg)
        return False
    # if the col name list not matched, failed
    if expectation != list(target_state):
      err_msg = (f"Unexpected column names.\n"
              f"Expectated {expectation} but got {list(target_state.columns)}.")
      logger.error(err_msg, exc_info=True)
      self.app.comp_fact.build_reminder_box("Error", err_msg)
      return False
    
    return True