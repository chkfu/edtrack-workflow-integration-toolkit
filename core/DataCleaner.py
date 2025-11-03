import re
import statistics
import pandas as pd

  
  
DEFAULT_DTYPE_CONFIG: dict = {
  "string": ["Action", "Code", "Component", "Target"],
  "integer": ["User Full Name *Anonymized"],
  "float": [],
  "boolean": [],
  "datetime": ["Date", "Time"]
}
  
  
  
#  CLASS
  
class DataCleaner:

  #  CONSTRUCTOR

  def __init__(self):
    print("[DataCleaner] initialised successfully.")
    
    
    
  #  METHOD -  SUPPORTING  -  Fisrt Screening
  
  def validate_col(self, 
                   target_df: pd.DataFrame, 
                   target_col: str) -> str:
    
    #  for index
    if target_col.strip().lower() == "index":
      return "index"
    #  for columns
    output = next((col for col in target_df.columns if col.strip().lower() == target_col.strip().lower()), None)
    if output is None:
      raise ValueError("[DataManager] target column is not found.")
    return output.strip()
  
  
  def handle_duplication(self, target_df: pd.DataFrame) -> pd.DataFrame:
    output = target_df.drop_duplicates()
    print("[DataCleaner] Duplicated record(s) has/have been removed.")
    return output
  
  
  def handle_na(self, 
                target_df: pd.DataFrame, 
                drop_missing: bool, 
                na_subset_col: list) -> pd.DataFrame:
    
    if not drop_missing:
        return target_df
    #  case NaN
    if na_subset_col is not None or na_subset_col != []:
      output = target_df.dropna()
    else:
      output = target_df.dropna(subset=[na_subset_col])
    return output
      
      
  def handle_sort(self, 
                  target_df: pd.DataFrame, 
                  target_col: str, 
                  is_ascending=True):
    
    if target_col == "index":
      output = target_df.sort_index(ascending=is_ascending)
    else:
      valid_col = self.validate_col(target_df, target_col)
      output = target_df.sort_values(by=valid_col, ascending=is_ascending)
    return output
  
  
  #  METHOD -  SUPPORTING  -  Fisrt Screening
  
  def validate_dtypes(self, 
                      target_df: pd.DataFrame, 
                      default_dtype: dict):
    
    for dtype, list in default_dtype.items():
      for col in list:
        if col not in target_df.columns:
          continue
        if dtype == "string":
          target_df[col] = target_df[col].astype("string").fillna("Not Specified")
        if dtype == "integer":
          target_df[col] = pd.to_numeric(target_df[col], errors="coerce").astype("Int64")
          target_df[col] = target_df[col].fillna(target_df[col].median())
        if dtype == "float":
          target_df[col] = pd.to_numeric(target_df[col], errors="coerce").astype("Float64")
          target_df[col] = target_df[col].fillna(target_df[col].median())
        if dtype == "boolean":
          target_df[col] = target_df[col].astype("boolean").fillna(False)
        if dtype == "datetime":
          target_df[col] = pd.to_datetime(target_df[col], errors="coerce", format="%d/%m/%Y")
    return target_df
  
  
  #  METHOD  -  SUPPORTING -  Second Screening
  
  def trim_string(self, input: str, isAlpha: bool=False) -> str:
    if pd.isna(input):
      return "Not Specified"
    if isAlpha:
      output = re.sub(r'[^A-Za-z]', "", input.strip())
    else:
        output = input.strip()
    if output == "":
      return "Not Specified"
    return output
  
  def manage_string_case(self, input: str, case: str="title") -> str:
    case = case.lower()
    if case not in ["upper", "lower", "capitalize", "capitalise", "title"]:
      return input.title()
    if case == "upper":
      output =  input.upper()
    elif case == "lower":
      output =  input.lower()
    elif case == "capitalise" or case == "capitalize":
      output = input.capitalize()
    else:
      output = input.title()
    return output
  
  def handle_num_na(self, series: pd.Series, filling: str="median"):   
    if filling.lower() not in ["mean", "median", "mode"]:
      return series
    if filling == "mean":
      temp_val = series.mean()
    elif filling == "mode":
      temp_val = statistics.mode(series)
    else:
      temp_val = series.median()
    if series.isna().any():
      series = series.fillna(temp_val)
    return series
  
  def spec_cleaning_str(self, target_df: pd.DataFrame, target_col: str) -> pd.DataFrame:
    output = target_df.copy()
    output[target_col] = output[target_col].astype("string").fillna("Not Specified")
    for index, value in target_df[target_col].items():
      temp_val = self.trim_string(input=value, isAlpha=False)
      temp_val = self.manage_string_case(input=value, case="title")
      output.loc[index, target_col] = temp_val
    return output
  
  def spec_cleaning_int(self, target_df: pd.DataFrame, target_col: str) -> pd.DataFrame:
    output = target_df.copy()
    output[target_col] = output[target_col].astype(str).map(lambda el: re.sub(r'[^0-9\.,]', "", el))
    output[target_col] = pd.to_numeric(output[target_col], errors="coerce")
    output[target_col] = self.handle_num_na(output[target_col], filling="median")
    output[target_col] = output[target_col].round().astype("Int64")
    return output

  def spec_cleaning_float(self, target_df: pd.DataFrame, target_col: str) -> pd.DataFrame:
    output = target_df.copy()
    output[target_col] = output[target_col].astype(str).map(lambda el: re.sub(r'[^0-9\.,]', "", el))
    output[target_col] = pd.to_numeric(output[target_col], errors="coerce")
    output[target_col] = self.handle_num_na(output[target_col], filling="median")
    output[target_col] = output[target_col].round(2).astype("Float64")
    return output
  
  #  METHOD  -  PIPELINES
  
  def first_data_cleaning(self, 
                          target_df: pd.DataFrame, 
                          drop_missing: bool = True,
                          na_subset_col = None,
                          sort_item: str = "index", 
                          sort_ascending: bool = True) -> pd.DataFrame:
    
    output = target_df.copy()
    
    #  validate data type
  
    if not isinstance(target_df, pd.DataFrame):
      raise TypeError("[DataCleaner] target dataframe must be a pandas DataFrame.")
    if not isinstance(drop_missing, bool):
      raise TypeError("[DataCleaner] the option for drop rows with missing cell must be boolean.")
    
    #  execution
    output  = self.handle_duplication(output)
    output  = self.handle_na(output, drop_missing, na_subset_col)
    output  = self.validate_dtypes(output, DEFAULT_DTYPE_CONFIG)
    output  = self.handle_sort(output, sort_item, sort_ascending)
    
    #  output
    if not output.empty:
      print("[DataCleaner] First cleaning is completed.")
    return output
  
  
  def second_data_cleaning(self, 
                           target_df: pd.DataFrame,
                           default_dtype: dict = DEFAULT_DTYPE_CONFIG) -> pd.DataFrame:
    
    if not isinstance(default_dtype, dict):
      raise TypeError("[DataCleaner] the input default data types config is not in dict format.")
  
    output = target_df.copy()
  
    for dtype, list in default_dtype.items():
      for col in list:
        
        if col not in target_df.columns:
          continue
        
        if dtype == "string":
          output = self.spec_cleaning_str(output, col)
        if dtype == "integer":
          output = self.spec_cleaning_int(output, col)
        if dtype == "float":
          output = self.spec_cleaning_float(output, col)
        if dtype == "boolean":
          output[col] = output[col].astype("boolean").fillna(False)
        if dtype == "datetime":
          output[col] = pd.to_datetime(output[col], errors="coerce", format="%d/%m/%Y")
                
    #  output
    if not output.empty:     
      print("Second cleaning is completed.")    
    return output
    
    
    