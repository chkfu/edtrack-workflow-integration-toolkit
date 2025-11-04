import pandas as pd
import datetime
import hashlib


#  CLASS

class DataPreprocessor:
  
  def __init__ (self, 
                data_manager: object):
    self.data_manager = data_manager
    print("[DataPreprocessor] initialised successfully.")
  
  
  #  METHODS  -  VALIDATION
  def validate_col(self, target_df: pd.DataFrame, target_col: str) -> str:
    #  for index
    if target_col.strip().lower() == "index":
      return "index"
    #  for columns
    output = next((col for col in target_df.columns if col.strip().lower() == target_col.strip().lower()), None)
    if output is None:
      raise ValueError("[DataManager] target column is not found.")
    return output.strip()
    
  #  METHODS  -   MAIN
  
  
  def remove_time_col(self, 
                      target_df: pd.DataFrame, 
                      time_col: str=None) -> pd.DataFrame:
    output = target_df.copy()
    #  validate cols
    time_col_r = self.validate_col(target_df=output, target_col=time_col)
    #  remove time column
    if time_col is not None:
      output = self.data_manager.remove_col(target_df=target_df, target_col=time_col_r)
    #  output
    return output
  
  
  def hash_name_col(self, 
                    target_df: pd.DataFrame, 
                    name_col: str) -> pd.DataFrame:
    output = target_df.copy()
    name_col_r = self.validate_col(target_df, name_col)
    output[name_col_r] = output[name_col_r].astype(str).str.strip().str.lower()
    #  learnt:  expected result -> if conditions -> loop  (if / else case, loop chain)
    output[name_col_r] = [hashlib.sha256(name.encode()).hexdigest()[:10] 
                          if name not in [None, ""] 
                          else "Not Specified" 
                          for index, name in output[name_col_r].items()]
    return output
  
  
  def encode_component_col(self, 
                           target_df: pd.DataFrame, 
                           target_col: str, 
                           code_df: pd.DataFrame, 
                           dict_idx: str, 
                           dict_val: str):
    output = target_df.copy()
    #  validate column name
    comp_col_r = self.validate_col(target_df, target_col)
    dict_idx_r = self.validate_col(code_df, dict_idx)
    dict_val_r = self.validate_col(code_df, dict_val)
    #  turn component df into dict.
    code_dict: dict = code_df.set_index(dict_idx_r)[dict_val_r].to_dict()
    #  convert code_dict to uppercase
    code_dict = {index.upper(): value.upper() 
                 for index, value in code_dict.items()}
    #  replace comp names in target_df
    output[comp_col_r] = [code_dict[comp] 
                          if comp in code_dict 
                          else comp 
                          for comp in output[comp_col_r]]
    return output
    
  
  def regulate_actions(self,
                       target_df: pd.DataFrame,
                       target_col: str) -> pd.DataFrame:
    output = target_df.copy()
    #  validate column name
    action_col_r = self.validate_col(target_df, target_col)
    #  regulate options
    output[action_col_r] = [item
                            if str(item).lower() in ["answered", "created", "uploaded", "updated", "reviewed", "submitted", "viewed"]
                            else "Not Specified"
                            for item in output[action_col_r]]
    return output
  
    
  def revise_target_col(self,
                       target_df: pd.DataFrame,
                       target_col: str) -> pd.DataFrame:
    output = target_df.copy()
    #  validate column name
    target_col_r = self.validate_col(target_df, target_col)
    #  unify similar options
    output[target_col_r] = ["submission".upper().strip()
                          if str(item).lower().strip() in ["file_submission", "submission_state", "submission_status", "submission_text"]
                          else item.upper()
                          for item in output[target_col_r]]
    return output