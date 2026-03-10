from unittest import result

import pandas as pd
import pytest
from models.DataCleaner import DataCleaner


#  MAIN

class TestDataCleanerTypes:
  
  #  FIXTURE
  
  #  Learnt: enable diffent tests reuse the same item
  @pytest.fixture(autouse=True)
  def setup(self):
    self.cleaner = DataCleaner()
  
  
  #  METHODS
  
  """   ****   (strings) trim string   ****   """
  
  #  Remarks: for trim string, for normal case without changes
  def test_trim_string_original(self):
    test_string = "test string @%^&"
    result = self.cleaner.trim_string(input=test_string, isAlpha=True)
    assert result == "teststring"
  
  #  Remarks: for trim string, for normal case with alpha
  def test_trim_string_original_alpha(self):
    test_string = "test string @%^&"
    result = self.cleaner.trim_string(input=test_string, isAlpha=False)
    assert result == "test string @%^&"
  
  #  Remarks: for trim string, for string with forward and backward spacing
  def test_trim_string_spacing(self):
    test_string = " test string @%^&"
    result = self.cleaner.trim_string(input=test_string, isAlpha=True)
    assert result == "teststring"
    
  #  Remarks: for trim string, for string with forward and backward spacing
  def test_trim_string_spec_space(self):
    test_string = "  @%^&  "
    result = self.cleaner.trim_string(input=test_string, isAlpha=False)
    assert result == "@%^&"
    
  #  Remarks: for trim string, for string with forward and backward spacing
  def test_trim_string_spec_alpha_spacing(self):
    test_string = "  @  %^&  "
    result = self.cleaner.trim_string(input=test_string, isAlpha=True)
    assert result == "Not Specified"
    
  #  Remarks: for trim string, for string with forward and backward spacing
  def test_trim_string_empty(self):
    test_string = ""
    result = self.cleaner.trim_string(input=test_string, isAlpha=True)
    assert result == "Not Specified"
    
  #  Remarks: for trim string, for string with forward and backward spacing
  def test_trim_string_only_space(self):
    test_string = "     "
    result = self.cleaner.trim_string(input=test_string, isAlpha=True)
    assert result == "Not Specified"
    
  #  Remarks: for trim string, for None
  def test_trim_string_missing(self):
    test_string = None
    result = self.cleaner.trim_string(input=test_string, isAlpha=True)
    assert result == "Not Specified"
    

  """   ****   (strings) manage_string_case   ****   """
  
  #  Remarks: for manage string case, for lower case
  def test_manage_string_case_lower(self):
    test_string = "TesT StriNg @%^&"
    result = self.cleaner.manage_string_case(input=test_string, case="lower")
    assert result == "test string @%^&"
    
  #  Remarks: for manage string case, for upper case
  def test_manage_string_case_upper(self):
    test_string = "TesT StriNg @%^&"
    result = self.cleaner.manage_string_case(input=test_string, case="upper")
    assert result == "TEST STRING @%^&"
  
  #  Remarks: for manage string case, for title case
  def test_manage_string_case_title(self):
    test_string = "TesT StriNg @%^&"
    result = self.cleaner.manage_string_case(input=test_string, case="title")
    assert result == "Test String @%^&" 
    
  #  Remarks: for manage string case, for capitalize case
  def test_manage_string_casecapitalize(self):
    test_string = "TesT StriNg @%^&"
    result = self.cleaner.manage_string_case(input=test_string, case="capitalize")
    assert result == "Test string @%^&" 
  
  #  Remarks: for manage string case, for invalid
  def test_manage_string_case_invalid(self):
    test_string = "test string"
    result = self.cleaner.manage_string_case(input=test_string, case="invalid")
    assert result == "Test String"
    
  #  Remarks: for manage string case, for capitalise case
  def test_manage_string_casecapitalise(self):
    test_string = "TesT StriNg @%^&"
    result = self.cleaner.manage_string_case(input=test_string, case="capitalize")
    assert result == "Test string @%^&" 
    
  #  Remarks: for manage string case, for strip case
  def test_manage_string_case_strips(self):
    test_string = "  TesT StriNg @%^&  "
    result = self.cleaner.manage_string_case(input=test_string, case="lower")
    assert result == "test string @%^&"
     
  #  Remarks: for manage string case, for spacing
  def test_manage_string_case_spacing(self):
    test_string = "  "
    result = self.cleaner.manage_string_case(input=test_string, case="lower")
    assert result == ""
  
  #  Remarks: for manage string case, for empty string
  def test_manage_string_case_empty(self):
    test_string = ""
    result = self.cleaner.manage_string_case(input=test_string, case="lower")
    assert result == ""
  
  #  Remarks: for manage string case, for None
  def test_manage_string_case_none(self):
    test_string = None
    result = self.cleaner.manage_string_case(input=test_string, case="lower")
    assert result == "Not Specified"
  
  
  """   ****   (numbers) handle_num_na   ****   """
  
  #  Remarks: for handle num na, for original case with no change
  def test_handle_num_na_original(self):
    test_series = pd.Series([1.0, 5.0, 5.0, 7.0, 9.0])
    test_filling = "mean"
    result = self.cleaner.handle_num_na(series=test_series, filling=test_filling)
    assert result.tolist() == [1.0, 5.0, 5.0, 7.0, 9.0]

  #  Remarks: for handle num na, for mean case
  def test_handle_num_na_mean(self):
    test_series = pd.Series([1.0, None, 5.0, 7.0, 9.0])
    test_filling = "mean"
    result = self.cleaner.handle_num_na(series=test_series, filling=test_filling)
    assert result.tolist() == [1.0, 5.5, 5.0, 7.0, 9.0]

  #  Remarks: for handle num na, for mean case with non-standard case filling
  def test_handle_num_na_mean_spec(self):
    test_series = pd.Series([1.0, None, 5.0, 7.0, 9.0])
    test_filling = "MeAn"
    result = self.cleaner.handle_num_na(series=test_series, filling=test_filling)
    assert result.tolist() == [1.0, 5.5, 5.0, 7.0, 9.0]
  
  #  Remarks: for handle num na, for median case
  def test_handle_num_na_median(self):
    test_series = pd.Series([1.0, None, 5.0, 7.0, 9.0])
    test_filling = "median"
    result = self.cleaner.handle_num_na(series=test_series, filling=test_filling)
    assert result.tolist() == [1.0, 6.0, 5.0, 7.0, 9.0]
  
  #  Remarks: for handle num na, for moce case with single mode filling
  def test_handle_num_na_mode_single(self):
    test_series = pd.Series([1.0, None, 5.0, 7.0, 7.0])
    test_filling = "mode"
    result = self.cleaner.handle_num_na(series=test_series, filling=test_filling)
    assert result.tolist() == [1.0, 7.0, 5.0, 7.0, 7.0]
    
  #  Remarks: for handle num na, for mode case with plural mode filling 
  def test_handle_num_na_mode_plural(self):
    test_series = pd.Series([1.0, None, 1.0, 7.0, 7.0])
    test_filling = "mode"
    result = self.cleaner.handle_num_na(series=test_series, filling=test_filling)
    assert result.tolist() == [1.0, 1.0, 1.0, 7.0, 7.0]
  
  #  Remarks: for handle num na, for all missing
  def test_handle_num_na_missing(self):
    test_series = pd.Series([None, None, None, None, None])
    test_filling = "mean"
    result = self.cleaner.handle_num_na(series=test_series, filling=test_filling)
    assert result.isna().all()
  
  #  Remarks: for handle num na, for empty
  def test_handle_num_na_empty(self):
    test_series = pd.Series()
    test_filling = "mode"
    result = self.cleaner.handle_num_na(series=test_series, filling=test_filling)
    assert result.tolist() == []
    
    
  
  """   ****   (strings) spec_cleaning_str, type-cleaning   ****   """
  
  #  Remarks: string type cleaning, for original case with no change
  def test_spec_cleaning_str_original(self):
    test_df = pd.DataFrame({
      "col-a": ["item 1", "item 2", "item 3"],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_str(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == ["ITEM 1", "ITEM 2", "ITEM 3"]
    
  #  Remarks: string type cleaning, for integer string case
  def test_spec_cleaning_str_int(self):
    test_df = pd.DataFrame({
      "col-a": [1, 2, 3],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_str(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == ["1", "2", "3"]   
    
  #  Remarks: string type cleaning, for float string case
  def test_spec_cleaning_str_float(self):
    test_df = pd.DataFrame({
      "col-a": [1.0, 2.0, 3.0],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_str(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == ["1.0", "2.0", "3.0"]
    
  #  Remarks: string type cleaning, for bool string case
  def test_spec_cleaning_str_bool(self):
    test_df = pd.DataFrame({
      "col-a": [True, False, True],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_str(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == ["TRUE", "FALSE", "TRUE"]
    
  #  Remarks: string type cleaning, for missing case
  def test_spec_cleaning_str_missing(self):
    test_df = pd.DataFrame({
      "col-a": [None, None, None],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_str(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == ["Not Specified", "Not Specified", "Not Specified"]
    
  
  """   ****   (numbers) spec_cleaning_int, type-cleaning   ****   """

  #  Remarks: integer type cleaning, for original case with no change
  def test_spec_cleaning_int_original(self):
    test_df = pd.DataFrame({
      "col-a": [1, 2, 3],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_int(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [1, 2, 3]
    
  #  Remarks: integer type cleaning, for string case with no change
  def test_spec_cleaning_int_string(self):
    test_df = pd.DataFrame({
      "col-a": ["1", "2", "3"],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_int(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [1, 2, 3]
    
  #  Remarks: integer type cleaning, for float case with no change
  def test_spec_cleaning_int_float(self):
    test_df = pd.DataFrame({
      "col-a": [1.0, 2.0, 3.0],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_int(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [1, 2, 3]
    
  #  Remarks: integer type cleaning, for boolean case with no change
  def test_spec_cleaning_int_bool(self):
    test_df = pd.DataFrame({
      "col-a": [True, False, True],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_int(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [1, 0, 1]
    
  #  Remarks: integer type cleaning, for missing case with no change
  def test_spec_cleaning_int_missing(self):
    test_df = pd.DataFrame({
      "col-a": [None, None, None],
      "col-b": [1, 2, 3]
    })
    #  Learnt: use 'with' word for check value errors
    with pytest.raises(ValueError):
      self.cleaner.spec_cleaning_int(target_df=test_df, target_col="col-a")
  
  
  """   ****   (numbers) spec_cleaning_float, type-cleaning   ****   """

  #  Remarks: integer type cleaning, for original case with no change
  def test_spec_cleaning_float_original(self):
    test_df = pd.DataFrame({
      "col-a": [1.0, 2.0, 3.0],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_float(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [1.0, 2.0, 3.0]
    
  #  Remarks: integer type cleaning, for string case with no change
  def test_spec_cleaning_float_string(self):
    test_df = pd.DataFrame({
      "col-a": ["1.0", "2.0", "3.0"],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_float(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [1.0, 2.0, 3.0]
    
  #  Remarks: integer type cleaning, for string case with no change
  def test_spec_cleaning_float_int(self):
    test_df = pd.DataFrame({
      "col-a": [1, 2, 3],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_float(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [1.0, 2.0, 3.0]
    
  #  Remarks: integer type cleaning, for string case with no change
  def test_spec_cleaning_float_bool(self):
    test_df = pd.DataFrame({
      "col-a": [True, False, True],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_float(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [1.0, 0.0, 1.0]
    
  #  Remarks: integer type cleaning, for missing case with no change
  def test_spec_cleaning_float_missing(self):
    test_df = pd.DataFrame({
      "col-a": [None, None, None],
      "col-b": [1, 2, 3]
    })
    #  Learnt: use 'with' word for check value errors
    with pytest.raises(ValueError):
      self.cleaner.spec_cleaning_float(target_df=test_df, target_col="col-a")
      
      
  """   ****   (booleans) spec_cleaning_bool, type-cleaning   ****   """

  #  Remarks: bool type cleaning, for original case with no change
  def test_spec_cleaning_bool_original(self):
    test_df = pd.DataFrame({
      "col-a": [True, False, True],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_bool(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [True, False, True]
    
  #  Remarks: bool type cleaning, for string case
  def test_spec_cleaning_bool_string(self):
    test_df = pd.DataFrame({
      "col-a": ["True", "False", "True"],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_bool(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [True, False, True]
    
  #  Remarks: bool type cleaning, for string case with Yes-No format
  def test_spec_cleaning_bool_langStr(self):
    test_df = pd.DataFrame({
      "col-a": ["Yes", "No", "Yes"],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_bool(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [True, False, True]
    
  #  Remarks: bool type cleaning, for string case with 1-0 format
  def test_spec_cleaning_bool_intStr(self):
    test_df = pd.DataFrame({
      "col-a": ["1", "0", "1"],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_bool(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [True, False, True]
    
  #  Remarks: bool type cleaning, for string case with 1.0-0.0 format
  def test_spec_cleaning_bool_floatStr(self):
    test_df = pd.DataFrame({
      "col-a": ["1.0", "0.0", "1.0"],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_bool(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [True, False, True]
    
  #  Remarks: bool type cleaning, for int case
  def test_spec_cleaning_bool_int(self):
    test_df = pd.DataFrame({
      "col-a": [1, 0, 1],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_bool(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [True, False, True]
    
  #  Remarks: bool type cleaning, for float case
  def test_spec_cleaning_bool_float(self):
    test_df = pd.DataFrame({
      "col-a": [1.0, 0.0, 1.0],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_bool(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [True, False, True]
    
  #  Remarks: bool type cleaning, for missing case with no change
  def test_spec_cleaning_bool_missing(self):
    test_df = pd.DataFrame({
      "col-a": [None, None, None],
      "col-b": [1, 2, 3]
    })
    result = self.cleaner.spec_cleaning_bool(target_df=test_df, target_col="col-a")
    assert len(result) == 3
    assert result["col-a"].tolist() == [False, False, False]
  
  
  """   ****   (datetime) spec_cleaning_datetime, type-cleaning   ****   """

  #  Remarks: datetime type cleaning, for original datetime case with no change
  def test_spec_cleaning_datetime_original(self):
      test_df = pd.DataFrame({
          "col-a": [pd.Timestamp("2021-01-01"), pd.Timestamp("2021-01-02"), pd.Timestamp("2021-01-03")],
          "col-b": [1, 2, 3]
      })
      result = self.cleaner.spec_cleaning_datetime(target_df=test_df, target_col="col-a")
      assert len(result) == 3
      assert result["col-a"].tolist() == [pd.Timestamp("2021-01-01"), pd.Timestamp("2021-01-02"), pd.Timestamp("2021-01-03")]

  #  Remarks: datetime type cleaning, for string case
  def test_spec_cleaning_datetime_string(self):
      test_df = pd.DataFrame({
          "col-a": ["2021-01-01", "2021-01-02", "2021-01-03"],
          "col-b": [1, 2, 3]
      })
      result = self.cleaner.spec_cleaning_datetime(target_df=test_df, target_col="col-a")
      assert len(result) == 3
      assert result["col-a"].tolist() == [pd.Timestamp("2021-01-01"), pd.Timestamp("2021-01-02"), pd.Timestamp("2021-01-03")]

  #  Remarks: datetime type cleaning, for string case with day-first format
  def test_spec_cleaning_datetime_dayFirst(self):
      test_df = pd.DataFrame({
          "col-a": ["01/01/2021", "02/01/2021", "03/01/2021"],
          "col-b": [1, 2, 3]
      })
      result = self.cleaner.spec_cleaning_datetime(target_df=test_df, target_col="col-a")
      assert len(result) == 3
      assert result["col-a"].tolist() == [pd.Timestamp("2021-01-01"), pd.Timestamp("2021-01-02"), pd.Timestamp("2021-01-03")]

  #  Remarks: datetime type cleaning, for string case with datetime format
  def test_spec_cleaning_datetime_withTime(self):
      test_df = pd.DataFrame({
          "col-a": ["2021-01-01 12:00:00", "2021-01-02 13:00:00", "2021-01-03 14:00:00"],
          "col-b": [1, 2, 3]
      })
      result = self.cleaner.spec_cleaning_datetime(target_df=test_df, target_col="col-a")
      assert len(result) == 3
      assert result["col-a"].tolist() == [pd.Timestamp("2021-01-01 12:00:00"), pd.Timestamp("2021-01-02 13:00:00"), pd.Timestamp("2021-01-03 14:00:00")]

  #  Remarks: datetime type cleaning, for all missing case
  def test_spec_cleaning_datetime_missing(self):
      test_df = pd.DataFrame({
          "col-a": [None, None, None],
          "col-b": [1, 2, 3]
      })
      with pytest.raises(ValueError):
          self.cleaner.spec_cleaning_datetime(target_df=test_df, target_col="col-a")