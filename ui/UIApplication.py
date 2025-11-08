import sys
from PyQt5.QtWidgets import QApplication, QWidget
from ui.components.ComponentsFactory import ComponentsFactory
from ui.components.LayoutFactory import LayoutFactory



#  CLASS

class UIApplication:
  
  def __init__(self):
    #  app
    self.app = None
    self.window = None
    #  class
    self.comp_fact = None
    self.layout_fact = None
    #  datasets
    self.curr_stage = "STEP_1"
    self.df_users = None
    self.df_activities = None
    self.df_components = None
    self.df_processed = None
    self.df_merged = None
    self.df_pivot = None
    
    
  #  METHODS - SETUP
    
  def setup_app(self) -> None:
    self.app = QApplication(sys.argv)
    self.comp_fact = ComponentsFactory()
    self.layout_fact = LayoutFactory(app_ref=self)

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
      raise Exception(f"[UIApplication] failed to disaply UI application: {ex}")
