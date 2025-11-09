from typing import Callable
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QLabel, QPushButton, QMessageBox, QStackedWidget,
    QListWidget, QFrame, QGridLayout, QVBoxLayout, QHBoxLayout
)
from ui.components.config.styles import (
    THEME_COLOR,
    style_btn_default,
    style_btn_contrast,
    style_lb_default,
    style_wd_default,
    style_wd_default_2,
    style_topbar_default,
    style_sidebar_default,
    style_content_panel_default,
    style_testing_border
)
from ui.components.config.events import (
  event_reset_app, 
  event_close_app, 
  event_done_btn,
  event_back_btn,
  event_next_btn
)



#  CLASS

class ComponentsFactory:
  
  #  Constructor
  
  def __init__(self, app_ref):
    self.app_ref = app_ref
    print("[ComponentsFactory] initialised successfully.") 


  #  build components
  
  def build_label(self, 
                lb_text: str | None,
                lb_type: str="p",
                lb_txtcolor: str=THEME_COLOR["dark"],
                lb_align: Qt.AlignmentFlag=Qt.AlignCenter,
                lb_bold: bool=False,
                lb_italic: bool=False,
                lb_wrap: bool=False) -> QLabel:
    lb = QLabel(lb_text.strip())
    font = lb.font()
    font.setFamily("Impact")
    font.setBold(lb_bold)
    font.setItalic(lb_italic)
    if lb_type == "h1":
      font.setPointSize(28)
    elif lb_type == "h2":
      font.setPointSize(20)
    elif lb_type == "h3":
      font.setPointSize(16)
    else:
      font.setPointSize(12)
      font.setFamily("Arial")
    lb.setStyleSheet(style_lb_default.format(txtcolor=lb_txtcolor))
    lb.setWordWrap(lb_wrap)
    lb.setAlignment(lb_align)
    lb.setFont(font)
    return lb
  
  
  def build_btn(self,
                btn_text: str | None, 
                btn_event: Callable | None,
                btn_bgcolor: str,
                btn_txtcolor: str,
                btn_hover_bgcolor: str) -> QPushButton:
    
    btn = QPushButton(btn_text.strip().title())
    btn.setFixedHeight(32)
    btn.setFixedWidth(92)
    btn.setCursor(Qt.PointingHandCursor)
    # style sheet option
    if btn_bgcolor == THEME_COLOR["white"]:
      adopted_style = style_btn_contrast
    else:
      adopted_style = style_btn_default
    btn.setStyleSheet(adopted_style.format(bgcolor=btn_bgcolor, 
                                            txtcolor=btn_txtcolor,
                                            hover_bgcolor=btn_hover_bgcolor))
    #  events
    if btn_event:
      btn.clicked.connect(btn_event)
    return btn
    
    
  def build_msg_box(self, 
                    app_window: QWidget,
                    title: str | None, 
                    question: str) -> bool:
    #  get response
    res = QMessageBox.question(app_window, 
                                title, 
                                question, 
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No)
    #  make decision
    return res == QMessageBox.Yes
  
  
  def build_reminder_box(self,
                         title: str, 
                         txt_msg: str) -> QMessageBox:
    msg = QMessageBox(self.app_ref.window)
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle(title)
    msg.setText(txt_msg)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
    return msg
    

  #  section components
  
  def create_topbar(self) -> QFrame:
    
    #  inner frame - left
    
    label_title = self.build_label(lb_text=style_wd_default["title"],
                                  lb_type="h1",
                                  lb_txtcolor=THEME_COLOR["white"],
                                  lb_align=Qt.AlignVCenter | Qt.AlignLeft,
                                  lb_italic=True,
                                  lb_bold=True)
    
    inner_lframe = QFrame()
    inner_lframe_layout = QHBoxLayout(inner_lframe)
    inner_lframe_layout.addWidget(label_title)
    inner_lframe.setLayout(inner_lframe_layout)
    
    
    #  inner frame - right
    btn_reset = self.build_btn(btn_text="reset",
                              btn_event=lambda: event_reset_app(self.app_ref),
                              btn_bgcolor="#fab005",
                              btn_txtcolor=THEME_COLOR["dark"],
                              btn_hover_bgcolor="#f08c00")
    btn_exit = self.build_btn(btn_text="exit", 
                              btn_event=lambda: event_close_app(self.app_ref),
                              btn_bgcolor="#fa5252",
                              btn_txtcolor=THEME_COLOR["dark"],
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
  

  def create_status_sect(self, 
                         sect_title:str="Insert Title",
                         sect_des:str="Insert Description"):

     # inner - title
    title = self.build_label(lb_text=sect_title, 
                            lb_type="h2", 
                            lb_align=Qt.AlignVCenter | Qt.AlignLeft,
                            lb_bold=True)

    title.setFixedHeight(32)
    
    # inner - item list
    description = self.build_label(lb_text=sect_des, 
                                  lb_type="h3", 
                                  lb_align=Qt.AlignLeft, 
                                  lb_wrap=True,
                                  lb_italic=True)
    description.setStyleSheet("margin-bottom: 4px;")
    
    # outer
    status_sect = QWidget()
    status_sect_layout  = QVBoxLayout()
    status_sect_layout.addWidget(title)
    status_sect_layout.addWidget(description)
    status_sect_layout.setContentsMargins(0, 0, 0, 0)
    status_sect_layout.setSpacing(0)
    status_sect.setLayout(status_sect_layout)
    return status_sect
  
  
  
  

  
  
  
