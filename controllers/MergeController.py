import logging
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
import pandas as pd
from pandas.api.types import is_numeric_dtype
from models import DataManager
from states import CleanState, CleanDataState
from views.components.config.views_config import MERGE_METHOD_OPT


#  LOGGING

logger = logging.getLogger("MERGE_CONTROLLER")


# CLASS

class MergeController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    self.temp_merge_dataset: pd.DataFrame | None = None
    self.manage_model = DataManager()
    logger.info("initialised sucessfully.")
    
  
  def preview_selected_table(self, target_tb: str) -> None:
    print("preview_selected_table")
    pass
    
    
  def preview_merge_df(self) -> None:
    print("preview_merge_df")
    pass
  
  
  def manage_dd_table_event(self) -> None:
    print("manage_dd_table_event")
    pass
  
  
  def manage_dd_col_event(self) -> None:
    print("manage_dd_col_event")
    pass
  
  
  def manage_method_radio_event(self, target_txt: str) -> None:
    #  if not matched, pass
    if target_txt not in MERGE_METHOD_OPT.values():
      logger.error(f"The selected merge method is not invalid - {target_txt}.",
                   exc_info=True)
      return
    #  if matched, return recognisable merge method
    target_method: str = next(key for key, value in MERGE_METHOD_OPT.items()
                              if value == target_txt)
    self.app.merge_state.target_method = target_method
  
  
  def execute_merge_df(self) -> None:
    #  TODO: a pop-up window for preview is requried
    print("execute_merge_df")
    pass
    
    
  def reset_merge_page(self) -> None:
    #  TODO: UI is required to be reset
    self.temp_merge_dataset = None
    self.app.merge_state.reset_merge_ds()
    print("activated on reset merge page method")