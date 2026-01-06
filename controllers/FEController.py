import logging
import pandas as pd
from PyQt5.QtWidgets import (
  QFrame, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea,
  QDialog, QMessageBox
)
from states.CleanDataState import CleanDataState
from controllers.ValidController import ValidController
from models.DataCleaner import DataCleaner
from models.DataManager import DataManager
from models.DataPreprocessor import DataPreprocessor
import re


#  LOGGING

logger = logging.getLogger("FE_CONTROLLER")


# CLASS

class FEController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    self.data_cleaner = DataCleaner()
    self.data_manager = DataManager()
    self.data_preproc = DataPreprocessor(data_manager=self.data_manager, 
                                         valid_cont=self.app.valid_cont)
    logger.info("initialised sucessfully.")
    
    
    
  #  METHODS - SUPPORTING
  
  def normalise_final_name(self, 
                           target_df: pd.DataFrame, 
                           new_name: str) -> str:
    
    final_name = str(new_name).strip() if new_name else "Untitled"
    #  prevent numeric start and spec_char start
    final_name = re.sub(r"[^A-Za-z0-9_-]", "", final_name)
    if not final_name:
      final_name = "Untitled"
    #  detect no alphabets
    if not final_name[0].isalpha() and final_name[0] != "_":
      final_name = f"Column_{final_name}"
    base_name = final_name
    #  prevent duplicates
    count = 1
    while final_name in target_df.columns:
        final_name = f"{base_name}_{count}"
        count += 1
    return final_name
        
        
  #  METHODS - EVENTS
  
  def assign_regulate_type_event(self, target_dict: dict) -> None:
    
    #  validation
    if not isinstance(target_dict, dict):
      err_msg: str = "The inserted item is not a dictionary."
      self.app.comp_fact.build_reminder_box(title="Type Error",
                                            txt_msg=err_msg)
      logger.warning(err_msg)
      return
    if not target_dict or len(target_dict) < 1:
      reminder_msg: str = "No type change has been specified. Data types remain unchanged."
      self.app.comp_fact.build_reminder_box(title="Type Error",
                                            txt_msg=reminder_msg)
      return
    
    #  execution
    try:
      for column, dtype in target_dict.items():
        if dtype == "datetime":
          self.app.merge_state.merge_proc = self.data_cleaner.spec_cleaning_datetime(target_df=self.app.merge_state.merge_proc,
                                                                                     target_col=column)
        elif dtype == "integer":
          self.app.merge_state.merge_proc = self.data_cleaner.spec_cleaning_int(target_df=self.app.merge_state.merge_proc,
                                                                                target_col=column)
        elif dtype == "float":
          self.app.merge_state.merge_proc = self.data_cleaner.spec_cleaning_float(target_df=self.app.merge_state.merge_proc,
                                                                                  target_col=column)
        elif dtype == "boolean":
          self.app.merge_state.merge_proc = self.data_cleaner.spec_cleaning_bool(target_df=self.app.merge_state.merge_proc,
                                                                                 target_col=column)
        else:
          self.app.merge_state.merge_proc = self.data_cleaner.spec_cleaning_str(target_df=self.app.merge_state.merge_proc,
                                                                                target_col=column)
      success_msg: str = f"Normalise data type successfully."
      self.app.comp_fact.build_reminder_box(title="Success",
                                            txt_msg=success_msg)
    except Exception as ex:
      err_msg: str = f"Failed to normalise data type - {ex}"
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=err_msg)
      logger.error(err_msg, exc_info=True)
        
    
  
  def assign_remove_cols_event(self, target_col_list: list) -> None:    
    #  validation
    #  remarks: data manager contains dataset and individual column validation
    if not isinstance(target_col_list, list):
      err_msg: str = "The target removal list is not valid. Unable to remove columns from merged dataset."
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=err_msg)
      logger.error(err_msg, exc_info=True)
      return
    #  execution
    output_df: pd.DataFrame = self.app.merge_state.merge_proc
    for column in target_col_list:
      output_df = self.data_manager.remove_col(target_df=output_df, 
                                               target_col=column)
    self.app.merge_state.merge_proc = output_df
    self.app.comp_fact.build_reminder_box(title="Success",
                                          txt_msg="Selected columns have been removed from the transformed dataset.")
  
  
  def assign_rename_col_event(self, target_dict: dict) -> None:
    
    #  validation
    if not isinstance(target_dict, dict) or len(target_dict) < 1:
      err_msg: str = "Failed to rename columns with invalid dictionary input."
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=err_msg)
      logger.warning(err_msg)
      return
    
    #  execution
    try:
      temp_list: list = []
      for column in list(target_dict.keys()):
        #  1. in-loop declaration
        
        
        final_name: str = self.normalise_final_name(target_df=self.app.merge_state.merge_proc,
                                                    new_name=target_dict[column])
        #  2. in-loop execution
        self.app.merge_state.merge_proc = self.data_manager.rename_col(target_df=self.app.merge_state.merge_proc, 
                                                                       target_col=column, 
                                                                       new_name=final_name)
        temp_list.append(f"{final_name} (prev: {column})")
      self.app.comp_fact.build_reminder_box(title="Success",
                                            txt_msg=f"Renamed {temp_list} for processed dataset successfully.")
    except Exception as ex:
      err_msg = "Failed to renamed columns for processed dataset. The action will be skipped."
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=f"{err_msg} - {ex}")
      
      
  
  def assign_time_feat_event(self, 
                             col_select: list, 
                             feat_select: list, 
                             keep_origin: bool=True) -> pd.DataFrame:
    
    try:
      output_df: pd.DataFrame = self.app.merge_state.merge_proc.copy()
      
      for column in col_select:   
        for feature in feat_select:
          output_df = self.data_preproc.create_dt_feat(target_df=output_df, 
                                                      target_col=column,
                                                      target_opt=feature)
        if not keep_origin:
          output_df = self.data_manager.remove_col(target_df=output_df, 
                                                  target_col=column)
      self.app.merge_state.merge_proc = output_df
      self.app.comp_fact.build_reminder_box(title="Success",
                                            txt_msg="Time features have been created for transformed dataset successfully.")
    except Exception as ex:
      err_msg = "Failed to create time features for processed dataset."
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=f"{err_msg} - {ex}")
      logger.error(err_msg, exc_info=True)
      return
    
    
    
  def assign_filter_rows_event(self, 
                               col_set: set, 
                               val_set: set) -> None:
    
    #  validation
    if not isinstance(col_set, set) or not isinstance(val_set, set):
      err_msg: str = "Invalid types. Failed to filter the designated valies with invalid data input."
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=err_msg)
      logger.warning(err_msg)
      return
    if len(col_set) < 1 or len(val_set) < 1:
      err_msg: str = "Invalid input. The size of selected columns or values cannot be emptied."
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=err_msg)
      logger.warning(err_msg)
      return
    
    #  execution
    try:
      temp_df = self.app.merge_state.merge_proc
      for column in col_set:
        temp_df = self.data_manager.remove_rows(target_df=temp_df,
                                                target_col=column,
                                                target_rows=list(val_set))
        self.app.merge_state.merge_proc = temp_df
      self.app.comp_fact.build_reminder_box(title="Success",
                                            txt_msg=f"Filtered rows {val_set} successfully.")
    except Exception as ex:
      err_msg = "Failed to filter rows for processed dataset."
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=f"{err_msg} - {ex}")
  
  
  def assign_encode_hash_event(self, encode_list=None, 
                               hash_list=None, 
                               opt_dict=None) -> None:
    
    #  declaration
    encode_list = encode_list or []
    hash_list = hash_list or []
    opt_dict = opt_dict or {}
    
    #  encoding with component code
    def operate_encoding() -> None:
      if encode_list is None or len(encode_list) < 1:
        logger.warning("Encoded list is empty. The encoding process will be skipped.")
        return
      for column in encode_list:
        if column not in self.app.merge_state.merge_proc.columns:
          continue
        else:
          comp_df: CleanDataState = self.app.clean_state.get_spec_dataframe(target_name="Dataset - Components").data_raw
          self.app.merge_state.merge_proc = self.data_preproc.encode_component_col(target_df=self.app.merge_state.merge_proc,
                                                                                   target_col=column,
                                                                                   code_df=comp_df,
                                                                                   dict_idx=list(comp_df.columns)[0],
                                                                                   dict_val=list(comp_df.columns)[1])
    
    #  regualte action
    def operate_regulate_action() -> None:
      if "action" not in opt_dict.keys():
        logger.warning("Failed to find the designated action column, regulating process will be skipped ")
        return
      if opt_dict["action"] is None or opt_dict["action"] not in self.app.merge_state.merge_proc.columns:
        logger.warning("Failed to find the designated action column, regulating process will be skipped ")
        return
      self.app.merge_state.merge_proc = self.data_preproc.regulate_actions(target_df=self.app.merge_state.merge_proc,
                                                                           target_col=opt_dict["action"])
      

    #  regulate target
    def operate_regulate_target() -> None:
      if "target" not in opt_dict.keys():
        logger.warning("Failed to find the designated target column, regulating process will be skipped ")
        return
      if opt_dict["target"] is None or opt_dict["target"] not in self.app.merge_state.merge_proc.columns:
        logger.warning("Failed to find the designated target column, regulating process will be skipped ")
        return
      self.app.merge_state.merge_proc = self.data_preproc.regulate_targets(target_df=self.app.merge_state.merge_proc,
                                                                           target_col=opt_dict["target"])
    
    #  hashing confidential
    def operate_hashing() -> None:
      if hash_list is None or len(hash_list) < 1:
        logger.warning("Hashing list is empty. The hashing process will be skipped.")
        return
      for column in hash_list:
        if column not in self.app.merge_state.merge_proc.columns:
          continue
        else:
          self.app.merge_state.merge_proc = self.data_preproc.hash_secret_col(target_df=self.app.merge_state.merge_proc,
                                                                              name_col=column)
      
    #  execution
    #  Remarks: regulate the values first, and thereby encoding collectively
    try:
      operate_regulate_action() 
      operate_regulate_target()
      operate_encoding()
      operate_hashing()
      self.app.comp_fact.build_reminder_box(title="Success",
                                            txt_msg="Encoding / hashing has been processed for transformed dataset.")
    except Exception as ex:
      err_msg: str = f"Failed to encode / hash the selected cells for transformed dataset - {ex}"
      self.app.comp_fact.build_reminder_box(title="Success",
                                            txt_msg=err_msg)
      logger.warning(err_msg)
    return
  
  
  #  METHODS - POPUP TRIGGERS
  
  def handle_regulate_type_cols(self) -> None:
    popup = self.app.pages_fact.page_feateng.handle_regulate_type_popup()
    popup.exec_()
  
  def handle_remove_cols(self):
    popup = self.app.pages_fact.page_feateng.build_remove_cols_popup()
    popup.exec_()
  
  
  def handle_rename_cols(self) -> None:
    popup = self.app.pages_fact.page_feateng.build_rename_cols_popup()
    popup.exec_()
  
  
  def handle_filter_rows(self) -> None:
    popup = self.app.pages_fact.page_feateng.build_filter_rows_popup()
    popup.exec_()
  
  
  def handle_time_feat(self) -> None:
    popup = self.app.pages_fact.page_feateng.build_time_feat_popup()
    popup.exec_()
    
  
  def handle_encoding(self) -> None:
    popup = self.app.pages_fact.page_feateng.build_encoding_cols_popup()
    popup.exec_()


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
        

