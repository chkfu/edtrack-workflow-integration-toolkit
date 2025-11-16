import re
import statistics
import pandas as pd
import logging

  
  
DEFAULT_DTYPE_CONFIG: dict = {
  "string": ["Action", "Code", "Component", "Target"],
  "integer": ["User Full Name *Anonymized"],
  "float": [],
  "boolean": [],
  "datetime": ["Date", "Time"]
}
  

#  LOGGING

logger = logging.getLogger("APPLICATION")

  
#  CLASS
  
class DataCleaner:

  #  CONSTRUCTOR

  def __init__(self):
    logger.info("[DataCleaner] initialised successfully.")
    
    
    
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
    logger.info("[DataCleaner] Duplicated record(s) has/have been removed.")
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
  
  
  #  METHOD  -  SUPPORTING -  Second Screening
  
  def trim_string(self, 
                  input: str, 
                  isAlpha: bool=False) -> str:
    if pd.isna(input):
      return "Not Specified"
    if isAlpha:
      output = re.sub(r'[^A-Za-z]', "", input.strip())
    else:
        output = input.strip()
    if output == "":
      return "Not Specified"
    return output
  
  
  def manage_string_case(self, 
                         input: str, 
                         case: str="title") -> str:
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
    return output.strip()
  
  def handle_num_na(self, 
                    series: pd.Series, 
                    filling: str="median") -> pd.Series:   
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
  
  
  def spec_cleaning_str(self, 
                        target_df: pd.DataFrame, 
                        target_col: str) -> pd.DataFrame:
    output = target_df.copy()
    output[target_col] = output[target_col].astype("string").fillna("Not Specified")
    for index, value in target_df[target_col].items():
      temp_val = self.trim_string(input=value, isAlpha=False)
      temp_val = self.manage_string_case(input=value, case="upper")
      output.loc[index, target_col] = temp_val
    return output
  
  
  def spec_cleaning_int(self, 
                        target_df: pd.DataFrame, 
                        target_col: str) -> pd.DataFrame:
    output = target_df.copy()
    output[target_col] = output[target_col].astype(str).str.strip().map(lambda el: re.sub(r'[^0-9\.,]', "", el))
    output[target_col] = pd.to_numeric(output[target_col], errors="coerce")
    output[target_col] = self.handle_num_na(output[target_col], filling="median")
    output[target_col] = output[target_col].round().astype("Int64")
    return output


  def spec_cleaning_float(self, 
                          target_df: pd.DataFrame, 
                          target_col: str) -> pd.DataFrame:
    output = target_df.copy()
    output[target_col] = output[target_col].astype(str).str.strip().map(lambda el: re.sub(r'[^0-9\.,]', "", el))
    output[target_col] = pd.to_numeric(output[target_col], errors="coerce")
    output[target_col] = self.handle_num_na(output[target_col], filling="median")
    output[target_col] = output[target_col].round(2).astype("Float64")
    pd.options.display.float_format = "{:.2f}".format
    return output
  
  
  def spec_cleaning_bool(self, 
                        target_df: pd.DataFrame, 
                        target_col: str) -> pd.DataFrame:
    output = target_df.copy()
    output[target_col] = output[target_col].astype(str).str.strip().str.lower()
    output[target_col] = output[target_col].replace({
                                                "true": True,
                                                "yes": True,
                                                "y": True,
                                                "1": True,
                                                "1.0": True,
                                                "false": False,
                                                "no": False,
                                                "n": False,
                                                "0": False,
                                                "0.0": False,
                                                "": False,
                                                "none": False,
                                                "nan": False
                                              })
    output[target_col] = output[target_col].astype("boolean").fillna(False)
    return output
  
  
  def spec_cleaning_datetime(self, 
              target_df: pd.DataFrame, 
              target_col: str) -> pd.DataFrame:
    output = target_df.copy()
    output[target_col] = output[target_col].astype(str).str.strip().str.lower()
    output[target_col] = pd.to_datetime(
                                output[target_col],
                                errors="coerce",
                                dayfirst=True,
                                infer_datetime_format=True
                            )
    return output
  
  
  #  METHOD  -  PIPELINES
  
  def first_data_cleaning(self, 
                          target_df: pd.DataFrame,
                          drop_duplicated: bool = True, 
                          drop_missing: bool = True,
                          na_subset_col = None,
                          sort_item: str = "index", 
                          sort_ascending: bool | None = True) -> pd.DataFrame:
    
  
    #  validate data type
    try:
      output = target_df.copy()
      if not isinstance(target_df, pd.DataFrame):
        raise TypeError("[DataCleaner] target dataframe must be a pandas DataFrame.")
      if not isinstance(drop_missing, bool):
        raise TypeError("[DataCleaner] the option for drop rows with missing cell must be boolean.")
      
      #  execution
      if drop_duplicated:
        output  = self.handle_duplication(output)
      if drop_missing:
        output  = self.handle_na(output, drop_missing, na_subset_col)
      if sort_item != "index" and sort_ascending is not None:
        output  = self.handle_sort(output, sort_item, sort_ascending)
      
      #  output
      if not output.empty:
        logger.info("[DataCleaner] First cleaning is completed.")
      return output
    
    except Exception as ex:
      logger.error("[DataCleaner] Failed to apply the first cleaniing.", exc_info=True)
  
  
  def second_data_cleaning(self, 
                           target_df: pd.DataFrame,
                           default_dtype: dict = DEFAULT_DTYPE_CONFIG) -> pd.DataFrame:
    
    if not isinstance(default_dtype, dict):
      raise TypeError("[DataCleaner] the input default data types config is not in dict format.")
  
    output = target_df.copy()
  
    try: 
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
            output = self.spec_cleaning_bool(output, col)  
          if dtype == "datetime":
            output = self.spec_cleaning_datetime(output, col)
          print()
                  
      #  output
      if not output.empty:     
        print("[DataCleaner] Second cleaning is completed.")    
      return output
      
    except Exception as ex:
      logger.error("[DataCleaner] Failed to apply the first cleaniing- {ex}.", exc_info=True)  
      