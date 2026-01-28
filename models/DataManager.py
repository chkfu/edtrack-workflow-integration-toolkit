import pandas as pd
import logging


#  LOGGING

logger = logging.getLogger("DATA_MANAGER")


#  CLASS

class DataManager:
  
  def __init__(self):
    self.col_name_list = None
    #  Learnt: prevent defer import validation controller into models
    #  remarks: temporary solution for breaking circular imports
    #  solution: in the future, validation to be done in controller, while models for simple calculation only
    from controllers.ValidController import ValidController
    self.valid_cont = ValidController()
    logger.info("initialised successfully.")
    
   
    
  #  METHOD - REUSE / SUPPORTING
    
  def update_valid_lists(self, target_df: pd.DataFrame, target_parameter: list, valid_list: list) -> list: 
    for el in target_parameter:
      testing_el = str(el).strip()
      valid_el = self.valid_cont.validate_col(target_df=target_df, target_col=testing_el)
      if valid_el:
        valid_list.append(valid_el) 
      else:
        logger.warning(f"Option {el} is not found, option skipped.")
     
        
  #  Remarks: supporting method to groupby_table
  def update_groupby_parameters(self, target_df: pd.DataFrame, input_list: list, acted_list: list) -> list:
    for column in input_list:
      if column not in target_df.columns:
        logger.warning(f"Column {column} is not valid, option skipped.")
      else:
        acted_list.append(column)
    return acted_list
  
  
  #  Remarks: supporting method to groupby_table 
  def get_mode(self, series: pd.Series) -> pd.Series | None:
    temp_mode = series.mode()
    length = len(temp_mode)
    if length < 1:
      return None
    #  Leanrt: set boundary for extraction, prevent unnecessary crash
    if length > 1:
      logger.warning("More than 1 mode are found.")
      return None
    return temp_mode.iloc[0]
    
  #  METHOD - CRUD
  
  def remove_col(self, target_df: pd.DataFrame, target_col: str) -> pd.DataFrame:
   
    #  validate types  
    if not isinstance(target_df, pd.DataFrame):
      raise TypeError("Target dataframe must be a pandas DataFrame.")
    if not isinstance(target_col, str):
      raise TypeError("Target column must be a string.")
    
    #  validate column
    valid_col: str = self.valid_cont.validate_col(target_df=target_df, target_col=target_col)
    if not valid_col:
      logger.error(f"'{target_col}' is not valid.", exc_info=True)
    #  output
    output = target_df.drop(columns=[valid_col])
    logger.info(f"Target column has been removed.")
    return output
    
    
  def remove_rows(self, target_df: pd.DataFrame, target_col: str, target_rows:list) -> pd.DataFrame:
    #  validate types
    if not isinstance(target_df, pd.DataFrame):
      raise TypeError("Target dataframe must be a pandas DataFrame.")
    if not isinstance(target_col, str):
      raise TypeError("Target column must be a string.")
    if not isinstance(target_rows, list):
      raise TypeError("Target input must be a list of strings.")
    
    #  validate column
    valid_col: str = self.valid_cont.validate_col(target_df=target_df, target_col=target_col)
    
    #  validate row
    rows_removal = {str(el).strip().lower() for el in target_rows}
    col_series = (target_df[valid_col].astype(str).str.strip().str.lower())
    matched_list: pd.Series = col_series.isin(rows_removal)  # isin() extracts rows with matched criteria
    
    #  output
    output = target_df[~matched_list]   # learnt: ~ sign as NOT operator
    logger.info(f"[DataManager] target row(s) has/have been removed.")
    return output
  
      
  def rename_col(self, target_df: pd.DataFrame, target_col: str, new_name: str) -> pd.DataFrame:
    
    #  validate types
    if not isinstance(target_df, pd.DataFrame):
      raise TypeError("Target dataframe must be a pandas DataFrame.")
    if not isinstance(target_col, str):
      raise TypeError(f"Target column {target_col} must be a string.")
    
    #  validate column
    valid_col: str = self.valid_cont.validate_col(target_df=target_df, target_col=target_col)
    
    #  convert name
    new_name_r: str = str(new_name).strip()
    
    # output
    output:  pd.DataFrame = target_df.rename(columns={valid_col: new_name_r})
    logger.info(f"The target column {target_col} has been renamed as {new_name_r}")
    return output
    
    
  def merge_tables(self, target_df_left: pd.DataFrame, target_df_right: pd.DataFrame, target_col_left: str, target_col_right: str, merge_type: str = "inner") -> pd.DataFrame:
    #  validate types
    if not isinstance(target_df_left, pd.DataFrame) or not isinstance(target_df_right, pd.DataFrame):
        raise TypeError("Target dataframe must be a pandas DataFrame.")
    if not isinstance(target_col_left, str) or not isinstance(target_col_right, str):
        raise TypeError("Target column must be a string.")
    if not isinstance(merge_type, str):
        raise TypeError("Merge_type must be a string.")

    formatted_col_left: str = target_col_left.strip().lower()
    formatted_col_right: str = target_col_right.strip().lower()
    formatted_merge_type: str = merge_type.strip().lower()

    #  validate columns
    if formatted_col_left == "index":
      valid_col_left = "index"
    else:
      valid_col_left = self.valid_cont.validate_col(target_df=target_df_left,
                                                    target_col=target_col_left)
    if formatted_col_right == "index":
      valid_col_right = "index"
    else:
      valid_col_right = self.valid_cont.validate_col(target_df=target_df_right,
                                                     target_col=target_col_right)
    if valid_col_left is None or valid_col_right is None:
      raise ValueError("[DataManager] invalid merge column after validation.")

    #  validate merge type
    if formatted_merge_type not in ["left", "right", "inner", "outer", "cross"]:
      err_msg = f"Failed to merge with {merge_type}. only accepted: inner, outer, left, right, and cross."
      logger.warning(err_msg)
      raise ValueError(err_msg)

    if formatted_merge_type == "cross" and formatted_col_left == "index" and formatted_col_right == "index":
      err_msg = "Cross merge method is not applicable for join indice."
      logger.warning(err_msg)
      raise ValueError(err_msg)

    #  merge tables
    if formatted_col_left == "index" and formatted_col_right == "index":
      output = target_df_left.join(target_df_right,
                                   how=formatted_merge_type,
                                   rsuffix="_y")

    elif formatted_col_left == "index" and formatted_col_right != "index":
      output = target_df_left.merge(target_df_right,
                                    left_index=True,
                                    right_on=valid_col_right,
                                    how=formatted_merge_type,
                                    suffixes=("", "_y"))

    elif formatted_col_left != "index" and formatted_col_right == "index":
      output = target_df_left.merge(target_df_right,
                                    right_index=True,
                                    left_on=valid_col_left,
                                    how=formatted_merge_type,
                                    suffixes=("", "_y"))

    else:
      output = target_df_left.merge(target_df_right,
                                    left_on=valid_col_left,
                                    right_on=valid_col_right,
                                    how=formatted_merge_type,
                                    suffixes=("", "_y"))

    #  output
    logger.info("A new merged table has been created.")
    return output
  
  
  #  DATA MANIPULATION
     
  def reshape_pivot(self, target_df: pd.DataFrame, target_cols: list, target_rows: list, target_val: str, target_aggfunc: str, target_filling: int | None) -> pd.DataFrame:
      
    #  validate types
    if not isinstance(target_df, pd.DataFrame):
      raise TypeError("Target dataframe must be a pandas DataFrame.")
    if not isinstance(target_cols, list):
      raise TypeError("Target column must be a list.")
    if not isinstance(target_rows, list):
      raise TypeError("Target input must be a list.")
      
    #  validate column
    valid_col_list: list = []
    valid_row_list: list = []

    self.update_valid_lists(target_df, target_cols, valid_col_list)
    self.update_valid_lists(target_df,target_rows, valid_row_list)
    valid_val: str = self.valid_cont.validate_col(target_df=target_df, target_col=target_val)
    
    #  output 
    output = pd.pivot_table(data=target_df, columns=valid_col_list, index=valid_row_list, values=valid_val, aggfunc=target_aggfunc, fill_value=target_filling)
    logger.info("A new pivot table has been created.")
    return output



  def groupby_table(self, target_df: pd.DataFrame, target_groupby_cols: list, target_val_cols: list, target_agg_func: list) -> pd.DataFrame:
    
    #  declaration
    result_df = None
    acted_groupby: list = []
    acted_vals: list = []
    acted_aggs: list = []
    AGG_FUNC_LIST: list = ["sum", "mean", "median", "mode"]
    
    #  validate types
    
    #  1. valid dataframe
    if not isinstance(target_df, pd.DataFrame):
      raise TypeError("Target dataframe must be a pandas DataFrame.")
    
    #  2. valid input list
    acted_groupby: list = self.update_groupby_parameters(target_df=target_df,
                                                         input_list=target_groupby_cols,
                                                         acted_list=acted_groupby)
    acted_vals: list = self.update_groupby_parameters(target_df=target_df,
                                                      input_list=target_val_cols,
                                                      acted_list=acted_vals)
    if not acted_groupby:
      raise ValueError("No valid groupby columns.")
    if not acted_vals:
      raise ValueError("No aggregation option is specified.")
    
    #  3. update agg functions list (temp)
    
    for agg in target_agg_func:
      agg = agg.strip().lower()
      if agg not in AGG_FUNC_LIST:
        logger.warning(f"Aggrefate option {agg} is not valid, option skipped.")
      else:
        acted_aggs.append(agg)
     
    #  exercise groupby dataframe
    result_df = target_df.groupby(acted_groupby, dropna=False)[acted_vals].agg('count')
    result_df.columns = [col for col in result_df.columns]
    
    #  exercise aggregations
    for agg in acted_aggs:
      for col in result_df.columns:
        col_name = f"{col} ({agg})"
        if agg == "sum":
          result_df[col_name] = result_df[col].sum()
        elif agg == "mean":
          result_df[col_name] = result_df[col].mean()
        elif agg == "median":
          result_df[col_name] = result_df[col].median()
        elif agg == "mode":
          mode_val = result_df[col].mode()
          result_df[col_name] = mode_val.iloc[0] if not mode_val.empty else None
    
    #  return dataframe, prevent crash with empty dataframe
    if result_df is not None:
      return result_df
    else:
      return pd.DataFrame(columns=acted_groupby)