"""
This controller manages UI navigation with the changes of steps.
It bridges the UI events and the application's state changes, applying
preferred logic into user workflow.
"""


from views.components.config.views_config import STEP_NAME_LIST
import logging

#  LOGGING

logger = logging.getLogger("NAV_CONTROLLER")


#  CLASS

class NavController:
  
  #  CONSTRUCTOR
  def __init__(self, app_ref):
    self.app = app_ref
    logger.info("[NavController] initialised sucessfully.")


  #  MEHTODS
  
  def back_btn(self) -> None:
    """ USE: navigate to go to previous workflow step"""
    
    #  false cases
    self.validate_qstacks()
    #  get variables
    curr_page = self.app.page_stack.currentIndex()
    #  execution
    if curr_page > 0:
          self.app.page_stack.setCurrentIndex(curr_page-1)
    else:
      self.app.comp_fact.build_reminder_box(title="Error",
                                          txt_msg="Already at the first page or step.")
    #  update task list
    self.update_workflow(target_action="back", 
                         curr_page=curr_page)
    #  refresh sidebar list status
    self.app.layout_fact.refresh_db_sect()
    
    
  def next_btn(self) -> None:
    """ USE: navigate to go to next workflow step"""

    #  false cases
    self.validate_qstacks()
    #  get variables
    total_pages = self.app.page_stack.count()
    curr_page = self.app.page_stack.currentIndex()
    #  execution
    if curr_page < total_pages - 1:
      #  step-specific validation before proceeding
      if not self._validate_step_before_next(curr_page):
        return
      self.app.page_stack.setCurrentIndex(curr_page+1)
      if curr_page == 3:    #  Remarks: PageFE's button trigger PageAnalyse rendering
        self.app.analyse_cont.rebuild_metrics_val_cell()
    else:
      self.app.comp_fact.build_reminder_box(title="Error",
                                          txt_msg="Application failed to switch next steps and pages.")
    #  update tasks list
    self.update_workflow(target_action="next",
                         curr_page=curr_page)
    #  refresh sidebar list status
    self.app.layout_fact.refresh_db_sect()


  def _validate_step_before_next(self, curr_page: int) -> bool:
    """ USE: validate step-specific conditions before allowing navigation to next page.
        Returns True if navigation should proceed, False to block. """

    #  Step 1 (page 0): at least one dataset must be loaded
    if curr_page == 0:
      validity = self.app.clean_state.get_clean_ds_validity()
      if not any(validity.values()):
        self.app.comp_fact.build_reminder_box(
          title="Warning",
          txt_msg="Please select at least one dataset before proceeding.")
        return False

    #  Step 2 (page 1): confirm if no dataset has been cleaned
    elif curr_page == 1:
      any_cleaned = any(
        ds.data_clean is not None
        for ds in self.app.clean_state.dataset_states.values()
      )
      if not any_cleaned:
        confirmed = self.app.comp_fact.build_msg_box(
          title="Confirmation",
          question="Are you sure to proceed further without cleaning any dataset?")
        if not confirmed:
          return False

    #  Step 3 (page 2): merge must be completed
    elif curr_page == 2:
      if self.app.merge_state.merge_raw is None:
        self.app.comp_fact.build_reminder_box(
          title="Warning",
          txt_msg="Please complete the dataset merge before proceeding.")
        return False

    #  Step 4 (page 3): confirm if no feature engineering was applied
    elif curr_page == 3:
      merge_raw = self.app.merge_state.merge_raw
      merge_proc = self.app.merge_state.merge_proc
      fe_applied = (
        merge_proc is not None and merge_raw is not None and
        (list(merge_proc.columns) != list(merge_raw.columns) or
         merge_proc.shape != merge_raw.shape)
      )
      if not fe_applied:
        confirmed = self.app.comp_fact.build_msg_box(
          title="Confirmation",
          question="Are you sure to proceed further without applying any feature engineering?")
        if not confirmed:
          return False

    return True
      
      
  def validate_qstacks(self) -> None:
    """ USE: check whether the pages workflow has been initialised. """
    
    if self.app.page_stack is None:
      logger.error("Page stack is not found. Failed to operate the step flow.")
      self.app.comp_fact.build_reminder_box(title="Error",
                                          txt_msg="Page storage is not found.")
    if self.app.page_stack.count() < 1:
      logger.error("No page is not found. Failed to operate the step flow.")
      self.app.comp_fact.build_reminder_box(title="Error",
                                          txt_msg="Page storage is empty.")
      

  def update_workflow(self, 
                      target_action: str,
                      curr_page: int) -> None:
    """ USE: apply the core navigation logic for workflow changes. """
    
    step_total: int = len(STEP_NAME_LIST)
    target_action_r = target_action.strip().lower()
    
    #  error handling
    if target_action_r not in ["back", "next", "reset"]:
      logger.warning("the instructed navigation is not in the option. Unable to execute.")
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
    list = self.app.layout_fact.task_list_widget
    for index in range(list.count()):
      item = STEP_NAME_LIST[index]
      txt = f"🟢 {item['step']}" if item["visited"] else f"🔴 {item['step']}"
      list_item = list.item(index)
      label_widget = list.itemWidget(list_item)
      if label_widget:
          label_widget.setText(txt)