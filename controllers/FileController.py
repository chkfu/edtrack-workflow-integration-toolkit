"""
This controller manages file browsing and dataset loading.
It bridges the UI interface with underlying I/O logic and 
temporary dataset loading.
"""


from PyQt5.QtWidgets import QFileDialog
from views.components.config.views_config import DATASET_LIST
import pandas as pd
import logging


#  LOGGING

logger = logging.getLogger("APPLICATION")


# CLASS

class FileController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    logger.info("[FileController] initialised sucessfully.")
    
    
    
  #  METHODS
  
  def browse_files(self, target, lb_widget) -> str | None:
    """ USE: indicate the designated file locaiton. """
    try:
      # _ refers to file type, namely .csv, .json, .xml
      file_name, _ = QFileDialog.getOpenFileName(self.app.window, 
                                              "Open File", 
                                              "./data/raw", 
                                              "CSV Files (*.csv);;JSON Files (*.json);;XML Files (*xml);;All Files (*)",
                                              "CSV Files (*.csv)")
      if not file_name:
        return 
      
      lb_widget.setText(file_name)
      
      #  update temp path state, used to trace the correct dataframe to store
      if target == DATASET_LIST[1]["data"]:
          self.app.pages_fact.temp_path_user = file_name
      elif target== DATASET_LIST[2]["data"]:
          self.app.pages_fact.temp_path_activity = file_name
      elif target == DATASET_LIST[3]["data"]:
          self.app.pages_fact.temp_path_comp = file_name
      logger.info(f"Browsed the selected file - {file_name}, {target}.")
      return file_name

    except Exception as ex:
      logger.error(f"Failed to browse the selected file - {ex}", exc_info=True)


#  ATTN: target_dataset would be critical debug point: type conflicts
  def preview_dataset(self,
                      target_key: str) -> pd.DataFrame:
    """ USE: store the designated dataset path to temp state """
    #  validation
    path_map = {
      DATASET_LIST[1]["data"]: self.app.pages_fact.temp_path_user,
      DATASET_LIST[2]["data"]: self.app.pages_fact.temp_path_activity,
      DATASET_LIST[3]["data"]: self.app.pages_fact.temp_path_comp
    }  
    if target_key not in path_map:
      return self.app.comp_fact.build_reminder_box(title="Error",
                                                  txt_msg="[Error] Failed to match the path in the dataset list.")
    target_path = path_map[target_key]
    if not target_path:
      return self.app.comp_fact.build_reminder_box(title="Error",
                                                  txt_msg="[Error] Failed to search the path of selected dataset.")

    #  store target dataset in temp states for preview
    try:
      temp_dataset = self.app.data_loader.import_dataset(target_path)
      if target_key == DATASET_LIST[1]["data"]:
        print(temp_dataset)
        self.app.temp_table_user = temp_dataset
        self.app.comp_fact.build_popup_wd(wd_title="Preview",
                                          popup_title="Preview: User Dataset",
                                          popup_content=self.app.comp_fact.build_table_view(
                                            target_df=self.app.temp_table_user))
      elif target_key == DATASET_LIST[2]["data"]:
        self.app.temp_table_activity = temp_dataset
        self.app.comp_fact.build_popup_wd(wd_title="Preview",
                                          popup_title="Preview: Activity Dataset",
                                          popup_content=self.app.comp_fact.build_table_view(
                                            target_df=self.app.temp_table_activity))
      elif target_key == DATASET_LIST[3]["data"]:
        self.app.temp_table_component = temp_dataset
        self.app.comp_fact.build_popup_wd(wd_title="Preview",
                                          popup_title="Preview: Component Dataset",
                                          popup_content=self.app.comp_fact.build_table_view(
                                            target_df=self.app.temp_table_component))
    #  1. sucess
      logger.info(f"Previewed the selected file - {target_key}.")
      return temp_dataset
    #  2. failure
    except Exception as ex:
      logger.error(f"Failed to browse the selected file - {ex}", exc_info=True)
      return self.app.comp_fact.build_reminder_box(title="Error",
                                                   txt_msg="[Error] Failed to load the selected dataset.")
    