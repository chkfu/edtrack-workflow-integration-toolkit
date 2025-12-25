import logging
import pandas as pd
from PyQt5.QtWidgets import (
  QFrame, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea,
  QDialog, QMessageBox
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
    output_df = target_df.copy()
    for column in target_col_list:
      output_df = self.data_manager.remove_col(target_df=output_df, 
                                               target_col=column)
    self.app.merge_state.merge_proc = output_df
    self.app.comp_fact.build_reminder_box(title="Success",
                                          txt_msg="Selected columns have been removed from the transformed dataset.")
  
  
  
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


  def preview_proc_tb(self) -> None:
    target_df: pd.DataFrame = self.app.merge_state.merge_proc
    if target_df is None or target_df.empty:
      return self.app.comp_fact.build_reminder_box(title="Error", 
                                                   txt_msg="Please ensure the merged table for feature engineering is valid.")
    popup_wd = self.app.comp_fact.build_popup_wd(wd_title="Preview Table Options",
                                                target_df=self.app.merge_state.merge_proc,
                                                popup_title="Preview Transformed Dataset",
                                                popup_content=self.app.comp_fact.build_table_view(target_df=self.app.merge_state.merge_proc))
    return popup_wd
  
  
  #  RESET
  
  def reset_fe_page(self) -> None:
    auth= self.app.comp_fact.build_msg_box(title="Confirmation", 
                                           question="Are you sure to revert to the original merged dataset?")
    if auth == True:
      merge_raw: pd.DataFrame = self.app.merge_state.merge_raw
      if merge_raw is not None and not merge_raw.empty:
        self.app.merge_state.merge_proc = merge_raw.copy()
        self.app.comp_fact.build_reminder_box(title="Success",
                                              txt_msg="Transoformed dataset has been reset.")
      else:
        err_msg: str = f"No original merged dataset has been found. Failed to reset transformed dataset."
        self.app.comp_fact.build_reminder_box(title="Warning",
                                              txt_msg=err_msg)
        logger.warning(err_msg, exc_info=True)
        return
        

