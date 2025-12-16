import pandas as pd
import logging
from states.CleanDataState import CleanDataState
from views.components.config.views_config import DATASET_LIST



#  LOGGING

logger = logging.getLogger("MERGE_STATE")


#  CLASS

class MergeState:
  
  def __init__(self):
    
    #  CONSTRUCTOR
    
    #  temporary datasets
    self.raw_merge: pd.DataFrame | None = None
    self.proc_merge: pd.DataFrame | None = None
    
    #  merger settings
    self.target_ltable: str | None = None
    self.target_rtable: str | None = None
    self.target_lcol: str | None = None
    self.target_rcol: str | None = None
    self.target_method: str | None = None
    
    
  
    #  METHODS
    
    #  remarks: requires to start from merging cleaned datasets, instead first merge
    def set_raw_merge(self, target_df: pd.DataFrame) -> None:
      self.raw_merge = target_df
    
    #  remarks: for data analysis after feature engineering stage
    def set_proc_merge(self, target_df: pd.DataFrame) -> None:
      self.raw_merge = target_df
      
      
    #  table selection related 
    
    def set_target_ltable(self, target_df: pd.DataFrame) -> None:
      self.raw_merge = target_df
      

    def set_target_rtable(self, target_df: pd.DataFrame) -> None:
      self.raw_merge = target_df
      
      
    def set_target_lcol(self, target_col: str) -> None:
      if self.target_ltable is None:
        return
      matching: bool = any(target_col.strip().lower() == column.strip().lower() 
                           for column in self.ltable.columns)
      #  if matched, store the original col name; else pass
      if matching:
        self.target_lcol = self.app.valid_cont.validate_col(target_df=self.ltable, 
                                                            target_col=target_col)
        
        
    def set_target_rcol(self, target_col: str) -> None:
      if self.target_ltable is None:
        return
      matching: bool = any(target_col.strip().lower() == column.strip().lower() 
                           for column in self.rtable.columns)
      #  if matched, store the original col name; else pass
      if matching:
        self.target_rcol = self.app.valid_cont.validate_col(target_df=self.rtable, 
                                                            target_col=target_col)
        
        
    def set_target_method(self, target_method: str) -> None:
      temp_method = target_method.strip().lower() 
      if temp_method not in ["left", "right", "outer", "inner"]:
        logger.error(f"The provided target method of '{target_method}' is invalid.", 
                     exc_info=True)
        return
      self.target_method = temp_method
      

    def reset_merge_ds(self) -> None:
      self.raw_merge = None
      self.proc_merge = None
      self.target_ltable = None
      self.target_rtable = None
      self.target_lcol = None
      self.target_rcol = None
      self.target_method  = None

    
  
  