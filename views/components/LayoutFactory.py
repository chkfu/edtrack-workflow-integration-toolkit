from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QStackedWidget, QGridLayout,QListWidget, QFrame, QHBoxLayout, QWidget,
    QVBoxLayout, QListWidgetItem
)
from PyQt5.QtGui import QFont
from views.components.config.views_styles import (
  THEME_COLOR, style_wd_default, style_topbar_default, style_wd_default_2, 
  style_sidebar_box_default)
from views.components.config.views_config import STEP_NAME_LIST, DATASET_LIST
import logging


#  LOGGER

logger = logging.getLogger("LAYOUT_FACTORY")


#  CLASS

class LayoutFactory:
  
  #  Constructor    
  
  def __init__(self, app_ref):
    
    super().__init__()
    
    #  setup ref states
    self.app = app_ref  
    self.comp_fact = self.app.comp_fact
    self.pages_fact = self.app.pages_fact
    
    #  setup page stack
    self.page_stack = QStackedWidget()
    self.page_1 = self.app.pages_fact.page_import.merge_sections()
    self.page_2 = self.app.pages_fact.page_clean.merge_sections()
    self.page_3 = self.app.pages_fact.page_merge.merge_sections()
    self.page_4 = self.app.pages_fact.page_feateng.merge_sections()
    self.page_5 = self.app.pages_fact.page_analyse.merge_sections()

    #  setup visualise list stack - widget based
    self.task_list_widget = None
    self.dataset_list_widget = None
    
    #  initialised instructions
    self.page_stack.addWidget(self.page_1)
    self.page_stack.addWidget(self.page_2)
    self.page_stack.addWidget(self.page_3)
    self.page_stack.addWidget(self.page_4)
    self.page_stack.addWidget(self.page_5)
    
    
    #  learnt: to get total num, use stack.count()
    self.page_stack.setCurrentIndex(0)

    logger.info("initialised successfully.") 
    
    
    #  LAYER 3 -  SIDEBAR

  def create_task_sect(self) -> QWidget:
    #  sections
    sect_top = self.comp_fact.build_sidebar_listItem(lb_text="Work Flow",
                                                     is_listTop=True)
    
    #  set the widget in constructor - for dynamic update
    self.task_list_widget = QListWidget()
    #  update the list item into list
    for item in STEP_NAME_LIST:
      txt = f"🟢 {item["step"]}" if item["visited"] else f"🔴 {item["step"]}"
      list_item = QListWidgetItem()
      #  learnt: qlist is only for data storage, still need label for visualise
      new_lb_widget = self.comp_fact.build_sidebar_listItem(is_listTop=False, lb_text=txt)
      #  learnt: instruct the virtual list item now follow the label item
      list_item.setSizeHint(new_lb_widget.sizeHint())
      self.task_list_widget.addItem(list_item)
      self.task_list_widget.setItemWidget(list_item, new_lb_widget)
    #  outer frame
    task_sect = QWidget()
    task_sect_layout = QVBoxLayout()
    task_sect_layout.addWidget(sect_top, alignment=Qt.AlignTop)
    task_sect_layout.addWidget(self.task_list_widget)
    task_sect_layout.setSpacing(0)
    task_sect.setLayout(task_sect_layout)
    task_sect.setStyleSheet(style_sidebar_box_default)
    return task_sect 


  def create_db_sect(self) -> QWidget:
      #  title label
      sect_top = self.comp_fact.build_sidebar_listItem(lb_text="Dataset Status", is_listTop=True)
      self.dataset_list_widget = QListWidget()
      #  list items
      for data in DATASET_LIST:
          txt = f"🟢 {data['data']}" if data["status"] else f" 🔴{data['data']}"
          list_item = QListWidgetItem()
          new_lb_widget = self.comp_fact.build_sidebar_listItem(is_listTop=False, lb_text=txt)
          #  learnt: sync the label and listitem widget
          list_item.setSizeHint(new_lb_widget.sizeHint())
          #  learnt: self.list_widget is a list to contain the new list items
          self.dataset_list_widget.addItem(list_item)
          #  learnt: also need to add the labels back to the list with setitemwidget
          self.dataset_list_widget.setItemWidget(list_item, new_lb_widget)

      db_sect = QWidget()
      layout = QVBoxLayout()
      layout.addWidget(sect_top, alignment=Qt.AlignTop)
      layout.addWidget(self.dataset_list_widget)
      layout.setSpacing(0)
      db_sect.setLayout(layout)
      db_sect.setStyleSheet(style_sidebar_box_default)
      return db_sect  


  #  LAYER 2  -  MAIN COMPONENTS 
  def create_topbar(self) -> QFrame:
    
    #  inner frame - left
    
    label_title = self.comp_fact.build_label(lb_text=style_wd_default["title"],
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
    btn_reset = self.comp_fact.build_btn(btn_text="reset",
                              btn_event=lambda: self.app.app_cont.reset_app(),
                              btn_bgcolor=THEME_COLOR["yellow"],
                              btn_txtcolor=THEME_COLOR["dark"],
                              btn_hover_bgcolor=THEME_COLOR["yellow_hvr"])
    btn_exit = self.comp_fact.build_btn(btn_text="exit", 
                              btn_event=lambda: self.app.app_cont.close_app(),
                              btn_bgcolor=THEME_COLOR["red"],
                              btn_txtcolor=THEME_COLOR["dark"],
                              btn_hover_bgcolor=THEME_COLOR["red_hvr"])
    
    inner_rframe = QFrame()
    inner_rframe_layout = QHBoxLayout()
    inner_rframe_layout.addWidget(btn_reset)
    inner_rframe_layout.addWidget(btn_exit)
    inner_rframe.setLayout(inner_rframe_layout)
    
    #  outer frame
    #  learnt:  widget -> layout -> widget -> layout ....
    topbar = QFrame()
    topbar_layout = QGridLayout()
    topbar_layout.addWidget(inner_lframe, 0, 0)
    topbar_layout.addWidget(inner_rframe, 0, 1)
    topbar_layout.setColumnStretch(0, 5)
    topbar_layout.setColumnStretch(1, 2)
    topbar_layout.setContentsMargins(0, 0, 0, 0)
    topbar.setStyleSheet(style_topbar_default)
    topbar.setLayout(topbar_layout)
    
    return topbar
  
  
  def create_sidebar(self) -> QWidget:
    #  inner
    task_sect = self.create_task_sect()
    db_sect = self.create_db_sect()
    #  outer
    sidebar = QWidget()
    sidebar_layout = QGridLayout()
    sidebar_layout.addWidget(task_sect, 0, 0)
    sidebar_layout.addWidget(db_sect, 1, 0)
    sidebar_layout.setRowStretch(0, 4)
    sidebar_layout.setRowStretch(1, 5)
    sidebar_layout.setContentsMargins(0, 0, 0, 0)
    sidebar_layout.setSpacing(0)
    sidebar.setLayout(sidebar_layout)
    return sidebar


  #  *** Remarks: Content Panel => self.page_stack



  #  LAYER 1  -  WINDOW
    
  def create_window(self) -> QWidget:
    
    #  from window 
    window = QWidget()
    window_layout = QGridLayout()
    
    #  add child components
    widget_topbar = self.create_topbar()
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
    
    