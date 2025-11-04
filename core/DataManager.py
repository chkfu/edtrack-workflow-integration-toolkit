import pandas as pd


class DataManager:
  
  def __init__(self):
    self.col_name_list = None
    print("[DataManager] initialised successfully.")
    
   
    
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
    print(f"[DataManager] target column has been removed.")
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
    print(f"[DataManager] target row(s) has/have been removed.")
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
    print(f"[DataManager] the target column {target_col} has been renamed as {new_name_r}")
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
      raise ValueError(f"[DataManager] failed to merge with {merge_type}. only accepted: inner, outer, left, right, and cross.")
    if formatted_merge_type == "cross" and formatted_col_left == "index" and formatted_col_right == "index":
      raise ValueError(f"[DataManager] cross merge method is not aapplicable for join indice.")
    
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
    print("[DataManager] a new merged table has been created.")
    return output
    
    
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
    print("[DataManager] a new pivot table has been created.")
    return output
  
  
  def count_user_event_monthly(self, 
                               target_df: pd.DataFrame,
                               date_col: str) -> pd.DataFrame:
    
    output = target_df.copy()
    month_col: str = "Month"
    
    #  grouping monthly in new column, remove date column
    date_col_r = self.validate_col(target_df, date_col)
    output[month_col] = output[date_col_r].dt.month
    output = self.remove_col(output, date_col_r)
    
    #  grouping
    #  learnt: .size() used for traffic (task frequency), .nunique() used for usage (user engagement)
    output = output.groupby(["Month", "Component"])["User"].nunique().reset_index(name="User_Count")
    
    #  format in multiple index
    output = output.set_index(["Month", "Component"]).sort_index(level="Month")
    #  learnt: grouping before sort_values, otherwise sorting will not based on month
    #  learnt: groupkey = False, prevent duplicated column caused by data restructure with grouping
    #  learnt: no mapping in pd.DataFrame, use apply instead
    output = output.groupby("Month", group_keys=False).apply(lambda el: el.sort_values(by="User_Count", ascending=False))
    return output
      
    