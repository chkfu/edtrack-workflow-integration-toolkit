"""
This controller bridges the models and views.
It specific become the wrapper of models' methods, enabling minor adjustment
and prevent directly changes to the data transformation logic.
"""


import logging
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
import pandas as pd
from pandas.api.types import is_numeric_dtype
from models.DataCleaner import DataCleaner
from controllers.ValidController import ValidController
from states import CleanDataState


#  LOGGING

logger = logging.getLogger("CLEAN_CONTROLLER")


# CLASS

class CleanController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    self.clean_model = DataCleaner()
    self.valid_cont = ValidController()
    logger.info("initialised sucessfully.")
    
    
  #  METHODS
  
  #  1. manage tab switching
  
  def handle_clean_tab_switch(self, target_index: int):
    if target_index == 0:
      self.app.clean_state.set_clean_target(target_index)
    elif target_index == 1:
      self.app.clean_state.set_clean_target(target_index)
    elif target_index == 2:
      self.app.clean_state.set_clean_target(target_index)
    else:
      return
    
    
  def handle_clean_dup_cols(self, target_state: int, target_name: str) -> None:
    if target_state is None:
      return
    # successful case
    curr_ds = self.app.clean_state.get_clean_target()
    if target_state == Qt.Checked:
      curr_ds.set_handle_duplicate_cols(target_action="push",
                                        target_col=target_name)
    else:
      curr_ds.set_handle_duplicate_cols(target_action="pull",
                                        target_col=target_name)
    
    
  #  2. manage radio buttons
  
  #  2a. remove duplicates
  
  def handle_clean_dup_opt(self, target_list: list, text: str, checked: bool):
    # validate list
    if not isinstance(target_list, list):
      err_msg: str = "The option list is not applied in handling duplicates option."
      logger.error(err_msg, exc_info=True)
      raise TypeError(err_msg)
    
    #  check cases
    curr_ds = self.app.clean_state.get_clean_target()
    if text == target_list[1]:
      curr_ds.set_enable_duplicate(False)
      return
    elif text == target_list[0]:
      if checked:
        popup = self.app.pages_fact.page_clean.build_dup_popup()
        popup.exec_()
        #  remarks: activate after popup. keep off if not selected
        if curr_ds.handle_duplicate_cols:
          curr_ds.set_enable_duplicate(True)
        else:
          curr_ds.set_enable_duplicate(False)
      return
    
    else: 
      return
    
    
  def select_clean_dup_dropdown(self, selected_opt: str, opt_list: list, cb_list: list):
    
    if not isinstance(cb_list, list):
      err_msg: str = "The input checkbox list is not valid for cleaning dupliacate options."
      logger.error(err_msg, exc_info=True)
      raise TypeError(err_msg)
    if not isinstance(opt_list, list):
      err_msg: str = "The input option list is not valid for cleaning dupliacate options."
      logger.error(err_msg, exc_info=True)
      raise TypeError(err_msg)
    
    #  not selected, keep empty and require to make decision
    curr_ds_state = self.app.clean_state.get_clean_target()
    if selected_opt == opt_list[0]:
      for checkbox in cb_list:
        checkbox.setChecked(False)
        checkbox.setEnabled(False)
      curr_ds_state.set_handle_duplicate_cols(target_action="empty", 
                                              target_col=None)

    
    #  select all cols, all checked and disabled options
    elif selected_opt == opt_list[1]:
      for checkbox in cb_list:
        checkbox.setChecked(True)
        checkbox.setEnabled(False)
      full_cols = [checkbox.text() for checkbox in cb_list]
      curr_ds_state.set_handle_duplicate_cols(target_action="replace",
                                              target_col=full_cols)
    
    #  select specific cols, enable to reset and select options
    elif selected_opt == opt_list[2]:
      for checkbox in cb_list:
        checkbox.setChecked(False) 
        checkbox.setEnabled(True)
      curr_ds_state.set_handle_duplicate_cols(target_action="empty", 
                                              target_col=None)
      
    #  Option must be in the list with dropdown, case ignore
    else:
      return
  
  
  def select_clean_dup_checkbox(self, target_state: int, target_name: str) -> None:
    curr_ds_state = self.app.clean_state.get_clean_target()
    curr_status = (target_state == Qt.Checked)
    if curr_status and target_name not in curr_ds_state.handle_duplicate_cols:
      curr_ds_state.set_handle_duplicate_cols(target_action="push", target_col=target_name)
    elif not curr_status and target_name in curr_ds_state.handle_duplicate_cols:
      curr_ds_state.set_handle_duplicate_cols(target_action="pull", target_col=target_name)
    else:
      return
      
      
  def close_clean_dup_popup(self, target_popup: QDialog):
    if not isinstance(target_popup, QDialog):
      err_msg: str = "The close popup method only works for pop-up windows."
      logger.error(err_msg, exc_info=True)
      raise TypeError(err_msg)
    #  failed case: reminder box
    curr_ds = self.app.clean_state.get_clean_target()
    if curr_ds.handle_duplicate_cols == [] or len(curr_ds.handle_duplicate_cols) < 1:
      self.app.comp_fact.build_reminder_box(title="Warning", 
                                            txt_msg="Please ensure the target duplicate columns option has been set.")
      return
    #  successful case: close popup
    return target_popup.close()
  
  
  #  2b. handling blanks
  
  def handle_clean_blank_opt(self, target_list: list, text: str, checked: bool):
    # validate list
    if not isinstance(target_list, list):
      err_msg: str = "The option list is not applied in handling duplicates option."
      logger.error(err_msg, exc_info=True)
      raise TypeError(err_msg)
    
    temp_output = {}
    curr_ds = self.app.clean_state.get_clean_target()
    if text == target_list[0]:
      if checked:
        popup = self.app.pages_fact.page_clean.build_blank_popup()
        popup.exec_()
    elif text == target_list[1]:
      for column in curr_ds.data_raw.columns:
        temp_output[column] = {"method": "ignore", "value": None}
      curr_ds.set_handle_blanks(temp_output)
      return
    
    
  def get_blank_dropdown(self, target_series: pd.Series) -> list:
    NUM_OPT_LIST = ["--- Please Select ---", 
                    "Remain Unchanged",
                    "Remove Blanks",
                    "Fill Previous Value",
                    "Fill Next Value",
                    "Fill Numeric Mean",
                    "Fill Numeric Median",
                    "Fill Numeric Zeros"]
    NON_NUM_OPT_LIST =  ["--- Please Select ---", 
                        "Remain Unchanged",
                        "Remove Blanks",
                        "Fill Previous Value",
                        "Fill Next Value",
                        "Fill Default Text"]
    
    if is_numeric_dtype(target_series):
      return NUM_OPT_LIST
    return NON_NUM_OPT_LIST
  
  
  def select_blank_opt(self, target_col: str, selected_opt: str):
    #  remarks: options called from columns, false case not needed
    MATCHING = {
      "--- Please Select ---": {"method": "ignore", "value": None},
      "Remove Blanks": {"method": "drop", "value": None},
      "Fill Previous Value": {"method": "bfill", "value": None},
      "Fill Next Value": {"method": "ffill", "value": None},
      "Fill Default Text": {"method": "fill", "value": "(Not Specified)"},
      "Fill Numeric Mean": {"method": "mean", "value": None},
      "Fill Numeric Median": {"method": "median", "value": None},
      "Fill Numeric Zeros": {"method": "constant", "value": 0}
    }
    
    curr_ds = self.app.clean_state.get_clean_target()
    target_val = MATCHING.get(selected_opt, {"method": "ignore", "value": None})
    curr_ds.update_handle_blanks(target_col=target_col, target_val=target_val)
    
    
  def close_clean_blank_popup(self, target_popup: QDialog):
    if not isinstance(target_popup, QDialog):
      err_msg: str = "The close popup method only works for pop-up windows."
      logger.error(err_msg, exc_info=True)
      raise TypeError(err_msg)
    #  failed case: reminder box
    curr_ds_state = self.app.clean_state.get_clean_target()
    for column in curr_ds_state.data_raw.columns:
      if column not in curr_ds_state.handle_blanks:
        curr_ds_state.handle_blanks[column] = {"method": "ignore", "value": None}
    #  successful case: close popup
    return target_popup.close()
        
  
  #  2c. sorting options
  
  def handle_clean_sort_opt(self, target_list: list, text: str, checked: bool):
    
    # validate list
    if not isinstance(target_list, list):
      err_msg: str = "The option list is not applied in handling sorting option."
      logger.error(err_msg, exc_info=True)
      raise TypeError(err_msg)
    
    #  check cases
    curr_ds = self.app.clean_state.get_clean_target()
    if text == target_list[1]:
      curr_ds.set_enable_sort(False)
      curr_ds.set_sort_col(None)
      curr_ds.set_sort_ascending(None)
      return
    elif text == target_list[0]:
      curr_ds.set_enable_sort(True)
      #  Learnt: set none valuse before popup, otherwise, crash after reset
      curr_ds.set_sort_col(None)
      curr_ds.set_sort_ascending(None)   
      if checked:
        popup = self.app.pages_fact.page_clean.build_sort_popup()
        popup.exec_()
      return
    
    else: 
      return
    
    
  def handle_clean_sort_detail(self, target_col: str, target_isAsc: bool):
    curr_ds = self.app.clean_state.get_clean_target()
    #  validate column
    if not self.valid_cont.validate_col(target_df=curr_ds, target_col=target_col):
      logger.info("target column is not available for cleaning sort details.")
      return
    #  update state
    curr_ds.set_sort_col(target_col=target_col)
    curr_ds.set_sort_ascending(target_opt=target_isAsc)


  def select_sort_opt(self, selected_opt: str):
      #  remarks: options called from columns, false case not needed
      curr_ds_state = self.app.clean_state.get_clean_target()
      if selected_opt == "--- Please Select ---":
        curr_ds_state.set_sort_col(None)
      else:
        curr_ds_state.set_sort_col(selected_opt)
      return
    
    
  def select_sort_order(self, selected_opt: str):
    #  remarks: options called from columns, false case not needed
    curr_ds_state = self.app.clean_state.get_clean_target()
    if selected_opt == "--- Please Select ---":
      curr_ds_state.set_sort_ascending(None)
    else:
      curr_ds_state.set_sort_ascending(selected_opt == "Ascending")
    return


  def close_clean_sort_popup(self, target_popup: QDialog):
    if not isinstance(target_popup, QDialog):
      err_msg: str = "The close popup method only works for pop-up windows."
      logger.error(err_msg, exc_info=True)
      raise TypeError(err_msg)
    #  failed case: reminder box
    curr_ds_state = self.app.clean_state.get_clean_target()
    if curr_ds_state.sort_col is None:
      self.app.comp_fact.build_reminder_box(title="Warning", 
                                            txt_msg="Please ensure the sorting option has been set.")
      return
    if curr_ds_state.sort_ascending is None:
      self.app.comp_fact.build_reminder_box(title="Warning", 
                                            txt_msg="Please ensure the sorting order has been set.")
      return
    #  successful case: close popup
    return target_popup.close()
  
  
  #  2d. execute cleaning
  
  def handle_clean_single(self, target_ds: CleanDataState) -> pd.DataFrame:
    output_df: pd.DataFrame = target_ds.data_raw.copy()
    #  1. handle duplicates
    if target_ds.enable_duplicate:
      output_df = self.clean_model.handle_duplication(output_df)
    #  2. handle blanks
    if target_ds.handle_blanks:
      output_df = self.clean_model.handle_na(target_df=output_df,
                                              drop_missing=True,
                                              na_subset_col=None)
    #  3. handle sorts
    if target_ds.enable_sort and target_ds.sort_col is not None and target_ds.sort_ascending is not None:
      output_df = self.clean_model.handle_sort(target_df=output_df,
                                                target_col=target_ds.sort_col,
                                                is_ascending=target_ds.sort_ascending)
    #  4. update state
    target_ds.set_data_clean(output_df)
    logger.info(f"Data cleaning is applied to dataset: {target_ds.state_name}.")
    return
  
  
  def execute_clean_all(self) -> None:
    for datastate in self.app.clean_state.dataset_states.values():
      self.handle_clean_single(target_ds=datastate)
    return
  
  
  #  2e. reset section
  
  def reset_clean_tab_state(self) -> None:
    curr_ds_state = self.app.clean_state.get_clean_target()
    confirmation = self.app.comp_fact.build_msg_box(title="Warning", 
                                                    question="Are you sure to reset the cleaning options?")
    if confirmation:
      curr_ds_state.reset_clean()
      self.app.pages_fact.page_clean.reset_display()
    return