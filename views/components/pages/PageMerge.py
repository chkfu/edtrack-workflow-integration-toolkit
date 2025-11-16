from PyQt5.QtWidgets import QWidget, QGridLayout
from views.components.config.views_styles import style_nav_sect_default
from views.components.pages.PageTemplate import PageTemplate


#  CLASS


class PageMerge(PageTemplate):
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    super().__init__(app_ref)
    print("[PageMerge] initialised successfully.")
    
    
  #  METHODS
  
  def merge_sections(self):
    #  title section
    inner_title_sect = self.create_title_sect(sect_title="Step 3: Merge Tables", 
                                                sect_des="This step refines the imported dataset by handling missing values, correcting data types, and preparing it for further analysis.")
    #  statistic section
    inner_stat_sect = self.create_stat_sect(target_page=3)
    #  nav section
    inner_nav_sect = self.create_nav_sect(enable_back=True, enable_next=True)
    
    #  Work Panel Grid
    page = QWidget()
    page_layout = QGridLayout()
    page_layout = self.reuse_page_setting(inner_title_sect=inner_title_sect,
                                           inner_stat_sect=inner_stat_sect,
                                           inner_nav_sect=inner_nav_sect)
    page.setStyleSheet(style_nav_sect_default)
    page.setLayout(page_layout)
    return page