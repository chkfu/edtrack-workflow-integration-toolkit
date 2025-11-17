import pandas as pd
import logging
from models.config.monthList import MONNTH_LIST



#  LOGGING

logger = logging.getLogger("APPLICATION")


#  CLASS

class DataManager:
  
  def __init__(self):
    self.col_name_list = None
    logger.info("[DataManager] initialised successfully.")
    
   
    
  #  METHOD - REUSE
  
  def validate_col(self, target_df: pd.DataFrame, target_col: str) -> str:
    #  for index
    if target_col.strip().lower() == "index":
      return "index"
    #  for columns
    output = next((col for col in target_df.columns if col.strip().lower() == target_col.strip().lower()), None)
    if output is None:
      raise ValueError("[DataManager] target column is not found.")
    return output.strip()
    
  def update_valid_lists(self, target_df: pd.DataFrame, target_parameter: list, valid_list: list) -> None: 
    for el in target_parameter:
      testing_el = str(el)
      valid_el = self.validate_col(target_df=target_df, target_col=testing_el)
      if valid_el:
        valid_list.append(valid_el) 
    
    
    
  #  METHOD - CRUD
  
  def remove_col(self, target_df: pd.DataFrame, target_col: str) -> pd.DataFrame:
   
    #  validate types  
    if not isinstance(target_df, pd.DataFrame):
      raise TypeError("[DataManager] target dataframe must be a pandas DataFrame.")
    if not isinstance(target_col, str):
      raise TypeError("[DataManager] target column must be a string.")
    
    #  validate column
    valid_col: str = self.validate_col(target_df=target_df, target_col=target_col)
    
    #  output
    output = target_df.drop(columns=[valid_col])
    logger.info(f"[DataManager] target column has been removed.")
    return output
    
    
  def remove_rows(self, target_df: pd.DataFrame, target_col: str, target_rows:list) -> pd.DataFrame:
    
    #  validate types
    if not isinstance(target_df, pd.DataFrame):
      raise TypeError("[DataManager] target dataframe must be a pandas DataFrame.")
    if not isinstance(target_col, str):
      raise TypeError("[DataManager] target column must be a string.")
    if not isinstance(target_rows, list):
      raise TypeError("[DataManager] target input must be a list of strings.")
    
    #  validate column
    valid_col: str = self.validate_col(target_df=target_df, target_col=target_col)
    
    #  validate row
    rows_removal: list = [el.strip().lower() for el in target_rows]
    matched_list: list = target_df[valid_col].isin(rows_removal)  # isin() extracts rows with matched criteria
    
    #  output
    output = target_df[~matched_list]   # learnt: ~ sign as NOT operator
    logger.info(f"[DataManager] target row(s) has/have been removed.")
    return output
  
      
  def rename_col(self, target_df: pd.DataFrame, target_col: str, new_name: str) -> pd.DataFrame:
    
    #  validate types
    if not isinstance(target_df, pd.DataFrame):
      raise TypeError("[DataManager] target dataframe must be a pandas DataFrame.")
    if not isinstance(target_col, str):
      raise TypeError(f"[DataManager] target column {target_col} must be a string.")
    
    #  validate column
    valid_col: str = self.validate_col(target_df=target_df, target_col=target_col)
    
    #  convert name
    new_name_r: str = str(new_name).strip()
    
    # output
    output:  pd.DataFrame = target_df.rename(columns={valid_col: new_name_r})
    logger.info(f"[DataManager] the target column {target_col} has been renamed as {new_name_r}")
    return output
    
    
  def merge_tables(self, target_df_left: pd.DataFrame, target_df_right: pd.DataFrame, target_col_left: str, target_col_right: str, merge_type: str = "inner") -> pd.DataFrame:
    # reuse
    formatted_col_left: str = target_col_left.strip().lower()
    formatted_col_right: str = target_col_right.strip().lower()
    formatted_merge_type: str = merge_type.strip().lower()
  
    #  validate types
    if not isinstance(target_df_left, pd.DataFrame):
      raise TypeError("[DataManager] target dataframe must be a pandas DataFrame.")
    if not isinstance(target_df_right, pd.DataFrame):
      raise TypeError("[DataManager] target dataframe must be a pandas DataFrame.")
    if not isinstance(target_col_left, str):
      raise TypeError("[DataManager] target column must be a string.")
    if not isinstance(target_col_right, str):
      raise TypeError("[DataManager] target column must be a string.")
    if not isinstance(merge_type, str):
      raise TypeError("[DataManager] merge_type must be a string.")
    
    #  validate columns
    valid_col_left: str | None = None
    valid_col_right: str | None = None
    if formatted_col_left != "index":
      valid_col_left = self.validate_col(target_df=target_df_left, target_col=target_col_left)
    else:
      valid_col_left = "index"
    if formatted_col_right != "index":
      valid_col_right: str = self.validate_col(target_df=target_df_right, target_col=target_col_right)
    else:
      valid_col_right = "index"
    
    #  validate merge type
    if formatted_merge_type not in ["left", "right", "inner", "outer", "cross"]:
      err_msg = f"[DataManager] failed to merge with {merge_type}. only accepted: inner, outer, left, right, and cross."
      logger.warning(err_msg)
      raise ValueError(err_msg)
    if formatted_merge_type == "cross" and formatted_col_left == "index" and formatted_col_right == "index":
      err_msg = f"[DataManager] cross merge method is not aapplicable for join indice."
      logger.warning(err_msg)
      raise ValueError(err_msg)
    
    #  merge tables
    if formatted_col_left == "index" and formatted_col_right== "index":
      output =target_df_left.join(target_df_right, how=merge_type, lsuffix="", rsuffix="_y")
    
    elif formatted_col_left == "index" and formatted_col_right != "index":
      output =target_df_left.merge(target_df_right, left_index=True, right_on=valid_col_right, how=merge_type, suffixes=("", "_y"))
    
    elif formatted_col_left != "index" and formatted_col_right == "index":
      output=target_df_left.merge(target_df_right, right_index=True, left_on=valid_col_left, how=merge_type, suffixes=("", "_y"))
    
    else:
      output=target_df_left.merge(target_df_right, left_on=valid_col_left, right_on=valid_col_right, how=merge_type, suffixes=("", "_y"))
    
    #  output
    logger.info("[DataManager] a new merged table has been created.")
    return output
    
  
  
  #  DATA MANIPULATION
     
  def reshape_pivot(self, target_df: pd.DataFrame, target_cols: list, target_rows: list, target_val: str, target_aggfunc: str = "count", target_filling: int | None = None):
      
    #  validate types
    if not isinstance(target_df, pd.DataFrame):
      raise TypeError("[DataManager] target dataframe must be a pandas DataFrame.")
    if not isinstance(target_cols, list):
      raise TypeError("[DataManager] target column must be a list.")
    if not isinstance(target_rows, list):
      raise TypeError("[DataManager] target input must be a list.")
      
    #  validate column
    valid_col_list: list = []
    valid_row_list: list = []

    self.update_valid_lists(target_df, target_cols, valid_col_list)
    self.update_valid_lists(target_df,target_rows, valid_row_list)
    valid_val: str = self.validate_col(target_df=target_df, target_col=target_val)
    
    #  output 
    output = pd.pivot_table(data=target_df, columns=valid_col_list, index=valid_row_list, values=valid_val, aggfunc=target_aggfunc, fill_value=target_filling)
    logger.info("[DataManager] a new pivot table has been created.")
    return output
  
  
  def count_user_event_monthly(self, 
                               target_df: pd.DataFrame,
                               target_col: str,
                               target_row: str,
                               date_col: str) -> pd.DataFrame:
    
    output = target_df.copy()
    month_col: str = "Month"
    
    #  validate col name
    target_col_r = self.validate_col(target_df, target_col)
    target_row_r = self.validate_col(target_df, target_row)
    date_col = self.validate_col(target_df, date_col)
    
    #  grouping monthly in new column, remove date column
    date_col_r = self.validate_col(target_df, date_col)
    output[month_col] = output[date_col_r].dt.month
    output = self.remove_col(output, date_col_r)
    
    #  grouping
    #  learnt: .size() used for traffic (task frequency), .nunique() used for usage (user engagement)
    output = output.groupby([month_col, target_row_r])[target_col_r].nunique().reset_index(name=f"{target_col_r}_Count")
    
    #  format in multiple index
    output = output.set_index([month_col, target_row_r]).sort_index(level=month_col)
    #  learnt: grouping before sort_values, otherwise sorting will not based on month
    #  learnt: groupkey = False, prevent duplicated column caused by data restructure with grouping
    #  learnt: no mapping in pd.DataFrame, use apply instead
    output = output.groupby(month_col, group_keys=False).apply(lambda el: el.sort_values(by=f"{target_col_r}_Count", ascending=False))
    return output
      
      
  def calculate_statistics(self,
                           target_df: pd.DataFrame,
                           target_row: str,
                           selected_row_list: list,
                           target_val: str,
                           date_col: str) -> pd.DataFrame:
    output = target_df.copy()
    stat_names: dict = {
      "month_col": "Month",
      "overall_row": "(Overall)",
      "mean_col": "Mean",
      "median_col": "Median",
      "mode_col": "Mode",
      "sum_col": "Total"
    }

    #  validate column names
    target_row_r: str = self.validate_col(target_df, target_row)
    target_val_r: str = self.validate_col(target_df, target_val)
    date_col_r: str = self.validate_col(target_df, date_col)
    
    output[stat_names["month_col"]] = output[date_col_r].dt.month
    output = self.remove_col(output, date_col_r)
    
    #  initialise tabular table by months and overall
    #  learnt: .isin() for list matches
    output_r = output[output[target_row_r].str.upper().isin([val.upper() for val in selected_row_list])]
    output_r = pd.pivot_table(data=output_r, 
                              columns=stat_names["month_col"], 
                              index=target_row_r, 
                              values=target_val_r, 
                              aggfunc="count", 
                              fill_value=0)

    #  append new row and merge
    #  reminder: specify axis 1 for matching formats
    #  learnt: to_frame turns the series in to a row of dataframe, enable to merge vertically
    #  learnt: the new row is vertically visualised, need to be transpose
    output_r[stat_names["overall_row"]]= output_r.sum(axis=1, numeric_only=True)

    #  calculate component statistic
    temp_mean_row = output_r.mean(numeric_only=True)
    temp_median_row = output_r.median(numeric_only=True)
    temp_mode_row = output_r.mode(numeric_only=True).iloc[0]
    temp_sum_row = output_r.sum(numeric_only=True)
    temp_mean_row.name = stat_names["mean_col"]
    temp_median_row.name = stat_names["median_col"]
    temp_mode_row.name = stat_names["mode_col"]
    temp_sum_row.name = stat_names["sum_col"]
    
    #  merge new statistic rows into dataframe
    output_r = pd.concat([output_r,
                          temp_mean_row.to_frame().T,
                          temp_median_row.to_frame().T,
                          temp_mode_row.to_frame().T,
                          temp_sum_row.to_frame().T])
    
    #  rename columns
    output_r.columns = [(MONNTH_LIST[str(col)][0:3].title() + "/25")  
                        if str(col) in MONNTH_LIST
                        else col 
                        for col in output_r.columns]
    
    return output_r