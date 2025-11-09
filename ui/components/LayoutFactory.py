from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMessageBox, QPushButton, QStackedWidget, QGridLayout,QListWidget,
    QFrame, QHBoxLayout, QWidget, QMainWindow, QVBoxLayout, QLabel
)
from PyQt5.QtGui import QFont
from ui.components.ComponentsFactory import ComponentsFactory
from ui.components.config.styles import (
  THEME_COLOR, style_wd_default, style_topbar_default, style_wd_default_2, 
  style_testing_border, style_sidebar_box_default, style_content_panel_default,
  style_nav_sect_default)
from ui.components.config.events import (event_reset_app, event_close_app, event_next_btn, event_back_btn, event_done_btn)


#  CLASS

class LayoutFactory:
  
  #  Constructor    
  
  def __init__(self, app_ref):
    
    super().__init__()
    self.app_ref = app_ref  
    self.comp_fact = app_ref.comp_fact
    
    #  pages stack
    
    self.page_stack = QStackedWidget()
    
    self.page_1 = self.create_page_1()
    self.page_2 = self.create_page_2()
    # self.page_3 = self.create_page_3()
    # self.page_4 = self.create_page_4()
    # self.page_5 = self.create_page_5()
    # self.page_6 = self.create_page_6()
    # self.page_7 = self.create_page_7()

    #  step stack
    self.step_1 = self.create_step_1()
    self.step_2 = self.create_step_2()
    # self.step_3 = self.create_step_3()
    # self.step_4 = self.create_step_4()
    # self.step_5 = self.create_step_5()
    # self.step_6 = self.create_step_6()
    # self.step_7 = self.create_step_7()
    
    #  execution
    
    self.page_stack.addWidget(self.page_1)
    self.page_stack.addWidget(self.page_2)
    # self.page_stack.addWidget(self.page_3)
    # self.page_stack.addWidget(self.page_4)
    # self.page_stack.addWidget(self.page_5)
    # self.page_stack.addWidget(self.page_6)
    # self.page_stack.addWidget(self.page_7)
    
    #  learnt: to get total num, use stack.count()
    self.page_stack.setCurrentIndex(0)

    print("[PagesFactory] initialised successfully.") 
    
    
  #  METHODS - Page SETUPS
  
  def create_page_1(self):
    #  status section
    inner_status_sect = self.comp_fact.create_status_sect(sect_title="Step 1: Import Database", 
                                                          sect_des="This step reads the dataset, checks its structure, and prepares it for cleaning and processing.")
    
    #  statistic section
    inner_stat_sect = self.create_stat_sect()
    
    #  nav section
    inner_nav_sect = self.create_nav_sect()
    
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
    inner_status_sect = self.comp_fact.create_status_sect(sect_title="Step 2: Clean Data and Preprocessing", 
                                                          sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
    
    #  statistic section
    inner_stat_sect = self.create_stat_sect()
    
    #  nav section
    inner_nav_sect = self.create_nav_sect()
    
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
    print("page 3")
    
  def create_page_4(self):
    print("page 4")
    
  def create_page_5(self):
    print("page 5")
    
  def create_page_6(self):
    print("page 6")
    
  def create_page_7(self):
    print("page 7")
    
    
    
    
  #  METHODS - STEP SETUPS

  def create_step_1(self):
    return self.comp_fact.build_label(lb_text="🔘 1: Import Datasets",
                                      lb_type="h2",
                                      lb_align=Qt.AlignVCenter | Qt.AlignLeft,
                                      lb_bold=True
                                      )


  def create_step_2(self):
    return self.comp_fact.build_label(lb_text="🔘 2: Data Cleaning",
                                      lb_type="h2",
                                      lb_align=Qt.AlignVCenter | Qt.AlignLeft,
                                      lb_bold=True
                                      )
    
  def create_step_3(self):
    print("step 3")
    
  def create_step_4(self):
    print("step 4")
    
  def create_step_5(self):
    print("step 5")
    
  def create_step_6(self):
    print("step 6")
    
  def create_step_7(self):
    print("step 7")
      
      
      
      
  #  LAYER 4  -  SIDEBAR

  def create_task_sect(self) -> QWidget:
    sect_top = self.comp_fact.build_sidebar_listItem(lb_text="Task Process",
                                                     is_listTop=True)
    # outer frame
    task_sect = QWidget()
    task_sect_layout = QVBoxLayout()
    task_sect_layout.addWidget(sect_top, alignment=Qt.AlignTop)
    task_sect.setContentsMargins(0, 0, 0, 0)
    task_sect_layout.setSpacing(0)
    task_sect_layout.addStretch()
    task_sect.setLayout(task_sect_layout)
    task_sect.setStyleSheet(style_sidebar_box_default)
    return task_sect 


  def create_db_sect(self) -> QWidget:
    sect_top = self.comp_fact.build_sidebar_listItem(lb_text="Dataset Status",
                                                     is_listTop=True)
    # outer frame
    db_sect = QWidget()
    db_sect_layout = QVBoxLayout()
    db_sect_layout.addWidget(sect_top, alignment=Qt.AlignTop)
    db_sect.setContentsMargins(0, 0, 0, 0)
    db_sect_layout.setSpacing(0)
    db_sect_layout.addStretch()
    db_sect.setLayout(db_sect_layout)
    db_sect.setStyleSheet(style_sidebar_box_default)
    return db_sect    


  #  LAYER 4  -  WORK PANEL

  def create_stat_sect(self):
    # outer
    outer = QWidget()
    return outer


  def create_nav_sect(self):
    #  inner
    #  leanrt: lambda: enable importing parameters to fn
    btn_back = self.comp_fact.build_btn(btn_text="back",
                                        btn_event=lambda: event_back_btn(self.app_ref),
                                        btn_bgcolor=THEME_COLOR["white"],
                                        btn_txtcolor=THEME_COLOR["primary"],
                                        btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    btn_next = self.comp_fact.build_btn(btn_text="Next", 
                                              btn_event=lambda: event_next_btn(self.app_ref),
                                              btn_bgcolor=THEME_COLOR["primary"],
                                              btn_txtcolor=THEME_COLOR["white"],
                                              btn_hover_bgcolor=THEME_COLOR["primary_hvr"])
    btn_completed = self.comp_fact.build_btn(btn_text="Done",
                                              btn_event=lambda: event_reset_app(self.app_ref), 
                                              btn_bgcolor=THEME_COLOR["primary"],
                                              btn_txtcolor=THEME_COLOR["white"],
                                              btn_hover_bgcolor=THEME_COLOR["primary_hvr"])
    #  outer
    outer = QWidget()
    outer_layout = QHBoxLayout()
    outer_layout.addWidget(btn_back)
    outer_layout.addWidget(btn_next)
    outer_layout.addWidget(btn_completed)
    outer_layout.setContentsMargins(4, 4, 4, 4)
    outer_layout.setAlignment(Qt.AlignRight)
    outer.setStyleSheet(style_nav_sect_default)
    outer.setLayout(outer_layout)
    return outer


  #  LAYER 3  -  MAIN PANEL  -  
      
  def create_sidebar(self) -> QWidget:
    #  inner
    task_sect = self.create_task_sect()
    db_sect = self.create_db_sect()
    #  outer
    sidebar = QWidget()
    sidebar_layout = QGridLayout()
    sidebar_layout.addWidget(task_sect, 0, 0)
    sidebar_layout.addWidget(db_sect, 1, 0)
    sidebar_layout.setRowStretch(0, 5)
    sidebar_layout.setRowStretch(1, 3)
    sidebar_layout.setContentsMargins(0, 0, 0, 0)
    sidebar_layout.setSpacing(0)
    sidebar.setLayout(sidebar_layout)
    return sidebar


  #  LAYER 2  -   WINDOW

  # def create_content(self) -> QFrame:
    
  #   #  inner frame - left
  #   widget_sidebar = self.create_sidebar()
    
  #   #  inner frame - right
  #   widget_content= self.create_content()
    
  #   #  outer frame
  #   outer = QWidget()
  #   outer_layout = QGridLayout()
  #   outer_layout.addWidget(widget_sidebar, 0, 0)
  #   outer_layout.addWidget(widget_content, 0, 1)
  #   outer_layout.setColumnStretch(0, 1)
  #   outer_layout.setColumnStretch(1, 3)
  #   # .....
  #   outer.setLayout(outer_layout)
  #   return outer
    


  #  LAYER 1  -  WINDOW
    
  def create_window(self) -> QWidget:
    
    #  from window 
    window = QWidget()
    window_layout = QGridLayout()
    
    #  add child components
    widget_topbar = self.comp_fact.create_topbar()
    window_layout.addWidget(widget_topbar, 0, 0, 1, 2)
    widget_sidebar = self.create_sidebar()
    window_layout.addWidget(widget_sidebar, 1, 0)
    widget_content = self.page_stack
    window_layout.addWidget(widget_content, 1, 1)
    #  grid distribution
    window_layout.setRowStretch(0, 1)
    window_layout.setRowStretch(1, 9) 
    window_layout.setColumnStretch(0, 3)
    window_layout.setColumnStretch(1, 7)
    window_layout.setSpacing(0) 
    window_layout.setContentsMargins(0, 0, 0, 0)
    #  window setting
    window.setWindowTitle(style_wd_default["title"])
    window.setFont(QFont(style_wd_default["f_fam"], 
                          style_wd_default["f_size"]))
    window.resize(style_wd_default["resolution_width"], 
                  style_wd_default["resolution_height"])
    window.setStyleSheet(style_wd_default_2)
    window.setLayout(window_layout)
    #  learnt: disable flexible size
    window.setFixedSize(
      style_wd_default["resolution_width"],
      style_wd_default["resolution_height"]
    ) 
    #  learnt: disable window max.
    window.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
    
    return window
    
    