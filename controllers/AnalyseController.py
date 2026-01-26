import logging
from PyQt5.QtCore import Qt
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
  def deliver_pivots_col_opts(self) -> list:
    if self.app.merge_state.merge_proc is None:
      return ["--- Please Select ---"]
    include_list: list = [col for col in self.app.merge_state.merge_proc.columns]
    return ["--- Please Select ---", *include_list]
  
  
  #  Remarks: generate list of metrics value column options 
  def deliver_metrics_val_col_opts(self) -> list:
    if self.app.merge_state.merge_proc is None:
      return []
    include_list: list = [col for col in self.app.merge_state.merge_proc.columns]
    return include_list
  
  
  #  Remarks: generate list of aggregation options
  def deliver_pivots_agg_func_opts(self) -> list:
    include_list: list = ["Number of Entries (Exclude Blanks)",
                          "Number of Entries (Include Blanks)",
                          "Number of Different Items",
                          "Total Value",
                          "Minimum Value",
                          "Average Value",
                          "Maximum Value"]
    return ["--- Please Select ---", *include_list]
  
  
  #  Remarks: generate list of fill options
  def deliver_pivots_fill_opts(self) -> list:
    include_list: list = ["Remain Blank",
                          "Fill Zero"]
    return ["--- Please Select ---", *include_list]


  #  METHODS - TABS SPEC

  #  Remarks: for updating analyse options into analyse state
  def analyse_dd_pivots_event(self, target_col: str, selected_text: str) -> None:
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
    
      
  #  Remarks: for updating analyse options into analyse state
  def analyse_dd_metrics_event(self, target_col: str, selected_text: str, selected_state: Qt.CheckState | None) -> None:
    if selected_text == "--- Please Select ---":
      return
    if target_col == "metrics_groupby_01":
      self.app.analyse_state.set_metrics_grouped_01(target_col=selected_text)
    elif target_col == "metrics_groupby_02":
      self.app.analyse_state.set_metrics_grouped_02(target_col=selected_text)
    elif target_col == "metrics_val_cell":
      self.app.analyse_state.set_metrics_val_list(target_col=selected_text,
                                                  target_state=selected_state)
    elif target_col == "metrics_agg_func_cell":
      self.app.analyse_state.set_metrics_agg_func_list(target_col=selected_text,
                                                       target_state=selected_state)
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
      self.execute_metrics_btn_event()
    
    elif target_tab == "graphs":
      self.execute_graphs_btn_event()
    
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
      self.app.comp_fact.build_popup_wd(wd_title="Preview Pivots Table",
                                        target_df=target_tb,
                                        popup_title=f"Preview Pivots Table",
                                        popup_content=self.app.comp_fact.build_table_view(target_df=target_tb))
    except Exception as ex:
      err_msg: str = f"Failed to prepare pivots table"
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=err_msg)
      logger.error(err_msg + f"- {ex}", exc_info=True)
  
  
  #  Remarks: instructed by event generator and behaviors specifically (Metrics)
  def execute_metrics_btn_event(self):
    try:
      #  1. decalrarion
      input_groupby: list = [self.app.analyse_state.metrics_grouped_01,
                             self.app.analyse_state.metrics_grouped_02]
      input_val: list = self.app.analyse_state.metrics_val_list
      input_agg_func: list = self.app.analyse_state.metrics_agg_func_list
      
      #  2. validate inputs 
         
      #  2a. invalid list parameters
      if not input_groupby or input_groupby.empty:
        err_msg: str = f"Failed to transform metrics table. Invalid parameters: groupby column list"
        logger.warning(err_msg)
        raise ValueError(err_msg)
      if not input_val or input_val.empty:
        err_msg: str = f"Failed to transform metrics table. Invalid parameters: value column list"
        logger.warning(err_msg)
        raise ValueError(err_msg)
      #  trade-offs: pure groupby methods for empty, or statistical analysis with opts
      if not input_agg_func or input_agg_func.empty:
        input_agg_func = []
        
      #  2b. invalid value to be processed
      for column in input_groupby:
        self.app.valid_cont.validate_col(target_df=self.app.merge_state.merge_proc,
                                         target_col=column)
      for column in input_val:
        self.app.valid_cont.validate_col(target_df=self.app.merge_state.merge_proc,
                                         target_col=column)
        
      #  2c. remove invalid items, in case mistakenly input as final check
      #      trade-offs: pure groupby methods for empty, or statistical analysis with opts
      for column in input_agg_func:
        if column.strip().lower() not in ["count", "sum", "mean", "mode", "median"]:
          input_agg_func.remove(column)
      
      #  3. data transformation 
      target_tb = self.app.data_manager.groupby_table(target_df=self.app.merge_state.merge_proc, 
                                                      target_groupby_cols=input_groupby, 
                                                      target_val_cols=input_val, 
                                                      target_agg_func=input_agg_func)
      #  4. build pop-up window
      self.app.comp_fact.build_popup_wd(wd_title="Preview Metrics Table",
                                        target_df=target_tb,
                                        popup_title=f"Preview Metrics Table",
                                        popup_content=self.app.comp_fact.build_table_view(target_df=target_tb))
    
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
      
      
  #  METHODS - REFRESH
  
  # def refresh_checkbox_cell(self, target_tab: str, target_state_name: str, new_opt_list: list): 
  #   #  1. get layout from temp state
  #   cb_layout = getattr(self, f"{target_tab}_{target_state_name}_layout", None)
  #   if not cb_layout: 
  #     return
    
  #   #  2. remove original child items
  #   #  Learnt: use countdown to make sure the continuity of child removal
  #   while cb_layout.count() > 0:
  #     child = cb_layout.takeAt(0)
  #     if child.widget():
  #       child.widget().deleteLater()
        
  #   #  3. build new children
  #   temp_list: list = []
  #   if not new_opt_list or len(new_opt_list) < 1:
  #     err_lb = self.app.comp_fact.build_label(lb_text="(No option found)", lb_align=Qt.AlignLeft)
  #     cb_layout.addWidget(err_lb)
  #   else:
  #     for column in new_opt_list:
  #       cb = self.app.comp_fact.build_checkbox(target_name=column, target_event=None)
  #       cb_layout.addWidget(cb)
  #       temp_list.append(cb)
  #     setattr(self, f"{target_tab}_{target_state_name}", temp_list)
      
  
  def reset_analyse_option_generator(self, target_tab):
    #  error handling
    target_tab_r = target_tab.strip().lower()
    if target_tab_r not in ["pivots", "metrics", "graphs", "all"]:
      err_msg: str = f"Failed to reset the options due to invalid tab of targets - {target_tab}"
      self.app.comp_fact.build_reminder_box(err_msg)
      logger.warning(err_msg)
      return
    #  Remarks: operate reset
    RESET_DECISIONS: dict = {
      "pivots": self.reset_pivots_options,
      "metrics": self.reset_metrics_options,
      "graphs": self.reset_graphs_options,
      "all": self.reset_all_options
    }
    return RESET_DECISIONS[target_tab]()

  
  def reset_pivots_options(self) -> None:
    self.app.pages_fact.page_analyse.reset_widget_display(self, target_tab="pivots")
    self.app.analyse_state.reset_state_generator(target_tab="pivots")
    logger.info("Pivots options has been reset at PageAnalyse.")
    return
  
    
  def reset_metrics_options(self) -> None:
    self.app.pages_fact.page_analyse.reset_widget_display(self, target_tab="metrics")
    self.app.analyse_state.reset_state_generator(target_tab="metircs")
    logger.info("Metrics options has been reset at PageAnalyse.")
    return
  
  
  def reset_graphs_options(self) -> None:
    self.app.pages_fact.page_analyse.reset_widget_display(self, target_tab="graphs")
    self.app.analyse_state.reset_state_generator(target_tab="graphs")
    logger.info("Graphs options has been reset at PageAnalyse.")
    return
  
  
  def reset_all_options(self) -> None:
    self.reset_pivots_options()
    self.reset_metrics_options()
    self.reset_graphs_options()
    #  Remarks: reset general setting in analyse state
    self.TAB_LIST: list = ["Pivots", "Metrics", "Graphs"]
    self.curr_tab: str = "Pivots"
    logger.info("All options has been reset at PageAnalyse.")
    return