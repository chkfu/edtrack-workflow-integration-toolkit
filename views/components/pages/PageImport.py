from typing import Callable
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QVBoxLayout, QFrame
)
from views.components.config.views_styles import THEME_COLOR
from views.components.config.views_config import DATASET_LIST
from views.components.pages.PageTemplate import PageTemplate
import logging


#  LOGGING

logger = logging.getLogger("APPLICATION")


#  CLASS


class PageImport(PageTemplate):
  
  #  CONSTRUCTOR
  def __init__(self, app_ref):
    super().__init__(app_ref)
    logger.info("[PageImport] initialised successfully.")
    
    
  #  METHODS
  def merge_sections(self):
    #  title section
    inner_title_sect = self.create_title_sect(sect_title="Step 1: Import Datasets", 
                                                sect_des="This step reads the dataset, checks its structure, and prepares it for cleaning and processing.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=1)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_next=True)
    
    #  Work Panel Grid
    page = QWidget()
    page_layout = self.reuse_page_setting(inner_title_sect=inner_title_sect,
                                           inner_stat_sect=inner_stat_sect,
                                           inner_nav_sect=inner_nav_sect)
    page.setLayout(page_layout)
    return page
  
  
  def create_browser_container(self) -> QWidget:
      container_title = self.app.comp_fact.build_label(lb_text="A.  Browse Files",
                                                           lb_type="h3",
                                                           lb_align=Qt.AlignLeft)
      user_broswer = self.browser_comp_box(lb_text=DATASET_LIST[1]["data"], 
                                          path_txt="",
                                          btn_text="Search",
                                          btn_event=None)
      comp_broswer = self.browser_comp_box(lb_text=DATASET_LIST[2]["data"], 
                                            path_txt="",
                                            btn_text="Search",
                                            btn_event=None)
      activity_broswer = self.browser_comp_box(lb_text=DATASET_LIST[3]["data"], 
                                              path_txt="",
                                              btn_text="Search",
                                              btn_event=None)
      #  scope: container
      content = QWidget()
      content_layout = QVBoxLayout()
      content_layout.addWidget(container_title)
      content_layout.addWidget(user_broswer)
      content_layout.addWidget(comp_broswer)
      content_layout.addWidget(activity_broswer)
      content_layout.setAlignment(Qt.AlignTop) 
      content_layout.setSpacing(4)
      content_layout.setContentsMargins(0, 8, 0, 0) 
      content.setLayout(content_layout)
      return content
    
    
  def create_preview_container(self) -> QFrame:
    title_label = self.app.comp_fact.build_label(lb_text="B. Preview Datasets",
                                                  lb_type="h3",
                                                  lb_txtcolor=THEME_COLOR["primary"],
                                                  lb_align=Qt.AlignVCenter | Qt.AlignLeft)
    #   group frame
    user_box= self.preview_comp_box(lb_text=DATASET_LIST[1]["data"], 
                                    btn_text="Preview",
                                    btn_event=lambda: self.app.file_cont.preview_dataset(target_key=DATASET_LIST[1]["data"]))
    comp_box = self.preview_comp_box(lb_text=DATASET_LIST[2]["data"], 
                                        btn_text="Preview",
                                        btn_event=lambda: self.app.file_cont.preview_dataset(target_key=DATASET_LIST[2]["data"]))
    activity_box = self.preview_comp_box(lb_text=DATASET_LIST[3]["data"], 
                                      btn_text="Preview",
                                      btn_event=lambda: self.app.file_cont.preview_dataset(target_key=DATASET_LIST[3]["data"]))
    title_label.setFixedHeight(24)
    #  inner grid
    frame = QFrame()
    frame_layout = QGridLayout(frame)
    frame_layout.addWidget(title_label, 0, 0, 1, 3)
    frame_layout.addWidget(user_box, 1, 0)
    frame_layout.addWidget(comp_box, 1, 1)
    frame_layout.addWidget(activity_box, 1, 2)
    frame_layout.setColumnStretch(0, 1)
    frame_layout.setColumnStretch(1, 1)
    frame_layout.setColumnStretch(2, 1)
    frame_layout.setRowStretch(0, 0)
    frame_layout.setRowStretch(1, 0)
    frame_layout.setContentsMargins(0, 16, 0, 0)
    frame_layout.setSpacing(8)
    return frame

  
  def create_import_container(self,
                              btn_text:str="",
                              btn_event: Callable | None =None) -> QFrame:
    title_label = self.app.comp_fact.build_label(lb_text="C. Import Datasets",
                                                  lb_type="h3",
                                                  lb_txtcolor=THEME_COLOR["primary"],
                                                  lb_align=Qt.AlignVCenter | Qt.AlignLeft)
    
    import_btn = self.app.comp_fact.build_btn(btn_text="Import",
                                                  btn_event=btn_event,
                                                  btn_bgcolor=THEME_COLOR["white"],
                                                  btn_txtcolor=THEME_COLOR["primary"],
                                                  btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    #   group frame
    title_label.setFixedHeight(24)
    #  inner
    i_frame = QFrame()
    i_frame_layout = QVBoxLayout()
    i_frame_layout.addWidget(import_btn, alignment=Qt.AlignVCenter | Qt.AlignLeft)
    i_frame_layout.setSpacing(0)
    i_frame_layout.setContentsMargins(24, 0, 0, 0)
    i_frame.setLayout(i_frame_layout)
    #  outer
    frame = QFrame()
    frame_layout = QVBoxLayout(frame)
    frame_layout.addWidget(title_label)
    frame_layout.addWidget(i_frame)
    frame_layout.setContentsMargins(0, 16, 0, 0)
    frame_layout.setSpacing(8)
    return frame
  
  
  def core_sect_import_dataset(self) -> QWidget:
    #  scope: core seciton
    browser_container = self.create_browser_container()
    preview_container = self.create_preview_container()
    import_container = self.create_import_container()
    #  outer
    core_sect = QWidget()
    core_sect_layout = QVBoxLayout()
    core_sect_layout.addWidget(browser_container, alignment=Qt.AlignTop)
    core_sect_layout.addWidget(preview_container, alignment=Qt.AlignTop)
    core_sect_layout.addWidget(import_container, alignment=Qt.AlignTop)
    core_sect_layout.setSpacing(4)
    core_sect_layout.setContentsMargins(0, 0, 0, 0)
    core_sect.setLayout(core_sect_layout)
    return core_sect
  
  
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
        self.temp_label_user = path_label
    elif lb_text == DATASET_LIST[2]["data"]:
        self.temp_label_comp = path_label
    elif lb_text == DATASET_LIST[3]["data"]:
        self.temp_label_activity = path_label
    #  learnt: .clicked is the signal itself, further connect to the function
    search_btn.clicked.connect(lambda: self.app.file_cont.browse_files(target=lb_text, 
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
  
  
  def import_comp_box(self, 
                       lb_text: str="", 
                       path_txt: str="",
                       btn_text:str="") -> QFrame:
      #  components
    preview_label = self.app.comp_fact.build_label(lb_text=lb_text,
                                                  lb_type="h3",
                                                  lb_txtcolor=THEME_COLOR["mid"],
                                                  lb_align=Qt.AlignVCenter | Qt.AlignCenter)
    preview_btn = self.app.comp_fact.build_btn(btn_text=btn_text,
                                                  btn_event="None",
                                                  btn_bgcolor=THEME_COLOR["white"],
                                                  btn_txtcolor=THEME_COLOR["primary"],
                                                  btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    #  avtivate btn event
    preview_btn.clicked.connect(lambda: self.app.file_cont.preview_dataset(target_dataset=path_txt))
    #  individual frame
    i_frame = QFrame()
    i_frame_layout = QVBoxLayout()
    i_frame_layout.addWidget(preview_label, alignment=Qt.AlignCenter)
    i_frame_layout.addWidget(preview_btn, alignment=Qt.AlignCenter)
    i_frame_layout.setContentsMargins(0, 8, 0, 0)
    i_frame_layout.setSpacing(0)
    i_frame.setLayout(i_frame_layout)
    return i_frame