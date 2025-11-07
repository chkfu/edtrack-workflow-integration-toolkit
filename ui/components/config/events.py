from PyQt5.QtWidgets import (
    QApplication
)
from ui.components.ComponentsFactory import ComponentsFactory


#  METHODS - APP OPERATION
#  learnt: use app_instance replaced self, as self cannot be read outside class
def event_reset_app(app_instance) -> None:
    #  asking
    res = app_instance.comp_fact.build_msg_box(
        app_window=app_instance.window,
        title="Reset",
        question="Are you sure you want to reset the appplication?\n\nCurrent data will be lost after reset."
      )
    if res:
      #  removal
      app_instance.curr_stage = "STEP_1"
      app_instance.df_users = None
      app_instance.df_activities = None
      app_instance.df_components = None
      app_instance.df_processed = None
      app_instance.df_merged = None
      app_instance.df_pivot = None
    #  confirmation
      app_instance.comp_fact.build_reminder_box(app_window=app_instance.window,
                                        title="Confirmation",
                                        txt_msg="The application has been reset."
                                        )


def event_close_app(app_instance) -> None:
  res = app_instance.comp_fact.build_msg_box(
        app_window=app_instance.window,
        title="Exit",
        question="Are you sure you want to quit?"
      )
  if res:
    QApplication.quit()