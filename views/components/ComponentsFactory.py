import pandas as pd
import logging
from typing import Callable
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
  QLabel, QPushButton, QMessageBox, QDialog, QVBoxLayout, QFrame, QHBoxLayout, 
  QGridLayout, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView, 
  QComboBox, QWidget, QButtonGroup, QRadioButton
)
from views.components.config.views_styles import (
    THEME_COLOR, style_btn_default, style_btn_contrast, style_lb_default, 
    style_sidebar_listItem_default
)
from views.components.config.views_config import DATASET_LIST


#  LOGGING

logger = logging.getLogger("COMPONENT_FACTORY")


#  CLASS

class ComponentsFactory:
  
  #  Constructor
  
  def __init__(self, app_ref):
    self.app = app_ref
    logger.info("initialised successfully.") 


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
  
  
  def build_dropdown(self, 
                     target_options: list,
                     target_default: int,
                     event: Callable | None=None) -> QComboBox:
    #  setup
    combo = QComboBox()
    combo.addItems(target_options)
    combo.setCurrentIndex(target_default)
    #  udpate
    if event:
      combo.currentTextChanged.connect(event)
    return combo
    
    
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
    
    PRVIEW_ROW_MAX = 100
    
    #  validation
    if not isinstance(target_df, pd.DataFrame):
      err_msg = "Imported table is invalid."
      logger.error(err_msg, exc_info=True)
      raise ValueError(err_msg)
    #  Impactface
    table = QTableWidget()
    display_df = target_df.head(PRVIEW_ROW_MAX)
    rows, cols = display_df.shape
    table.setRowCount(rows)
    table.setColumnCount(cols)
    #  loop for filling
    
    #  table head for once setup, prevent repeated
    table.setHorizontalHeaderLabels([str(col) for col in display_df[:100].columns])
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
    for row in range(rows):
      for col in range(cols):
        #  cell val
        cell_val = str(display_df.iloc[row, col])
        tb_cell = QTableWidgetItem(cell_val)
        tb_cell.setTextAlignment(Qt.AlignCenter)
        #  table management
        #  leanrt: use sub-fn in horizontalHeader to manage
        table.setItem(row, col, QTableWidgetItem(tb_cell))
    table.setStyleSheet("border: 0.5px solid #333333")
    return table
  
  
  def build_popup_wd(self, 
                     wd_title:str,
                     target_df: pd.DataFrame,
                     popup_title:str="Untitled",
                     popup_content: Callable | None = None) -> QFrame:
    
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
    def add_content_box() -> QScrollArea:
      #  component
      diagram = popup_content
      #  frame
      frame = QScrollArea()
      frame_layout = QVBoxLayout()
      frame_layout.addWidget(diagram)
      frame.setLayout(frame_layout)
      return frame
    
    #  button sect
    def add_option_box(target_window: QDialog, 
                       target_df: pd.DataFrame, 
                       target_format: str) -> QFrame:
      #  components
      export_lb = self.build_label(lb_text="Export Format:",
                                   lb_txtcolor="white")
      export_ddlist = self.build_dropdown(target_options=[".csv", ".xml", ".json", ".png"],
                                          target_default=0)
      export_btn = self.build_btn(btn_text="Export", 
                                  #  Leanrt: .currentText() for getting drop list option
                                  btn_event=lambda: self.app.file_cont.export_preview(target_df=target_df,
                                                                                      target_format=export_ddlist.currentText()), 
                                  btn_bgcolor=THEME_COLOR["white"],
                                  btn_txtcolor=THEME_COLOR["primary"],
                                  btn_hover_bgcolor=THEME_COLOR["white_hvr"])
      box_confirm_btn = self.build_btn(btn_text="Back", 
                            btn_event=target_window.close,
                            btn_bgcolor=THEME_COLOR["primary"],
                            btn_txtcolor=THEME_COLOR["white"],
                            btn_hover_bgcolor=THEME_COLOR["primary_hvr"])
      #  grid frame
      box_export_grid = QFrame()
      grid_layout = QGridLayout()
      grid_layout.addWidget(export_lb, 0, 0)
      grid_layout.addWidget(export_ddlist, 0, 1, alignment=Qt.AlignLeft)
      grid_layout.addWidget(export_btn, 0, 2)
      grid_layout.addWidget(box_confirm_btn, 0, 3)
      export_lb.setMaximumWidth(100)
      export_ddlist.setMaximumWidth(100)
      
      grid_layout.setContentsMargins(8, 0, 8, 0)
      grid_layout.setSpacing(8)
      box_export_grid.setLayout(grid_layout)
      
      return box_export_grid
    
    #  frame
    window = QDialog()
    window.setWindowTitle(wd_title)
    #  learnt: setModal, prevent users manage main window simultanously
    window.setModal(True)
    window.setFixedSize(600, 600)
    #  setup components after window created
    p_title = add_title_box()
    p_content = add_content_box()
    p_opt = add_option_box(target_window=window,
                           target_df=target_df,
                           target_format=".csv")
    #  continue
    window_layout = QGridLayout()
    window_layout.addWidget(p_title, 1, 0)
    window_layout.addWidget(p_content, 2, 0)
    window_layout.addWidget(p_opt, 3, 0)
    window_layout.setRowStretch(1, 3)
    window_layout.setRowStretch(2, 21)
    window_layout.setRowStretch(3, 4)
    window_layout.setSpacing(0)
    window_layout.setContentsMargins(0, 0, 0, 0)
    window.setLayout(window_layout)
    window.exec()
    
    
  #  component box
  
  def browser_comp_box(self, 
                       lb_text: str="", 
                       path_txt: str="",
                       btn_text:str="",
                       btn_event: Callable | None =None) -> QFrame:
    #  components
    title_label = self.app.comp_fact.build_label(lb_text=lb_text,
                                                     lb_type="h3",
                                                     lb_txtcolor=THEME_COLOR["mid"],
                                                     lb_align=Qt.AlignVCenter | Qt.AlignLeft)
    path_label = self.app.comp_fact.build_label(lb_text=path_txt,
                                                    lb_type="p",
                                                    lb_txtcolor=THEME_COLOR["mid"],
                                                    lb_align=Qt.AlignVCenter | Qt.AlignLeft)
    search_btn = self.app.comp_fact.build_btn(btn_text=btn_text,
                                                  btn_event=btn_event,
                                                  btn_bgcolor=THEME_COLOR["white"],
                                                  btn_txtcolor=THEME_COLOR["primary"],
                                                  btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    #  update temp labels list
    if lb_text == DATASET_LIST[1]["data"]:
        self.app.pages_fact.temp_label_users = path_label
    elif lb_text == DATASET_LIST[2]["data"]:
        self.app.pages_fact.temp_label_activities = path_label
    elif lb_text == DATASET_LIST[3]["data"]:
        self.app.pages_fact.temp_label_components = path_label
    #  learnt: .clicked is the signal itself, further connect to the function
    search_btn.clicked.connect(lambda: self.app.file_cont.browse_files(target_key=lb_text, 
                                                                       lb_widget=path_label))
    #  path layer for spec styling
    p_frame = QFrame()
    p_frame_layout = QVBoxLayout()
    p_frame.setStyleSheet("""
        QFrame {
            background-color: "#dddddd";
            border-radius: 14px;
            padding: 0px 4px;
        }
    """)
    p_frame_layout.addWidget(path_label)
    p_frame.setFixedWidth(320)
    p_frame_layout.setContentsMargins(8, 0, 8, 0)
    p_frame_layout.setSpacing(8)
    p_frame.setLayout(p_frame_layout)
    #  overall layer
    frame = QFrame()
    frame_layout = QGridLayout()
    frame_layout.addWidget(title_label, 0, 0, 1, 2)
    frame_layout.addWidget(p_frame, 1, 0, alignment=Qt.AlignLeft)
    frame_layout.addWidget(search_btn, 1, 1, alignment=Qt.AlignCenter)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame_layout.setSpacing(0)
    frame.setLayout(frame_layout)
    return frame
  
  
  def preview_comp_box(self, 
                       lb_text: str="", 
                       btn_text:str="",
                       btn_event: Callable | None =None) -> QFrame:
    
  
    #  components
    preview_label = self.app.comp_fact.build_label(lb_text=lb_text,
                                                      lb_type="h3",
                                                      lb_txtcolor=THEME_COLOR["mid"],
                                                      lb_align=Qt.AlignVCenter | Qt.AlignCenter)
    preview_btn = self.app.comp_fact.build_btn(btn_text=btn_text,
                                                  btn_event=btn_event,
                                                  btn_bgcolor=THEME_COLOR["white"],
                                                  btn_txtcolor=THEME_COLOR["primary"],
                                                  btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    #  individual frame
    i_frame = QFrame()
    i_frame_layout = QVBoxLayout()
    i_frame_layout.addWidget(preview_label, alignment=Qt.AlignCenter)
    i_frame_layout.addWidget(preview_btn, alignment=Qt.AlignCenter)
    i_frame_layout.setContentsMargins(0, 0, 0, 0)
    i_frame_layout.setSpacing(0)
    i_frame.setLayout(i_frame_layout)
    return i_frame
  
  
  def build_radio_group(self, 
                        target_list: list,
                        target_event: Callable=None,
                        is_horizontal: bool=True):
    
    #  Learnt: QButtonGroup is also a logical object, still need an visual body
    container = QWidget()
    #  Learnt: will go to gabage if not add parent container
    group = QButtonGroup(container)
    if is_horizontal:
      group_layout = QHBoxLayout()
    else:
      group_layout = QVBoxLayout()
    
    for index, opt in enumerate(target_list):
      btn = QRadioButton(opt)
      group.addButton(btn, index)
      group_layout.addWidget(btn)
    
    #  Learnt: 2 options can be returned
    if target_event:
      group.buttonClicked.connect(lambda el: target_event(el.text(), el.isChecked()))
      
    group_layout.setSpacing(8)
    group_layout.setAlignment(Qt.AlignLeft)
    group_layout.setContentsMargins(0, 0, 0, 0) 
    container.setLayout(group_layout)
    
    return {"widget": container, "group": group}