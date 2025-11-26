import pandas as pd
\
#  CLASS

#  Learnt: managing different datasets, for cleaning options
#          centialised control in CleanState
class DatasetState:
  
  def __init__(self):
    
    #  DataFrame Management
    self.data_raw: pd.DataFrame = None
    self.data_cleaned_1st: pd.DataFrame = None
    self.data_cleaned_2nd: pd.DataFrame = None
    
    #  Basic Cleaning
    self.enable_duplicate: bool = False
    self.enable_empty: bool = False
    self.enable_sort: bool = False
    self.sort_col: str = "index"
    self.sort_ascending: bool = True
    
    #  Advanced Cleaning
    self.remove_cols: list = []
    self.rename_cols: dict = {}
    self.remove_rows: dict = {}
    
    #  Type Specification
    self.str_spec: dict = {}
    self.num_spec: dict = {}
    self.bool_spec: dict = {}
    self.dat_spec: dict = {}
    
    
  #  set data state
  
  def set_data_raw(self, target_df: pd.DataFrame) -> None:
    self.data_raw = target_df
    
  def set_data_cleaned_1st(self, target_df: pd.DataFrame) -> None:
    self.data_cleaned_1st = target_df
    
  def set_data_cleaned_2nd(self, target_df: pd.DataFrame) -> None:
    self.data_cleaned_2nd = target_df
    
  
  #  set basic cleaning opt
    
  def toggle_enable_duplicate(self) -> None:
    self.enable_duplicate = not self.enable_duplicate
  
  def toggle_enable_empty(self) -> None:
    self.enable_empty = not self.enable_empty
    
  def toggle_enable_sort(self) -> None:
    self.enable_sort = not self.enable_sort
    
  def set_sort_col(self, target_col: str, ascending=True):
    self.sort_col = target_col
    self.sort_ascending = ascending
    
    
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
      

  #  set type spec
  
  
  
  
  #  reset ds
  def reset_ds(self) -> None:
    
    self.data_raw = None
    self.data_cleaned_1st = None
    self.data_cleaned_2nd = None
    
    self.enable_duplicate = False
    self.enable_empty = False
    self.enable_sort = False
    self.sort_col = "index"
    self.sort_ascending = True
    
    self.remove_cols = []
    self.rename_cols = {}
    self.remove_rows = {}
    
    self.str_spec = {}
    self.num_spec = {}
    self.bool_spec = {}
    self.dat_spec = {}
    
    
