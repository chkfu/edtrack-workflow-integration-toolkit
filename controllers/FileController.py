"""
This controller manages file browsing and dataset loading.
It bridges the UI interface with underlying I/O logic and 
temporary dataset loading.
"""


from PyQt5.QtWidgets import QFileDialog
from models.DataLoader import DataLoader
from views.components.config.views_config import DATASET_LIST, RAW_COL_SCHEMA
import pandas as pd
import logging


#  LOGGING

logger = logging.getLogger("FILE_CONTROLLER")


# CLASS

class FileController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    self.data_loader = DataLoader()
    logger.info("[FileController] initialised sucessfully.")
    
  
  #  REUSED METHODS
  def update_temp_state(self) -> None:
    print

  
    
  #  METHODS
  
  def browse_files(self, target_key, lb_widget) -> str | None:
    """ USE: indicate the designated file locaiton. """
    try:
      
      #  task 1: display path at label
      
      # _ refers to file type, namely .csv, .json, .xml
      file_name, _ = QFileDialog.getOpenFileName(self.app.window, 
                                              "Open File", 
                                              "./data/raw", 
                                              "CSV Files (*.csv);;JSON Files (*.json);;XML Files (*xml);;All Files (*)",
                                              "CSV Files (*.csv)")
      if not file_name:
        return 
      
      lb_widget.setText(file_name)
      
      
      #  task 2: store dataframe path - further tracing
      
      #  update temp path state, used to trace the correct dataframe to store
      if target_key == DATASET_LIST[1]["data"]:
          self.app.pages_fact.temp_path_users = file_name
      elif target_key == DATASET_LIST[2]["data"]:
          self.app.pages_fact.temp_path_activities = file_name
      elif target_key == DATASET_LIST[3]["data"]:
          self.app.pages_fact.temp_path_components = file_name
      else:
        return self.app.comp_fact.build_reminder_box(
                title="Error",
                txt_msg="Failed to hit the selected dataset path.")
      logger.info(f"Browsed the selected file - {file_name}, {target_key}.")
      
      
      #  task 3: store the temp dataframe table
      
      #  load datasets and check whether it matched the designated schema
      temp_df = self.data_loader.import_dataset(file_name)
      if not self.app.valid_cont.validate_preview_df(
            lb_text=target_key,
            target_state=temp_df,
            target_schema=RAW_COL_SCHEMA
        ):
        err_msg: str = "Failed to match the dataset schema. The selected dataset is not matched."
        logger.warning(err_msg)
        return
      
      #  store correct dataset into corresponding state
      if target_key == DATASET_LIST[1]["data"]:
          self.app.df_users = temp_df
      elif target_key == DATASET_LIST[2]["data"]:
          self.app.df_activities= temp_df
      elif target_key == DATASET_LIST[3]["data"]:
          self.app.df_components = temp_df
      
      #  output file-name for the label display only, temp state prev. stored
      return file_name
    
    except Exception as ex:
      logger.error(f"Failed to browse the selected file - {ex}", exc_info=True)



#  ATTN: target_dataset would be critical debug point: type conflicts
  def preview_dataset(self,
                      target_key: str) -> pd.DataFrame:
    """ USE: store the designated dataset path to temp state """
    #  validation
    path_map = {
      DATASET_LIST[1]["data"]: self.app.pages_fact.temp_path_users,
      DATASET_LIST[2]["data"]: self.app.pages_fact.temp_path_activities,
      DATASET_LIST[3]["data"]: self.app.pages_fact.temp_path_components
    }  
    if target_key not in path_map:
      return self.app.comp_fact.build_reminder_box(title="Error",
                                                  txt_msg="[Error] Failed to match the path in the dataset list.")
    target_path = path_map[target_key]
    if not target_path:
      return self.app.comp_fact.build_reminder_box(title="Error",
                                                   txt_msg="[Error] Failed to search the path of selected dataset.")

    #  store target dataset in temp states for preview
    #  remarks: needs to try-catch for data-loader, considering SQL might crash
    try:
      temp_dataset = self.data_loader.import_dataset(target_path)
      if not self.app.valid_cont.validate_preview_df(lb_text=target_key, 
                                                     target_state=temp_dataset,
                                                     target_schema=RAW_COL_SCHEMA):
        return
      if target_key == DATASET_LIST[1]["data"]:
        self.app.df_users = temp_dataset
        self.app.comp_fact.build_popup_wd(wd_title="Preview",
                                          popup_title="Preview: User Dataset",
                                          target_df=self.app.df_users,
                                          popup_content=self.app.comp_fact.build_table_view(target_df=self.app.df_users))
      elif target_key == DATASET_LIST[2]["data"]:
        self.app.df_activities= temp_dataset
        self.app.comp_fact.build_popup_wd(wd_title="Preview",
                                          target_df=self.app.df_activities,
                                          popup_title="Preview: Activity Dataset",
                                          popup_content=self.app.comp_fact.build_table_view(target_df=self.app.df_activities))
      elif target_key == DATASET_LIST[3]["data"]:
        self.app.df_components = temp_dataset
        self.app.comp_fact.build_popup_wd(wd_title="Preview",
                                          target_df=self.app.df_components,
                                          popup_title="Preview: Component Dataset",
                                          popup_content=self.app.comp_fact.build_table_view(target_df=self.app.df_components))
    #  1. success
      logger.info(f"Previewed the selected file - {target_key}.")
      return temp_dataset
    #  2. failure
    except Exception as ex:
      logger.error(f"Failed to browse the selected file - {ex}", exc_info=True)
      return self.app.comp_fact.build_reminder_box(title="Error",
                                                   txt_msg="[Error] Failed to load the selected dataset.")
      
      
  def export_preview(self,
                     target_df: pd.DataFrame,
                     target_format: str=".csv"):
    """USE: enable user to export designated dataset into their local directory"""
    
    #  validate parameters
    if not isinstance(target_df, pd.DataFrame):
      err_msg: str = "The selected dataset is not in pandas dataframe format."
      self.app.comp_fact.build_reminder_box(title="Error", txt_msg=err_msg)
      logger.error(err_msg, exc_info=True)
      return
    
    #  slightly formatting, enhance error tolerance
    target_format_r: str = str(target_format).strip().lower()
    target_format_r = target_format_r if target_format_r.startswith(".") else f".{target_format_r}"
    
    if target_format_r not in [".csv", ".xml",".json", ".png"]:
      err_msg: str = "The selected dataset is not in pandas dataframe format."
      self.app.comp_fact.build_reminder_box(title="Error", txt_msg=err_msg)
      logger.warning(err_msg, exc_info=True)
      return
    
    #  Learnt: form the whitelist for filtering
    format_dict: dict = {
        ".csv": "CSV Files (*.csv)",
        ".json": "JSON Files (*.json)",
        ".xlsx": "Excel Files (*.xlsx)",
        ".xml": "XML Files (*.xml)"
    }
    #  Learnt: suceed case -> target, failed case -> "All Files"
    target_criteria = format_dict.get(target_format_r, "All Files (*)")
    
    try:
      #  search file
      file, _ = QFileDialog.getSaveFileName(
        self.app.window,
        "Save As",
        f"output{target_format_r}", 
        target_criteria
      )
      
      if not file:
        logger.warning("File not found, No export task.")
        return
      
      self.data_loader.convert_dataset(dataframe=target_df, 
                                            fileType=target_format_r,
                                            destination=file)
      suceed_msg: str = f"The new file has been stored at {file}."
      logger.info(suceed_msg)
      self.app.comp_fact.build_reminder_box(title="Success", 
                                            txt_msg=suceed_msg)
    
    except Exception as ex:
      logger.error(f"file path not found. unable to export the selected dataset. {ex}", exc_info=True)
      self.app.comp_fact.build_reminder_box("Error", f"{ex}")
    
    
    
  # def import_datasets(self):
  #   """USE: adopted designated datasets for further transformation, once all three datasets available"""

  #   def print_msg(type: str):
  #     type_r: str = str(type).strip().lower()
  #     if type_r not in ["users", "activities", "components"]:
  #       err_msg: str = "Unable to detect error messages for further identification."
  #       logger.error(err_msg, exc_info=True)
  #       raise ValueError(err_msg)
  #     return f"Table {type_r} is not uploaded. Please try again."
    
  #   #  reject the failed cases
  #   if self.app.df_users is None or self.app.df_users.empty:
  #       self.app.comp_fact.build_reminder_box("Error", print_msg("users"))
  #       return
  #   if self.app.df_activities is None or self.app.pages_fact.temp_table_activity.empty:
  #       self.app.comp_fact.build_reminder_box("Error", print_msg("activities"))
  #       return
  #   if self.app.df_components is None or self.app.df_components.empty:
  #       self.app.comp_fact.build_reminder_box("Error", print_msg("components"))
  #       return
      
  #   #  1. copy dataframe to global state
  #   self.app.df_users = self.app.df_users
  #   self.app.df_activities = self.app.pages_fact.temp_table_activity
  #   self.app.df_components = self.app.df_components
    
  #   #  2. store data into SQL
  #   self.app.sql_connector.import_dataframe(target_table="users",
  #                                         target_df=self.app.df_users)
  #   self.app.sql_connector.import_dataframe(target_table="activities",
  #                                         target_df=self.app.df_activities)
  #   self.app.sql_connector.import_dataframe(target_table="components",
  #                                         target_df=self.app.df_components)
    
  #   #  3. check dataset and update dataset list UI