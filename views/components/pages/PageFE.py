from PyQt5.QtWidgets import (
  QFrame, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from views.components.pages.PageTemplate import PageTemplate
from views.components.config.views_styles import style_tab_scroll
from views.components.config.views_styles import THEME_COLOR
import logging


#  LOGGING

logger = logging.getLogger("PAGE_FEATENG")


#  CLASS

class PageFE(PageTemplate):
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    super().__init__(app_ref)
    logger.info("initialised successfully.")
    
    
  #  METHODS -  MAIN
  
  def merge_sections(self) -> QWidget:
    #  title section
    inner_title_sect = self.create_title_sect(sect_title="Step 4: Feature Engineering", 
                                              sect_des="This step enhances the dataset by creating or transforming features, helping prepare the data for deeper analysis.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=4)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True,
                                          enable_next=True)
    #  Work Panel Grid
    page = QWidget()
    page_layout = self.reuse_page_setting(inner_title_sect=inner_title_sect,
                                          inner_stat_sect=inner_stat_sect,
                                          inner_nav_sect=inner_nav_sect)
    page.setLayout(page_layout)
    return page
  

  def core_sect_feateng(self) -> QFrame:
    #  components
    action_panel = self.build_action_container()
    dataset_panel = self.build_dataset_container()
    #  frame
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)

    container = QWidget()
    layout = QHBoxLayout(container)
    layout.addWidget(action_panel, alignment=Qt.AlignTop | Qt.AlignCenter)
    layout.addWidget(dataset_panel, alignment=Qt.AlignTop | Qt.AlignCenter)
    layout.setSpacing(24)
    layout.setContentsMargins(0, 0, 0, 0)
    scroll.setStyleSheet(style_tab_scroll)
    scroll.setWidget(container)
    return scroll
  
  
  
  def build_action_container(self) -> QFrame:
    #  declatation
    FE_CONFIG: list = [
        {
          "title": "Remove Columns ",
          "event": lambda text, checked: self.app.fe_cont.handle_remove_cols()
        },
        {
          "title": "Rename Columns",
          "event": lambda text, checked: self.app.fe_cont.handle_rename_cols()
        },
        {
          "title": "Filter Rows",
          "event": lambda text, checked: self.app.fe_cont.handle_filter_rows()
        },
        {
          "title": "Time Features",
          "event": lambda text, checked: self.app.fe_cont.handle_time_feat()
        },
        {
          "title": "Encode / Hash",
          "event": lambda text, checked: self.app.fe_cont.handle_encoding()
        }
      ]
    # frame setup
    container = QWidget()
    layout = QVBoxLayout()
    #  build label
    title_lb = self.app.comp_fact.build_label(lb_text="A. Action Panel",
                                              lb_type="h3",
                                              lb_txtcolor=THEME_COLOR["primary"])
    layout.addWidget(title_lb)
    #  build buttons
    for obj in FE_CONFIG:
      btn = self.app.comp_fact.build_btn(btn_text=obj["title"],
                                         btn_event=obj["event"],
                                         btn_bgcolor=THEME_COLOR["white"],
                                         btn_txtcolor=THEME_COLOR["primary"],
                                         btn_hover_bgcolor=THEME_COLOR["white_hvr"],
                                         btn_size="long")
      layout.addWidget(btn, alignment=Qt.AlignCenter)
    #  frame display
    layout.setSpacing(12)
    layout.setContentsMargins(8, 8, 8, 8)
    container.setLayout(layout)
    return container
  
  
  def build_dataset_container(self) -> QFrame:
    preview_sect =  self.app.comp_fact.build_reused_single_btn_box(target_title="B. Transformed Dataset",
                                                             target_statement=None,
                                                             target_btn_text="Preview",
                                                             target_btn_event=lambda: self.app.fe_cont.preview_proc_tb())
    reset_sect =  self.app.comp_fact.build_reused_single_btn_box(target_title="C. Reset Options",
                                                             target_statement=None,
                                                             target_btn_text="Reset",
                                                             target_btn_event=lambda: self.app.fe_cont.reset_fe_page())
    container = QFrame()
    layout = QVBoxLayout()
    layout.addWidget(preview_sect, alignment=Qt.AlignTop | Qt.AlignCenter)
    layout.addWidget(reset_sect, alignment=Qt.AlignTop | Qt.AlignCenter)
    layout.setSpacing(36)
    layout.setContentsMargins(8, 8, 8, 8)
    container.setLayout(layout)
    return container
  
    
      

    