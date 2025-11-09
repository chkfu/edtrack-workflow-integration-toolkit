from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout
)
from ui.components.config.styles import (
    THEME_COLOR, style_content_panel_default, style_nav_sect_default,
)
from ui.components.config.events import (
    event_reset_app,event_next_btn,event_back_btn,
)



#  CLASS

class PagesFactory:
  
  #  Constructor
  
  def __init__(self, app_ref):
    super().__init__()
    #  setup ref states
    self.app_ref = app_ref  
    
    

    #  LAYER 3  -  PAGES
  
  def create_page_1(self):
    #  status section
    inner_status_sect = self.create_status_sect(sect_title="Step 1: Import Datasets", 
                                                sect_des="This step reads the dataset, checks its structure, and prepares it for cleaning and processing.")
    
    #  statistic section
    inner_stat_sect = self.create_stat_sect()
    
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_next=True)
    
    #  Work Panel Grid
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout.addWidget(inner_status_sect, 0, 0)
    outer_layout.addWidget(inner_stat_sect, 1, 0)
    outer_layout.addWidget(inner_nav_sect, 2, 0)
    outer_layout.setRowStretch(0, 2)
    outer_layout.setRowStretch(1, 8)
    outer_layout.setRowStretch(2, 1)
    outer_layout.setContentsMargins(24, 16, 24, 24)
    outer_layout.setSpacing(12)
    outer.setStyleSheet(style_content_panel_default)
    outer.setLayout(outer_layout)
    return outer


  def create_page_2(self):
    #  status section
    inner_status_sect = self.create_status_sect(sect_title="Step 2: Clean Data and Preprocessing", 
                                                sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
    
    #  statistic section
    inner_stat_sect = self.create_stat_sect()
    
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, enable_next=True)
    
    #  Work Panel Grid
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout.addWidget(inner_status_sect, 0, 0)
    outer_layout.addWidget(inner_stat_sect, 1, 0)
    outer_layout.addWidget(inner_nav_sect, 2, 0)
    outer_layout.setRowStretch(0, 2)
    outer_layout.setRowStretch(1, 8)
    outer_layout.setRowStretch(2, 1)
    outer_layout.setContentsMargins(24, 16, 24, 24)
    outer_layout.setSpacing(12)
    outer.setStyleSheet(style_nav_sect_default)
    outer.setLayout(outer_layout)
    return outer


  def create_page_3(self):
    #  status section
    inner_status_sect = self.create_status_sect(sect_title="Step 3: Merge Tables", 
                                                sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
    
    #  statistic section
    inner_stat_sect = self.create_stat_sect()
    
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, enable_next=True)
    
    #  Work Panel Grid
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout.addWidget(inner_status_sect, 0, 0)
    outer_layout.addWidget(inner_stat_sect, 1, 0)
    outer_layout.addWidget(inner_nav_sect, 2, 0)
    outer_layout.setRowStretch(0, 2)
    outer_layout.setRowStretch(1, 8)
    outer_layout.setRowStretch(2, 1)
    outer_layout.setContentsMargins(24, 16, 24, 24)
    outer_layout.setSpacing(12)
    outer.setStyleSheet(style_nav_sect_default)
    outer.setLayout(outer_layout)
    return outer

  def create_page_4(self):
    #  status section
    inner_status_sect = self.create_status_sect(sect_title="Step 4: Analyse Data", 
                                                sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
    
    #  statistic section
    inner_stat_sect = self.create_stat_sect()
    
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, enable_done=True)
    
    #  Work Panel Grid
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout.addWidget(inner_status_sect, 0, 0)
    outer_layout.addWidget(inner_stat_sect, 1, 0)
    outer_layout.addWidget(inner_nav_sect, 2, 0)
    outer_layout.setRowStretch(0, 2)
    outer_layout.setRowStretch(1, 8)
    outer_layout.setRowStretch(2, 1)
    outer_layout.setContentsMargins(24, 16, 24, 24)
    outer_layout.setSpacing(12)
    outer.setStyleSheet(style_nav_sect_default)
    outer.setLayout(outer_layout)
    return outer
  
  
  
   #  LAYER 3  -  SECTIONS
  
  def create_status_sect(self, 
                         sect_title:str="Insert Title",
                         sect_des:str="Insert Description"):

     # inner - title
    title = self.app_ref.comp_fact.build_label(lb_text=sect_title, 
                                      lb_type="h2", 
                                      lb_align=Qt.AlignVCenter | Qt.AlignLeft,
                                      lb_bold=True)

    title.setFixedHeight(32)
    
    # inner - item list
    description = self.app_ref.comp_fact.build_label(lb_text=sect_des, 
                                             lb_txtcolor=THEME_COLOR["mid"],
                                              lb_type="h3", 
                                              lb_align=Qt.AlignLeft, 
                                              lb_wrap=True)
    
    # outer
    status_sect = QWidget()
    status_sect_layout  = QVBoxLayout()
    status_sect_layout.addWidget(title)
    status_sect_layout.addWidget(description)
    status_sect_layout.setContentsMargins(0, 0, 0, 0)
    status_sect_layout.setSpacing(0)
    status_sect.setLayout(status_sect_layout)
    return status_sect
  

  def create_stat_sect(self):
    # outer
    outer = QWidget()
    return outer


  def create_nav_sect(self, 
                    enable_back: bool = False,
                    enable_next: bool = False,
                    enable_done: bool = False):
    #  inner
    #  leanrt: lambda: enable importing parameters to fn
    btn_back = self.app_ref.comp_fact.build_btn(btn_text="back",
                                        btn_event=lambda: event_back_btn(self.app_ref),
                                        btn_bgcolor=THEME_COLOR["white"],
                                        btn_txtcolor=THEME_COLOR["primary"],
                                        btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    btn_next = self.app_ref.comp_fact.build_btn(btn_text="Next", 
                                              btn_event=lambda: event_next_btn(self.app_ref),
                                              btn_bgcolor=THEME_COLOR["primary"],
                                              btn_txtcolor=THEME_COLOR["white"],
                                              btn_hover_bgcolor=THEME_COLOR["primary_hvr"])
    btn_completed = self.app_ref.comp_fact.build_btn(btn_text="Done",
                                              btn_event=lambda: event_reset_app(self.app_ref), 
                                              btn_bgcolor=THEME_COLOR["primary"],
                                              btn_txtcolor=THEME_COLOR["white"],
                                              btn_hover_bgcolor=THEME_COLOR["primary_hvr"])
    #  outer
    outer = QWidget()
    outer_layout = QHBoxLayout()
    
    if enable_back:
      outer_layout.addWidget(btn_back)
    if enable_next:
      outer_layout.addWidget(btn_next)
    if enable_done:
      outer_layout.addWidget(btn_completed)
      
    outer_layout.setContentsMargins(4, 4, 4, 4)
    outer_layout.setAlignment(Qt.AlignRight)
    outer.setStyleSheet(style_nav_sect_default)
    outer.setLayout(outer_layout)
    return outer