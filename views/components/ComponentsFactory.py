import pandas as pd
import logging
from typing import Callable
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
  QLabel, QPushButton, QMessageBox, QDialog, QVBoxLayout, QWidget,
  QFrame, QHBoxLayout, QGridLayout, QScrollArea, QTableWidget,
  QTableWidgetItem
)
from views.components.config.views_styles import (
    THEME_COLOR, style_btn_default, style_btn_contrast, style_lb_default, 
    style_sidebar_listItem_default
)


#  LOGGING

logger = logging.getLogger("APPLICATION")


#  CLASS

class ComponentsFactory:
  
  #  Constructor
  
  def __init__(self, app_ref):
    self.app = app_ref
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
    lb = QLabel(lb_text)
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
    res = QMessageBox.question(self.app.window, 
                                title, 
                                question, 
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No)
    #  make decision
    return res == QMessageBox.Yes
  
  
  def build_reminder_box(self,
                         title: str, 
                         txt_msg: str) -> QMessageBox:
    msg = QMessageBox(self.app.window)
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
  
  
  def build_table_view(self,
                     target_df: pd.DataFrame):
    
    #  validation
    if not isinstance(target_df, pd.DataFrame):
      err_msg = "Imported table is invalid."
      logger.error(err_msg, exc_info=True)
      raise ValueError()
    #  interface
    table = QTableWidget()
    rows, cols = target_df.shape
    table.setRowCount(rows)
    table.setColumnCount(cols)
    #  loop for filling
    
    for row in range(rows):
      for col in range(cols):
        item = str(target_df.iloc[row, col])
        table.setHorizontalHeaderLabels([str(col) for col in target_df[:100].columns])
        table.setItem(row, col, QTableWidgetItem(item))
    table.setStyleSheet("color: #333333; border: 1px solid #333333")
    return table
  
  
  def build_popup_wd(self, 
                     wd_title:str="Untitled",
                     popup_title:str="Untitled",
                     popup_content: Callable | None = None):
    
    #  title sect
    def add_title_box() -> QFrame:
      content_title = self.build_label(lb_text=popup_title,
                      lb_type="h1",
                      lb_txtcolor=THEME_COLOR["primary"],
                      lb_align=Qt.AlignLeft | Qt.AlignVCenter,
                      lb_bold=True)
      content_title.setStyleSheet("background-color: #213D57; padding: 12px")
      box = QFrame()
      box_layout = QHBoxLayout()
      box_layout.setSpacing(0)
      box_layout.setContentsMargins(0, 0, 0, 0)
      box_layout.addWidget(content_title)
      box.setLayout(box_layout)
      return box
    
    #  grpah
    def add_content_box():
      #  component
      diagram = popup_content
      #  frame
      frame = QScrollArea()
      frame_layout = QVBoxLayout()
      frame_layout.addWidget(diagram)
      frame.setLayout(frame_layout)
      return frame
    
    #  button sect
    def add_option_box() -> QFrame:
      box_export_btn = self.build_btn(btn_text="Export", 
                                  btn_event=None, 
                                  btn_bgcolor=THEME_COLOR["white"],
                                  btn_txtcolor=THEME_COLOR["primary"],
                                  btn_hover_bgcolor=THEME_COLOR["white_hvr"])
      box_back_btn = self.build_btn(btn_text="Confirmed", 
                                  btn_event=None, 
                                  btn_bgcolor=THEME_COLOR["primary"],
                                  btn_txtcolor=THEME_COLOR["white"],
                                  btn_hover_bgcolor=THEME_COLOR["primary_hvr"])
      box = QFrame()
      #  add
      box_layout = QHBoxLayout()
      box_layout.addWidget(box_export_btn)
      box_layout.addWidget(box_back_btn)
      box_layout.setSpacing(0)
      box_layout.setContentsMargins(0, 0, 0, 0)
      box.setLayout(box_layout)
      return box
    
    #  setup components
    p_title = add_title_box()
    p_content = add_content_box()
    p_opt = add_option_box()
    
    #  frame
    window = QDialog()
    window.setWindowTitle(wd_title)
    #  learnt: setModal, prevent users manage main window simultanously
    window.setModal(True)
    window.setFixedSize(600, 600)
    window_layout = QGridLayout()
    window_layout.addWidget(p_title, 1, 0)
    window_layout.addWidget(p_content, 2, 0)
    window_layout.addWidget(p_opt, 3, 0)
    window_layout.setRowStretch(1, 3)
    window_layout.setRowStretch(2, 21)
    window_layout.setRowStretch(3, 4)
    window_layout.setSpacing(0)
    window_layout.setContentsMargins(0, 0, 0, 0)
    window.setStyleSheet("background-color: #C6D1D8; border: 1px solid red;")
    window.setLayout(window_layout)
    window.exec()
      
