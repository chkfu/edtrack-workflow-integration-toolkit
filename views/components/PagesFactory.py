import logging
from views.components.pages import (
  PageImport, PageClean, PageMerge, PageFE, PageAnalyse
)
from PyQt5.QtWidgets import QLabel
from views.components.config.views_config import DATASET_LIST



#  LOGGER

logger = logging.getLogger("PAGES_FACTORY")


#  CLASS

class PagesFactory:
  
  #  Constructor
  
  def __init__(self, app_ref):
    super().__init__()
    #  setup ref states
    self.app = app_ref 
    #  store temp paths
    self.temp_path_users: str = None
    self.temp_path_activities: str = None
    self.temp_path_components: str = None
    #  store temp labels (for reset)
    #  learnt: emb to render the state again, unlike declared variables
    self.temp_label_users: QLabel = None
    self.temp_label_activities: QLabel = None
    self.temp_label_components: QLabel = None
    #  activate pages classes
    self.page_import = PageImport(app_ref)
    self.page_clean = PageClean(app_ref,
                                target_ds_list=[item["data"] for item in DATASET_LIST[1:4]])
    self.page_merge = PageMerge(app_ref)
    self.page_feateng = PageFE(app_ref)
    self.page_analyse = PageAnalyse(app_ref)
    #  log
    logger.info("initialised successfully.") 
