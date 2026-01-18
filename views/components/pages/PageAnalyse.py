from PyQt5.QtWidgets import ( 
  QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QScrollArea, QTabWidget,
  QSizePolicy, QFrame, QComboBox, QLabel, QDialog
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
    self.metrics_col_dd_01: QComboBox | None = None
    self.metrics_row_dd_01: QComboBox | None = None
    self.metrics_val_dd_01: QComboBox | None = None
    
    #  4. graphs components
    self.graphs_col_dd_01: QComboBox | None = None
    self.graphs_row_dd_01: QComboBox | None = None
    self.graphs_val_dd_01: QComboBox | None = None

    #  5. setup tabs
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
  
  
  #  METHODS  -  CONTAINERS
  
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
      # frame_layout.addWidget(basic_opt_box)
      frame_layout.addWidget(opt_box)
      frame_layout.addWidget(opt_control, alignment=Qt.AlignLeft)
      frame_layout.setSpacing(4)
      frame_layout.setContentsMargins(0, 0, 0, 0) 
      frame.setLayout(frame_layout)
      frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
      return frame
    
    
  #  METHODS -  BOXES
  
  def build_tab_opt_baseline_box(self, target_title: str) -> QWidget:
  
    #  build elective options
    if target_title == "Pivots":
      return self.build_pivots_opts_layout()
    # elif target_title == "Metrics": 
    #   return self.build_metrics_opts_layout()
    # elif target_title == "Graphs":
    #   return self.build_graphs_opts_layout()
    else:
      return QWidget()
   

  #  METHODS - OPTS LAYOUTS
  
  def build_pivots_opts_layout(self) -> QHBoxLayout:
    
    OPTS_DICT: dict = {
      "col_dd_01": {
        "label": "1a. Select Column (Primary)",
        "options": ["--- Please Select ---"],
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivot_event(target_col="pivots_col_01",
                                                                           selected_text=text)
      },
      "col_dd_02": {
        "label": "1b. Select Column (Secondary) - optional",
        "options": ["--- Please Select ---"],
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivot_event(target_col="pivots_col_02",
                                                                           selected_text=text)
      },
      "row_dd_01": {
        "label": "2a. Select Row (Primary)",
        "options": ["--- Please Select ---"],
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivot_event(target_col="pivots_row_01",
                                                                           selected_text=text)
      },
      "row_dd_02": {
        "label": "2b. Select Row (Secondary) - optional",
        "options": ["--- Please Select ---"], 
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivot_event(target_col="pivots_row_02",
                                                                           selected_text=text)
      },
      "val_dd_01": {
        "label": "3. Select Values",
        "options": ["--- Please Select ---"], 
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivot_event(target_col="pivots_val_01",
                                                                           selected_text=text)
      },
      "agg_func": {
        "label": "4. Select Aggregation Type",
        "options": ["--- Please Select ---"], 
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivot_event(target_col="agg_func",
                                                                           selected_text=text)
      },
      "fill": {
        "label": "5. Select Blank Filling - optional",
        "options": ["--- Please Select ---"], 
        "default": 0,
        "event": lambda text: self.app.analyse_cont.analyse_dd_pivot_event(target_col="fill",
                                                                           selected_text=text)
      }
    }
     
    #  setup frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    
    #  build compulsory labels
    col_lb_01 = self.app.comp_fact.build_label(lb_text=OPTS_DICT["col_dd_01"]["label"],
                                               lb_type="p",
                                               lb_txtcolor=THEME_COLOR["mid"])
    col_lb_02 = self.app.comp_fact.build_label(lb_text=OPTS_DICT["col_dd_02"]["label"],
                                               lb_type="p",
                                               lb_txtcolor=THEME_COLOR["mid"])
    row_lb_01 = self.app.comp_fact.build_label(lb_text=OPTS_DICT["row_dd_01"]["label"],
                                               lb_type="p",
                                               lb_txtcolor=THEME_COLOR["mid"])
    row_lb_02 = self.app.comp_fact.build_label(lb_text=OPTS_DICT["row_dd_02"]["label"],
                                               lb_type="p",
                                               lb_txtcolor=THEME_COLOR["mid"])
    val_lb_01 = self.app.comp_fact.build_label(lb_text=OPTS_DICT["val_dd_01"]["label"],
                                               lb_type="p",
                                               lb_txtcolor=THEME_COLOR["mid"])
    agg_func_lb = self.app.comp_fact.build_label(lb_text=OPTS_DICT["agg_func"]["label"],
                                                 lb_type="p",
                                                 lb_txtcolor=THEME_COLOR["mid"])
    fill_lb = self.app.comp_fact.build_label(lb_text=OPTS_DICT["fill"]["label"],
                                             lb_type="p",
                                             lb_txtcolor=THEME_COLOR["mid"])
    
    #  build compulsory dropdowns
    col_dd_01 = self.build_table_opt_cell(target_label=OPTS_DICT["col_dd_01"]["label"],
                                          target_options=OPTS_DICT["col_dd_01"]["options"],
                                          target_default=OPTS_DICT["col_dd_01"]["default"],
                                          event=OPTS_DICT["col_dd_01"]["event"])    
    col_dd_02 = self.build_table_opt_cell(target_label=OPTS_DICT["col_dd_02"]["label"],
                                          target_options=OPTS_DICT["col_dd_02"]["options"],
                                          target_default=OPTS_DICT["col_dd_02"]["default"],
                                          event=OPTS_DICT["col_dd_02"]["event"])
    row_dd_01 = self.build_table_opt_cell(target_label=OPTS_DICT["row_dd_01"]["label"],
                                          target_options=OPTS_DICT["row_dd_01"]["options"],
                                          target_default=OPTS_DICT["row_dd_01"]["default"],
                                          event=OPTS_DICT["row_dd_01"]["event"])    
    row_dd_02 = self.build_table_opt_cell(target_label=OPTS_DICT["row_dd_02"]["label"],
                                          target_options=OPTS_DICT["row_dd_02"]["options"],
                                          target_default=OPTS_DICT["row_dd_02"]["default"],
                                          event=OPTS_DICT["row_dd_02"]["event"])    
    val_dd_01 = self.build_table_opt_cell(target_label=OPTS_DICT["val_dd_01"]["label"],
                                          target_options=OPTS_DICT["val_dd_01"]["options"],
                                          target_default=OPTS_DICT["val_dd_01"]["default"],
                                          event=OPTS_DICT["val_dd_01"]["event"])
    agg_func_dd = self.build_table_opt_cell(target_label=OPTS_DICT["agg_func"]["label"],
                                            target_options=OPTS_DICT["agg_func"]["options"],
                                            target_default=OPTS_DICT["agg_func"]["default"],
                                            event=OPTS_DICT["agg_func"]["event"]) 
    fill_dd = self.build_table_opt_cell(target_label=OPTS_DICT["fill"]["label"],
                                        target_options=OPTS_DICT["fill"]["options"],
                                        target_default=OPTS_DICT["fill"]["default"],
                                        event=OPTS_DICT["fill"]["event"])    
    
    
    #  package into widget
    container_01 = self.package_opt_containers(target_lb=col_lb_01,
                                               target_dd=col_dd_01["dropdown"])
    container_02 = self.package_opt_containers(target_lb=col_lb_02,
                                               target_dd=col_dd_02["dropdown"])
    container_03 = self.package_opt_containers(target_lb=row_lb_01,   
                                               target_dd=row_dd_01["dropdown"])
    container_04 = self.package_opt_containers(target_lb=row_lb_02,
                                               target_dd=row_dd_02["dropdown"])
    container_05 = self.package_opt_containers(target_lb=val_lb_01,
                                               target_dd=val_dd_01["dropdown"])
    container_06 = self.package_opt_containers(target_lb=agg_func_lb,
                                               target_dd=agg_func_dd["dropdown"])
    container_07 = self.package_opt_containers(target_lb=fill_lb,
                                               target_dd=fill_dd["dropdown"])
    
    #  update temp state
    self.pivots_col_dd_01 = col_dd_01["dropdown"]
    self.pivots_col_dd_02 = col_dd_02["dropdown"]
    self.pivots_row_dd_01 = row_dd_01["dropdown"]
    self.pivots_row_dd_02 = row_dd_02["dropdown"]
    self.pivots_val_dd_01 = val_dd_01["dropdown"]
    self.pivots_agg_func = agg_func_dd["dropdown"]
    self.pivots_fill = fill_dd["dropdown"]
    
    #  refresh
    self.app.comp_fact.refresh_dropdowns(target_dd=col_dd_01["dropdown"],
                                         target_event=lambda: self.app.analyse_cont.deliver_col_opts())
    self.app.comp_fact.refresh_dropdowns(target_dd=col_dd_02["dropdown"],
                                         target_event=lambda: self.app.analyse_cont.deliver_col_opts())
    self.app.comp_fact.refresh_dropdowns(target_dd=row_dd_01["dropdown"],
                                         target_event=lambda: self.app.analyse_cont.deliver_col_opts())
    self.app.comp_fact.refresh_dropdowns(target_dd=row_dd_02["dropdown"],
                                         target_event=lambda: self.app.analyse_cont.deliver_col_opts())
    self.app.comp_fact.refresh_dropdowns(target_dd=val_dd_01["dropdown"],
                                         target_event=lambda: self.app.analyse_cont.deliver_col_opts())
    self.app.comp_fact.refresh_dropdowns(target_dd=agg_func_dd["dropdown"],
                                         target_event=lambda: self.app.analyse_cont.deliver_agg_func_opts())
    self.app.comp_fact.refresh_dropdowns(target_dd=fill_dd["dropdown"],
                                         target_event=lambda: self.app.analyse_cont.deliver_fill_opts())
    #  add to layout
    frame_layout.addWidget(container_01, alignment=Qt.AlignLeft)
    frame_layout.addWidget(container_02, alignment=Qt.AlignLeft)
    frame_layout.addWidget(container_03, alignment=Qt.AlignLeft)
    frame_layout.addWidget(container_04, alignment=Qt.AlignLeft)
    frame_layout.addWidget(container_05, alignment=Qt.AlignLeft)
    frame_layout.addWidget(container_06, alignment=Qt.AlignLeft)
    frame_layout.addWidget(container_07, alignment=Qt.AlignLeft)

    #  complete frame
    frame_layout.setSpacing(16)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame.setLayout(frame_layout)
    return frame
    
  
  
  # def build_metrics_opts_layout(self) -> QHBoxLayout:
  #   pass
  
  
  # def build_graphs_opts_layout(self) -> QHBoxLayout:
  #   pass
  
  
  #  METHODS - CONTAINERS

  def package_opt_containers(self, target_lb: QLabel, target_dd: QComboBox) -> QWidget:
    container = QWidget()
    container_layout = QVBoxLayout()
    container_layout.addWidget(target_lb, alignment=Qt.AlignLeft)
    container_layout.addWidget(target_dd, alignment=Qt.AlignLeft)
    container_layout.setSpacing(8)
    container_layout.setContentsMargins(0, 0, 0, 0)
    container.setLayout(container_layout)
    return container
  

  #  METHODS -  OTHERS
  
  def build_table_opt_cell(self, 
                           target_label=str,
                           target_options: list = [],
                           target_default: int=0,
                           event: Callable | None=None) -> QWidget:
    label = self.app.comp_fact.build_label(lb_text=target_label,
                                          lb_type="p")
    dropdown = self.app.comp_fact.build_dropdown(target_options=target_options,
                                                 target_default=target_default,
                                                 event=event)
    cell = QWidget()
    cell_layout = QVBoxLayout()
    cell_layout.setSpacing(4)
    cell_layout.setContentsMargins(0, 0, 0, 0)
    cell_layout.addWidget(label, alignment=Qt.AlignLeft)
    cell_layout.addWidget(dropdown, alignment=Qt.AlignLeft)
    cell.setLayout(cell_layout)
    cell.setFixedWidth(200)
    cell.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    return {"box": cell, "dropdown": dropdown}
    
    
  def build_tab_opt_controls(self) -> QWidget:
    # components
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
    frame_layout.setContentsMargins(0, 8, 0, 0)
    frame.setLayout(frame_layout)
    return frame
  
  
  def build_tab_display_board(self, 
                              target_title: str, 
                              target_df: pd.DataFrame = None) -> QWidget:
    #  error handling
    if target_df is None or target_df.empty:
      logger.warning(f"No data available to display for {target_title} in PageAnalyse.")
      return
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
  
  
  
  #  METHODS -  RESETS
  
  def update_pivot_dd(self, target_dd: str, options: list):
    
    OPTS_DICT: dict = {
      "col_dd_01": self.pivots_col_dd_01,
      "col_dd_02": self.pivots_col_dd_02,
      "row_dd_01": self.pivots_row_dd_01,
      "row_dd_02": self.pivots_row_dd_02,
      "val_dd_01": self.pivots_val_dd_01
    }
    
    #  identify dropdown
    if target_dd not in OPTS_DICT.keys():
      logger.error(f"Failed to update pivots dropdown for invalid target - {target_dd}",
                   exc_info=True)
      return
    dropdown = OPTS_DICT[target_dd]
    
    #  refresh dropdown
    dropdown.blockSignals(True)
    dropdown.clear()
    dropdown.addItems(options)
    dropdown.setCurrentIndex(0)
    dropdown.blockSignals(False)
    
    
  def update_metrics_dd(self, target_dd: str, options: list):
    
    OPTS_DICT: dict = {
      "col_dd_01": self.metrics_col_dd_01,
      "row_dd_01": self.metrics_row_dd_01,
      "val_dd_01": self.metrics_val_dd_01
    }
    
    #  identify dropdown
    if target_dd not in OPTS_DICT.keys():
      logger.error(f"Failed to update metrics dropdown for invalid target - {target_dd}",
                   exc_info=True)
      return
    dropdown = OPTS_DICT[target_dd]
    
    #  refresh dropdown
    dropdown.blockSignals(True)
    dropdown.clear()
    dropdown.addItems(options)
    dropdown.setCurrentIndex(0)
    dropdown.blockSignals(False)
    
    
  def update_graphs_dd(self, target_dd: str, options: list):
  
    OPTS_DICT: dict = {
      "col_dd_01": self.graphs_col_dd_01,
      "row_dd_01": self.graph_row_dd_01,
      "val_dd_01": self.graphs_val_dd_01
    }
    
    #  identify dropdown
    if target_dd not in OPTS_DICT.keys():
      logger.error(f"Failed to update graphs dropdown for invalid target - {target_dd}",
                  exc_info=True)
      return
    dropdown = OPTS_DICT[target_dd]
    
    #  refresh dropdown
    dropdown.blockSignals(True)
    dropdown.clear()
    dropdown.addItems(options)
    dropdown.setCurrentIndex(0)
    dropdown.blockSignals(False)