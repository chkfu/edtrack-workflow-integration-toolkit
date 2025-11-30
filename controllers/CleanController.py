"""
This controller bridges the models and views.
It specific become the wrapper of models' methods, enabling minor adjustment
and prevent directly changes to the data transformation logic.
"""


import logging
from PyQt5.QtWidgets import (
    QStackedWidget, QGridLayout,QListWidget, QFrame, QHBoxLayout, QWidget,
    QVBoxLayout, QListWidgetItem, QDialog
)


#  LOGGING

logger = logging.getLogger("DATA_CONTROLLER")


# CLASS

class CleanController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
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
    
    
  #  2. manage radio buttons
  
  #  2a. remove duplicates
  
  
  
  #  2b. handling blanks
  
  
  
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
      if checked:
        popup = self.app.pages_fact.page_clean.build_sort_popup()
        popup.exec_()
      return
    
    else: 
      return
    
    
  def handle_clean_sort_detail(self, target_col: str, target_isAsc: bool):
    curr_ds = self.app.clean_state.get_clean_target()
    #  validate column
    if not self.app.valid_cont.validate_col(target_df=curr_ds, target_col=target_col):
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
    if curr_ds_state.sort_ascending is None:
      self.app.comp_fact.build_reminder_box(title="Warning", 
                                            txt_msg="Please ensure the sorting order has been set.")
      return
    if curr_ds_state.sort_col is None:
      self.app.comp_fact.build_reminder_box(title="Warning", 
                                            txt_msg="Please ensure the sorting option has been set.")
      return
    #  successful case: close popup
    return target_popup.close()