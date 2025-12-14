import pandas as pd
import logging


#  LOGGING

logger = logging.getLogger("CLEAN_DATA_STATE")


#  CLASS

#  Learnt: managing different datasets, for cleaning options
#          centialised control in CleanState
class CleanDataState:
  
  def __init__(self, state_name: str):
    
    self.state_name = state_name 
    
    #  DataFrame Management
    self.data_raw: pd.DataFrame = None
    self.data_clean: pd.DataFrame = None
    
    #  1. duplicates
    self.enable_duplicate: bool = False
    self.handle_duplicate_cols = []
    
    #  2. blanks
    self.handle_blanks = {}
    
    #  3. sorts
    self.enable_sort: bool = False
    self.sort_col: str = "index"
    self.sort_ascending: bool = True
    

  #  set data state
  
  def set_data_raw(self, target_df: pd.DataFrame) -> None:
    self.data_raw = target_df
    
  def set_data_clean(self, target_df: pd.DataFrame) -> None:
    self.data_clean = target_df
    
  def set_data_proc(self, target_df: pd.DataFrame) -> None:
    self.data_proc = target_df
    
  
  #  set basic cleaning opt
    
  def set_enable_duplicate(self, target_opt: bool | None) -> None:
    self.enable_duplicate = target_opt
    
    
  def set_handle_duplicate_cols(self, target_action: str, target_col: str | list) -> None:
    target_action_r = target_action.strip().lower()
    if target_action_r == "push":
      if target_col not in self.handle_duplicate_cols:
        self.handle_duplicate_cols.append(target_col)
    elif target_action_r == "pull":
      if target_col in self.handle_duplicate_cols:
        self.handle_duplicate_cols.remove(target_col)
    elif target_action_r == "replace":
      self.handle_duplicate_cols = target_col
    elif target_action_r == "empty":
      self.handle_duplicate_cols = list()
    else:
      return
  
  
  def set_handle_blanks(self, new_map: dict) -> None:
    for _, value in new_map.items():
      if "method" not in value or "value" not in value:
        err_msg: str = f"required standard input dictionary for managing blanks for data cleaning."
        logger.error(err_msg, exc_info=True)
        raise ValueError(err_msg)
    self.handle_blanks = new_map
    
    
  def update_handle_blanks(self, target_col: str, target_val: dict) -> None:
    self.handle_blanks[target_col] = target_val
    
    
  def set_enable_sort(self, target_opt: bool | None) -> None:
    self.enable_sort = target_opt

  def set_sort_col(self, target_col: str | None) -> None:
    self.sort_col = target_col

  def set_sort_ascending(self, target_opt: bool | None) -> None:
    self.sort_ascending = target_opt
    
  #  set advanced cleaning opt
  
  def push_remove_col(self, target_col: str) -> None:
    if target_col not in self.remove_cols:
      self.remove_cols.append(target_col)
      
  def pull_remove_col(self, target_col: str) -> None:
    if target_col in self.remove_cols:
      self.remove_cols.remove(target_col)
      
  def push_rename_col(self, prev_name: str, new_name: str) -> None:
    self.rename_cols[prev_name] = new_name
      
  def pull_rename_col(self, prev_name: str) -> None:
    if prev_name in self.rename_cols:
      del self.rename_cols[prev_name]
      
  def push_remove_row(self, target_col: str, value: str) -> None:
    if target_col not in self.remove_rows:
      self.remove_rows[target_col] = []
    self.remove_rows[target_col].append(value)
    
  def pull_remove_row(self, target_col: str, value: str) -> None:
    if target_col in self.remove_rows:
      if value in self.remove_rows[target_col]:
        self.remove_rows[target_col].remove(value)
        
  
  #  reset
  
  def reset_dataset_state(self, reset_type: str) -> None:
    target_type = reset_type.strip().lower()
    if target_type not in ["raw", "clean", "proc"]:
      err_msg = "Reset type not in list. The instruction will be ignored"
      logger.warning(err_msg)
      return
    if target_type == "proc":
      self.data_proc = None
    elif target_type == "clean": 
      self.data_clean = None
      self.data_proc = None
    else:  
      self.data_raw = None
      self.data_clean = None
      self.data_proc = None
  
  
  def reset_clean(self) -> None:
    #  reset duplicate
    self.enable_duplicate = False
    self.handle_duplicate_cols = []
    #  reset blanks
    self.handle_blanks = {}
    #  reset sorts
    self.enable_sort = False
    self.sort_col = "index"
    self.sort_ascending = True
    
    
  def reset_preproc(self) -> None:
    self.remove_cols = []
    self.rename_cols = {}
    self.remove_rows = {}
    
  
  #  for checking
  def to_string(self) -> None:
    print("\n==== Raw Data Info ====")
    print(f"state_name: {self.state_name}")
    print(f"data_raw: {self.data_raw}")
    print(f"data_clean: {self.data_clean}")
    print("\n==== Cleaned Data Info ====")
    print(f"enable_duplicate: {self.enable_duplicate}")
    print(f"handle_duplicate_cols: {self.handle_duplicate_cols}")
    print(f"handle_blanks: {self.handle_blanks}")
    print(f"enable_sort: {self.enable_sort}")
    print(f"sort_col: {self.sort_col}")
    print(f"sort_ascending: {self.sort_ascending}")
    print("\n==== Proc Data Info ====")
   