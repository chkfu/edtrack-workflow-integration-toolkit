from PyQt5.QtWidgets import (
  QWidget, QGridLayout, QVBoxLayout, QRadioButton, QButtonGroup, QFrame,
  QHBoxLayout, QCheckBox, QScrollArea, QTabWidget, QLabel, QDialog, QLineEdit
)
from PyQt5.QtCore import Qt
from views.components.config.views_config import DATASET_LIST
from views.components.config.views_styles import THEME_COLOR
from views.components.config.views_styles import (
  style_nav_sect_default, style_tab_scroll, style_tab_border
)
from views.components.pages.PageTemplate import PageTemplate
from states import DatasetState
import logging
from pandas.api.types import is_numeric_dtype
import pandas as pd


#  LOGGING

logger = logging.getLogger("PAGE_CLEAN")


#  CLASS

class PageClean(PageTemplate):
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref, target_ds_list: list | None = None):
    super().__init__(app_ref)
    
    if not target_ds_list:
      err_msg: str = "Dataset list is empty. Page tabs cannot be setup."
      logger.error(err_msg, exc_info=True)   
      raise ValueError(err_msg)
    
    #  setup tabs
    self.ds_list: list = target_ds_list
    self.tab_group: QTabWidget = QTabWidget()
    
    #  setup options reset
    self.radio_btn_list = []
    self.radio_groups = []


    #  build page tabs, store in self.tab_group. it stores:
    #  - tab = the output of build_cleaning_tab()
    #  - dataset = dataset names
    for title in target_ds_list:
      tab = self.build_cleaning_tab(target_title=title)
      self.tab_group.addTab(tab, title)
    
    #  Learnt: currentChanged method brings index naturally
    self.tab_group.currentChanged.connect(lambda index: self.app.clean_cont.handle_clean_tab_switch(target_index=index))
    logger.info("initialised successfully.")
    
 
  #  METHODS
  
  def merge_sections(self):
    #  title section
    inner_title_sect = self.create_title_sect(sect_title="Step 2: Clean Data and Preprocessing", 
                                              sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=2)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, enable_next=True)
    
    #  Work Panel Grid
    page = QWidget()
    page_layout = self.reuse_page_setting(inner_title_sect=inner_title_sect,
                                           inner_stat_sect=inner_stat_sect,
                                           inner_nav_sect=inner_nav_sect)
    page.setStyleSheet(style_nav_sect_default)
    page.setLayout(page_layout)
    return page
  
  
  # Override
  def core_sect_clean_data(self) -> QWidget:
    tab = self.tab_group
    tab.setStyleSheet(style_tab_border)
    return tab
  

  def build_cleaning_tab(self, target_title: str) -> QWidget:
    #  components
    tb_select_container = self.build_tb_opt_container(target_title=target_title)
    basic_clean_container = self.build_basic_clean_container()
    #  frame
    core_sect = QWidget()
    core_sect_layout = QVBoxLayout()
    core_sect_layout.addWidget(tb_select_container)
    core_sect_layout.addWidget(basic_clean_container)
    core_sect_layout.setAlignment(Qt.AlignTop)
    core_sect_layout.setSpacing(12)
    core_sect_layout.setContentsMargins(0, 0, 0, 0) 
    core_sect.setLayout(core_sect_layout)
    #  scroll
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet(style_tab_scroll)
    scroll.setWidget(core_sect)
    return scroll

    
  #  METHODS - CONTAINER
  
  def build_basic_clean_container(self) -> QFrame:
    #  components
    title_lb = self.app.comp_fact.build_label(lb_text="B. Data Cleaning",
                                              lb_type="h3",
                                              lb_align=Qt.AlignLeft,
                                              lb_bold=True)
    remove_duplicate_box = self.build_rm_duplicate_box()
    handle_blank_box = self.build_handle_blank_box()
    handle_sort_box = self.build_handle_sort_box()
    reset_box = self.build_reset_box()
    
    #  frame
    frame = QFrame()
    frame_layout = QVBoxLayout()
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(remove_duplicate_box)
    frame_layout.addWidget(handle_blank_box)
    frame_layout.addWidget(handle_sort_box)
    frame_layout.addWidget(reset_box)
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setContentsMargins(0, 12, 0, 0)
    frame.setLayout(frame_layout)
    return frame

  
  #  METHODS - BOX
  
  def build_tb_opt_container(self, target_title) -> QFrame:
    #  components
    title_lb = self.app.comp_fact.build_label(lb_text="A. Data Information",
                                              lb_type="h3",
                                              lb_align=Qt.AlignLeft,
                                              lb_bold=True)
    preview_box = self.app.comp_fact.preview_comp_box(lb_text=f"{target_title}", 
                                                      btn_text="Preview",
                                                      btn_event=lambda: self.app.file_cont.preview_dataset(target_key=target_title))
    
    #  frame
    frame = QFrame()
    frame_layout = QVBoxLayout()
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(preview_box)
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
    frame_layout.setContentsMargins(0, 16, 0, 0) 
    frame.setLayout(frame_layout)
    return frame
  
  
  
  def build_reset_box(self):
    title_lb = self.app.comp_fact.build_label(lb_text="C. Reset Option",
                                              lb_type="h3",
                                              lb_align=Qt.AlignLeft,
                                              lb_bold=True)
    #  frame
    reset_box = self.app.comp_fact.preview_comp_box(lb_text=f"Reset Cleaning Options", 
                                                      btn_text="Reset",
                                                      btn_event=lambda: self.app.clean_cont.reset_clean_tab_state())
    
    #  frame
    frame = QFrame()
    frame_layout = QVBoxLayout()
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(reset_box)
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
    frame_layout.setContentsMargins(0, 16, 0, 0) 
    frame.setLayout(frame_layout)
    return frame
  
  
  def build_rm_duplicate_box(self) -> QWidget:
    
    #  declaration
    OPT_LIST = ["Manage Duplicates.",
                "Remain Unchanged."]
    
    #  components
    title_lb = self.app.comp_fact.build_label(lb_text="1. Remove Duplicates",
                                              lb_type="h3",
                                              lb_txtcolor=THEME_COLOR["mid"],
                                              lb_align=Qt.AlignLeft,
                                              lb_bold=True)
    radio_group = self.app.comp_fact.build_radio_group(target_list=OPT_LIST,
                                                       target_event=lambda text, checked: self.app.clean_cont.handle_clean_dup_opt(target_list=OPT_LIST,
                                                                                                                                  text=text,
                                                                                                                                  checked=checked),
                                                       is_horizontal=False)
    #  store, in case reset options
    self.radio_groups.append(radio_group["group"])
    self.radio_btn_list.extend(radio_group["buttons"])
    
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(radio_group["widget"])
    frame.setLayout(frame_layout)
    return frame

  
  
  def build_handle_blank_box(self) -> QWidget:
    
    #  declaration
    OPT_LIST = ["Manage Blanks.",
                "Remain Unchanged."]
    # components
    title_lb = self.app.comp_fact.build_label(lb_text="2. Handling Blanks",
                                            lb_type="h3",
                                            lb_txtcolor=THEME_COLOR["mid"],
                                            lb_align=Qt.AlignLeft,
                                            lb_bold=True)
    radio_group = self.app.comp_fact.build_radio_group(target_list=OPT_LIST,
                                                      target_event=lambda text, checked: self.app.clean_cont.handle_clean_blank_opt(
                                                        target_list=OPT_LIST,
                                                        text=text, 
                                                        checked=checked),
                                                      is_horizontal=False)
    #  store, in case reset options
    self.radio_groups.append(radio_group["group"])
    self.radio_btn_list.extend(radio_group["buttons"])
    
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(radio_group["widget"])
    frame.setLayout(frame_layout)
    return frame
    

  def build_handle_sort_box(self) -> QWidget:
    
    #  declaration
    OPT_LIST = ["Reorder Records.",
                "Remain Unsorted."]
    # components
    title_lb = self.app.comp_fact.build_label(lb_text="3. Sorting",
                                              lb_type="h3",
                                              lb_txtcolor=THEME_COLOR["mid"],
                                              lb_align=Qt.AlignLeft,
                                              lb_bold=True)
    radio_group = self.app.comp_fact.build_radio_group(
                                        target_list=OPT_LIST,
                                        target_event=lambda text, checked: self.app.clean_cont.handle_clean_sort_opt(target_list=OPT_LIST,
                                                                                                                      text=text,
                                                                                                                      checked=checked),
                                        is_horizontal=False)
    #  store, in case reset options
    self.radio_groups.append(radio_group["group"])
    self.radio_btn_list.extend(radio_group["buttons"])
    
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.setSpacing(8)
    frame_layout.setAlignment(Qt.AlignTop)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame_layout.addWidget(title_lb)
    frame_layout.addWidget(radio_group["widget"])
    frame.setLayout(frame_layout)
    return frame
  
  
  #  POP-UP WINDOWS (for state management)
  
  
  def identify_target_df(self, curr_ds_key: str) -> DatasetState | None:
    valid_keys = [item["data"] for item in DATASET_LIST[1:4]]
    if curr_ds_key not in valid_keys:
        err_msg = f"Incorrect dataset key: {curr_ds_key}"
        logger.error(err_msg, exc_info=True)
        return None
    return self.app.clean_state.get_spec_dataframe(curr_ds_key)
  
    
  
  
  def build_dup_popup(self) -> QWidget:
    
    pop_wd = QDialog()
    
    curr_ds_key: str = self.app.clean_state.get_clean_target().state_name
    target_dataframe: DatasetState = self.identify_target_df(curr_ds_key=curr_ds_key)
    col_options = list(target_dataframe.data_raw.columns)
    checkbox_list: list = []
    OPT_LIST = ["--- Please Select ---", 
                "Apply to ALL columns", 
                "Apply to Specific columns"]
    
    #  drow down components
    opt_lb = self.app.comp_fact.build_label(lb_text="Handle Mode:",
                                            lb_txtcolor=THEME_COLOR["white"])
    opt_dd = self.app.comp_fact.build_dropdown(target_options=OPT_LIST,
                                                target_default=0,
                                                event=lambda text: self.app.clean_cont.select_clean_dup_dropdown(selected_opt=text,
                                                                                                                  opt_list=OPT_LIST,
                                                                                                                  cb_list=checkbox_list))
    cb_lb = self.app.comp_fact.build_label(lb_text="Target Columns:",
                                            lb_txtcolor=THEME_COLOR["white"])
    close_btn = self.app.comp_fact.build_btn(btn_text="Back", 
                                             btn_event=lambda: self.app.clean_cont.close_clean_dup_popup(target_popup=pop_wd),
                                             btn_bgcolor=THEME_COLOR["primary"],
                                             btn_txtcolor=THEME_COLOR["white"],
                                             btn_hover_bgcolor=THEME_COLOR["primary_hvr"])

    #  checkbox components
    
    cb_box = QWidget()
    cb_box_layout = QVBoxLayout()
    for column in col_options:
      checkbox = self.app.comp_fact.build_checkbox(target_name=column,
                                                   target_event=lambda target_state, target_name=column:
      #  Learnt: early binding col, prevent all points to last col
      self.app.clean_cont.select_clean_dup_checkbox(target_state=target_state,
                                                      target_name=target_name))
      cb_box_layout.addWidget(checkbox)
      checkbox_list.append(checkbox)
    cb_box.setLayout(cb_box_layout)
    #  remarks: checkbox only available for "select specific columns"
    for cb in checkbox_list:
        cb.setEnabled(False)
    
    #  frame
    pop_wd.setWindowTitle("Duplicate Options")
    pop_wd_layout = QGridLayout()
    pop_wd_layout.addWidget(opt_lb, 0, 0, alignment=Qt.AlignLeft)
    pop_wd_layout.addWidget(opt_dd, 0, 1)
    pop_wd_layout.addWidget(cb_lb, 1, 0, alignment=Qt.AlignLeft)
    pop_wd_layout.addWidget(cb_box, 1, 1)
    pop_wd_layout.addWidget(close_btn, 2, 0, 1, 2, alignment=Qt.AlignCenter)
    pop_wd.setLayout(pop_wd_layout)
    pop_wd.setMaximumWidth(200)
    return pop_wd
  
  
  def build_blank_popup(self) -> QWidget:
    
    #  setup frame
    pop_wd = QDialog()
    pop_wd.setWindowTitle("Blank Options")
    pop_wd_layout = QGridLayout()
    
    #  declare variables
    curr_ds_key: str = self.app.clean_state.get_clean_target().state_name
    target_dataframe: DatasetState = self.identify_target_df(curr_ds_key=curr_ds_key)

    #  loop to build components
    for index, column in enumerate(target_dataframe.data_raw.columns):

      target_col = target_dataframe.data_raw[column]
    
      col_lb = self.app.comp_fact.build_label(
          lb_text=column,
          lb_txtcolor=THEME_COLOR["white"]
      )  
      type_lb = self.app.comp_fact.build_label(
          lb_text=str(target_col.dtype),
          lb_txtcolor=THEME_COLOR["white"]
      )
      opt_dd = self.app.comp_fact.build_dropdown(
          target_options=self.app.clean_cont.get_blank_dropdown(target_series=target_col),
          target_default=0,
          event=lambda text, col=column: self.app.clean_cont.select_blank_opt(target_col=col, 
                                                                              selected_opt=text))

      pop_wd_layout.addWidget(col_lb, index, 0, alignment=Qt.AlignLeft)
      pop_wd_layout.addWidget(type_lb, index, 1, alignment=Qt.AlignLeft)
      pop_wd_layout.addWidget(opt_dd, index, 2, alignment=Qt.AlignLeft)
    
    #  back option
    close_btn = self.app.comp_fact.build_btn(btn_text="Back", 
                                             btn_event=lambda: self.app.clean_cont.close_clean_blank_popup(target_popup=pop_wd),
                                             btn_bgcolor=THEME_COLOR["primary"],
                                             btn_txtcolor=THEME_COLOR["white"],
                                             btn_hover_bgcolor=THEME_COLOR["primary_hvr"])
    btn_box = QWidget()
    btn_layout = QHBoxLayout()
    btn_layout.addWidget(close_btn, alignment=Qt.AlignCenter)
    btn_box.setLayout(btn_layout)
    #  complete frame
    final_row = len(target_dataframe.data_raw.columns)
    pop_wd_layout.addWidget(btn_box, final_row, 0, 1, 3, Qt.AlignCenter)
    pop_wd.setLayout(pop_wd_layout)
    pop_wd.setMaximumWidth(200)
    return pop_wd
  
  
  def build_sort_popup(self) -> QWidget:
    
    #  identify target dataframe
    curr_ds_key: str = self.app.clean_state.get_clean_target().state_name
    target_dataframe: DatasetState = self.identify_target_df(curr_ds_key=curr_ds_key)
    
    #  setup options
    OPT_LIST = ["--- Please Select ---"] + list(target_dataframe.data_raw.columns)
    ORDER_LIST = ["--- Please Select ---", 
                  "Ascending", 
                  "Descending"]
    
    pop_wd = QDialog()
  
    #  components
    opt_lb = self.app.comp_fact.build_label(lb_text="Target Column:",
                                            lb_txtcolor=THEME_COLOR["white"])
    order_lb = self.app.comp_fact.build_label(lb_text="Sorting Order:",
                                              lb_txtcolor=THEME_COLOR["white"])
    opt_dd = self.app.comp_fact.build_dropdown(target_options=OPT_LIST,
                                                target_default=0,
                                                event=lambda el: self.app.clean_cont.select_sort_opt(selected_opt=el))
    order_dd = self.app.comp_fact.build_dropdown(target_options=ORDER_LIST,
                                                 target_default=0,
                                                 event=lambda el: self.app.clean_cont.select_sort_order(selected_opt=el))
    close_btn = self.app.comp_fact.build_btn(btn_text="Back", 
                                             btn_event=lambda: self.app.clean_cont.close_clean_sort_popup(target_popup=pop_wd),
                                             btn_bgcolor=THEME_COLOR["primary"],
                                             btn_txtcolor=THEME_COLOR["white"],
                                             btn_hover_bgcolor=THEME_COLOR["primary_hvr"])
    btn_box = QWidget()
    btn_box_layout = QHBoxLayout()
    btn_box_layout.addWidget(close_btn, alignment=Qt.AlignCenter)
    btn_box.setLayout(btn_box_layout)
    #  frame
    pop_wd.setWindowTitle("Sorting Options")
    pop_wd_layout = QGridLayout()
    pop_wd_layout.addWidget(opt_lb, 0, 0, alignment=Qt.AlignLeft)
    pop_wd_layout.addWidget(opt_dd, 0, 1)
    pop_wd_layout.addWidget(order_lb, 1, 0, alignment=Qt.AlignLeft)
    pop_wd_layout.addWidget(order_dd, 1, 1)
    pop_wd_layout.addWidget(order_dd, 1, 1)
    pop_wd_layout.addWidget(btn_box, 2, 0, 1, 2, alignment=Qt.AlignCenter)
    pop_wd.setLayout(pop_wd_layout)
    pop_wd.setMaximumWidth(200)
    return pop_wd
  
  
  
  #  RESET
  
  def reset_display(self):
    #  Learnt: need to close exclusive first, and re-activate it for new visual
    for group in self.radio_groups:
      group.setExclusive(False)
    for btn in self.radio_btn_list:
      btn.blockSignals(True)
      btn.setChecked(False)
      btn.blockSignals(False)
    for group in self.radio_groups:
      group.setExclusive(True)