import sys
import os
import logging
from PyQt5.QtWidgets import QApplication, QWidget
from models import SQLConnector
from views.components import ComponentsFactory, LayoutFactory, PagesFactory
from controllers import (
  AppController, NavController, FileController, CleanController, MergeController,
  FEController, AnalyseController, ValidController
)
from states import CleanState, MergeState, AnalyseState
from dotenv import load_dotenv



#  ENVIRONMENT
load_dotenv(dotenv_path="config.env")


#  LOGGER

logger = logging.getLogger("USER_INTERFACE")


#  CLASS

class UserInterface:
  
  def __init__(self):
    
    #  setup this app
    #  Remarks: either setup QApplication at first, or setup other components in another function
    #           the order of QApplication always superior than others
    self.app = QApplication(sys.argv)
    self.window = None
    
    
    #  setup state
    self.clean_state = CleanState()
    self.merge_state = MergeState()
    self.analyse_state = AnalyseState()
    
    #  setup controllers
    self.app_cont = AppController(self)
    self.nav_cont = NavController(self)
    self.valid_cont = ValidController()
    self.file_cont = FileController(self)
    self.clean_cont = CleanController(self)
    self.merge_cont = MergeController(self)
    self.fe_cont = FEController(self)
    self.analyse_cont = AnalyseController(self)
    
    #  setup factory classes
    """ 
    Reminder: set None, prevent access controller or components before
              application initialised
    """
    #  Learnt: from less dependent to most dependent, prevent initialising conflicts
    #          (i.e. create before lower layer exists - nothing to be created)
    self.comp_fact = ComponentsFactory(app_ref=self)
    self.pages_fact = PagesFactory(app_ref=self)
    self.layout_fact = LayoutFactory(app_ref=self)
    
    #  setup pipeline
    self.sql_connector = SQLConnector(host=os.getenv("DB_HOST"),
                                      user=os.getenv("DB_USER"),
                                      password=os.getenv("DB_PW"),
                                      database = os.getenv("DB_NAME"),
                                      port= os.getenv("DB_PORT"))
    #  setup page stack
    self.page_stack = self.layout_fact.page_stack

    

  def finalise_app(self, widget: QWidget) -> None:
    widget.show()
    sys.exit(self.app.exec_())    
  
  
  #  EXECUTION
  
  def run_app(self) -> None:
    
    try:  
      #  prepare ui
      widget_window = self.layout_fact.create_window()
      self.finalise_app(widget=widget_window)
      logger.info("User Interface started to run sucessfully.")
      
    except Exception as ex:
      logger.error("User Interface crashed", exc_info=True)
      self.comp_fact.build_reminder_box(title="Error",
                                        txt_msg="Please contact the administrator for your further action.")
      raise SystemError(f"{ex}")