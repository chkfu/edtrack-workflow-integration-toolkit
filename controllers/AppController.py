"""
This controller manages the application's lifecycle.
It bridges the UI interface and the deeper application logic,
exercising the event instruction to normal applicaiton's rountine.
"""

from PyQt5.QtWidgets import QApplication


#  CLASS

class AppController:
  
  #  CONSTRUCTOR
  def __init__(self, app_ref):
    self.app = app_ref
    print("[AppController] initialised sucessfully.")


  #  MEHTODS
  
  def reset_app(self) -> None:
    """ USE: empty the state memories and application workflow """
    
    try:
        #  asking
        res = self.app.comp_fact.build_msg_box(title="Reset",
                                              question="Are you sure you want to reset the appplication?\n\nCurrent data will be lost after reset."
          )
        if res:
          #  state: UIApplication reset
          self.app.df_users = None
          self.app.df_activities = None
          self.app.df_components = None
          self.app.df_processed = None
          self.app.df_merged = None
          self.app.df_pivot = None
          #  state: PagesFactory reset
          self.app.pages_fact.temp_path_user = None
          self.app.pages_fact.temp_path_activity = None
          self.app.pages_fact.temp_path_comp = None
          self.app.pages_fact.temp_table_user = None
          self.app.pages_fact.temp_table_activity = None
          self.app.pages_fact.temp_table_component = None
          #  reset temp state in import page
          self.app.pages_fact.page_import.page_refresh()
          #  follow-up event
          self.app.page_stack.setCurrentIndex(0)
        
          # update task list
          self.app.nav_cont.update_workflow(target_action="reset", 
                                            curr_page=0)
        
          #  confirmation
          self.app.comp_fact.build_reminder_box(title="Confirmation",
                                                txt_msg="The application has been reset.")
        
    except Exception as ex:
      raise SystemError(f"{ex}")


  def close_app(self) -> None:
    """ USE: instruct to close the application in preferred way """
    try:
      res = self.app.comp_fact.build_msg_box(title="Exit",
                                            question="Are you sure you want to quit?")
      if res:
        QApplication.quit()
    except Exception as ex:
      raise SystemError(f"{ex}")
    