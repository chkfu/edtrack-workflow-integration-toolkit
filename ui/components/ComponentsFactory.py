from typing import Callable
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QPushButton, QLabel, QWidget
from ui.components.config.styles import (
    style_btn_default,
    style_lb_default_h1,
    style_lb_default_p
)



#  CLASS

class ComponentsFactory:
  
  #  Constructor
  
  def __init__(self):
    print("[ComponentsFactory] initialised successfully.") 


  #  build components
  
  def build_label(self, 
                lb_text: str | None,
                lb_type: str="p",
                lb_txtcolor: str="#333333",
                lb_align: Qt.AlignmentFlag=Qt.AlignCenter,
                lb_wrap: bool=False) -> QLabel:
    lb = QLabel(lb_text.strip())
    if lb_wrap:
      lb.setWordWrap(True)
    if lb_align:
      lb.setAlignment(lb_align)
    if lb_type == "h1":
      lb.setStyleSheet(style_lb_default_h1.format(txtcolor=lb_txtcolor))
    else:
      lb.setStyleSheet(style_lb_default_p.format(txtcolor=lb_txtcolor))
    return lb
  
  
  def build_btn(self,
                btn_text: str | None, 
                btn_event: Callable | None,
                btn_bgcolor: str,
                btn_txtcolor: str,
                btn_hover_bgcolor: str) -> QPushButton:
    
    btn = QPushButton(btn_text.strip().title())
    btn.setCursor(Qt.PointingHandCursor)
    btn.setStyleSheet(style_btn_default.format(bgcolor=btn_bgcolor, 
                                               txtcolor=btn_txtcolor,
                                               hover_bgcolor=btn_hover_bgcolor))
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
                         app_window: QWidget,
                         title: str, 
                         txt_msg: str) -> QMessageBox:
    msg = QMessageBox(app_window)
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle(title)
    msg.setText(txt_msg)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
    return msg
    


  
  

  
  
  
