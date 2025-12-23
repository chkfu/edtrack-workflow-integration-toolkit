import logging
import pandas as pd
from controllers.ValidController import ValidController


#  LOGGING

logger = logging.getLogger("FE_CONTROLLER")


# CLASS

class FEController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    logger.info("initialised sucessfully.")
  
  
  #  METHODS - POPUP TRIGGERS
  
  def handle_remove_cols(self) -> None:
    print("rename_spec_cols")
    pass
  
  
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
  

