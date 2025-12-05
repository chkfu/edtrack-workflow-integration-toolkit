from PyQt5.QtWidgets import QWidget, QGridLayout
from views.components.pages.PageTemplate import PageTemplate
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
  
  def merge_sections(self):
    #  title section
    inner_title_sect = self.create_title_sect(sect_title="Step 4: Feature Engineering", 
                                                sect_des="This step reads the dataset, checks its structure, and prepares it for cleaning and processing.")
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