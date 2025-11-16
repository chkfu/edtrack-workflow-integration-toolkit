import sys
from PyQt5.QtWidgets import QApplication, QWidget
from views.components import ComponentsFactory, LayoutFactory, PagesFactory
from controllers import AppController, NavController, FileController
from core import DataLoader


#  CLASS

class UserInterface:
  
  def __init__(self):
    
    #  setup this app
    self.app = None
    self.window = None
    
    #  setup factory classes
    """ 
    Reminder: set None, prevent access controller or components before
              application initialised
    """
    self.comp_fact = None
    self.layout_fact = None
    self.pages_fact = None
    
    #  setup pipeline
    self.data_loader = DataLoader()
    
    #  setup controllers
    self.app_cont = AppController(self)
    self.nav_cont = NavController(self)
    self.file_cont = FileController(self)
    
    #  setup datasets
    self.df_users = None
    self.df_activities = None
    self.df_components = None
    self.df_processed = None
    self.df_merged = None

    
    
  #  METHODS - SETUP
    
  def setup_app(self) -> None:
    #  allow child class to use parent constructors
    self.app = QApplication(sys.argv)
    #  setup child classes
    self.comp_fact = ComponentsFactory(app_ref=self)
    self.pages_fact = PagesFactory(app_ref=self)
    self.layout_fact = LayoutFactory(app_ref=self)
    #  setup the stacks for transitional views
    self.page_stack = self.layout_fact.page_stack

  def finalise_app(self, widget: QWidget) -> None:
    widget.show()
    sys.exit(self.app.exec_())    
  
  
  #  EXECUTION
  
  def run_app(self) -> None:
    
    try:  
      #  prepare ui
      self.setup_app()
      widget_window = self.layout_fact.create_window()
      self.finalise_app(widget=widget_window)
      
    except Exception as ex:
      self.comp_fact.build_reminder_box(title="Error",
                                        txt_msg="Error 500: Please contact the administrator for your further action.")
      raise SystemError(f"{ex}")