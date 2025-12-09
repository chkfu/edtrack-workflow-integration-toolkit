from PyQt5.QtWidgets import ( 
  QWidget, QGridLayout, QVBoxLayout, QScrollArea, QTabWidget
)
from PyQt5.QtCore import Qt
from views.components.pages.PageTemplate import PageTemplate
from views.components.config.views_styles import (
  style_nav_sect_default, style_tab_border, style_tab_scroll
)
import logging



#  LOGGING

logger = logging.getLogger("PAGE_ANALYSE")


#  CLASS


class PageAnalyse(PageTemplate):
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    super().__init__(app_ref)
    self.ds_list: list = ["Pivots", "Grouping", "Metrics", "Visuals"]
    self.tab_group: QTabWidget = QTabWidget()
    logger.info("initialised successfully.")
    
    for title in self.ds_list:
      tab = self.build_analyse_tab(target_title=title)
      self.tab_group.addTab(tab, title)
      self.tab_group.tabBar().setCursor(Qt.PointingHandCursor)
    
    
  #  METHODS  -  MAIN
  
  def merge_sections(self) -> QWidget:
    #  title section
    inner_title_sect = self.create_title_sect(sect_title="Step 5: Analyse Data", 
                                                sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
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
    # tb_select_container = self.build_tb_opt_container(target_title=target_title)
    # basic_clean_container = self.build_basic_clean_container()
    # reset_container = self.app.comp_fact.build_reused_single_btn_box(target_title="C. Reset Options",
    #                                                            target_statement=None,
    #                                                            target_btn_text="Reset",
    #                                                            target_btn_event=lambda: self.reset_display())
    #  frame
    core_sect = QWidget()
    core_sect_layout = QVBoxLayout()

    core_sect_layout.setAlignment(Qt.AlignTop)
    core_sect_layout.setSpacing(24)
    core_sect_layout.setContentsMargins(0, 16, 0, 0) 
    core_sect.setLayout(core_sect_layout)
    #  scroll
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet(style_tab_scroll)
    scroll.setWidget(core_sect)
    return scroll
  
  #  METHODS  -  SUPPORTING
  
  
  
 