from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMessageBox, QPushButton, QStackedWidget, QGridLayout,QListWidget,
    QFrame, QHBoxLayout, QWidget, QMainWindow
)
from PyQt5.QtGui import QFont
from ui.components.ComponentsFactory import ComponentsFactory
from ui.components.config.styles import (style_wd_default, style_topbar_default, style_wd_default_2)
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
    #  outer frame
    outer = QFrame()
    outer_layout = QGridLayout()
    # .....
    outer.setLayout(outer_layout)
    return outer
    
  
    
  def create_sidebar(self):
    #  outer frame
    outer = QListWidget()
    outer_layout = QHBoxLayout()
    # .....
    outer.setLayout(outer_layout)
    return outer
  
    
  def create_work_panel(self):
    print()

    
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
    
    