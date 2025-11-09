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
    style_sidebar_listItem_default,
    style_wd_default,
    style_wd_default_2,
    style_topbar_default,
    style_sidebar_box_default,
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
                lb_txtcolor: str=THEME_COLOR["primary"],
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
      font.setPointSize(24)
    elif lb_type == "h2":
      font.setPointSize(18)
    elif lb_type == "h3":
      font.setPointSize(14)
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
                    title: str | None, 
                    question: str) -> bool:
    #  get response
    res = QMessageBox.question(self.app_ref.window, 
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
    
    
  #  section child items
  
  def build_sidebar_listItem(self, 
              is_listTop: bool=False,
              lb_text: str = "") -> QLabel:
  
    lb = QLabel(lb_text.strip())
    font = lb.font()
    font.setFamily("Impact")
    lb.setFont(font)
    lb.setFixedHeight(36)
    lb.setContentsMargins(0, 0, 0, 0)   
    if is_listTop:
      font.setPointSize(14)
      lb.setStyleSheet(style_sidebar_listItem_default.format(txtcolor=THEME_COLOR["white_hvr"],
                                                            bgcolor=THEME_COLOR["primary"]))
      lb.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
    
    else:
      font.setPointSize(14)
      lb.setStyleSheet(style_sidebar_listItem_default.format(txtcolor=THEME_COLOR["primary"],
                                                            bgcolor=THEME_COLOR["white_hvr"]))
      lb.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    
    lb.setFont(font)
      
    return lb
      
