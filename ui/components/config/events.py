from PyQt5.QtWidgets import (
    QApplication, QLabel
)
from ui.components.config.config import STEP_NAME_LIST



#  METHODS - APP OPERATION
#  learnt: use app_instance replaced self, as self cannot be read outside class

def event_reset_app(app_ref) -> None:
  try:
      #  asking
      res = app_ref.comp_fact.build_msg_box(title="Reset",
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
        app_ref.comp_fact.build_reminder_box(title="Confirmation",
                                            txt_msg="The application has been reset.")
      #  follow-up event
      app_ref.page_stack.setCurrentIndex(0)
     
      # update task list
      update_workflow(app_ref, "reset", 0)
      
  except Exception as ex:
    raise SystemError(f"{ex}")


def event_close_app(app_ref) -> None:
  try:
    res = app_ref.comp_fact.build_msg_box(title="Exit",
                                          question="Are you sure you want to quit?")
    if res:
      QApplication.quit()
  except Exception as ex:
    raise SystemError(f"{ex}")
  
  
def event_back_btn(app_ref) -> None:
  #  false cases
  validate_qstacks(app_ref)
  #  get variables
  curr_page = app_ref.page_stack.currentIndex()
  #  execution
  if curr_page > 0:
        app_ref.page_stack.setCurrentIndex(curr_page-1)
  else:
    app_ref.comp_fact.build_reminder_box(title="Error",
                                        txt_msg="Already at the first page or step.")
  #  update task list
  update_workflow(app_ref, "back", curr_page)

  
def event_next_btn(app_ref) -> None:
  #  false cases
  validate_qstacks(app_ref)
  #  get variables
  total_pages = app_ref.page_stack.count()
  curr_page = app_ref.page_stack.currentIndex()
  #  execution
  if curr_page < total_pages - 1:
    app_ref.page_stack.setCurrentIndex(curr_page+1)
  else:
    app_ref.comp_fact.build_reminder_box(title="Error",
                                        txt_msg="Application failed to switch next steps and pages.")
  #  update tasks list
  update_workflow(app_ref, "next", curr_page)
  
  
def update_workflow(app_ref, 
                    target_action: str,
                    curr_page: int) -> None:
  
  step_total: int = len(STEP_NAME_LIST)
  target_action_r = target_action.strip().lower()
  
  #  error handling
  if target_action_r not in ["back", "next", "reset"]:
    return
  
  #  update the static list first
  if target_action_r == "back":
    if curr_page > 0:
      STEP_NAME_LIST[curr_page]["visited"] = False
    
  elif target_action_r == "next":
    if curr_page < step_total - 1:
      STEP_NAME_LIST[curr_page + 1]["visited"] = True
    
  elif target_action_r == "reset":
    for index, item in enumerate(STEP_NAME_LIST):
      new_val = True if index == 0 else False
      item["visited"] = new_val
      
  else: 
    return
  
  #  update the dynamic widget list
  list = app_ref.layout_fact.task_list_widget
  for index in range(list.count()):
    item = STEP_NAME_LIST[index]

    # ✅ 只依據 visited 狀態顯示圖示
    txt = f"🟢 {item['step']}" if item["visited"] else f"🔴 {item['step']}"

    list_item = list.item(index)
    label_widget = list.itemWidget(list_item)
    if label_widget:
        label_widget.setText(txt)
  
#  SUPPORTING METHODS

def validate_qstacks(app_ref) -> None:  
  
  if app_ref.page_stack is None:
    app_ref.comp_fact.build_reminder_box(title="Error",
                                        txt_msg="Page storage is not found.")
  if app_ref.page_stack.count() < 1:
    app_ref.comp_fact.build_reminder_box(title="Error",
                                        txt_msg="Page storage is empty.")