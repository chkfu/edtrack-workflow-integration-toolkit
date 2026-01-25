import pandas as pd
from PyQt5.QtCore import Qt
import logging


#  LOGGING

logger = logging.getLogger("ANALYSE_STATE")


#  CLASS

class AnalyseState:
  
  def __init__(self):
    
    #  Tab States
    self.TAB_LIST: list = ["Pivots", "Metrics", "Graphs"]
    self.curr_tab: str = "Pivots"
    
    #  DataFrame Management
    self.data_pivots: pd.DataFrame = None
    self.data_metrics: pd.DataFrame = None
    self.data_graphs: pd.DataFrame = None

    #  1. pivots options
    self.pivots_col_01: str | None = None
    self.pivots_col_02: str | None = None
    self.pivots_row_01: str | None = None
    self.pivots_row_02: str | None = None
    self.pivots_val_01: str | None = None
    self.pivots_agg_func: str | None = None
    self.pivots_fill: str | None = None

    #  2. metrics options
    self.metrics_grouped_01: str | None = None
    self.metrics_grouped_02: str | None = None
    self.metrics_val_list: list | None = None
    self.metrics_agg_func_list: list | None = None

    #  3. graphs options
    self.graphs_col_01: str | None = None
    self.graphs_row_01: str | None = None
    self.graphs_val_01: str | None = None


  #  METHODS
  
  #  1. set tabs
  
  def set_tab_list(self, target_list) -> None:
    self.TAB_LIST = target_list
    
  def set_curr_tab(self, target_tab) -> None:
    self.curr_tab = target_tab
  
  
  #  2. set data state

  def set_data_pivots(self, target_df: pd.DataFrame) -> None:
    self.data_pivots = target_df


  def set_data_metrics(self, target_df: pd.DataFrame) -> None:
    self.data_metrics = target_df


  def set_data_graphs(self, target_df: pd.DataFrame) -> None:
    self.data_graphs = target_df


  #  2. set pivots options

  def set_pivots_col_01(self, target_col: str) -> None:
    self.pivots_col_01 = target_col


  def set_pivots_col_02(self, target_col: str) -> None:
    self.pivots_col_02 = target_col


  def set_pivots_row_01(self, target_row: str) -> None:
    self.pivots_row_01 = target_row


  def set_pivots_row_02(self, target_row: str) -> None:
    self.pivots_row_02 = target_row


  def set_pivots_val_01(self, target_val: str) -> None:
    self.pivots_val_01 = target_val
    
    
  def set_pivots_agg_func(self, target_fn: str) -> None:
    AGGFUNC_OPTS: dict = {"Number of Entries (Exclude Blanks)" : "count",
                          "Number of Entries (Include Blanks)": "size",
                          "Number of Different Items": "nunique",
                          "Total Value": "sum",
                          "Minimum Value": "min",
                          "Average Value": "mean",
                          "Maximum Value": "max"}  
    if target_fn not in AGGFUNC_OPTS:
      self.pivots_agg_func = None
      return
    self.pivots_agg_func = AGGFUNC_OPTS[target_fn]
    return
    
    
  def set_pivots_fill(self, target_fill: str) -> None:
    FILL_OPTS = {
      "Remain Blank": None,
      "Fill Zero": 0
    }
    if target_fill not in FILL_OPTS:
      self.pivots_fill = None
      return
    self.pivots_fill = FILL_OPTS[target_fill]
    return
  
  
  #  3. set metrics options
  
  def set_metrics_grouped_01(self, target_col: str) -> None:
    self.metrics_grouped_01 = target_col
    
  
  def set_metrics_grouped_02(self, target_col: str) -> None:
    self.metrics_grouped_02 = target_col
    
    
  #  remarks: list-based, checkbox return a full list directly
  def set_metrics_val_list(self, target_state: Qt.Checked, target_col: str) -> None:
    if target_state == Qt.Checked:
      self.metrics_val_list.append(target_col)
    elif target_state == Qt.UnChecked:
      self.metrics_val_list.remove(target_col)
    else:
      return
    return
  
  
  #  remarks: list-based, checkbox return a full list directly
  def set_metrics_agg_func_list(self, target_state: Qt.Checked, target_col: str) -> None:
    if target_col not in ["count", "sum", "mean", "mode", "median"]:
      pass
    if target_state == Qt.Checked:
      self.metrics_agg_func_list.append(target_col)
    elif target_state == Qt.UnChecked:
      self.metrics_agg_func_list.remove(target_col)
    else:
      return
    return
    
    
  #  4. set graphs options