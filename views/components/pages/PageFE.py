from PyQt5.QtWidgets import (
  QFrame, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea,
  QDialog
)
from PyQt5.QtCore import Qt
from views.components.pages.PageTemplate import PageTemplate
from views.components.config.views_styles import style_tab_scroll
from views.components.config.views_styles import THEME_COLOR
import logging
from typing import Callable
import pandas as pd


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
    FE_CONFIG = [
        {
            "title": "Remove Columns",
            "event": lambda: self.app.fe_cont.handle_remove_cols()
        },
        {
            "title": "Rename Columns",
            "event": lambda: self.app.fe_cont.handle_rename_cols()
        },
        {
            "title": "Filter Rows",
            "event": lambda: self.app.fe_cont.handle_filter_rows()
        },
        {
            "title": "Time Features",
            "event": lambda: self.app.fe_cont.handle_time_feat()
        },
        {
            "title": "Encode / Hash",
            "event": lambda: self.app.fe_cont.handle_encoding()
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
  
  
  #  METHODS - POPUPS
  
  def build_reused_popup_btns(self,
                              target_popup: QWidget,
                              proc_event: Callable | None = None) -> QWidget: 
    #  build frame
    box = QWidget()
    box_layout = QHBoxLayout()
    
    #  build back button (essential)
    #  Remarks: return to main window without memorise curr options (new empty variable each triggering)
    back_btn = self.app.comp_fact.build_btn(btn_text="Back",
                                        btn_event=lambda: target_popup.close(),
                                        btn_bgcolor=THEME_COLOR["white"],
                                        btn_txtcolor=THEME_COLOR["primary"],
                                        btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    box_layout.addWidget(back_btn)
    
    #  build proceed button, depends on validity of parameters
    #  components
    if proc_event is not None:
      proceed_btn = self.app.comp_fact.build_btn(btn_text="Proceed",
                                                btn_event=proc_event,
                                                btn_bgcolor=THEME_COLOR["primary"],
                                                btn_txtcolor=THEME_COLOR["white"],
                                                btn_hover_bgcolor=THEME_COLOR["primary_hvr"])
      box_layout.addWidget(proceed_btn)
    
    #  complete frame, return blank box if event not found
    box_layout.setSpacing(8)
    box_layout.setContentsMargins(0, 12, 0, 0)
    box.setLayout(box_layout)
    return box
  
    
  def build_remove_cols_popup(self):
    #  declaration
    remove_list: list = []
    #  select merge datafram
    target_df = self.app.fe_cont.search_editable_merged_dataset()
    if target_df is None:
      return
    #  setup popup
    pop_wd = QDialog()
    pop_wd.setWindowTitle("Remove Columns")
    pop_wd.setMinimumWidth(400)
    popup_layout = QVBoxLayout(pop_wd)
    #  build title sect
    title_sect = QWidget()
    title_sect_layout = QHBoxLayout()
    title_lb = self.app.comp_fact.build_label(lb_text="Option: Remove Columns",
                                              lb_type="h2",
                                              lb_txtcolor=THEME_COLOR["white"],
                                              lb_align=Qt.AlignLeft)
    title_sect_layout.addWidget(title_lb)
    title_sect.setLayout(title_sect_layout)
    #  build checkbox sect
    cb_sect = QScrollArea()
    cb_sect.setWidgetResizable(True)
    cb_content = QWidget()
    cb_content_layout = QVBoxLayout()
    cb_sect.setMinimumHeight(250) 
    cb_statement = self.app.comp_fact.build_label(lb_text="Please select the dataset columns to be removed:",
                                                  lb_txtcolor=THEME_COLOR["white"],
                                                  lb_align=Qt.AlignLeft,
                                                  lb_wrap=True)
    cb_content_layout.addWidget(cb_statement)
    for column in target_df.columns:
      cb = self.app.comp_fact.build_checkbox(target_name=column,
                                             target_event=lambda target_state, target_name:
        remove_list.append(target_name) if target_state == Qt.Checked else None)
      cb_content_layout.addWidget(cb)
    cb_content_layout.addStretch()
    cb_content.setLayout(cb_content_layout)
    cb_sect.setWidget(cb_content)
    #  build undo / proceed button
    btn_sect = self.build_reused_popup_btns(target_popup=pop_wd,
                                            proc_event=lambda: [
                                              self.app.fe_cont.assign_remove_cols_event(
                                                  target_df=target_df,
                                                  target_col_list=list(remove_list)),
                                              pop_wd.close()])

    #  finalise popup
    popup_layout.addWidget(title_sect)
    popup_layout.addWidget(cb_sect)
    popup_layout.addWidget(btn_sect)
    popup_layout.setSpacing(4)
    popup_layout.setContentsMargins(24, 24, 24, 24)
    pop_wd.setLayout(popup_layout)
    return pop_wd
      

  def build_preview_fe_popup(self) -> QWidget:
    pass