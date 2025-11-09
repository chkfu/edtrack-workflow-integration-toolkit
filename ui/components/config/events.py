from PyQt5.QtWidgets import (
    QApplication
)



#  METHODS - APP OPERATION
#  learnt: use app_instance replaced self, as self cannot be read outside class

def event_reset_app(app_ref) -> None:
    #  asking
    res = app_ref.comp_fact.build_msg_box(
        app_window=app_ref.window,
        title="Reset",
        question="Are you sure you want to reset the appplication?\n\nCurrent data will be lost after reset."
      )
    if res:
      #  removal
      app_ref.curr_stage = "STEP_1"
      app_ref.df_users = None
      app_ref.df_activities = None
      app_ref.df_components = None
      app_ref.df_processed = None
      app_ref.df_merged = None
      app_ref.df_pivot = None
    #  confirmation
      app_ref.comp_fact.build_reminder_box(app_window=app_ref.window,
                                        title="Confirmation",
                                        txt_msg="The application has been reset.")


def event_close_app(app_ref) -> None:
  res = app_ref.comp_fact.build_msg_box(
        app_window=app_ref.window,
        title="Exit",
        question="Are you sure you want to quit?"
      )
  if res:
    QApplication.quit()
  
  
def event_back_btn(app_ref) -> None:
  #  false cases
  validate_qstacks(app_ref)
  #  get variables
  curr_page = app_ref.page_stack.currentIndex()
  curr_step = app_ref.step_stack.currentIndex()
  #  execution
  if curr_page > 0 and curr_step > 0:
        app_ref.page_stack.setCurrentIndex(curr_page-1)
        app_ref.step_stack.setCurrentIndex(curr_step-1)
  else:
    app_ref.comp_fact.build_reminder_box(app_window=app_ref.window,
                                        title="Error",
                                        txt_msg="Already at the first page or step.")
    
    
def event_next_btn(app_ref) -> None:
  #  false cases
  validate_qstacks(app_ref)
  #  get variables
  total_pages = app_ref.page_stack.count()
  total_steps = app_ref.step_stack.count()
  curr_page = app_ref.page_stack.currentIndex()
  curr_step = app_ref.step_stack.currentIndex()
  #  execution
  if curr_page < total_pages - 1 and curr_step < total_steps - 1:
    app_ref.page_stack.setCurrentIndex(curr_page+1)
    app_ref.step_stack.setCurrentIndex(curr_page+1)
  else:
    app_ref.comp_fact.build_reminder_box(app_window=app_ref.window,
                                        title="Error",
                                        txt_msg="Application failed to switch next steps and pages.")
  
def event_done_btn(app_ref) -> None:
  #  false cases
  validate_qstacks(app_ref)
  #  execution
  app_ref.page_stack.setCurrentIndex(0)
  app_ref.step_stack.setCurrentIndex(0)
  
  
  
  
#  SUPPORTING METHODS

def validate_qstacks(app_ref) -> None:  
  
  if app_ref.page_stack is None or app_ref.step_stack is None:
    app_ref.comp_fact.build_reminder_box(app_window=app_ref.window,
                                        title="Error",
                                        txt_msg="Step and page storage is not found.")
  if app_ref.page_stack.count() < 1 or app_ref.step_stack.count() < 1:
    app_ref.comp_fact.build_reminder_box(app_window=app_ref.window,
                                        title="Error",
                                        txt_msg="Step and page storage is empty.")