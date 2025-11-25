from PyQt5.QtWidgets import (
  QWidget, QGridLayout, QVBoxLayout, QRadioButton, QButtonGroup, QFrame,
  QHBoxLayout, QCheckBox
)
from PyQt5.QtCore import Qt
from views.components.config.views_config import DATASET_LIST
from views.components.config.views_styles import THEME_COLOR
from views.components.config.views_styles import style_nav_sect_default
from views.components.pages.PageTemplate import PageTemplate
import logging
from typing import Callable


#  LOGGING

logger = logging.getLogger("PAGE_CLEAN")



#  CLASS


class PageClean(PageTemplate):
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    super().__init__(app_ref)
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
    page_layout = QGridLayout()
    page_layout = self.reuse_page_setting(inner_title_sect=inner_title_sect,
                                           inner_stat_sect=inner_stat_sect,
                                           inner_nav_sect=inner_nav_sect)
    page.setStyleSheet(style_nav_sect_default)
    page.setLayout(page_layout)
    return page


  def core_sect_clean_data(self) -> QWidget:
    #  components
    tb_select_container = self.build_tb_opt_container()
    basic_clean_container = self.build_basic_clean_container()
    #  frame
    core_sect = QWidget()
    core_sect_layout = QVBoxLayout()
    core_sect_layout.addWidget(tb_select_container)
    core_sect_layout.addWidget(basic_clean_container)
    core_sect_layout.setAlignment(Qt.AlignTop)
    core_sect_layout.setSpacing(16)
    core_sect_layout.setContentsMargins(0, 0, 0, 0) 
    core_sect.setLayout(core_sect_layout)
    return core_sect
    
    
  #  METHODS - CONTAINER
  
  def build_tb_opt_container(self) -> QFrame:
    #  components
    title_lb = self.app.comp_fact.build_label(lb_text="A. Table Selection",
                                              lb_type="h3",
                                              lb_align=Qt.AlignLeft,
                                              lb_bold=True)
    
    OPT_LIST: list = [item["data"] for item in DATASET_LIST[1:4]]
    radio_box = self.build_radio_group(target_list=OPT_LIST)["widget"]
    
    #  frame
    frame = QFrame()
    frame_layout = QVBoxLayout()
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(radio_box)
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setContentsMargins(0, 0, 0, 0) 
    frame.setLayout(frame_layout)
    return frame
  
  
  def build_basic_clean_container(self) -> QFrame:
    #  components
    title_lb = self.app.comp_fact.build_label(lb_text="B. Basic Cleaning",
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
    # ....
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setContentsMargins(0, 0, 0, 0) 
    frame.setLayout(frame_layout)
    return frame
  
  
  def build_advanced_clean_container(self) -> QFrame:
    #  components
    title_lb = self.app.comp_fact.build_label(lb_text="C. Advanced Cleaning",
                                              lb_type="h3",
                                              lb_align=Qt.AlignLeft,
                                              lb_bold=True)

    #  frame
    frame = QFrame()
    frame_layout = QVBoxLayout()
    frame_layout.addWidget(title_lb)
    # ....
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setContentsMargins(0, 0, 0, 0) 
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
    radio_group = self.build_radio_group(target_list=OPT_LIST,
                                         target_event=None,
                                         is_horizontal=False)
    
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.setSpacing(4)
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
    radio_group = self.build_radio_group(target_list=OPT_LIST,
                                         target_event=None,
                                         is_horizontal=False)
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.setSpacing(4)
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
    radio_group = self.build_radio_group(target_list=OPT_LIST,
                                         target_event=None,
                                         is_horizontal=False)
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.setSpacing(4)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(radio_group["widget"])
    frame.setLayout(frame_layout)
    return frame
  
  
  
  #  RESET
  
  # TODO: @ move to comp fact
  def build_radio_group(self, 
                        target_list: list,
                        target_event: Callable=None,
                        is_horizontal: bool=True):
    
    #  Learnt: QButtonGroup is also a logical object, still need an visual body
    container = QWidget()
    group = QButtonGroup()
    if is_horizontal:
      group_layout = QHBoxLayout()
    else:
      group_layout = QVBoxLayout()
    
    for index, opt in enumerate(target_list):
      btn = QRadioButton(opt)
      group.addButton(btn, index)
      group_layout.addWidget(btn)
      
    if target_event:
      group.buttonClicked.connect(lambda el: target_event(el.text()))
      
    group_layout.setSpacing(4)
    group_layout.setAlignment(Qt.AlignLeft)
    group_layout.setContentsMargins(0, 0, 0, 0) 
    container.setLayout(group_layout)
    
    return {"widget": container, "group": group}