from typing import Callable
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QVBoxLayout, QFrame,
    QFileDialog, QPushButton, QLabel
)
from models.config.paths import (PATH_DATA_USER, PATH_DATA_ACTIVITY, PATH_DATA_COMPONENT)
from ui.components.config.styles import (
    THEME_COLOR, style_content_panel_default, style_nav_sect_default,
)
from ui.components.config.events import (
    event_reset_app,event_next_btn,event_back_btn, browse_files
)
from ui.components.config.config import (
  DATASET_LIST
)
import pandas as pd



#  CLASS

class PagesFactory:
  
  #  Constructor
  
  def __init__(self, app_ref):
    super().__init__()
    #  setup ref states
    self.app_ref = app_ref 
    #  store temp paths
    self.temp_path_user: str = None
    self.temp_path_activity: str = None
    self.temp_path_comp: str = None
    #  store temp tables
    self.temp_table_user: pd.DataFrame = None
    self.temp_table_activity: pd.DataFrame = None
    self.temp_table_component: pd.DataFrame = None
    #  store temp labels (for reset)
    #  learnt: emb to render the state again, unlike declared variables
    self.temp_label_user: pd.DataFrame = None
    self.temp_label_activity: pd.DataFrame = None
    self.temp_label_component: pd.DataFrame = None
    

  #  LAYER 3  -  PAGES
  
  def create_page_1(self):
    #  status section
    inner_status_sect = self.create_status_sect(sect_title="Step 1: Import Datasets", 
                                                sect_des="This step reads the dataset, checks its structure, and prepares it for cleaning and processing.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=1)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_next=True)
    
    #  Work Panel Grid
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout = self.reuse_page_setting(inner_status_sect=inner_status_sect,
                                           inner_stat_sect=inner_stat_sect,
                                           inner_nav_sect=inner_nav_sect)
    outer.setLayout(outer_layout)
    return outer


  def create_page_2(self):
    #  status section
    inner_status_sect = self.create_status_sect(sect_title="Step 2: Clean Data and Preprocessing", 
                                                sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=2)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, enable_next=True)
    
    #  Work Panel Grid
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout = self.reuse_page_setting(inner_status_sect=inner_status_sect,
                                           inner_stat_sect=inner_stat_sect,
                                           inner_nav_sect=inner_nav_sect)
    outer.setStyleSheet(style_nav_sect_default)
    outer.setLayout(outer_layout)
    return outer


  def create_page_3(self):
    #  status section
    inner_status_sect = self.create_status_sect(sect_title="Step 3: Merge Tables", 
                                                sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=3)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, enable_next=True)
    
    #  Work Panel Grid
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout = self.reuse_page_setting(inner_status_sect=inner_status_sect,
                                           inner_stat_sect=inner_stat_sect,
                                           inner_nav_sect=inner_nav_sect)
    outer.setStyleSheet(style_nav_sect_default)
    outer.setLayout(outer_layout)
    return outer


  def create_page_4(self):
    #  status section
    inner_status_sect = self.create_status_sect(sect_title="Step 4: Analyse Data", 
                                                sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=4)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, enable_done=True)
    
    #  Work Panel Grid
    outer = QWidget()
    outer_layout = QGridLayout()
    outer_layout = self.reuse_page_setting(inner_status_sect=inner_status_sect,
                                           inner_stat_sect=inner_stat_sect,
                                           inner_nav_sect=inner_nav_sect)
    outer.setStyleSheet(style_nav_sect_default)
    outer.setLayout(outer_layout)
    return outer
  
  
  
   #  LAYER 3  -  SECTIONS
  
  def create_status_sect(self, 
                         sect_title:str="Insert Title",
                         sect_des:str="Insert Description") -> QWidget:

     # inner - title
    title = self.app_ref.comp_fact.build_label(lb_text=sect_title, 
                                                lb_type="h2", 
                                                lb_align=Qt.AlignVCenter | Qt.AlignLeft,
                                                lb_bold=True)
    title.setFixedHeight(32)
    
    # inner - item list
    description = self.app_ref.comp_fact.build_label(lb_text=sect_des, 
                                                    lb_txtcolor=THEME_COLOR["mid"],
                                                    lb_type="h3", 
                                                    lb_align=Qt.AlignLeft, 
                                                    lb_wrap=True)  
    # outer
    status_sect = QWidget()
    status_sect_layout  = QVBoxLayout()
    status_sect_layout.addWidget(title)
    status_sect_layout.addWidget(description)
    status_sect_layout.setContentsMargins(0, 0, 0, 0)
    status_sect_layout.setSpacing(0)
    status_sect.setLayout(status_sect_layout)
    return status_sect
  

  def create_stat_sect(self, target_page: int) -> QWidget | None:
      if target_page == 1:
          return self.core_sect_import_dataset()
      elif target_page == 2:
          return self.core_sect_clean_data()
      elif target_page == 3:
          return self.core_sect_merge_tables()
      elif target_page == 4:
          return self.core_sect_analyse_data()
      return None

    
  def create_nav_sect(self, 
                      enable_back: bool = False,
                      enable_next: bool = False,
                      enable_done: bool = False) -> QWidget:
    #  inner
    #  leanrt: lambda: enable importing parameters to fn
    btn_back = self.app_ref.comp_fact.build_btn(btn_text="back",
                                                btn_event=lambda: event_back_btn(self.app_ref),
                                                btn_bgcolor=THEME_COLOR["white"],
                                                btn_txtcolor=THEME_COLOR["primary"],
                                                btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    btn_next = self.app_ref.comp_fact.build_btn(btn_text="Next", 
                                                btn_event=lambda: event_next_btn(self.app_ref),
                                                btn_bgcolor=THEME_COLOR["primary"],
                                                btn_txtcolor=THEME_COLOR["white"],
                                                btn_hover_bgcolor=THEME_COLOR["primary_hvr"])
    btn_completed = self.app_ref.comp_fact.build_btn(btn_text="Done",
                                                      btn_event=lambda: event_reset_app(self.app_ref), 
                                                      btn_bgcolor=THEME_COLOR["primary"],
                                                      btn_txtcolor=THEME_COLOR["white"],
                                                      btn_hover_bgcolor=THEME_COLOR["primary_hvr"])
    #  outer
    nav = QWidget()
    nav_layout = QHBoxLayout()
    
    if enable_back:
      nav_layout.addWidget(btn_back)
    if enable_next:
      nav_layout.addWidget(btn_next)
    if enable_done:
      nav_layout.addWidget(btn_completed)
      
    nav_layout.setContentsMargins(4, 4, 4, 4)
    nav_layout.setAlignment(Qt.AlignRight)
    nav.setStyleSheet(style_nav_sect_default)
    nav.setLayout(nav_layout)
    return nav
  
   
   
  #  SUB-SECTIONS (PAGE 1)
  
  def create_browser_container(self) -> QWidget:
      container_title = self.app_ref.comp_fact.build_label(lb_text="A.  Browse Files",
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
    title_label = self.app_ref.comp_fact.build_label(lb_text="B. Preview Datasets",
                                                  lb_type="h3",
                                                  lb_txtcolor=THEME_COLOR["primary"],
                                                  lb_align=Qt.AlignVCenter | Qt.AlignLeft)
    #   group frame
    user_box= self.preview_comp_box(lb_text=DATASET_LIST[1]["data"], 
                                    btn_text="Preview",
                                    btn_event=lambda: self.event_preview_dataset(target_key=DATASET_LIST[1]["data"]))
    comp_box = self.preview_comp_box(lb_text=DATASET_LIST[2]["data"], 
                                        btn_text="Preview",
                                        btn_event=lambda: self.event_preview_dataset(target_key=DATASET_LIST[2]["data"]))
    activity_box = self.preview_comp_box(lb_text=DATASET_LIST[3]["data"], 
                                      btn_text="Preview",
                                      btn_event=lambda: self.event_preview_dataset(target_key=DATASET_LIST[3]["data"]))
    title_label.setFixedHeight(24)
    #  inner grid
    frame = QFrame()
    frame_layout = QGridLayout(frame)
    frame_layout.addWidget(title_label, 0, 0, 1, 3)
    frame_layout.addWidget(user_box, 1, 0)
    frame_layout.addWidget(comp_box, 1, 2)
    frame_layout.addWidget(activity_box, 1, 1)
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
    title_label = self.app_ref.comp_fact.build_label(lb_text="C. Import Datasets",
                                                  lb_type="h3",
                                                  lb_txtcolor=THEME_COLOR["primary"],
                                                  lb_align=Qt.AlignVCenter | Qt.AlignLeft)
    
    import_btn = self.app_ref.comp_fact.build_btn(btn_text="Import",
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
  
  
  
  #  SUB-SECTIONS (PAGE 4)
  
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
  
  
  def core_sect_clean_data(self) -> QWidget:
    #  outer
    core_sect = QWidget()
    core_sect_layout = QVBoxLayout()
    # .....
    core_sect.setLayout(core_sect_layout)
    return core_sect
    
    
  def core_sect_merge_tables(self) -> QWidget:
    
    #  outer
    core_sect = QWidget()
    core_sect_layout = QVBoxLayout()
    # .....
    core_sect.setLayout(core_sect_layout)
    return core_sect
    
    
  def core_sect_analyse_data(self) -> QWidget:
    
    #  outer
    core_sect = QWidget()
    core_sect_layout = QVBoxLayout()
    # .....
    core_sect.setLayout(core_sect_layout)
    core_sect_layout.addStretch(0)
    core_sect_layout.setContentsMargins(0, 0, 0, 0)
    core_sect_layout.setSpacing(4)
    return core_sect
    
    
    
  #  MINOR COMPONENTS
  
  def browser_comp_box(self, 
                       lb_text: str="", 
                       path_txt: str="",
                       btn_text:str="",
                       btn_event: Callable | None =None) -> QFrame:
    #  components
    title_label = self.app_ref.comp_fact.build_label(lb_text=lb_text,
                                                     lb_type="h3",
                                                     lb_txtcolor=THEME_COLOR["mid"],
                                                     lb_align=Qt.AlignVCenter | Qt.AlignLeft)
    path_label = self.app_ref.comp_fact.build_label(lb_text=path_txt,
                                                    lb_type="p",
                                                    lb_txtcolor=THEME_COLOR["mid"],
                                                    lb_align=Qt.AlignVCenter | Qt.AlignLeft)
    search_btn = self.app_ref.comp_fact.build_btn(btn_text=btn_text,
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
    search_btn.clicked.connect(lambda: browse_files(app_ref=self.app_ref, 
                                                    target=lb_text, 
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
    preview_label = self.app_ref.comp_fact.build_label(lb_text=lb_text,
                                                      lb_type="h3",
                                                      lb_txtcolor=THEME_COLOR["mid"],
                                                      lb_align=Qt.AlignVCenter | Qt.AlignCenter)
    preview_btn = self.app_ref.comp_fact.build_btn(btn_text=btn_text,
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
                       btn_text:str="",
                       btn_event: Callable | None =None) -> QFrame:
      #  components
    preview_label = self.app_ref.comp_fact.build_label(lb_text=lb_text,
                                                      lb_type="h3",
                                                      lb_txtcolor=THEME_COLOR["mid"],
                                                      lb_align=Qt.AlignVCenter | Qt.AlignCenter)
    preview_btn = self.app_ref.comp_fact.build_btn(btn_text=btn_text,
                                                  btn_event=btn_event,
                                                  btn_bgcolor=THEME_COLOR["white"],
                                                  btn_txtcolor=THEME_COLOR["primary"],
                                                  btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    #  avtivate btn event
    preview_btn.clicked.connect(lambda: self.event_preview_dataset(target_dataset=path_txt))
    #  individual frame
    i_frame = QFrame()
    i_frame_layout = QVBoxLayout()
    i_frame_layout.addWidget(preview_label, alignment=Qt.AlignCenter)
    i_frame_layout.addWidget(preview_btn, alignment=Qt.AlignCenter)
    i_frame_layout.setContentsMargins(0, 8, 0, 0)
    i_frame_layout.setSpacing(0)
    i_frame.setLayout(i_frame_layout)
    return i_frame


  def reuse_page_setting(self,
                        inner_status_sect: QWidget,
                        inner_stat_sect: QWidget,
                        inner_nav_sect: QWidget) -> QGridLayout:
      layout = QGridLayout()
      layout.addWidget(inner_status_sect, 0, 0)
      layout.addWidget(inner_stat_sect, 1, 0)
      layout.addWidget(inner_nav_sect, 2, 0)
      layout.setRowStretch(0, 2)
      layout.setRowStretch(1, 8)
      layout.setRowStretch(2, 1)
      layout.setContentsMargins(24, 16, 24, 24)
      layout.setSpacing(12)
      return layout