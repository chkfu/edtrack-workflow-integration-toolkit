import pandas as pd
import pytest
from models.DataCleaner import DataCleaner


#  MAIN

class TestDataCleanerBasic:
  
  #  FIXTURE
  
  #  Learnt: enable diffent tests reuse the same item
  @pytest.fixture(autouse=True)
  def setup(self):
    self.cleaner = DataCleaner()
  
  
  #  METHODS
  
  """ ==== handle duplication ==== """
  
  #  Remarks: for duplicates, for no duplicates
  def test_handle_duplication_original(self):
    test_df: pd.DataFrame = pd.DataFrame({
      "col_a": ["item-1", "item-2", "item-3"], 
      "col_b": ["item-1", "item-2", "item-3"]})
    result = self.cleaner.handle_duplication(test_df)
    assert len(result) == 3
    assert result.equals(test_df)
  
  #  Remarks: for duplicates, for removing duplicates
  def test_handle_duplication_with_duplicates(self):
    test_df: pd.DataFrame = pd.DataFrame({
      "col_a": ["item-1", "item-1", "item-2"], 
      "col_b": ["item-1", "item-1", "item-3"]})
    result = self.cleaner.handle_duplication(test_df)
    assert len(result) == 2
    assert result["col_a"].tolist() == ["item-1", "item-2"]
  
  #  Remarks: for duplicates, for empty dataframe
  def test_handle_duplication_empty(self):
    test_df = pd.DataFrame(columns=["col_a", "col_b"])
    result = self.cleaner.handle_duplication(test_df)
    assert result.empty
    
  #  Remarks: for duplicates, for missing data
  def test_handle_duplication_missing(self):
    test_df: pd.DataFrame = pd.DataFrame({
      "col_a": ["item-1", "item-1", "item-2"], 
      "col_b": [None, None, None]
      })
    result = self.cleaner.handle_duplication(test_df)
    assert len(result) == 2
    assert result["col_a"].tolist() == ["item-1", "item-2"]
    assert result["col_b"].isna().all()
  
    
  """ ==== handle na ==== """
    
  #  Remarks: for NA, for no na
  def handle_na_original(self):
    test_df: pd.DataFrame = pd.DataFrame({
      "col_a": ["item-1", "item-2", "item-3"], 
      "col_b": ["item-1", "item-2", "item-3"]
    })
    result = self.cleaner.handle_na(test_df, drop_missing=True)
    assert len(result) == 3
    assert result["col_a"].tolist() == ["item-1", "item-2", "item-3"]
    assert result["col_b"].tolist() == ["item-1", "item-2", "item-3"]
    
  #  Remarks: for NA, for any na in 1 columns
  def test_handle_na_single_none(self):
    test_df: pd.DataFrame = pd.DataFrame({
      "col_a": ["item-1", "item-2", "item-3"], 
      "col_b": ["item-1", "item-2", None]
      })
    result = self.cleaner.handle_na(test_df, drop_missing=True)
    assert len(result) == 2
    assert result["col_a"].tolist() == ["item-1", "item-2"]
    assert result["col_b"].tolist() == ["item-1", "item-2"]
    
  #  Remarks: for NA, for any na in 2 columns
  def test_handle_na_plural_none(self):
    test_df: pd.DataFrame = pd.DataFrame({
      "col_a": [None, "item-2", "item-3"], 
      "col_b": ["item-1", "item-2", None]
      })
    result = self.cleaner.handle_na(test_df, drop_missing=True)
    assert len(result) == 1
    assert result["col_a"].tolist() == ["item-2"]
    assert result["col_b"].tolist() == ["item-2"]
    
  #  Remarks: for NA, for any na in 2 columns
  def test_handle_na_all_none(self):
    test_df: pd.DataFrame = pd.DataFrame({
      "col_a": [None, "item-2", "item-3"], 
      "col_b": ["item-1", "item-2", None]
      })
    result = self.cleaner.handle_na(test_df, drop_missing=True)
    assert result["col_a"].isna().all()
    assert result["col_b"].isna().all()
    
  #  Remarks: for NA, for empty dataframe
    #  Remarks: for NA, for na in 1 row
  def test_handle_na_empty(self):
    test_df = pd.DataFrame(columns=["col_a", "col_b"])
    result = self.cleaner.handle_na(test_df, drop_missing=True)
    assert result.empty
    
    
  """ ==== handle sort ==== """
    
  #  Remarks: for sorting, for all in acending
  def test_handle_sort_original_asc(self):
    test_df = pd.DataFrame({
      "col_a": ["item-2", "item-1", "item-3"], 
      "col_b": ["item-2", "item-1", "item-3"]
    })
    result = self.cleaner.handle_sort(test_df, sort_item="col_a", sort_ascending=True)
    assert len(result) == 3
    assert result["col_a"].tolist() == ["item-1", "item-2", "item-3"]
    assert result["col_b"].tolist() == ["item-1", "item-2", "item-3"]
    
  #  Remarks: for sorting, for all in descending
  def test_handle_sort_original_desc(self):
    test_df = pd.DataFrame({
      "col_a": ["item-2", "item-1", "item-3"], 
      "col_b": ["item-2", "item-1", "item-3"]
    })
    result = self.cleaner.handle_sort(test_df, sort_item="col_a", sort_ascending=False)
    assert len(result) == 3
    assert result["col_a"].tolist() == ["item-3", "item-2", "item-1"]
    assert result["col_b"].tolist() == ["item-3", "item-2", "item-1"]
    
  #  Remarks: for sorting, for any 1 None in ascending
  def test_handle_sort_single_none_asc(self):
    test_df = pd.DataFrame({
      "col_a": [None, "item-2", "item-3"], 
      "col_b": ["item-2", "item-1", "item-3"]
    })
    result = self.cleaner.handle_sort(test_df, sort_item="col_a", sort_ascending=True)
    assert len(result) == 3
    assert result["col_a"].tolist()[:2] == ["item-2", "item-3"]
    assert pd.isna(result["col_a"].iloc[2])
    
  #  Remarks: for sorting, for any 1 None in descending
  def test_handle_sort_single_none_desc(self):
    test_df = pd.DataFrame({
      "col_a": [None, "item-2", "item-3"], 
      "col_b": ["item-2", "item-1", "item-3"]
    })
    result = self.cleaner.handle_sort(test_df, sort_item="col_a", sort_ascending=False)
    assert len(result) == 3
    assert result["col_a"].tolist()[:2] == ["item-3", "item-2"]
    assert pd.isna(result["col_a"].iloc[2])
  
  #  Remarks: for sorting, for empty in ascending
  def test_handle_sort_original_asc(self):
    test_df = pd.DataFrame()
    result = self.cleaner.handle_sort(test_df, sort_item="col_a", sort_ascending=True)
    assert result["col_a"].tolist() == pd.DataFrame().empty()
    