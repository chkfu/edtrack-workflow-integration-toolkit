import pandas as pd
import logging
from typing import Callable
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
  QLabel, QPushButton, QMessageBox, QDialog, QVBoxLayout, QFrame, QHBoxLayout, 
  QGridLayout, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView, 
  QComboBox, QWidget, QButtonGroup, QRadioButton, QCheckBox
)
from views.components.config.views_styles import (
    THEME_COLOR, style_btn_default, style_btn_contrast, style_lb_default, 
    style_sidebar_listItem_default, style_table_view_border, style_popup_title_box
)


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
    combo.setCursor(Qt.PointingHandCursor)
    combo.setCurrentIndex(target_default)
    combo.setFixedHeight(28)
    #  udpate
    if event:
      combo.currentTextChanged.connect(event)
    return combo
  
  
  def refresh_dropdowns(self, target_dd: QComboBox, target_event: Callable | None=None):
    #  Learnt: store the popup funciton first
    dd_popup = target_dd.showPopup
    def updated_popup_callback():
      #  Learnt: get the up-to-date list
      opts: list = target_event()
      #  Learnt: clear original and update new options
      target_dd.blockSignals(True)
      target_dd.clear()
      target_dd.addItems(opts)
      target_dd.setCurrentIndex(0)
      target_dd.blockSignals(False)
      #  Learnt: run the popup function for execution
      dd_popup()
    #  Leanrt: replace the prev popup function
    target_dd.showPopup = updated_popup_callback
    
  
  def build_checkbox(self,
                     target_name: str="Untitled",
                     target_event: Callable | None=None) -> QCheckBox:
    checkbox = QCheckBox(str(target_name))
    checkbox.setChecked(False)
    checkbox.setCursor(Qt.PointingHandCursor)
    if target_event:
        checkbox.stateChanged.connect(
          lambda state, name=target_name: target_event(target_state=state,
                                           target_name=name))
    return checkbox
    

    
    
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
                       target_df: pd.DataFrame) -> QTableWidget:
    
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
    table.setStyleSheet(style_table_view_border)
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
      content_title.setStyleSheet(style_popup_title_box)
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
      export_lb.setMaximumWidth(240)
      export_ddlist.setMaximumWidth(240)
      
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
  
  def preview_comp_box(self, 
                       lb_text: str | None, 
                       btn_text:str | None,
                       btn_event: Callable | None =None) -> QFrame:
    
    #  setup frame
    i_frame = QFrame()
    i_frame_layout = QVBoxLayout()
    #  components
    if lb_text is not None and lb_text.strip() != "": 
      preview_label = self.app.comp_fact.build_label(lb_text=lb_text,
                                                        lb_type="h3",
                                                        lb_txtcolor=THEME_COLOR["mid"],
                                                        lb_align=Qt.AlignVCenter | Qt.AlignCenter)
      i_frame_layout.addWidget(preview_label, alignment=Qt.AlignCenter)
    preview_btn = self.app.comp_fact.build_btn(btn_text=btn_text,
                                                  btn_event=btn_event,
                                                  btn_bgcolor=THEME_COLOR["white"],
                                                  btn_txtcolor=THEME_COLOR["primary"],
                                                  btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    i_frame_layout.addWidget(preview_btn, alignment=Qt.AlignCenter)
    #  complete frame
    i_frame_layout.setContentsMargins(0, 0, 0, 0)
    i_frame_layout.setSpacing(4)
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

    btn_storage = []
    for index, opt in enumerate(target_list):
      btn = QRadioButton(opt)
      btn.setCursor(Qt.PointingHandCursor)
      group.addButton(btn, index)
      group_layout.addWidget(btn)
      btn_storage.append(btn)
      
    #  Learnt: 2 options can be returned
    if target_event:
      group.buttonClicked.connect(lambda el: target_event(el.text(), el.isChecked()))
    group_layout.setSpacing(8)
    group_layout.setAlignment(Qt.AlignLeft)
    group_layout.setContentsMargins(0, 0, 0, 0) 
    container.setLayout(group_layout)
    return {"widget": container, "group": group, "buttons": btn_storage}
  
  
  
  def build_reused_opt_container(self, 
                         target_title: str,
                         target_config: list) -> QWidget:
    #  setup container
    content = QWidget()
    content_layout = QVBoxLayout()
    #  components
    container_title = self.build_label(lb_text=target_title,
                                                      lb_type="h3",
                                                      lb_align=Qt.AlignLeft)
    content_layout.addWidget(container_title)
    for config in target_config:
      opt_box = self.build_reused_opt_box(target_title=config["title"],
                                          target_optlist=config["options"],
                                          target_func=config["function"]) 
      content_layout.addWidget(opt_box, alignment=Qt.AlignTop | Qt.AlignLeft)
    #  complete container
    content_layout.setAlignment(Qt.AlignTop) 
    content_layout.setSpacing(8)
    content_layout.setContentsMargins(0, 0, 0, 0) 
    content.setLayout(content_layout)
    return content
  
  
  def build_reused_opt_box(self, 
                           target_title: str,
                           target_optlist: list,
                           target_func: Callable | None) -> QWidget:
    
    title_lb = self.app.comp_fact.build_label(lb_text=target_title,
                                              lb_type="h3",
                                              lb_txtcolor=THEME_COLOR["mid"])  
    opt_box = self.app.comp_fact.build_radio_group(target_list=target_optlist,
                                                   target_event=target_func,
                                                   is_horizontal=False)["widget"]
    # frame
    box = QFrame()
    box_layout = QVBoxLayout()
    box_layout.addWidget(title_lb, alignment=Qt.AlignTop | Qt.AlignLeft)
    box_layout.addWidget(opt_box, alignment=Qt.AlignTop | Qt.AlignLeft)
    box_layout.setContentsMargins(0, 0, 0, 0)
    box_layout.setSpacing(4)
    box.setLayout(box_layout)
    return box
  
  
  def build_reused_single_btn_box(self,
                                  target_title: str,
                                  target_statement: str,
                                  target_btn_text: str,
                                  target_btn_event: Callable) -> QFrame:
    title_lb = self.app.comp_fact.build_label(lb_text=target_title,
                                              lb_type="h3",
                                              lb_align=Qt.AlignLeft,
                                              lb_bold=True)
    #  frame
    reset_box = self.app.comp_fact.preview_comp_box(lb_text=target_statement, 
                                                    btn_text=target_btn_text,
                                                    btn_event=target_btn_event)
    
    #  frame
    frame = QFrame()
    frame_layout = QVBoxLayout()
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(reset_box)
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
    frame_layout.setContentsMargins(0, 0, 0, 0) 
    frame.setLayout(frame_layout)
    return frame
  
  