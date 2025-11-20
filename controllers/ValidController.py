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

logger = logging.getLogger("APPLICATION")


#  CLASS

class ValidController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    logger.info("[ValidController] initialised sucessfully.")
    
  
  #  METHODS

  def validate_preview_df(self,
                          lb_text: str,
                          target_state: pd.DataFrame,
                          target_schema: dict) -> bool:
    expectation: str = target_schema[lb_text]
    
    # if schema not found, unable to match, failed
    if expectation is None:
        err_msg = f"[ValidController] {lb_text} is not in the target schema."
        logger.error(err_msg, exc_info=True)
        self.app.comp_fact.build_reminder_box("Error", err_msg)
        return False
    # if the col name list not matched, failed
    if expectation != list(target_state):
      err_msg = (f"[ValidController] Unexpected column names.\n"
              f"Expectated {expectation} but got {list(target_state.columns)}.")
      logger.error(err_msg, exc_info=True)
      self.app.comp_fact.build_reminder_box("Error", err_msg)
      return False
    
    return True