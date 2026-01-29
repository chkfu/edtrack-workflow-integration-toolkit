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
  
  #  Remarks: rebuild value options with up-to-date columns data with 'Next' btn
  def rebuild_metrics_val_cell(self) -> None:
    
    #  clear prev setting
    self.app.analyse_state.metrics_val_list.clear() 
    self.app.analyse_state.metrics_agg_func_list.clear()
    
    #  update temp state (initialise merge_proc is None)
    update_options: list = self.app.merge_state.merge_proc.columns
    if update_options is None or update_options.empty:
      return
    temp_dict = self.app.pages_fact.page_analyse.METRICS_OPTS_DICT["value_col_cell"]
    temp_dict["options"] = update_options.tolist()
    
    #  declaration
    curr_widget = self.app.pages_fact.page_analyse.metrics_val_cell
    replace_widget = self.app.pages_fact.page_analyse.build_checkbox_cell(target_tab="Metrics", 
                                                                            target_state_name="value_col_cell", 
                                                                            target_opt_dict=temp_dict)
    #  get master level
    master_widget = curr_widget.parentWidget()
    if not master_widget:
      return
    master_widget_layout = master_widget.layout()
    if not master_widget_layout:
      return
    #  swapping items
    #  Learnt: get the index -> search item -> insert new -> remove old
    curr_widget_index = master_widget_layout.indexOf(curr_widget)
    master_widget_layout.takeAt(curr_widget_index)
    master_widget_layout.insertWidget(curr_widget_index, replace_widget)
    curr_widget.deleteLater()
    self.app.pages_fact.page_analyse.metrics_val_cell = replace_widget
    return
  
  
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
      raw_groupby: list = [self.app.analyse_state.metrics_grouped_01,
                             self.app.analyse_state.metrics_grouped_02]
      input_groupby = [el for el in raw_groupby if el is not None and el != "--- Please Select ---"]
      input_val: list = self.app.analyse_state.metrics_val_list
      input_agg_func: list = self.app.analyse_state.metrics_agg_func_list
      
      #  2. validate inputs 
         
      #  2a. invalid list parameters
      if not input_groupby:
        err_msg: str = f"Failed to transform metrics table. Invalid parameters: groupby column list"
        logger.warning(err_msg)
        raise ValueError(err_msg)
      if not input_val:
        err_msg: str = f"Failed to transform metrics table. Invalid parameters: value column list"
        logger.warning(err_msg)
        raise ValueError(err_msg)
      #  trade-offs: pure groupby methods for empty, or statistical analysis with opts
      if not input_agg_func:
        input_agg_func = []
        
      #  2b. invalid value to be processed
      for column in self.app.merge_state.merge_proc.columns:
        self.app.valid_cont.validate_col(target_df=self.app.merge_state.merge_proc,
                                         target_col=column)
      for column in self.app.merge_state.merge_proc.columns:
        self.app.valid_cont.validate_col(target_df=self.app.merge_state.merge_proc,
                                         target_col=column)
        
      #  2c. remove invalid items, in case mistakenly input as final check
      #      trade-offs: pure groupby methods for empty, or statistical analysis with opts
      for column in input_agg_func:
        if column.strip().lower() not in ["sum", "mean", "mode", "median"]:
          input_agg_func.remove(column)
      
      #  3. data transformation 
      target_tb = self.data_manager.groupby_table(target_df=self.app.merge_state.merge_proc, 
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
    self.app.pages_fact.page_analyse.reset_widget_display(target_tab="pivots")
    self.app.analyse_state.reset_state_generator(target_tab="pivots")
    logger.info("Pivots options has been reset at PageAnalyse.")
    return
  
    
  def reset_metrics_options(self) -> None:
    self.app.pages_fact.page_analyse.reset_widget_display(target_tab="pivots")
    self.app.analyse_state.reset_state_generator(target_tab="pivots")
    logger.info("Metrics options has been reset at PageAnalyse.")
    return
  
  
  def reset_graphs_options(self) -> None:
    self.app.pages_fact.page_analyse.reset_widget_display(target_tab="graphs")
    self.app.analyse_state.reset_state_generator(target_tab="graphs")
    logger.info("Graphs options has been reset at PageAnalyse.")
    return
  
  
  def reset_all_options(self) -> None:
    self.reset_pivots_options()
    self.reset_metrics_options()
    self.reset_graphs_options()
    #  Remarks: reset general setting in analyse state
    self.app.analyse_state.curr_tab = "Pivots" 
    #  Remarks: reset updated temp state
    self.app.pages_fact.page_analyse.METRICS_OPTS_DICT["value_col_cell"]["options"] = None
    logger.info("All options has been reset at PageAnalyse.")
    return