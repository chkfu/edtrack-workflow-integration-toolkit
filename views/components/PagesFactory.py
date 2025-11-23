import logging
from views.components.pages import PageImport, PageClean, PageMerge, PageAnalyse
from PyQt5.QtWidgets import QLabel



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
    # #  store temp tables
    # self.temp_table_user: pd.DataFrame = None
    # self.temp_table_activity: pd.DataFrame = None
    # self.temp_table_component: pd.DataFrame = None
    #  store temp labels (for reset)
    #  learnt: emb to render the state again, unlike declared variables
    self.temp_label_users: QLabel = None
    self.temp_label_activities: QLabel = None
    self.temp_label_components: QLabel = None
    #  activate pages classes
    self.page_import = PageImport(app_ref)
    self.page_clean = PageClean(app_ref)
    self.page_merge = PageMerge(app_ref)
    self.page_analyse = PageAnalyse(app_ref)
    #  log
    logger.info("initialised successfully.") 
