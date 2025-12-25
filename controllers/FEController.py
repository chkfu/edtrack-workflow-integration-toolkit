import logging
import pandas as pd
from PyQt5.QtWidgets import (
  QFrame, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea,
  QDialog
)
from controllers.ValidController import ValidController
from models.DataManager import DataManager


#  LOGGING

logger = logging.getLogger("FE_CONTROLLER")


# CLASS

class FEController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    self.data_manager = DataManager()
    logger.info("initialised sucessfully.")
    
  
  #  METHODS - SUPPORTING
  
  def search_editable_merged_dataset(self):
    #  Remarks: ensure merge_df store a copy in raw and proc versions
    #  Remarks: always use proc version for editing, takes raw version for reset
    merge_raw = self.app.merge_state.merge_raw
    merge_proc = self.app.merge_state.merge_proc
    if merge_proc is not None and not merge_proc.empty:
      target_df = merge_proc
    elif merge_raw is not None and not merge_raw.empty:
      merge_proc = merge_raw
      target_df = merge_proc
    else:
      err_msg: str = f"No merged dataset has been found. Failed to proceed further."
      self.app.comp_fact.build_reminder_box(title="Warning",
                                            txt_msg=err_msg)
      logger.warning(err_msg, exc_info=True)
      return
    return target_df
    
    
  #  METHODS - EVENTS
  
  def assign_remove_cols_event(self, target_df: pd.DataFrame, target_col_list: list) -> None:
    #  declaration
    output_df: pd.DataFrame = target_df.copy()
    #  validation
    #  remarks: data manager contains dataset and individual column validation
    if not isinstance(target_col_list, list):
      err_msg: str = "The target removal list is not valid. Unable to remove columns from merged dataset."
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=err_msg)
      logger.error(err_msg, exc_info=True)
      return
    #  execution
    for column in target_col_list:
      output_df = self.data_manager.remove_col(target_df=output_df, 
                                               target_col=column)
    self.app.merge_state.merge_proc = output_df
  
  
  
  
  #  METHODS - POPUP TRIGGERS
  
  def handle_remove_cols(self):
    popup = self.app.pages_fact.page_feateng.build_remove_cols_popup()
    popup.exec_()
  
  
  def handle_rename_cols(self) -> None:
    print("remove_spec_cols")
    pass
  
  
  def handle_filter_rows(self) -> None:
    print("remove_spec_value")
    pass
  
  
  def handle_time_feat(self) -> None:
    print("manage_time_feat")
    pass
  
  
  def handle_encoding(self) -> None:
    print("hash_name_cols")
    pass

  
  #  RESET
  
  def preview_proc_tb(self) -> None:
    print("preview_proc_tb")
    pass
  
  def reset_fe_page(self) -> None:
    print("reset_fe_page")
    pass
  

