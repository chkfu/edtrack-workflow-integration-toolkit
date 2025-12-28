from PyQt5.QtWidgets import (
  QFrame, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea,
  QDialog, QLineEdit, QSizePolicy
)
from PyQt5.QtCore import Qt
from views.components.pages.PageTemplate import PageTemplate
from views.components.config.views_styles import style_tab_scroll
from views.components.config.views_styles import THEME_COLOR
import logging
from typing import Callable
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime


#  LOGGING

logger = logging.getLogger("PAGE_FEATENG")


#  CLASS

class PageFE(PageTemplate):
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    super().__init__(app_ref)
    
    #  setup options reset
    self.sub_02_cb_list: list = []
    self.radio_btn_list: list = []
    self.radio_groups: list = []
    
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
    
  def build_remove_cols_popup(self)-> QDialog:
    #  declaration
    remove_list: list = []
    #  select merge datafram
    target_df = self.app.merge_state.merge_proc
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
    
    #  build button sect
    btn_sect = self.build_reused_popup_btns(target_popup=pop_wd,
                                            proc_event=lambda: [
                                              self.app.fe_cont.assign_remove_cols_event(target_col_list=list(remove_list)),
                                              pop_wd.close()])
    
    #  finalise popup
    popup_layout.addWidget(title_sect)
    popup_layout.addWidget(cb_sect)
    popup_layout.addWidget(btn_sect)
    popup_layout.setSpacing(4)
    popup_layout.setContentsMargins(24, 24, 24, 24)
    pop_wd.setLayout(popup_layout)
    return pop_wd
  
  
  # TODO: Proceeding event to be condfirmed
  def build_rename_cols_popup(self) -> QDialog:
    
    # declaration
    col_name_dict: dict = {}
    
    #  setup popup
    pop_wd = QDialog()
    pop_wd.setWindowTitle("Rename Columns")
    pop_wd.setMinimumWidth(400)
    popup_layout = QVBoxLayout(pop_wd)
    
    
    def update_col_name(target_column: str, target_input: str) -> None:
      nonlocal col_name_dict
      col_name_dict[target_column] = target_input.strip()
      return
    
    #  build title sect
    title_sect = self.build_reused_popup_title(target_title="Option: Rename Columns")

    #  build option sect
    option_sect = QScrollArea()
    option_sect.setWidgetResizable(True)
    option_content = QWidget()
    option_content_layout = QVBoxLayout()
    
    #  1. title and statements
    grid_title = self.app.comp_fact.build_label(lb_text="1. Replace with new column names, if applicable:",
                                                lb_type="p",
                                                lb_txtcolor=THEME_COLOR["white"],
                                                lb_align=Qt.AlignLeft)
    option_content_layout.addWidget(grid_title)
    
    #  2. grid layout
    grid_frame = QWidget()
    grid_frame_layout = QGridLayout()
    for index, column in enumerate(self.app.merge_state.merge_proc.columns):
      column_lb = self.app.comp_fact.build_label(lb_text=column,
                                                 lb_type="p",
                                                 lb_txtcolor=THEME_COLOR["white"],
                                                 lb_align=Qt.AlignLeft)
      line_edit = self.app.comp_fact.build_line_edit(
                        target_event=lambda text, name=column: update_col_name(target_column=name,
                                                                               target_input=text))
      
      grid_frame_layout.addWidget(column_lb, index, 0)
      grid_frame_layout.addWidget(line_edit, index, 1)
      
    grid_frame.setLayout(grid_frame_layout)
    option_content_layout.addWidget(grid_frame)
    
    option_content.setLayout(option_content_layout)
    option_sect.setWidget(option_content)
    
    #  build button sect
    btn_sect = self.build_reused_popup_btns(target_popup=pop_wd,
                                            proc_event=lambda: [self.app.fe_cont.assign_rename_col_event(target_dict=col_name_dict),
                                                                pop_wd.close()])
    
    #  finalise popup
    popup_layout.addWidget(title_sect)
    popup_layout.addWidget(option_sect)
    popup_layout.addWidget(btn_sect)
    popup_layout.setSpacing(4)
    popup_layout.setContentsMargins(24, 24, 24, 24)
    pop_wd.setLayout(popup_layout)
    return pop_wd
    
    
  def build_filter_rows_popup(self) -> QDialog:
    
    #  declaration
    col_select_dict: dict = {}
    sub_02_int_layout = QVBoxLayout() 
    
    def update_dict_sub_01(target_state: Qt.CheckState, 
                           target_col: str) -> None:
      nonlocal col_select_dict, sub_02_int_layout
      #  put column as key and cell value into a set
      if target_state == Qt.Checked:
        col_select_dict[target_col] = set(self.app.merge_state.merge_proc[target_col])
      else:
        col_select_dict.pop(target_col, None)
      #  rebuild the whole sub_02 checkbxes
      self.app.comp_fact.clear_layout_items(layout=sub_02_int_layout)
      build_reuse_sub_02()
        
        
    def update_dict_sub_02(target_col: str, 
                           target_val: str) -> None:
      nonlocal col_select_dict
      print(target_col, target_val)
      return
    
    def build_reuse_sub_02() -> None:
      for column in col_select_dict.keys():
        for value in col_select_dict[column]:
          sub_02_cb = self.app.comp_fact.build_checkbox(target_name=value,
                                                        target_event=lambda target_state, target_name, column=column, value=value: (
                                                          update_dict_sub_02(target_col=column,
                                                                             target_val=value)))
          sub_02_int_layout.addWidget(sub_02_cb)
      return
    
    
    
    #  setup popup
    pop_wd = QDialog()
    pop_wd.setWindowTitle("Filter Rows")
    pop_wd.setMinimumWidth(400)
    popup_layout = QVBoxLayout(pop_wd)
    
    #  build title sect
    title_sect = self.build_reused_popup_title(target_title="Option: Filter Rows")
    
    #  build content sect
    content_sect_scroll = QScrollArea()
    content_sect_scroll.setWidgetResizable(True)
    content_sect_widget = QWidget()
    content_sect_layout = QVBoxLayout()
    
    #  pre-build frame, in case refreshing items
    sub_01_ext = QWidget()
    sub_01_ext_layout = QVBoxLayout()
    sub_02_ext = QWidget()
    sub_02_ext_layout = QVBoxLayout()
     
    #  1. build sub 01 layout
    sub_01_statement = self.app.comp_fact.build_label(lb_text="1. Select the columns to be edited:",
                                                      lb_txtcolor=THEME_COLOR["white"],
                                                      lb_align=Qt.AlignLeft)
    sub_01_ext_layout.addWidget(sub_01_statement)
    
    sub_01_int_scroll = QScrollArea()
    sub_01_int_scroll.setWidgetResizable(True)
    sub_01_int_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    sub_01_int_content = QWidget()
    sub_01_int_layout = QVBoxLayout()
    for column in self.app.merge_state.merge_proc.columns:
      sub_01_cb = self.app.comp_fact.build_checkbox(target_name=column,
                                                    target_event=lambda target_state, target_name: update_dict_sub_01(
                                                      target_state=target_state,
                                                      target_col=target_name))
      sub_01_int_layout.addWidget(sub_01_cb)
    
    sub_01_int_content.setLayout(sub_01_int_layout)
    sub_01_int_scroll.setWidget(sub_01_int_content)
    sub_01_ext_layout.addWidget(sub_01_int_scroll)
    sub_01_ext.setLayout(sub_01_ext_layout) 
    
    #  2. select cells to be removed
    
    sub_02_statement = self.app.comp_fact.build_label(lb_text="2. Select the cell value to be processed:",
                                                      lb_txtcolor=THEME_COLOR["white"],
                                                      lb_align=Qt.AlignLeft)
    sub_02_ext_layout.addWidget(sub_02_statement)
    
    sub_02_int_scroll = QScrollArea()
    sub_02_int_scroll.setWidgetResizable(True)
    sub_02_int_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    sub_02_int_content = QWidget()
    sub_02_int_layout = QVBoxLayout()
    build_reuse_sub_02()
  
    sub_02_int_content.setLayout(sub_02_int_layout)
    sub_02_int_scroll.setWidget(sub_02_int_content)
    sub_02_ext_layout.addWidget(sub_02_int_scroll)
    sub_02_ext.setLayout(sub_02_ext_layout)
    
    content_sect_layout.addWidget(sub_01_ext)
    content_sect_layout.addWidget(sub_02_ext)
    content_sect_widget.setLayout(content_sect_layout)
    content_sect_scroll.setWidget(content_sect_widget)
    
    #  build button sect
    btn_sect = self.build_reused_popup_btns(target_popup=pop_wd,
                                            proc_event=lambda: [self.app.fe_cont.assign_filter_rows_event(target_dict=col_select_dict),
                                                                pop_wd.close()])
    
    #  finalise popup
    popup_layout.addWidget(title_sect)
    popup_layout.addWidget(content_sect_scroll)
    popup_layout.addWidget(btn_sect)
    popup_layout.setSpacing(4)
    popup_layout.setContentsMargins(24, 24, 24, 24)
    pop_wd.setLayout(popup_layout)
    return pop_wd
    
    
  # TODO: Proceeding event to be condfirmed
  def build_time_feat_popup(self) -> QDialog:
    
    #  declarations
    col_select: list = []
    feat_select: list = []
    keep_origin: bool | None = None
    sub_01_temp_count: int = 0
    
    def decide_keep_origin(input: str) -> None:
      #  Leant: enable the method to update var in external scope
      nonlocal keep_origin
      if input == OPTS_DICT["sub_03"]["options"][0]:
        keep_origin = True
      elif input == OPTS_DICT["sub_03"]["options"][1]:
        keep_origin = False
      else:
        keep_origin = None
    
    OPTS_DICT: dict = {
      "sub_01": {
        "title": "1. Select date / time column(s):",
        "options": self.app.merge_state.merge_proc.columns,
        "event": lambda target_state, target_name: col_select.append(target_name) if target_state == Qt.Checked else None
      },
      "sub_02": {
        "title": "2. Choose time features to extract",
        "options": ["Year", "Month", "Day", "Weekday", "Hour"],
        "event": lambda target_state, target_name: feat_select.append(target_name) if target_state == Qt.Checked else None
      },
      "sub_03": {
        "title": "3. Decide to keep or remove original column:",
        "options": ["Keep Originals", "Drop Originals"],
        "event": lambda text, checked: decide_keep_origin(input=text)
      }
    }
    
    #  setup popup
    pop_wd = QDialog()
    pop_wd.setWindowTitle("Time Features")
    pop_wd.setMinimumWidth(400)
    popup_layout = QVBoxLayout(pop_wd)
    
    #  build title sect
    title_sect = self.build_reused_popup_title(target_title="Option: Time Features")
    
    #  build cb sect
    cb_sect = QScrollArea()
    cb_sect.setWidgetResizable(True)
    cb_content = QWidget()
    cb_content_layout = QVBoxLayout()
    
    #  1. build sub 01
    sub_01_box = QWidget()
    sub_01_layout = QVBoxLayout()
    sub_01_title = self.app.comp_fact.build_label(lb_text=OPTS_DICT["sub_01"]["title"],
                                                  lb_txtcolor=THEME_COLOR["white"],
                                                  lb_align=Qt.AlignLeft)
    sub_01_layout.addWidget(sub_01_title)
    for column in OPTS_DICT["sub_01"]["options"]:
      if not is_datetime(self.app.merge_state.merge_proc[column]):
        continue
      else:
        opt_cb = self.app.comp_fact.build_checkbox(target_name=column,
                                                   target_event=OPTS_DICT["sub_01"]["event"])
        sub_01_layout.addWidget(opt_cb)
        sub_01_temp_count += 1
    if sub_01_temp_count < 1:
      empty_lb = self.app.comp_fact.build_label(lb_text="(Not Found)",
                                                lb_txtcolor=THEME_COLOR["white"],
                                                lb_align=Qt.AlignLeft)
      sub_01_layout.addWidget(empty_lb)
    sub_01_box.setLayout(sub_01_layout)
    
    #  2. build sub 02
    sub_02_box = QWidget()
    sub_02_layout = QVBoxLayout()
    sub_02_title = self.app.comp_fact.build_label(lb_text=OPTS_DICT["sub_02"]["title"],
                                                  lb_txtcolor=THEME_COLOR["white"],
                                                  lb_align=Qt.AlignLeft)
    sub_02_layout.addWidget(sub_02_title)
    for option in OPTS_DICT["sub_02"]["options"]:
      opt_cb = self.app.comp_fact.build_checkbox(target_name=option,
                                                 target_event=OPTS_DICT["sub_02"]["event"])
      sub_02_layout.addWidget(opt_cb)
    sub_02_box.setLayout(sub_02_layout)
    
    #  3.  build sub 03
    sub_03_box = QWidget()
    sub_03_layout = QVBoxLayout()
    sub_03_title = self.app.comp_fact.build_label(lb_text=OPTS_DICT["sub_03"]["title"],
                                                  lb_txtcolor=THEME_COLOR["white"],
                                                  lb_align=Qt.AlignLeft)
    sub_03_radio = self.app.comp_fact.build_radio_group(target_list=OPTS_DICT["sub_03"]["options"],
                                                        target_event=OPTS_DICT["sub_03"]["event"],
                                                        is_horizontal=True)
    sub_03_layout.addWidget(sub_03_title)
    sub_03_layout.addWidget(sub_03_radio["widget"])
    sub_03_box.setLayout(sub_03_layout)
    self.radio_groups.append(sub_03_radio["group"])
    self.radio_btn_list.extend(sub_03_radio["buttons"])
    
    cb_content_layout.addStretch()
    cb_content_layout.addWidget(sub_01_box)
    cb_content_layout.addWidget(sub_02_box)
    cb_content_layout.addWidget(sub_03_box)
    cb_content.setLayout(cb_content_layout)
    cb_sect.setWidget(cb_content)
    
    #  build button sect
    btn_sect = self.build_reused_popup_btns(target_popup=pop_wd,
                                            proc_event=lambda: [self.app.fe_cont.assign_time_feat_event(
                                              col_select=col_select,
                                              feat_select=feat_select,
                                              keep_origin=keep_origin),
                                              pop_wd.close()])
    
    #  finalise popup
    popup_layout.addWidget(title_sect)
    popup_layout.addWidget(cb_sect)
    popup_layout.addWidget(btn_sect)
    popup_layout.setSpacing(4)
    popup_layout.setContentsMargins(24, 24, 24, 24)
    pop_wd.setLayout(popup_layout)
    return pop_wd
      


  def build_encoding_cols_popup(self) -> QDialog:
    
    def update_opt_dict(target_dict: dict, key: str, value: str):
      if key is None or value is None or key == "" or value == "":
        return {}
      opt_dict[str(key)] = str(value)
      return opt_dict
    
    #  declaration
    encode_list: list = []
    hash_list: list = []
    opt_dict: dict = {}
    
    #  setup popup
    pop_wd = QDialog()
    pop_wd.setWindowTitle("Encoding / Hashing Values")
    pop_wd.setMinimumWidth(400)
    popup_layout = QVBoxLayout(pop_wd)  

    #  build title sect
    title_sect = self.build_reused_popup_title(target_title="Option: Encoding / Hashing Values")
    
    #  build encode sect
    encode_sect = QWidget()
    encode_sect_layout = QVBoxLayout()
    encode_lb = self.app.comp_fact.build_label(lb_text="1. Select the columns for applying component codes:",
                                               lb_type="p",
                                               lb_txtcolor=THEME_COLOR["white"],
                                               lb_align=Qt.AlignLeft)
    encode_sect_layout.addWidget(encode_lb)
    for column in self.app.merge_state.merge_proc.columns:
      cb = self.app.comp_fact.build_checkbox(target_name=column,
                                             target_event=lambda target_state, target_name:
                                              encode_list.append(target_name) if target_state == Qt.Checked else None)
      encode_sect_layout.addWidget(cb)
    encode_sect.setLayout(encode_sect_layout)
    
    #  build regulate sect
    regulate_sect = QWidget()
    regulate_sect_layout = QVBoxLayout()
    regulate_lb = self.app.comp_fact.build_label(lb_text="2. Select the columns for regulating input values:",
                                                 lb_type="p",
                                                 lb_txtcolor=THEME_COLOR["white"],
                                                 lb_align=Qt.AlignLeft)
    action_lb = self.app.comp_fact.build_label(lb_text="Action Column:",
                                               lb_type="p",
                                               lb_txtcolor=THEME_COLOR["white"],
                                               lb_align=Qt.AlignLeft)
    action_dd = self.app.comp_fact.build_dropdown(target_options = ["Remain Unchanged"] + list(self.app.merge_state.merge_proc.columns),
                                                  target_default=0,
                                                  event=lambda text: update_opt_dict(target_dict=opt_dict, key="action", value=text))
    target_lb = self.app.comp_fact.build_label(lb_text="Target Column:",
                                               lb_type="p",
                                               lb_txtcolor=THEME_COLOR["white"],
                                               lb_align=Qt.AlignLeft)
    target_dd = self.app.comp_fact.build_dropdown(target_options = ["Remain Unchanged"] + list(self.app.merge_state.merge_proc.columns),
                                                  target_default=0,
                                                  event=lambda text: update_opt_dict(target_dict=opt_dict, key="target", value=text))
    regulate_grid = QWidget()
    regulate_grid_layout = QGridLayout()
    regulate_grid_layout.addWidget(action_lb, 0, 0, Qt.AlignLeft)
    regulate_grid_layout.addWidget(action_dd, 0, 1, Qt.AlignLeft)
    regulate_grid_layout.addWidget(target_lb, 1, 0, Qt.AlignLeft)
    regulate_grid_layout.addWidget(target_dd, 1, 1, Qt.AlignLeft)
    regulate_grid.setLayout(regulate_grid_layout)
    regulate_sect_layout.addWidget(regulate_lb)
    regulate_sect_layout.addWidget(regulate_grid)
    regulate_sect.setLayout(regulate_sect_layout)
    
    #  build hash sect
    hash_sect = QWidget()
    hash_sect_layout = QVBoxLayout()
    hash_lb = self.app.comp_fact.build_label(lb_text="3. Select the columns for hashing confidential details:",
                                             lb_type="p",
                                             lb_txtcolor=THEME_COLOR["white"],
                                             lb_align=Qt.AlignLeft)
    hash_sect_layout.addWidget(hash_lb)
    for column in self.app.merge_state.merge_proc.columns:
      cb = self.app.comp_fact.build_checkbox(target_name=column,
                                             target_event=lambda target_state, target_name:
                                              hash_list.append(target_name) if target_state == Qt.Checked else None)
      hash_sect_layout.addWidget(cb)
    hash_sect.setLayout(hash_sect_layout)
    
    #  combine optios sect
    opt_scroll = QScrollArea()
    opt_scroll.setWidgetResizable(True) 
    opt_sect = QWidget()
    opt_sect_layout = QVBoxLayout(opt_sect)
    opt_sect_layout.addWidget(encode_sect)
    opt_sect_layout.addWidget(regulate_sect)
    opt_sect_layout.addWidget(hash_sect)
    opt_sect_layout.addStretch()
    opt_scroll.setWidget(opt_sect)
    
    #  build button sect
    btn_sect = self.build_reused_popup_btns(target_popup=pop_wd,
                                            proc_event=lambda: [
                                              self.app.fe_cont.assign_encode_hash_event(encode_list=encode_list,
                                                                                        hash_list=hash_list,
                                                                                        opt_dict=opt_dict), 
                                              pop_wd.close()])
    
    #  complete popup
    popup_layout.addWidget(title_sect)
    popup_layout.addWidget(opt_scroll)
    popup_layout.addWidget(btn_sect)
    popup_layout.setSpacing(4)
    popup_layout.setContentsMargins(24, 24, 24, 24)
    pop_wd.setLayout(popup_layout)
    return pop_wd
  
  
  
  #  METHODS - REUSE
  
  def build_reused_popup_title(self, target_title: str) -> QWidget:
    title_sect = QWidget()
    title_sect_layout = QHBoxLayout()
    title_lb = self.app.comp_fact.build_label(lb_text=target_title,
                                              lb_type="h2",
                                              lb_txtcolor=THEME_COLOR["white"],
                                              lb_align=Qt.AlignLeft)  
    title_sect_layout.addWidget(title_lb)
    title_sect.setLayout(title_sect_layout)
    return title_sect
  
  
  def build_reused_popup_btns(self,
                              target_popup: QWidget,
                              proc_event: Callable | None = None) -> QDialog: 
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
  