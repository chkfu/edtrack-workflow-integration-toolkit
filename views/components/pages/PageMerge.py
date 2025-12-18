from PyQt5.QtWidgets import (
  QFrame, QWidget, QGridLayout, QVBoxLayout, QLayout, QScrollArea,
  QComboBox
)
from PyQt5.QtCore import Qt
from views.components.config.views_config import MERGE_METHOD_OPT
from views.components.config.views_styles import (
  THEME_COLOR, style_nav_sect_default, style_tab_scroll
)
from views.components.pages.PageTemplate import PageTemplate
import logging



#  LOGGING
logger = logging.getLogger("PAGE_MERGE")


#  CLASS

class PageMerge(PageTemplate):
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    super().__init__(app_ref)
    self.dd_table_left: QComboBox = None
    self.dd_table_rightL: QComboBox = None
    self.dd_column_left: QComboBox = None
    self.dd_column_right: QComboBox = None
    logger.info("initialised successfully.")
    
    
  #  METHODS -  MAIN
  
  def merge_sections(self) -> QWidget:
    #  title section
    inner_title_sect = self.create_title_sect(sect_title="Step 3: Merge Tables", 
                                              sect_des="TThis step combines multiple datasets using matching columns or index keys to create a unified table for further processing.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=3)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, 
                                          enable_next=True)
    
    #  Work Panel Grid
    page = QWidget()
    page_layout = QGridLayout()
    page_layout = self.reuse_page_setting(inner_title_sect=inner_title_sect,
                                          inner_stat_sect=inner_stat_sect,
                                          inner_nav_sect=inner_nav_sect)
    page.setStyleSheet(style_nav_sect_default)
    page.setLayout(page_layout)
    return page
  
  
  def core_sect_merge_tables(self) -> QFrame:
    #  components
    table_select_container = self.build_select_table_container()
    method_select_container = self.build_select_method_container()
    output_merge_container = self.build_output_merge_container()
    reset_container = self.app.comp_fact.build_reused_single_btn_box(target_title="D. Reset Options",
                                                                     target_statement=None,
                                                                     target_btn_text="Reset",
                                                                     target_btn_event=lambda: self.app.merge_cont.reset_merge_page())
    #  outer
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    core_sect = QFrame()
    core_sect_layout = QVBoxLayout()
    core_sect_layout.addWidget(table_select_container)
    core_sect_layout.addWidget(method_select_container)
    core_sect_layout.addWidget(output_merge_container)
    core_sect_layout.addWidget(reset_container)
    core_sect_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft) 
    core_sect_layout.setSpacing(24)
    core_sect_layout.setContentsMargins(0, 8, 0, 0) 
    core_sect.setLayout(core_sect_layout)
    scroll.setStyleSheet(style_tab_scroll)
    scroll.setWidget(core_sect)
    return scroll
  
  
  #  METHODS -  CONTAINERS
  
  def build_select_table_container(self) -> QWidget:
    #  components - title
    title_lb = self.app.comp_fact.build_label(lb_text="A. Select Tables", 
                                              lb_type="h3")
    #  components - dropdowns
    dd_sect_left = self.build_table_opt_box(target_dropdown="dd_table",
                                            target_lb="1. Left Table",
                                            target_tb="left")
    dd_sect_right = self.build_table_opt_box(target_dropdown="dd_table",
                                             target_lb="2. Right Table",
                                             target_tb="right")
    table_opt_box_left = dd_sect_left["box"]
    table_opt_box_right = dd_sect_right["box"]
    #  update temporary dropdown state
    self.dd_table_left = dd_sect_left["dd_table"]
    self.dd_table_right = dd_sect_right["dd_table"]
    self.dd_column_left = dd_sect_left["dd_column"]
    self.dd_column_right = dd_sect_right["dd_column"]
    
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.addWidget(title_lb, alignment=Qt.AlignLeft)
    frame_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft) 
    frame_layout.setSpacing(8)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame_layout.addWidget(table_opt_box_left) 
    frame_layout.addWidget(table_opt_box_right) 
    frame.setLayout(frame_layout)
    return frame
  
  
  def build_select_method_container(self) -> QWidget:
    #  components
    title_lb = self.app.comp_fact.build_label(lb_text="B. Select Methods", 
                                              lb_type="h3")
    radio_group = self.app.comp_fact.build_radio_group(target_list=list(MERGE_METHOD_OPT.values()),
                                                       target_event=lambda text, checked: self.app.merge_cont.manage_method_radio_event(target_txt=text),
                                                       is_horizontal=False)["widget"]
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.addWidget(title_lb, alignment=Qt.AlignLeft)
    frame_layout.addWidget(radio_group)
    frame_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft) 
    frame_layout.setSpacing(8)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame.setLayout(frame_layout)
    return frame
  
  
  def build_output_merge_container(self) -> QWidget:
    #  components
    lb_title = self.app.comp_fact.build_label(lb_text="C. Merge Output", 
                                              lb_type="h3",
                                              lb_txtcolor=THEME_COLOR["primary"])
    opt_grid = self.build_ouput_opt_grid()
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.addWidget(lb_title, alignment=Qt.AlignLeft)
    frame_layout.addWidget(opt_grid)
    frame_layout.setSpacing(8)
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame.setLayout(frame_layout)
    return frame
  
  
  #  METHODS -  BOXES
  
  def build_table_opt_box(self, target_dropdown: str, target_lb: str, target_tb: str) -> QWidget:
    
    lb_box = self.app.comp_fact.build_label(lb_text=target_lb, 
                                            lb_type="h3",
                                            lb_txtcolor=THEME_COLOR["mid"])
    lb_table = self.app.comp_fact.build_label(lb_text="Selected Table", 
                                              lb_type="p",
                                              lb_txtcolor=THEME_COLOR["mid"])
    lb_column = self.app.comp_fact.build_label(lb_text="Selected Column", 
                                               lb_type="p",
                                               lb_txtcolor=THEME_COLOR["mid"])
    dd_table = self.app.comp_fact.build_dropdown(target_options=["--- Please Select ---"], 
                                                 target_default=0,
                                                 event=lambda text: self.app.merge_cont.manage_dd_table_event(target_tb=target_tb, 
                                                                                                              selected_text=text))
    dd_column = self.app.comp_fact.build_dropdown(target_options=["--- Please Select ---"], 
                                                  target_default=0,
                                                  event=lambda text: self.app.merge_cont.manage_dd_col_event(target_tb=target_tb, 
                                                                                                             selected_text=text))
    btn_preview = self.app.comp_fact.build_btn(btn_text="Preview",
                                               btn_event=lambda checked: self.app.merge_cont.preview_selected_table(target_tb=target_tb),
                                               btn_bgcolor=THEME_COLOR["white"],
                                               btn_txtcolor=THEME_COLOR["primary"],
                                               btn_hover_bgcolor=THEME_COLOR["white_hvr"])
    #  ==== testing ====
    self.app.comp_fact.refresh_dropdowns(target_dd=dd_table,
                                         target_event=lambda: self.app.merge_cont.deliver_dd_opts(target_tb=target_tb, 
                                                                                                  target_dropdown=target_dropdown))
    #  box
    grid = QWidget()
    grid_layout = QGridLayout()
    grid_layout.setHorizontalSpacing(20)
    grid_layout.setVerticalSpacing(0)
    grid_layout.setContentsMargins(0, 0, 0, 0) 
    grid_layout.addWidget(lb_table, 0, 0, alignment=Qt.AlignBottom)
    grid_layout.addWidget(lb_column, 0, 1, alignment=Qt.AlignBottom) 
    grid_layout.addWidget(dd_table, 1, 0)
    grid_layout.addWidget(dd_column, 1, 1)
    grid_layout.addWidget(btn_preview, 1, 2, alignment=Qt.AlignCenter)
    grid_layout.setColumnStretch(0, 1)
    grid_layout.setColumnStretch(1, 1)
    grid_layout.setColumnStretch(2, 1)
    grid.setLayout(grid_layout)
    #  frame
    frame = QWidget()
    frame_layout = QVBoxLayout()
    frame_layout.setContentsMargins(0, 0, 0, 0)
    frame_layout.setSpacing(4)
    frame_layout.addWidget(lb_box, alignment=Qt.AlignLeft)
    frame_layout.addWidget(grid)
    frame.setLayout(frame_layout)
    return {"box": frame, "dd_table": dd_table, "dd_column": dd_column}
  
  
  def build_ouput_opt_grid(self): 
    # components
    box_preview = self.app.comp_fact.preview_comp_box(lb_text="",
                                                     btn_text="Preview",
                                                     btn_event=lambda: self.app.merge_cont.preview_merge_df())   
    box_merge = self.app.comp_fact.preview_comp_box(lb_text="",
                                                     btn_text="Merge",
                                                     btn_event=lambda: self.app.merge_cont.execute_merge_df())
    #  frame
    grid = QWidget()
    grid_layout = QGridLayout()
    grid_layout = QGridLayout()
    grid_layout.setHorizontalSpacing(28)
    grid_layout.setContentsMargins(0, 0, 0, 0)
    grid_layout.setColumnStretch(0, 0)
    grid_layout.setColumnStretch(1, 0)
    grid_layout.addWidget(box_preview, 0, 0)
    grid_layout.addWidget(box_merge, 0, 1)
    grid_layout.setSizeConstraint(QLayout.SetFixedSize)
    grid.setLayout(grid_layout)
    return grid
  
  
  #  REFRESH
  
  def update_dd_col(self, target_tb: str, options: list):
    if target_tb == "left":
      dropdown = self.dd_column_left
    elif target_tb == "right":
      dropdown = self.dd_column_right
    else:
        return
    dropdown.blockSignals(True)
    dropdown.clear()
    dropdown.addItems(options)
    dropdown.setCurrentIndex(0)
    dropdown.blockSignals(False)
  
  
  def reset_display(self):
    #  Learnt: need to close exclusive first, and re-activate it for new visual
    for dropdown in self.dropdown_groups:
      dropdown.setExclusive(False)
    for btn in self.radio_btn_list:
      btn.blockSignals(True)
      btn.setChecked(False)
      btn.blockSignals(False)
    for group in self.radio_groups:
      group.setExclusive(True)
      
      