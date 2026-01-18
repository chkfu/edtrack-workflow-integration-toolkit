"""
This controller manages file browsing and dataset loading.
It bridges the UI interface with underlying I/O logic and 
temporary dataset loading.
"""


from PyQt5.QtWidgets import QFileDialog
from models.DataLoader import DataLoader
from controllers.ValidController import ValidController
from views.components.config.views_config import RAW_COL_SCHEMA
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
    self.valid_cont = ValidController()
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
    
      #  task 2: store the temp dataframe table
      #  load datasets and check whether it matched the designated schema
      temp_dataframe = self.data_loader.import_dataset(file_name)
      if not self.valid_cont.validate_preview_df(
            lb_text=target_key,
            target_state=temp_dataframe,
            target_schema=RAW_COL_SCHEMA
        ):
        err_msg: str = "Failed to match the dataset schema. The selected dataset is not matched."
        logger.warning(err_msg)
        return
      
      #  update temp path state, used to trace the correct dataframe to store
      self.app.clean_state.set_raw_data(target_key, temp_dataframe)
      logger.info(f"Loaded file {file_name}")
      return file_name
      
    except Exception as ex:
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=f"Failed to hit the selected dataset path.")
      logger.error(f"Browsed the selected file - {file_name}, {ex}, {target_key}.")


#  ATTN: target_dataset would be critical debug point: type conflicts
  def preview_dataset(self,
                      target_key: str) -> pd.DataFrame:
    """ USE: store the designated dataset path to temp state """
    #  validation
    try:
      
      target_dataset = self.app.clean_state.get_spec_dataframe(target_key)
      target_dataframe = target_dataset.data_raw
      
      if target_dataframe is None or target_dataframe.empty:
        return self.app.comp_fact.build_reminder_box(
                title="Error",
                txt_msg=f"No data is found. Please upload the valid file again.")
    
      #  remarks: needs to try-catch for data-loader, considering SQL might crash
      if not self.valid_cont.validate_preview_df(lb_text=target_key, 
                                                     target_state=target_dataframe,
                                                     target_schema=RAW_COL_SCHEMA):
        return
      
      # preview popup
      self.app.comp_fact.build_popup_wd(
          wd_title="Preview",
          popup_title=f"Preview: {target_key}",
          target_df=target_dataframe,
          popup_content=self.app.comp_fact.build_table_view(target_dataframe)
      )
      logger.info(f"Previewed the selected file - {target_key}.")
      return target_dataframe

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
    
    
