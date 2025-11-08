from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMessageBox, QPushButton, QStackedWidget, QGridLayout,QListWidget,
    QFrame, QHBoxLayout, QWidget, QMainWindow
)
from PyQt5.QtGui import QFont
from ui.components.ComponentsFactory import ComponentsFactory
from ui.components.config.styles import (
  style_wd_default, style_topbar_default, style_wd_default_2, 
  style_testing_border)
from ui.components.config.events import (event_reset_app, event_close_app)


#  CLASS

class LayoutFactory:
  
  #  Constructor    
  
  def __init__(self, app_ref):
    super().__init__()
    self.app_ref = app_ref    
    self.comp_fact = ComponentsFactory()
    print("[PagesFactory] initialised successfully.") 
    
    
  #  METHODS - PAGE SETUPS
  
  
  #  LAYER 4  -  SIDEBAR
  
  def create_task_sect(self):
    # outer frame
    outer = QListWidget()
    outer.setStyleSheet(style_testing_border)
    return outer
  
  
  def create_db_sect(self):
    # outer frame
    outer = QListWidget()
    outer.setStyleSheet(style_testing_border)
    return outer
  
  
  
  #  LAYER 4  -  WORK PANEL
  
  def create_status_sect(self):
    # outer
    outer = QWidget()
    outer_layout = QHBoxLayout()
    outer.setStyleSheet(style_testing_border)
    return outer
  
  
  def create_stat_sect(self):
    # outer
    outer = QStackedWidget()
    outer.setStyleSheet(style_testing_border)
    return outer
  
  
  def create_nav_sect(self):
    # outer
    outer = QStackedWidget()
    outer.setStyleSheet(style_testing_border)
    return outer
  
  
  
  #  LAYER 3  -  MAIN PANEL  -  
      
  def create_sidebar(self) -> QListWidget:
    #  inner
    inner_db_sect = self.create_db_sect()
    inner_task_sect = self.create_db_sect()
    #  outer
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout.addWidget(inner_task_sect, 0, 0)
    outer_layout.addWidget(inner_db_sect, 1, 0)
    outer_layout.setRowStretch(0, 7)
    outer_layout.setRowStretch(0, 2)
    outer_layout.setContentsMargins(0, 0, 0, 0)
    outer.setStyleSheet(style_testing_border)
    outer.setLayout(outer_layout)
    return outer
  
    
  def create_content(self) -> QWidget:
    #  inner
    inner_status_sect = self.create_status_sect()
    inner_stat_sect = self.create_stat_sect()
    inner_nav_sect = self.create_nav_sect()
    #  outer
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout.addWidget(inner_status_sect, 0, 0)
    outer_layout.addWidget(inner_stat_sect, 1, 0)
    outer_layout.addWidget(inner_nav_sect, 2, 0)
    outer_layout.setRowStretch(0, 2)
    outer_layout.setRowStretch(1, 8)
    outer_layout.setRowStretch(2, 1)
    outer_layout.setContentsMargins(0, 0, 0, 0)
    outer.setStyleSheet(style_testing_border)
    outer.setLayout(outer_layout)
    return outer



  #  LAYER 2  -   WINDOW
  
  def create_topbar(self) -> QFrame:
    
    #  inner frame - left
    
    # app_title = self.comp_fact.build_label(lb_text="APP TITLE")
    
    label_title = self.comp_fact.build_label(lb_text=style_wd_default["title"],
                                             lb_type="h1",
                                             lb_txtcolor="#f1f3f5",
                                             lb_align=Qt.AlignVCenter | Qt.AlignLeft)
    
    
    inner_lframe = QFrame()
    inner_lframe_layout = QHBoxLayout(inner_lframe)
    inner_lframe_layout.addWidget(label_title)
    inner_lframe.setLayout(inner_lframe_layout)
    
    
    #  inner frame - right
    btn_reset = self.comp_fact.build_btn(btn_text="🔄 reset",
                                        btn_event=lambda: event_reset_app(self.app_ref),
                                        btn_bgcolor="#fab005",
                                        btn_txtcolor="#333333",
                                        btn_hover_bgcolor="#f08c00")
    btn_exit = self.comp_fact.build_btn(btn_text="🚪 exit", 
                                        btn_event=lambda: event_close_app(self.app_ref),
                                        btn_bgcolor="#fa5252",
                                        btn_txtcolor="#333333",
                                        btn_hover_bgcolor="#e03131")
    
    inner_rframe = QFrame()
    inner_rframe_layout = QHBoxLayout()
    inner_rframe_layout.addWidget(btn_reset)
    inner_rframe_layout.addWidget(btn_exit)
    inner_rframe.setLayout(inner_rframe_layout)
    
    #  outer frame
    #  learnt:  widget -> layout -> widget -> layout ....
    outer = QFrame()
    outer_layout = QGridLayout()
    outer_layout.addWidget(inner_lframe, 0, 0)
    outer_layout.addWidget(inner_rframe, 0, 1)
    outer_layout.setColumnStretch(0, 5)
    outer_layout.setColumnStretch(1, 2)
    outer_layout.setContentsMargins(0, 0, 0, 0)
    outer.setStyleSheet(style_topbar_default)
    outer.setLayout(outer_layout)
    
    return outer
  
  
  def create_main_area(self) -> QFrame:
    
    #  inner frame - left
    widget_sidebar = self.create_sidebar()
    
    #  inner frame - right
    widget_content= self.create_content()
    
    #  outer frame
    outer = QFrame()
    outer_layout = QGridLayout()
    outer_layout.addWidget(widget_sidebar, 0, 0)
    outer_layout.addWidget(widget_content, 0, 1)
    outer_layout.setColumnStretch(0, 1)
    outer_layout.setColumnStretch(1, 3)
    # .....
    outer.setStyleSheet(style_testing_border)
    outer.setLayout(outer_layout)
    return outer
    
  

  #  LAYER 1  -  WINDOW
   
  def create_window(self) -> QWidget:
    
    #  from window 
    window = QWidget()
    window_layout = QGridLayout()
    
    #  add child components
    widget_topbar = self.create_topbar()
    window_layout.addWidget(widget_topbar, 0, 0)
    widget_main_area = self.create_main_area()
    window_layout.addWidget(widget_main_area, 1, 0)
    #  learnt: to split 1:9 
    window_layout.setRowStretch(0, 1)
    window_layout.setRowStretch(1, 9)
    
    window.setWindowTitle(style_wd_default["title"])
    window_layout.setContentsMargins(0, 0, 0, 0)
    window_layout.setSpacing(0)
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
    
    