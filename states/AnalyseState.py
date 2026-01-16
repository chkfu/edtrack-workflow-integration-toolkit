import pandas as pd
import logging


#  LOGGING

logger = logging.getLogger("ANALYSE_STATE")


#  CLASS

class AnalyseState:
  
  def __init__(self):
    
    #  DataFrame Management
    self.data_pivots: pd.DataFrame = None
    self.data_metrics: pd.DataFrame = None
    self.data_graphs: pd.DataFrame = None
    
    #  1. pivots options
    self.pivots_col_01: str | None = None
    self.pivots_col_02: str | None = None
    self.pivots_row_01: str | None = None
    self.pivots_row_02: str | None = None
    self.pivots_val: str | None = None
    
    #  2. metrics options
    self.metrics_col_01: str | None = None
    self.metrics_row_01: str | None = None
    self.metrics_val: str | None = None
    
    #  3. graphs options
    self.graphs_col_01: str | None = None
    self.graphs_row_01: str | None = None
    self.graphs_val: str | None = None


  #  METHODS
  
  #  1. set data state
  
  def set_data_pivots(self, target_df: pd.DataFrame) -> None:
    self.data_pivots = target_df
    
  def set_data_metrics(self, target_df: pd.DataFrame) -> None:
    self.data_metrics = target_df
    
  def set_data_graphs(self, target_df: pd.DataFrame) -> None:
    self.data_graphs = target_df
    
  #  2. set pivot options
  
  def set_pivots_col_01(self, target_col: str) -> None:
    self.pivots_col_01 = target_col 
    
  def set_pivots_col_02(self, target_col: str) -> None:
    self.pivots_col_02 = target_col
    
  def set_pivots_row_01(self, target_row: str) -> None:
    self.pivots_row_01 = target_row
    
  def set_pivots_row_02(self, target_row: str) -> None:
    self.pivots_row_02 = target_row
    
  def set_pivots_val(self, target_val: str) -> None:  
    self.pivots_val = target_val