from PyQt5.QtWidgets import ( 
  QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QScrollArea, QTabWidget,
  QSizePolicy, QFrame, QComboBox, QLabel
)
from PyQt5.QtCore import Qt
from views.components.pages.PageTemplate import PageTemplate
from views.components.config.views_styles import (
  THEME_COLOR, style_nav_sect_default, style_tab_border, style_tab_scroll
)
import pandas as pd
import logging
from typing import Callable


#  LOGGING
logger = logging.getLogger("PAGE_ANALYSE")


#  CLASS

class PageAnalyse(PageTemplate):
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    super().__init__(app_ref)
    self.app = app_ref
    
    #  1. tab UI
    self.tab_group: QTabWidget = QTabWidget()
  
    #  2. pivots components
    self.pivots_col_dd_01: QComboBox | None = None
    self.pivots_col_dd_02: QComboBox | None = None
    self.pivots_row_dd_01: QComboBox | None = None
    self.pivots_row_dd_02: QComboBox | None = None
    self.pivots_val_dd_01: QComboBox | None = None
    self.pivots_agg_func: QComboBox | None = None
    self.pivots_fill: QComboBox | None = None
    
    #  3. metrics components
    self.metrics_groupby_dd_01: QComboBox | None = None
    self.metrics_groupby_dd_02: QComboBox | None = None
    self.metrics_val_list: QWidget | None = None
    self.metrics_agg_func_list: QWidget | None = None
    
    #  4. graphs components
    self.graphs_col_dd_01: QComboBox | None = None
    self.graphs_row_dd_01: QComboBox | None = None
    self.graphs_val_dd_01: QComboBox | None = None
    
    #  5. tab content options collection
    self.PIVOTS_OPTS_DICT: dict = {
      "col_dd_01": {
        "type": "dropdown",
        "label": "1a. Select Column (Primary)",
        "options": ["--- Please Select ---"],
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivots_event(target_col="pivots_col_01",
                                                                           selected_text=text)
      },
      "col_dd_02": {
        "type": "dropdown",
        "label": "1b. Select Column (Secondary) - optional",
        "options": ["--- Please Select ---"],
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivots_event(target_col="pivots_col_02",
                                                                           selected_text=text)
      },
      "row_dd_01": {
        "type": "dropdown",
        "label": "2a. Select Row (Primary)",
        "options": ["--- Please Select ---"],
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivots_event(target_col="pivots_row_01",
                                                                           selected_text=text)
      },
      "row_dd_02": {
        "type": "dropdown",
        "label": "2b. Select Row (Secondary) - optional",
        "options": ["--- Please Select ---"], 
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivots_event(target_col="pivots_row_02",
                                                                           selected_text=text)
      },
      "val_dd_01": {
        "type": "dropdown",
        "label": "3. Select Values",
        "options": ["--- Please Select ---"], 
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivots_event(target_col="pivots_val_01",
                                                                           selected_text=text)
      },
      "agg_func": {
        "type": "dropdown",
        "label": "4. Select Aggregation Type",
        "options": ["--- Please Select ---"], 
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivots_event(target_col="agg_func",
                                                                           selected_text=text)
      },
      "fill": {
        "type": "dropdown",
        "label": "5. Select Blank Filling - optional",
        "options": ["--- Please Select ---"], 
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivots_event(target_col="fill",
                                                                           selected_text=text)
      }
    }
    self.METRICS_OPTS_DICT: dict = {
      "groupby_dd_01": {
        "type": "dropdown",
        "label": "1a. Select Groupby Column (Primary)",
        "options": ["--- Please Select ---"],
        "default": 0,
        "event": lambda text: print(text)
      },
      "groupby_dd_02": {
        "type": "dropdown",
        "label": "1b. Select Groupby Column (Secondary) - optional",
        "options": ["--- Please Select ---"],
        "default": 0,
        "event": lambda text: print(text)
      },
      "value_col_list": {
        "type": "checkbox",
        "label": "2. Select Value Column",
        "options": [],    # Remarks: merge_proc is None when initialised, update later
        "event": lambda text, checked: print(text, checked)
      },
      "agg_func_list": {
        "type": "checkbox",
        "label": "3. Select Aggregation Type",
        "options": ["count", "sum", "mean", "mode", "median"], 
        "default": 0,
        "event":  lambda text, checked: print(text, checked)
      }
    }
    
    #  6. dropdown refresh collection
    self.PIVOTS_REFRESH_DICT: dict = {
      "col_dd_01": self.app.analyse_cont.deliver_pivots_col_opts,
      "col_dd_02": self.app.analyse_cont.deliver_pivots_col_opts,
      "row_dd_01": self.app.analyse_cont.deliver_pivots_col_opts,
      "row_dd_02": self.app.analyse_cont.deliver_pivots_col_opts,
      "val_dd_01": self.app.analyse_cont.deliver_pivots_col_opts,
      "agg_func": self.app.analyse_cont.deliver_pivots_agg_func_opts,
      "fill": self.app.analyse_cont.deliver_pivots_fill_opts,
    }
    self.METRICS_REFRESH_DICT: dict = {
      "groupby_dd_01": self.app.analyse_cont.deliver_pivots_col_opts,
      "groupby_dd_02": self.app.analyse_cont.deliver_pivots_col_opts,
    }
    
    #  7. setup tabs
    for title in self.app.analyse_state.TAB_LIST:
      tab = self.build_analyse_tab(target_title=title)
      self.tab_group.addTab(tab, title)
      self.tab_group.tabBar().setCursor(Qt.PointingHandCursor)
    self.tab_group.currentChanged.connect(lambda index: self.app.analyse_cont.handle_analyse_tab_switch(target_index=index))
    logger.info("initialised successfully.")
  
    
  #  METHODS  -  MAIN
  
  def merge_sections(self) -> QWidget:
    #  title section
    inner_title_sect = self.create_title_sect(sect_title="Step 5: Analyse Data", 
                                              sect_des="This step explores the dataset through pivoting, grouping, statistical summaries, and visual analysis to reveal meaningful patterns and insights.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=5)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, enable_done=True)
    
    #  Work Panel Grid
    page = QWidget()
    page_layout = QGridLayout()
    page_layout = self.reuse_page_setting(inner_title_sect=inner_title_sect,
                                           inner_stat_sect=inner_stat_sect,
                                           inner_nav_sect=inner_nav_sect)
    page.setStyleSheet(style_nav_sect_default)
    page.setLayout(page_layout)
    return page
  
  
  def core_sect_analyse_data(self):
    tab = self.tab_group
    tab.setStyleSheet(style_tab_border)
    return tab
  
  
  def build_analyse_tab(self, target_title: str) -> QWidget:
    #  components
    title_container = self.build_tab_title_container(target_title=target_title)
    opt_container = self.build_tab_opt_container(target_title=target_title)
    #  frame
    core_sect = QWidget()
    core_sect_layout = QVBoxLayout()
    core_sect_layout.setAlignment(Qt.AlignTop)
    core_sect_layout.setSpacing(24)
    core_sect_layout.setContentsMargins(0, 16, 0, 0) 
    core_sect_layout.addWidget(title_container, alignment=Qt.AlignLeft | Qt.AlignTop)
    core_sect_layout.addWidget(opt_container)
    core_sect.setLayout(core_sect_layout)
    #  scroll
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet(style_tab_scroll)
    scroll.setWidget(core_sect)
    return scroll
  
  
  #  METHODS -  TAB-BASED
  
  #  Remarks: building corresponding tab's main title section
  def build_tab_title_container(self, target_title: str) -> QWidget:
    #  components   
    if target_title == "Pivots":
      title_lb = self.app.comp_fact.build_label(lb_text="I. Create Pivot Tables",
                                                lb_type="h3")
    elif target_title == "Metrics":
      title_lb = self.app.comp_fact.build_label(lb_text="II. Create Statistic Tables",
                                                lb_type="h3")
    elif target_title == "Graphs":
      title_lb = self.app.comp_fact.build_label(lb_text="IV. Visualise Trends and Patterns",
                                                lb_type="h3")
    else:
      title_lb = self.app.comp_fact.build_label(lb_text="Unknown Section",
                                                lb_type="h3")
      logger.error(f"Route to wrong tab {target_title} at PageAnalyse.")
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.addWidget(title_lb)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setSpacing(8)
    frame_layout.setContentsMargins(0, 0, 0, 0) 
    frame.setLayout(frame_layout)
    return frame
  
  
  #  Remarks: building corresponding tab's overall option section
  def build_tab_opt_container(self, target_title: str) -> QWidget:   
    #  components
    title_lb = self.app.comp_fact.build_label(lb_text="A. Configure Parameters",
                                              lb_type="h3")
    opt_box = self.build_tab_opt_baseline_box(target_title=target_title)
    opt_control = self.build_tab_opt_controls()
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout() 
    frame_layout.addWidget(title_lb, alignment=Qt.AlignLeft|Qt.AlignTop)
    frame_layout.addWidget(opt_box)
    frame_layout.addWidget(opt_control, alignment=Qt.AlignLeft)
    frame_layout.setSpacing(4)
    frame_layout.setContentsMargins(0, 0, 0, 0) 
    frame.setLayout(frame_layout)
    frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    return frame
  
  
  #  Remarks: re-directing corresponding tab content layout
  def build_tab_opt_baseline_box(self, target_title: str) -> QWidget:
    if target_title == "Pivots":
      return self.build_reused_opts_layout(target_tab="pivots",
                                           target_opt_dict=self.PIVOTS_OPTS_DICT, 
                                           target_refresh_dict=self.PIVOTS_REFRESH_DICT)
    elif target_title == "Metrics": 
      return self.build_reused_opts_layout(target_tab="metrics",
                                           target_opt_dict=self.METRICS_OPTS_DICT, 
                                           target_refresh_dict=self.METRICS_REFRESH_DICT)
    # elif target_title == "Graphs":
    #   return self.build_graphs_opts_layout()
    else:
      return QWidget()
    
  
  #  Remarks: the reusable generator for building layout of tab content
  #  TODO: Metrics Q2 checkboxes need to be fixed, and the styling issue with padding
  def build_reused_opts_layout(self, target_tab: str, target_opt_dict: dict, target_refresh_dict: dict) -> QWidget:
    
    #  declaration
    target_tab = target_tab.strip().lower()
    if not isinstance(target_opt_dict, dict) or not isinstance(target_refresh_dict, dict):
      err_msg: str = "Failed to build optioms layout. Required information is not found."
      logger.warning(err_msg + "(target_opt_dict or target_refresh_dict)")
      err_lb = self.app.comp_fact.build_label(lb_text=err_msg,
                                              lb_align=Qt.AlignLeft)
      return err_lb
    
    #  setup frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.setSpacing(16)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    
    #  1. setup dropdown widgets and update temp state
    for key, opt in target_opt_dict.items():
      opt_type = opt["type"]
      opt_cell = None
      if opt_type == "dropdown":
        opt_cell = self.build_dropdown_cell(target_tab=target_tab, 
                                            target_state_name=key, 
                                            target_opt_dict=opt)["cell"]
      elif opt_type == "checkbox":
        opt_cell = self.build_checkbox_cell(target_tab=target_tab, 
                                            target_state_name=key, 
                                            target_opt_dict=opt)
      if opt_cell:
        frame_layout.addWidget(opt_cell, alignment=Qt.AlignLeft)
       
    #  3. setup widget refresh
    for key, method in target_refresh_dict.items():
      dropdown = getattr(self, f"{target_tab}_{key}", None)
      if dropdown:
        self.app.comp_fact.refresh_dropdowns(target_dd=dropdown,target_event=method)
      
    #  4. complete frame
    frame.setLayout(frame_layout)
    return frame
  
  
  #  Remarks: cerate the dropdown cells, supporting to build_reused_opts_layout
  def build_dropdown_cell(self, target_tab: str, target_state_name, target_opt_dict: Callable) -> QWidget:
    opt_hybrid = self.build_table_opt_box(target_label=target_opt_dict["label"],
                                              target_options=target_opt_dict["options"],
                                              target_default=target_opt_dict["default"],
                                              event=target_opt_dict["event"])
    opt_combo = opt_hybrid["dropdown"]
    #  1b. update temp state (replace value)
    setattr(self, f"{target_tab}_{target_state_name}", opt_combo)
    return opt_hybrid
  
  
  #  Remarks: create the checkbox cells, supporting to build_reused_opts_layout
  def build_checkbox_cell(self, target_tab: str, target_state_name, target_opt_dict: Callable) -> QWidget:
        #  2a. build frame cell
        cb_cell = QWidget()
        cb_cell_layout = QVBoxLayout()
        
        #  2b. build label
        cb_cell_lb = self.app.comp_fact.build_label(lb_text=target_opt_dict["label"],
                                                    lb_type="p",
                                                    lb_align=Qt.AlignLeft)
        cb_cell_layout.addWidget(cb_cell_lb)
        
        #  2c. false case
        if len(target_opt_dict["options"]) < 1:
          err_lb = self.app.comp_fact.build_label(lb_text="(No option can be found.)",
                                                  lb_align=Qt.AlignCenter)
          cb_cell_layout.addWidget(err_lb)
          
        #  2d. suceed case: build checkbox group object
        else:
          temp_cb_list = getattr(self, f"{target_tab}_{target_state_name}", None)
          if not isinstance(temp_cb_list, list):
            temp_cb_list = []
          for column in target_opt_dict["options"]:
            cb = self.app.comp_fact.build_checkbox(target_name=column, 
                                                   target_event=None)  # event method to be appended
            cb_cell_layout.addWidget(cb)
            #  Remarks: setup temporary state
            temp_cb_list.append(cb)
          setattr(self, f"{target_tab}_{target_state_name}", temp_cb_list)
        cb_cell_layout.setSpacing(8)
        cb_cell_layout.setContentsMargins(0, 8, 0, 0)
        setattr(self, f"{target_tab}_{target_state_name}_layout", cb_cell_layout)
        cb_cell.setLayout(cb_cell_layout)
        #  Remarks: setup temporary state
        return cb_cell
  
  
  #  METHODS - BOXES

  #  Remarks: primary option containers
  def package_opt_box(self, target_lb: QLabel, target_dd: QWidget) -> QWidget:
    container = QWidget()
    container_layout = QVBoxLayout()
    container_layout.addWidget(target_lb, alignment=Qt.AlignLeft)
    container_layout.addWidget(target_dd, alignment=Qt.AlignLeft)
    container_layout.setSpacing(8)
    container_layout.setContentsMargins(0, 0, 0, 0)
    container.setLayout(container_layout)
    return container
  
  
  #  Remarks: sub-container to pack a label and a dropdown
  def build_table_opt_box(self, 
                          target_label=str,
                          target_options: list=None,
                          target_default: int=0,
                          event: Callable | None=None) -> QWidget:
    #  error handling
    if target_options is None:
      target_options = []
    #  declaration
    label = self.app.comp_fact.build_label(lb_text=target_label,
                                           lb_type="p",
                                           lb_align=Qt.AlignLeft)
    dropdown = self.app.comp_fact.build_dropdown(target_options=target_options,
                                                 target_default=target_default,
                                                 event=event)
    #  setup component
    cell = QWidget()
    cell_layout = QVBoxLayout()
    cell_layout.setSpacing(4)
    cell_layout.setContentsMargins(0, 0, 0, 0)
    cell_layout.addWidget(label, alignment=Qt.AlignLeft)
    cell_layout.addWidget(dropdown, alignment=Qt.AlignLeft)
    cell.setLayout(cell_layout)
    cell.setFixedWidth(280)
    cell.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    return {"cell": cell, "dropdown": dropdown}
    
    
  #  Remarks: control panel for trigger analysing option events 
  def build_tab_opt_controls(self) -> QWidget:
    #  components
    reset_btn = self.app.comp_fact.build_btn(btn_text="Reset",
                                             btn_event=lambda: print("Reset button clicked"),
                                             btn_bgcolor=THEME_COLOR["white"],
                                             btn_txtcolor=THEME_COLOR["primary"],
                                             btn_hover_bgcolor=THEME_COLOR["white_hvr"])  
    proceed_btn = self.app.comp_fact.build_btn(btn_text="Proceed",
                                             btn_event=lambda: self.app.analyse_cont.proceed_btn_event_generator(tab_list=self.app.analyse_state.TAB_LIST, 
                                                                                                                 target_tab=self.app.analyse_state.curr_tab),
                                             btn_bgcolor=THEME_COLOR["primary"],
                                             btn_txtcolor=THEME_COLOR["white"],
                                             btn_hover_bgcolor=THEME_COLOR["primary_hvr"])  
    #  frame
    frame = QFrame()
    frame_layout = QHBoxLayout()
    frame_layout.addWidget(reset_btn, alignment=Qt.AlignLeft)
    frame_layout.addWidget(proceed_btn, alignment=Qt.AlignLeft)
    frame_layout.setSpacing(12)
    frame_layout.setContentsMargins(0, 16, 0, 0)
    frame.setLayout(frame_layout)
    return frame
  
  
  def build_tab_display_board(self, 
                              target_title: str, 
                              target_df: pd.DataFrame = None) -> QWidget:
    #  error handling
    if target_df is None or target_df.empty:
      logger.warning(f"No data available to display for {target_title} in PageAnalyse.")
      return QWidget()
    #  setup frame
    frame = QFrame()
    frame_layout = QHBoxLayout()
    #  components
    if target_title in ["Pivots", "Metrics"]:
      title_lb = self.app.comp_fact.build_label(lb_text="B. Table Display",
                                                lb_type="h3")
      frame_layout.addWidget(title_lb, alignment=Qt.AlignLeft | Qt.AlignTop)
      if target_df is not None or not target_df.empty:
        table_board = self.app.comp_fact.build_table_widget(target_df=target_df)
        frame_layout.addWidget(table_board)
    elif target_title == "Graphs":
      title_lb = self.app.comp_fact.build_label(lb_text="B. Graph Display",
                                                lb_type="h3")
      frame_layout.addWidget(title_lb, alignment=Qt.AlignLeft | Qt.AlignTop)
      if target_df is not None or not target_df.empty:
        graph_board = None
    #  frame
    frame_layout.setSpacing(12)
    frame_layout.setContentsMargins(0, 8, 0, 0)
    frame.setLayout(frame_layout)
    return frame
  
  