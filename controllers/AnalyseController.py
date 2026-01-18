import logging
import pandas as pd
from controllers.ValidController import ValidController
from models.DataManager import DataManager
from views.components.config.views_config import MERGE_METHOD_OPT


#  LOGGING

logger = logging.getLogger("ANALYSE_CONTROLLER")


# CLASS

class AnalyseController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    self.data_manager = DataManager()
    logger.info("initialised sucessfully.")
    
    
  #  METHODS - GENERAL
  
  #  Remarks: update tabs at analyse state
  def handle_analyse_tab_switch(self, target_index: int):
    if target_index == 0:
      self.app.analyse_state.set_curr_tab("Pivots")
    elif target_index == 1:
      self.app.analyse_state.set_curr_tab("Metrics")
    elif target_index == 2:
      self.app.analyse_state.set_curr_tab("Graphs")
    else:
      return
    
    
  #  Remarks: generate list for dropdown options
  def deliver_col_opts(self) -> list:
    include_list: list = [col for col in self.app.merge_state.merge_proc.columns]
    return ["--- Please Select ---", *include_list]
  
  
  #  Remarks: generate list of aggregation options
  def deliver_agg_func_opts(self) -> list:
    include_list: list = ["Number of Entries (Exclude Blanks)",
                          "Number of Entries (Include Blanks)",
                          "Number of Different Items",
                          "Total Value",
                          "Minimum Value",
                          "Average Value",
                          "Maximum Value"]
    return ["--- Please Select ---", *include_list]
  
  
  #  Remarks: generate list of fill options
  def deliver_fill_opts(self) -> list:
    include_list: list = ["Remain Blank",
                          "Fill Zero"]
    return ["--- Please Select ---", *include_list]

  #  METHODS - TABS SPEC

  #  Remarks: for updating analyse options into analyse state
  def analyse_dd_pivot_event(self, target_col: str, selected_text: str) -> None:
    if selected_text == "--- Please Select ---":
      return
    if target_col == "pivots_col_01":
      self.app.analyse_state.set_pivots_col_01(selected_text)
    elif target_col == "pivots_col_02":
      self.app.analyse_state.set_pivots_col_02(selected_text)
    elif target_col == "pivots_row_01":
      self.app.analyse_state.set_pivots_row_01(selected_text)
    elif target_col == "pivots_row_02":
      self.app.analyse_state.set_pivots_row_02(selected_text)
    elif target_col == "pivots_val_01":
      self.app.analyse_state.set_pivots_val_01(selected_text)
    elif target_col == "agg_func":
      self.app.analyse_state.set_pivots_agg_func(selected_text)
    elif target_col == "fill":
      self.app.analyse_state.set_pivots_fill(selected_text)
    else:
      return
    
    
  
  
  
  
  #  METHODS - BTN EVENTS
  
  #  Remarks: identify tab and forwarding corr actions
  def proceed_btn_event_generator(self, tab_list: list, target_tab: str) -> None:
    
    #  error handling
    if target_tab not in tab_list:
      err_msg = f"Failed to proceed the analysis. Tab {target_tab} is not found."
      self.app.comp_fact.build_reminder_box(title="Error", 
                                            txt_msg=err_msg)
      logger.error(err_msg, exc_info=True)
      return
    
    #  run
    target_tab = str(target_tab).strip().lower()
    
    if target_tab == "pivots":
      self.execute_pivots_btn_event()
        
    elif target_tab == "metrics":
      print("metrics............................")
      pass
    
    elif target_tab == "graphs":
      print("graphs............................")
      pass
    
    else:
      err_msg = f"Failed to proceed the analysis. Invalid tab name."
      self.app.comp_fact.build_reminder_box(title="Error", 
                                            txt_msg=err_msg)
      logger.warning(err_msg)
    return
  
  
  #  Remarks: instructed by event generator and behaviors specifically (Pivots)
  #  TODO: error reminder should clarify if any requriement is missing
  def execute_pivots_btn_event(self):
    try:
      target_tb = self.data_manager.reshape_pivot(target_df=self.app.merge_state.merge_proc, 
                                                  target_cols=[col for col in [self.app.analyse_state.pivots_col_01, 
                                                                                self.app.analyse_state.pivots_col_02] 
                                                                if col], 
                                                  target_rows=[row for row in [self.app.analyse_state.pivots_row_01, 
                                                                                self.app.analyse_state.pivots_row_02] 
                                                                if row], 
                                                  target_val=self.app.analyse_state.pivots_val_01, 
                                                  target_aggfunc=self.app.analyse_state.pivots_agg_func,
                                                  target_filling=self.app.analyse_state.pivots_fill)
      self.app.comp_fact.build_popup_wd(wd_title="Preview Pivot Table",
                                        target_df=target_tb,
                                        popup_title=f"Preview Pivot Table",
                                        popup_content=self.app.comp_fact.build_table_view(target_df=target_tb))
    except Exception as ex:
      err_msg: str = f"Failed to prepare pivot table"
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=err_msg)
      logger.error(err_msg + f"- {ex}", exc_info=True)
  
  
  #  Remarks: instructed by event generator and behaviors specifically (Metrics)
  def execute_metrics_btn_event(self):
    try:
      pass
    except Exception as ex:
      err_msg: str = f"Failed to prepare metrics table"
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=err_msg)
      logger.error(err_msg + f"- {ex}", exc_info=True)
      
      
  #  Remarks: instructed by event generator and behaviors specifically (Graphs)
  def execute_graphs_btn_event(self):
    try:
      pass
    except Exception as ex:
      err_msg: str = f"Failed to prepare graphs table"
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=err_msg)
      logger.error(err_msg + f"- {ex}", exc_info=True)
    



