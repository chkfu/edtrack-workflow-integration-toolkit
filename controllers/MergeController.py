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
    
    
  #  METHODS - VISUAL CHANGES
    
  def deliver_table_opts(self, target_tb: str) -> list:    
    table_opts: list = ["--- Please Select ---"]
    #  for single raw / cleaned dataframe - user_df, activity_df, component_df
    for data_state in self.app.clean_state.dataset_states.values():
      if data_state.data_clean is not None or data_state.data_raw is not None:
        table_opts.append(data_state.state_name)
        print(data_state.state_name)
    #  for merged dataframe
    if self.app.merge_state.merge_raw is not None:
      table_opts.append("Dataset - Merged")
      print("dataset - merged")
    return table_opts
    
    
  def deliver_col_opts(self, target_tb: str) -> list:
    tb_opt: str = str(target_tb).strip().lower()
    #  check the temporary table
    if tb_opt not in ["left", "right"]:
      logger.error(f"Failed to display column dropdowns for invalid table to be selected - {target_tb}",
                   exc_info=True)
      return
    #  check table and get corresponding columns
    if tb_opt == "left" and self.app.merge_state.target_ltable is not None:
      dd_list: list = self.app.merge_state.target_ltable.columns
    elif tb_opt == "right" and self.app.merge_state.target_ltable is not None:
      dd_list: list = self.app.merge_state.target_rtable.columns
    print(f"dd_list: {dd_list}")
    return dd_list
  
  
  #  METHODS - EVENTS
  
  def preview_selected_table(self, target_tb: str) -> None:
    print("preview_selected_table")
    
    
    
  def preview_merge_df(self) -> None:
    print("preview_merge_df")
    pass
  
  
  def manage_dd_table_event(self, target_tb: str) -> None:
    print("manage_dd_table_event")
    pass
  
  
  def manage_dd_col_event(self, target_tb: str) -> None:
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