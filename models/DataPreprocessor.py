import pandas as pd
import logging
import hashlib
from pandas.api.types import is_datetime64_any_dtype



#  LOGGING

logger = logging.getLogger("DATA_PREPROCESSOR")


#  CLASS

class DataPreprocessor:
  
  def __init__ (self, data_manager, valid_cont):
    self.data_manager = data_manager
    self.valid_cont = valid_cont
    logger.info("initialised successfully.")
  

  #  METHODS  -   MAIN
  
  
  def remove_time_col(self, 
                      target_df: pd.DataFrame, 
                      time_col: str=None) -> pd.DataFrame:
    output = target_df.copy()
    #  validate cols
    time_col_r = self.valid_cont.validate_col(target_df=output, target_col=time_col)
    #  remove time column
    if time_col is not None:
      output = self.data_manager.remove_col(target_df=target_df, target_col=time_col_r)
    #  output
    return output
  
  
  def hash_secret_col(self, 
                      target_df: pd.DataFrame, 
                      name_col: str) -> pd.DataFrame:
    output = target_df.copy()
    name_col_r = self.valid_cont.validate_col(target_df, name_col)
    output[name_col_r] = output[name_col_r].astype(str).str.strip().str.lower()
    #  learnt:  expected result -> if conditions -> loop  (if / else case, loop chain)
    output[name_col_r] = [hashlib.sha256(name.encode()).hexdigest()[:10] 
                          if name not in [None, ""] 
                          else "Not Specified" 
                          for index, name in output[name_col_r].items()]
    return output
  
  
  def create_dt_feat(self,
                     target_df: pd.DataFrame,
                     target_col: str,
                     target_opt: str) -> pd.DataFrame:

    #  declaration
    temp_dt_name: str | None = None
    output_df: pd.DataFrame = target_df.copy()
    target_series: pd.Series= target_df[target_col].copy()  
    temp_dt_series: pd.Series | None = None
    
    #  validate column, logical error does not need ui reminders
    if not is_datetime64_any_dtype(target_series):
      raise ValueError("Failed to format datetime features with mon-datetime columns.")
      
    #  declaration
    MONTH_DICT: dict = {
      1: "January",
      2: "February",
      3: "March",
      4: "April",
      5: "May",
      6: "June",
      7: "July",
      8: "August",
      9: "September",
      10: "October",
      11: "November",
      12: "December",
    }
    WEEKDAY_DICT: dict = {
      0: "Monday",
      1: "Tuesday", 
      2: "Wednesday",
      3: "Thursday", 
      4: "Friday", 
      5: "Saturday", 
      6: "Sunday",
    }

    #  stage - handle datetime, matching options   
    #  remarks: temp store new column name (temp_dt_name), and store new column values (temp_dt_series)
    target_opt = target_opt.strip().lower()
    if target_opt == "year":
      temp_dt_name = target_col + "_year"
      temp_dt_series = target_series.dt.year
    elif target_opt == "month":
      temp_dt_name = target_col + "_month"
      temp_dt_series = target_series.dt.month
    elif target_opt == "day":
      temp_dt_name = target_col + "_day"
      temp_dt_series = target_series.dt.day
    elif target_opt == "weekday":
      temp_dt_name = target_col + "_weekday"
      temp_dt_series = target_series.dt.weekday
    elif target_opt == "hour":
      temp_dt_name = target_col + "_hour"
      temp_dt_series = target_series.dt.hour
    elif target_opt in ["minute", "minutes"] :
      temp_dt_name = target_col + "_minute"
      temp_dt_series = target_series.dt.minute
    else:
      raise ValueError(f"Failed to create selected time feature with datetime options.")
    
    #  translate the datetime with spec meaning
    if target_opt == "month":
      temp_dt_series = temp_dt_series.map(MONTH_DICT)
    elif target_opt == "weekday":
      temp_dt_series = temp_dt_series.map(WEEKDAY_DICT)
    
    #  check and produce new columns
    if temp_dt_series is None:
      raise ValueError("Failed to create selected time feature without specific information.")
    output_df[temp_dt_name] = temp_dt_series
    return output_df

    
  def encode_component_col(self, 
                           target_df: pd.DataFrame, 
                           target_col: str, 
                           code_df: pd.DataFrame, 
                           dict_idx: str, 
                           dict_val: str):
    output = target_df.copy()
    #  validate column name
    comp_col_r = self.valid_cont.validate_col(target_df, target_col)
    dict_idx_r = self.valid_cont.validate_col(code_df, dict_idx)
    dict_val_r = self.valid_cont.validate_col(code_df, dict_val)
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
    action_col_r = self.valid_cont.validate_col(target_df, target_col)
    #  regulate options
    output[action_col_r] = [item
                            if str(item).lower() in ["answered", "created", "uploaded", "updated", "reviewed", "submitted", "viewed"]
                            else "Not Specified"
                            for item in output[action_col_r]]
    return output
  
    
  def regulate_targets(self,
                       target_df: pd.DataFrame,
                       target_col: str) -> pd.DataFrame:
    output = target_df.copy()
    #  validate column name
    target_col_r = self.valid_cont.validate_col(target_df, target_col)
    #  unify similar options
    output[target_col_r] = ["submission".upper().strip()
                          if str(item).lower().strip() in ["file_submission", "submission_state", "submission_status", "submission_text"]
                          else item.upper()
                          for item in output[target_col_r]]
    return output