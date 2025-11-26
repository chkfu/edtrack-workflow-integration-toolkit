from PyQt5.QtWidgets import (
  QWidget, QGridLayout, QVBoxLayout, QRadioButton, QButtonGroup, QFrame,
  QHBoxLayout, QCheckBox, QScrollArea, QTabWidget, QLabel
)
from PyQt5.QtCore import Qt
from views.components.config.views_config import DATASET_LIST
from views.components.config.views_styles import THEME_COLOR
from views.components.config.views_styles import style_nav_sect_default
from views.components.pages.PageTemplate import PageTemplate
import logging
from typing import Callable
import pandas as pd


#  LOGGING

logger = logging.getLogger("PAGE_CLEAN")



#  CLASS


class PageClean(PageTemplate):
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref, target_ds_list: list | None = None):
    super().__init__(app_ref)
    
    if not target_ds_list:
      err_msg: str = "Dataset list is empty. Page tabs cannot be setup."
      logger.error(err_msg, exc_info=True)   
      raise ValueError(err_msg)
    
    self.ds_list: list = target_ds_list
    self.tab_group: QTabWidget = QTabWidget()

    #  build page tabs, store in self.tab_group. it stores:
    #  - tab = the output of build_cleaning_tab()
    #  - dataset = dataset names
    for title in target_ds_list:
      tab = self.build_cleaning_tab(target_title=title)
      self.tab_group.addTab(tab, title)
    logger.info("initialised successfully.")
    
   
    
  #  METHODS
  
  def merge_sections(self):
    #  title section
    inner_title_sect = self.create_title_sect(sect_title="Step 2: Clean Data and Preprocessing", 
                                              sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=2)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, enable_next=True)
    
    #  Work Panel Grid
    page = QWidget()
    page_layout = self.reuse_page_setting(inner_title_sect=inner_title_sect,
                                           inner_stat_sect=inner_stat_sect,
                                           inner_nav_sect=inner_nav_sect)
    page.setStyleSheet(style_nav_sect_default)
    page.setLayout(page_layout)
    return page
  
  
  # Override
  def core_sect_clean_data(self) -> QWidget:
    tab = self.tab_group
    tab.setStyleSheet("""
    QTabWidget {
        background: transparent;
        border: none;
    }
    QTabWidget::pane {
        background: transparent;
        border: none;
    }
    """)
    return tab
  


  def build_cleaning_tab(self, target_title: str) -> QWidget:
    #  components
    tb_select_container = self.build_tb_opt_container(target_title=target_title)
    basic_clean_container = self.build_basic_clean_container()
    #  frame
    core_sect = QWidget()
    core_sect_layout = QVBoxLayout()
    core_sect_layout.addWidget(tb_select_container)
    core_sect_layout.addWidget(basic_clean_container)
    core_sect_layout.setAlignment(Qt.AlignTop)
    core_sect_layout.setSpacing(8)
    core_sect_layout.setContentsMargins(0, 0, 0, 0) 
    core_sect.setLayout(core_sect_layout)
    #  scroll
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet("""
    QScrollArea {
        border: none;
        background: transparent;
    }
    QScrollBar:vertical {
        width: 2px;
        background: transparent;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #23405b;
        min-height: 16px;
        border-radius: 3px;
    }
    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0px;
    }
    QScrollBar::handle:vertical:hover {
        background: #365b7d;
    }
""")
    scroll.setWidget(core_sect)
    return scroll
  
  
    
    
  #  METHODS - CONTAINER
  
  def build_tb_opt_container(self, target_title) -> QFrame:
    #  components
    title_lb = self.app.comp_fact.build_label(lb_text="A. Data Information",
                                              lb_type="h3",
                                              lb_align=Qt.AlignLeft,
                                              lb_bold=True)
    preview_box = self.app.comp_fact.preview_comp_box(lb_text=f"{target_title}", 
                                                      btn_text="Preview",
                                                      btn_event=lambda: self.app.file_cont.preview_dataset(target_key=target_title))
    
    #  frame
    frame = QFrame()
    frame_layout = QVBoxLayout()
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(preview_box)
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
    frame_layout.setContentsMargins(8, 16, 8, 8) 
    frame.setLayout(frame_layout)
    return frame
  
  
  def build_basic_clean_container(self) -> QFrame:
    #  components
    title_lb = self.app.comp_fact.build_label(lb_text="B. Data Cleaning",
                                              lb_type="h3",
                                              lb_align=Qt.AlignLeft,
                                              lb_bold=True)
    remove_duplicate_box = self.build_rm_duplicate_box()
    handle_blank_box = self.build_handle_blank_box()
    handle_sort_box = self.build_handle_sort_box()
    
    #  frame
    frame = QFrame()
    frame_layout = QVBoxLayout()
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(remove_duplicate_box)
    frame_layout.addWidget(handle_blank_box)
    frame_layout.addWidget(handle_sort_box)
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setContentsMargins(8, 8, 8, 8) 
    frame.setLayout(frame_layout)
    return frame
  
  
  
  
  def build_clean_btn_box(self) -> QWidget:
    #  components
    reset_lb = self.app.comp_fact.build_label(lb_text="1a. Empty option and select again.",
                                              lb_type="h3",
                                              lb_txtcolor=THEME_COLOR["mid"],
                                              lb_align=Qt.AlignLeft,
                                              lb_bold=True)
    reset_btn = self.app.comp_fact.build_btn(btn_text="Reset",
                                             btn_event=None,
                                             btn_bgcolor=THEME_COLOR["white"],
                                             btn_txtcolor=THEME_COLOR["primary"],
                                             btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    proceed_lb = self.app.comp_fact.build_label(lb_text="1b. Confirmed, and proceed cleaning.",
                                              lb_type="h3",
                                              lb_txtcolor=THEME_COLOR["mid"],
                                              lb_align=Qt.AlignLeft,
                                              lb_bold=True)
    proceed_btn = self.app.comp_fact.build_btn(btn_text="Proceed",
                                             btn_event=None,
                                             btn_bgcolor=THEME_COLOR["white"],
                                             btn_txtcolor=THEME_COLOR["primary"],
                                             btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setContentsMargins(0, 0, 0, 0) 
    frame_layout.addWidget(reset_lb)
    frame_layout.addWidget(reset_btn)
    frame_layout.addWidget(proceed_lb)
    frame_layout.addWidget(proceed_btn)
    frame.setLayout(frame_layout)
    return frame
    
  
  
  
  #  METHODS - BOX
  
  
  def build_rm_duplicate_box(self) -> QWidget:
    
    #  declaration
    OPT_LIST = ["Remove duplicates for all columns.",
                "Remove duplications for selected columns ONLY.",
                "Keep unchanged."]
    
    #  components
    title_lb = self.app.comp_fact.build_label(lb_text="1. Remove Duplicates",
                                              lb_type="h3",
                                              lb_txtcolor=THEME_COLOR["mid"],
                                              lb_align=Qt.AlignLeft,
                                              lb_bold=True)
    radio_group = self.app.comp_fact.build_radio_group(target_list=OPT_LIST,
                                         target_event=None,
                                         is_horizontal=False)
    
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(radio_group["widget"])
    frame.setLayout(frame_layout)
    return frame
  
  
  def build_handle_blank_box(self) -> QWidget:
    
    #  declaration
    OPT_LIST = ["Drop rows with missing values.",
                "Fill missing values.",
                "Keep unchanged."]
    # components
    title_lb = self.app.comp_fact.build_label(lb_text="2. Handling Blanks",
                                            lb_type="h3",
                                            lb_txtcolor=THEME_COLOR["mid"],
                                            lb_align=Qt.AlignLeft,
                                            lb_bold=True)
    radio_group = self.app.comp_fact.build_radio_group(target_list=OPT_LIST,
                                         target_event=None,
                                         is_horizontal=False)
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(radio_group["widget"])
    frame.setLayout(frame_layout)
    return frame
    

  def build_handle_sort_box(self) -> QWidget:
    
    #  declaration
    OPT_LIST = ["Sort Ascendingly.",
                "Sort Decencdingly.",
                "Keep unsorted."]
    # components
    title_lb = self.app.comp_fact.build_label(lb_text="3. Sorting",
                                            lb_type="h3",
                                            lb_txtcolor=THEME_COLOR["mid"],
                                            lb_align=Qt.AlignLeft,
                                            lb_bold=True)
    radio_group = self.app.comp_fact.build_radio_group(target_list=OPT_LIST,
                                         target_event=None,
                                         is_horizontal=False)
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(radio_group["widget"])
    frame.setLayout(frame_layout)
    return frame
  
  
  
  #  RESET
  
  