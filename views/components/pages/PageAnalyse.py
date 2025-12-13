from PyQt5.QtWidgets import ( 
  QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QScrollArea, QTabWidget,
  QSizePolicy, QFrame
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


#  DECLARATIONS
DS_LIST: list = ["Pivots", "Grouping", "Metrics", "Graphs"]


#  CLASS

class PageAnalyse(PageTemplate):
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    super().__init__(app_ref)
    self.tab_group: QTabWidget = QTabWidget()
    logger.info("initialised successfully.")
    
    for title in DS_LIST:
      tab = self.build_analyse_tab(target_title=title)
      self.tab_group.addTab(tab, title)
      self.tab_group.tabBar().setCursor(Qt.PointingHandCursor)
    
    
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
    if target_title == DS_LIST[0]:
      title_lb = self.app.comp_fact.build_label(lb_text="I. Create Pivot Tables",
                                                lb_type="h3")
    elif target_title == DS_LIST[1]:
      title_lb = self.app.comp_fact.build_label(lb_text="II. Group Data by Fields",
                                                lb_type="h3")
    elif target_title == DS_LIST[2]:
      title_lb = self.app.comp_fact.build_label(lb_text="III. Compute Key Statistics",
                                                lb_type="h3")
    elif target_title == DS_LIST[3]:
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
      basic_opt_box = self.build_tab_opt_baseline_box()
      advanced_opt_box = self.build_tab_opt_advanced_box(target_title=target_title)
      opt_control = self.build_tab_opt_controls()
      #  frame
      frame = QWidget()
      frame_layout = QVBoxLayout() 
      frame_layout.addWidget(title_lb, alignment=Qt.AlignLeft|Qt.AlignTop)
      frame_layout.addWidget(basic_opt_box)
      frame_layout.addWidget(advanced_opt_box)
      frame_layout.addWidget(opt_control, alignment=Qt.AlignLeft)
      frame_layout.setSpacing(4)
      frame_layout.setContentsMargins(0, 0, 0, 0) 
      frame.setLayout(frame_layout)
      frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
      return frame
    
    
  #  METHODS -  BOXES
  
  def build_tab_opt_baseline_box(self) -> QWidget:
    #  components
    col_cell = self.build_table_opt_cell(target_label="Select Columns",
                                        target_options=[],
                                        target_default=0,
                                        event=None)
    row_cell = self.build_table_opt_cell(target_label="Select Rows",
                                        target_options=[],
                                        target_default=0,
                                        event=None)
    val_cell = self.build_table_opt_cell(target_label="Select Values",
                                        target_options=[],
                                        target_default=0,
                                        event=None)
    #  frame
    frame = QWidget()
    frame_layout = QHBoxLayout()
    frame_layout.addWidget(col_cell)
    frame_layout.addWidget(row_cell)
    frame_layout.addWidget(val_cell)
    frame_layout.setSpacing(12)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame.setLayout(frame_layout)
    frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    return frame
  
  
  def build_tab_opt_advanced_box(self, target_title: str) ->QWidget:
    #  components
    if target_title == DS_LIST[0]:
      pass
    elif target_title == DS_LIST[1]:
      pass
    elif target_title == DS_LIST[2]:
      pass
    elif target_title == DS_LIST[3]:
      pass
    else:
      pass
    #  frame
    frame = QWidget()
    frame_layout = QHBoxLayout()
    frame_layout.setSpacing(12)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame.setLayout(frame_layout)
    frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    return frame
  
  
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
    cell_layout.addWidget(label)
    cell_layout.addWidget(dropdown)
    cell.setLayout(cell_layout)
    return cell
    
    
  def build_tab_opt_controls(self) -> QWidget:
    # components
    reset_btn = self.app.comp_fact.build_btn(btn_text="Reset",
                                             btn_event=lambda: print("Reset button clicked"),
                                             btn_bgcolor=THEME_COLOR["white"],
                                             btn_txtcolor=THEME_COLOR["primary"],
                                             btn_hover_bgcolor=THEME_COLOR["white_hvr"])  
    proceed_btn = self.app.comp_fact.build_btn(btn_text="Proceed",
                                             btn_event=lambda: print("Proceed button clicked"),
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
    if target_title in [DS_LIST[0], DS_LIST[1], DS_LIST[2]]:
      title_lb = self.app.comp_fact.build_label(lb_text="B. Table Display",
                                                lb_type="h3")
      frame_layout.addWidget(title_lb, alignment=Qt.AlignLeft | Qt.AlignTop)
      if target_df is not None or not target_df.empty:
        table_board = self.app.comp_fact.build_table_widget(target_df=target_df)
        frame_layout.addWidget(table_board)
    elif target_title == DS_LIST[3]:
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