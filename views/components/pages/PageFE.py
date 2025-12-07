from operator import xor
from turtle import title
from PyQt5.QtWidgets import (
  QFrame, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from matplotlib import container
from views.components.pages.PageTemplate import PageTemplate
from views.components.config.views_styles import THEME_COLOR, style_tab_scroll
import logging
from typing import Callable
import pandas as pd


#  LOGGING

logger = logging.getLogger("PAGE_FEATENG")


#  CLASS

class PageFE(PageTemplate):
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    super().__init__(app_ref)
    logger.info("initialised successfully.")
    
    
  #  METHODS -  MAIN
  
  def merge_sections(self) -> QWidget:
    #  title section
    inner_title_sect = self.create_title_sect(sect_title="Step 4: Feature Engineering", 
                                                sect_des="This step reads the dataset, checks its structure, and prepares it for cleaning and processing.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=4)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True,
                                          enable_next=True)
    #  Work Panel Grid
    page = QWidget()
    page_layout = self.reuse_page_setting(inner_title_sect=inner_title_sect,
                                           inner_stat_sect=inner_stat_sect,
                                           inner_nav_sect=inner_nav_sect)
    page.setLayout(page_layout)
    return page
  

  def core_sect_feateng(self) -> QFrame:
    
    RESTRUCT_CONFIG: list= [
       {
          "title": "1. Rename Columns",
          "options": ["Select columns to be renamed.", "Remain Unchanged."],
          "function": lambda text, checked: print(f"{text}")
        },
        {
          "title": "2. Remove Columns",
          "options": ["Select columns to be removed.", "Remain Unchanged."],
          "function": lambda text, checked: print(f"{text}")
        },
        {
          "title": "3. Remove Specific Values",
          "options": ["Select Values to be removed.", "Remain Unchanged."],
          "function": lambda text, checked: print(f"{text}")
        },
    ]

    FE_CONFIG: list = [
        {
          "title": "1. Manage Time Features",
          "options": ["Manage the time features.", "Remain Unchanged."],
          "function": lambda text, checked: print(f"{text}")
        },
        {
          "title": "2. Hash Name Features",
          "options": ["Hash the name features.", "Remain Unchanged."],
          "function": lambda text, checked: print(f"{text}")
        },
        {
          "title": "3. Handle Target Items",
          "options": ["Standardise the items.", "Remain Unchanged."],
          "function": lambda text, checked: print(f"{text}")
        },
        {
          "title": "4. Handle Action Items",
          "options": ["Standardise the items.", "Remain Unchanged."],
          "function": lambda text, checked: print(f"{text}")
        }
      ]
      

    #  components
    restruct_container = self.app.comp_fact.build_reused_opt_container(target_title="A. Restructure Dataframe",
                                                                        target_config=RESTRUCT_CONFIG)
    fe_container = self.app.comp_fact.build_reused_opt_container(target_title="B. Feature Engineering",
                                                                 target_config=FE_CONFIG)
    reset_container = self.app.comp_fact.build_reused_single_btn_box(target_title="C. Reset Options",
                                                                   target_statement=None,
                                                                   target_btn_text="Reset",
                                                                   target_btn_event=lambda: print("Reset clicked"))
    #  frame
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.addWidget(restruct_container)
    layout.addWidget(fe_container)
    layout.addWidget(reset_container)
    layout.addStretch()
    layout.setSpacing(24)
    layout.setContentsMargins(0, 0, 0, 0)
    scroll.setStyleSheet(style_tab_scroll)
    scroll.setWidget(container)
    return scroll
  
  

  
    

    
      

    