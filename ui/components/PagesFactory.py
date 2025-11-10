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
    inner_stat_sect = self.create_stat_sect(target_page=1)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_next=True)
    
    #  Work Panel Grid
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout = self.reuse_page_setting(inner_status_sect, inner_stat_sect, inner_nav_sect)
    outer.setStyleSheet(style_content_panel_default)
    outer.setLayout(outer_layout)
    return outer


  def create_page_2(self):
    #  status section
    inner_status_sect = self.create_status_sect(sect_title="Step 2: Clean Data and Preprocessing", 
                                                sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=2)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, enable_next=True)
    
    #  Work Panel Grid
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout = self.reuse_page_setting(inner_status_sect, inner_stat_sect, inner_nav_sect)
    outer.setStyleSheet(style_content_panel_default)
    outer.setLayout(outer_layout)
    return outer


  def create_page_3(self):
    #  status section
    inner_status_sect = self.create_status_sect(sect_title="Step 3: Merge Tables", 
                                                sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=3)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, enable_next=True)
    
    #  Work Panel Grid
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout = self.reuse_page_setting(inner_status_sect, inner_stat_sect, inner_nav_sect)
    outer.setStyleSheet(style_content_panel_default)
    outer.setLayout(outer_layout)
    return outer


  def create_page_4(self):
    #  status section
    inner_status_sect = self.create_status_sect(sect_title="Step 4: Analyse Data", 
                                                sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=4)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, enable_done=True)
    
    #  Work Panel Grid
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout = self.reuse_page_setting(inner_status_sect, inner_stat_sect, inner_nav_sect)
    outer.setStyleSheet(style_content_panel_default)
    outer.setLayout(outer_layout)
    return outer
  
  
  
   #  LAYER 3  -  SECTIONS
  
  def create_status_sect(self, 
                         sect_title:str="Insert Title",
                         sect_des:str="Insert Description") -> QWidget:

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
  

  def create_stat_sect(self, target_page: int) -> QWidget | None:
    
    if target_page not in range(1, 5):
      return
    
    MATCHING = {
      "1": lambda: self.core_sect_import_dataset(),
      "2": lambda: self.core_sect_clean_data(),
      "3": lambda: self.core_sect_merge_tables(),
      "4": lambda: self.core_sect_analyse_data()
    }
    
    for index, fn in enumerate(MATCHING):
      return fn if int(index) == target_page else None
    
    
  def create_nav_sect(self, 
                      enable_back: bool = False,
                      enable_next: bool = False,
                      enable_done: bool = False) -> QWidget:
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
    nav = QWidget()
    nav_layout = QHBoxLayout()
    
    if enable_back:
      nav_layout.addWidget(btn_back)
    if enable_next:
      nav_layout.addWidget(btn_next)
    if enable_done:
      nav_layout.addWidget(btn_completed)
      
    nav_layout.setContentsMargins(4, 4, 4, 4)
    nav_layout.setAlignment(Qt.AlignRight)
    nav.setStyleSheet(style_nav_sect_default)
    nav.setLayout(nav_layout)
    return nav
  


  #  LAYER 4  -  SUBSTITUTE STATISTIC PANEL

  
  def core_sect_import_dataset(self) -> QWidget:
    
    #  outer
    core_sect = QWidget()
    core_sect_layout = QVBoxLayout()
    # .....
    core_sect.setLayout(core_sect_layout)
    return core_sect
  
  
  def core_sect_clean_data(self) -> QWidget:
    
    #  outer
    core_sect = QWidget()
    core_sect_layout = QVBoxLayout()
    # .....
    core_sect.setLayout(core_sect_layout)
    return core_sect
    
    
  def core_sect_merge_tables(self) -> QWidget:
    
    #  outer
    core_sect = QWidget()
    core_sect_layout = QVBoxLayout()
    # .....
    core_sect.setLayout(core_sect_layout)
    return core_sect
    
    
  def core_sect_analyse_data(self) -> QWidget:
    
    #  outer
    core_sect = QWidget()
    core_sect_layout = QVBoxLayout()
    # .....
    core_sect.setLayout(core_sect_layout)
    return core_sect
  
  
  def reuse_page_setting(self,
                        inner_status_sect: QWidget,
                        inner_stat_sect: QWidget,
                        inner_nav_sect: QWidget) -> QGridLayout:
      layout = QGridLayout()
      layout.addWidget(inner_status_sect, 0, 0)
      layout.addWidget(inner_stat_sect, 1, 0)
      layout.addWidget(inner_nav_sect, 2, 0)
      layout.setRowStretch(0, 2)
      layout.setRowStretch(1, 8)
      layout.setRowStretch(2, 1)
      layout.setContentsMargins(24, 16, 24, 24)
      layout.setSpacing(12)
      return layout