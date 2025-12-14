"""
This controller manages the application's lifecycle.
It bridges the UI interface and the deeper application logic,
exercising the event instruction to normal applicaiton's rountine.
"""


import logging
from PyQt5.QtWidgets import QApplication


#  LOGGING
logger = logging.getLogger("APP_CONTROLLER")


#  CLASS

class AppController:
  
  #  CONSTRUCTOR
  def __init__(self, app_ref):
    self.app = app_ref
    logger.info("[AppController] initialised sucessfully.")


  #  MEHTODS
  
  # TODO: reset has not re-detect the sideabr dataset status
  
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
          #  state: PagesFactory reset
          self.app.pages_fact.temp_path_users = None
          self.app.pages_fact.temp_path_activities = None
          self.app.pages_fact.temp_path_components = None
          #  reset temp state in import page
          self.app.pages_fact.page_import.reset_state_pageImport()
          #  follow-up event
          self.app.page_stack.setCurrentIndex(0)
        
          # update task list
          self.app.nav_cont.update_workflow(target_action="reset", 
                                            curr_page=0)
          
          #  confirmation
          self.app.comp_fact.build_reminder_box(title="Confirmation",
                                                txt_msg="The application has been reset.")
          #  refresh sidebar list status
          self.app.layout_fact.refresh_db_sect()
        
    except Exception as ex:
      logger.error(f"{ex}", exc_info=True)
      raise SystemError(f"{ex}")


  def close_app(self) -> None:
    """ USE: instruct to close the application in preferred way """
    try:
      res = self.app.comp_fact.build_msg_box(title="Exit",
                                            question="Are you sure you want to quit?")
      if res:
        QApplication.quit()
    except Exception as ex:
      logger.error(f"{ex}", exc_info=True)
      raise SystemError(f"{ex}")
    