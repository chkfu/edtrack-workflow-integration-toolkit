from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QVBoxLayout, QFrame
)
from views.components.config.views_styles import THEME_COLOR, style_nav_sect_default
from views.components.config.views_config import DATASET_LIST



#  CLASS

class PageTemplate:
  
  #  CONSTRUCTOR
  def __init__(self, app_ref):
    self.app = app_ref
    print("[PageTemplate] initialised successfully.")
    
    
  #  METHODS
  
  def merge_section(self) -> None:
    pass
    
      
  def create_title_sect(self, 
                         sect_title:str="Insert Title",
                         sect_des:str="Insert Description") -> QWidget:

     # inner - title
    title = self.app.comp_fact.build_label(lb_text=sect_title, 
                                                lb_type="h2", 
                                                lb_align=Qt.AlignVCenter | Qt.AlignLeft,
                                                lb_bold=True)
    title.setFixedHeight(32)
    
    # inner - item list
    description = self.app.comp_fact.build_label(lb_text=sect_des, 
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
  
    
  def create_nav_sect(self, 
                      enable_back: bool = False,
                      enable_next: bool = False,
                      enable_done: bool = False) -> QWidget:
    #  inner
    #  leanrt: lambda: enable importing parameters to fn
    btn_back = self.app.comp_fact.build_btn(btn_text="back",
                                                btn_event=lambda: self.app.nav_cont.back_btn(),
                                                btn_bgcolor=THEME_COLOR["white"],
                                                btn_txtcolor=THEME_COLOR["primary"],
                                                btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    btn_next = self.app.comp_fact.build_btn(btn_text="Next", 
                                                btn_event=lambda: self.app.nav_cont.next_btn(),
                                                btn_bgcolor=THEME_COLOR["primary"],
                                                btn_txtcolor=THEME_COLOR["white"],
                                                btn_hover_bgcolor=THEME_COLOR["primary_hvr"])
    btn_completed = self.app.comp_fact.build_btn(btn_text="Done",
                                                btn_event=lambda: self.app.app_cont.reset_app(), 
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
  
  
  def reuse_page_setting(self,
                        inner_title_sect: QWidget,
                        inner_stat_sect: QWidget,
                        inner_nav_sect: QWidget) -> QGridLayout:
      layout = QGridLayout()
      layout.addWidget(inner_title_sect, 0, 0)
      layout.addWidget(inner_stat_sect, 1, 0)
      layout.addWidget(inner_nav_sect, 2, 0)
      layout.setRowStretch(0, 2)
      layout.setRowStretch(1, 8)
      layout.setRowStretch(2, 1)
      layout.setContentsMargins(24, 16, 24, 24)
      layout.setSpacing(12)
      return layout
  
  
  def page_refresh(self):
    pass