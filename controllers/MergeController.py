import logging
import pandas as pd
from controllers.ValidController import ValidController
from models.DataManager import DataManager
from views.components.config.views_config import MERGE_METHOD_OPT


#  LOGGING

logger = logging.getLogger("MERGE_CONTROLLER")


# CLASS

class MergeController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    self.temp_merge_dataset: pd.DataFrame | None = None
    self.manage_model = DataManager()
    self.valid_cont = ValidController()
    logger.info("initialised sucessfully.")
    
    
  #  METHODS - VISUAL CHANGES
  
  def deliver_dd_opts(self, target_dropdown: str, target_tb: str) -> list:
    decision = target_dropdown.strip().lower()
    if decision == "dd_table":
        return self.deliver_table_opts(target_tb=target_tb)
    elif decision == "dd_column":
        return self.deliver_col_opts(target_tb=target_tb)
    else:
      logger.warning(f"Failed to identify dropdown list options - {target_dropdown}",
                   exc_info=True)
    return []
      
    
  def deliver_table_opts(self, target_tb: str) -> list:    
    table_opts: list = ["--- Please Select ---"]
    #  for single raw / cleaned dataframe - user_df, activity_df, component_df
    for data_state in self.app.clean_state.dataset_states.values():
      if data_state.data_clean is not None or data_state.data_raw is not None:
        table_opts.append(data_state.state_name)
        print(data_state.state_name)
    #  for merged dataframe
    if self.app.merge_state.merge_raw is not None:
      table_opts.append("Dataset - Merged")
      print("dataset - merged")
    return table_opts
    
    
  def deliver_col_opts(self, target_tb: str) -> list:
    tb_opt: str = str(target_tb).strip().lower()
    dd_list: list = ["--- Please Select ---"]
    #  check the temporary table
    if tb_opt not in ["left", "right"]:
      logger.error(f"Failed to display column dropdowns for invalid table to be selected - {target_tb}",
                   exc_info=True)
      # remarks: remind to return empty list, even failed
      return dd_list
    #  check table and get corresponding columns
    if tb_opt == "left" and self.app.merge_state.target_ltable is not None:
      dd_list += list(self.app.merge_state.target_ltable.columns)
    elif tb_opt == "right" and self.app.merge_state.target_rtable is not None:
      dd_list += list(self.app.merge_state.target_rtable.columns)
    return dd_list
  
  
  #  METHODS - EVENTS
  
  def preview_selected_table(self, target_tb: str) -> None:
    #  declaration
    target_df: pd.DataFrame | None = None
    target_tb_r: str = target_tb.strip().lower()
    #  error handling
    if target_tb_r not in ["left", "right"]:
      logger.warning(f"The selected table cannot be identified. Preview failed - {target_tb}",
                     exc_info=True)
      return self.app.comp_fact.build_reminder_box(title="Error", 
                                                   txt_msg="Please ensure left and right tables have been selected.")
    #  identify pop-up dataframe
    if target_tb_r == "left":
      target_df = self.app.merge_state.target_ltable
    if target_tb_r == "right":
      target_df = self.app.merge_state.target_rtable
    #  build pop-up window
    if target_df is not None and not target_df.empty:
      return self.app.comp_fact.build_popup_wd(wd_title="Preview Table Options",
                                               target_df=target_df,
                                               popup_title=f"{target_tb_r} Table".title(),
                                               popup_content=self.app.comp_fact.build_table_view(target_df=target_df))
    return self.app.comp_fact.build_reminder_box(title="Error", 
                                                 txt_msg="Please ensure left and right tables have been selected.")
  
  
  def manage_dd_table_event(self, target_tb: str, selected_text: str) -> None:
    #  error handling
    if selected_text == "--- Please Select ---":
      return
    #  get clean dataframe, if not raw.  otherwise, apss
    clean_state = self.app.clean_state.get_spec_dataframe(target_name=selected_text)
    if clean_state is None:
        return
    if clean_state.data_clean is not None:
      dataframe = clean_state.data_clean
    elif clean_state.data_raw is not None:
      dataframe = clean_state.data_raw
    else: 
      return
    # update
    if target_tb == "left":
      self.app.merge_state.target_ltable = dataframe
      self.app.merge_state.target_lcol = None
    elif target_tb == "right":
      self.app.merge_state.target_rtable = dataframe
      self.app.merge_state.target_rcol = None
    else:
      return
    #  Learnt: new method to force refresh dropdown UI by clicks
    opts = self.deliver_col_opts(target_tb)
    self.app.pages_fact.page_merge.update_dd_col(target_tb, opts)
  
  
  def manage_dd_col_event(self, target_tb: str, selected_text: str) -> None:
    if selected_text == "--- Please Select ---":
      return
    if target_tb == "left":
      self.app.merge_state.target_lcol = selected_text
    elif target_tb == "right":
      self.app.merge_state.target_rcol = selected_text
    else:
      return
  
  
  def manage_method_radio_event(self, target_txt: str) -> None:
    #  if not matched, pass
    if target_txt not in MERGE_METHOD_OPT.values():
      logger.error(f"The selected merge method is not invalid - {target_txt}.",
                   exc_info=True)
      return
    #  if matched, return recognisable merge method
    target_method: str = next(key for key, value in MERGE_METHOD_OPT.items()
                              if value == target_txt)
    self.app.merge_state.target_method = target_method
  
  
  def execute_merge_df(self) -> None:
    #  declaration
    temp_ltable: pd.DataFrame | None = self.app.merge_state.target_ltable
    temp_rtable: pd.DataFrame | None = self.app.merge_state.target_rtable
    temp_lcol: str | None = self.app.merge_state.target_lcol
    temp_rcol: str | None = self.app.merge_state.target_rcol
    temp_method: str | None = self.app.merge_state.target_method
    #  1a. validation - table cannot be empty
    if temp_ltable is None or temp_rtable is None or temp_ltable.empty or temp_rtable.empty:
      err_msg: str = "The selected left or right table are missing or empty. Unable to proceed merge."
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=err_msg)
      logger.warning(err_msg, exc_info=True)
      return
    #  1b. validation - merger parameter must be all valid
    if temp_lcol is None or temp_rcol is None or temp_method is None:
      err_msg: str = "Failed to merge table with potential missing parameters."
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=err_msg)
      logger.warning(err_msg, exc_info=True)
      return
    #  1c. validation - left and right table cannnot be the same
    if temp_ltable.equals(temp_rtable):
      err_msg: str = "The same table has been mistakenly selected for both tables to be merged."
      self.app.comp_fact.build_reminder_box(title="Error",
                                            txt_msg=err_msg)
      logger.warning(err_msg, exc_info=True)
      return
    
    #  merge table
    merged_df = self.manage_model.merge_tables(target_df_left=temp_ltable, 
                                               target_df_right=temp_rtable, 
                                               target_col_left=temp_lcol, 
                                               target_col_right=temp_rcol, 
                                               merge_type=temp_method)
    self.app.merge_state.set_merge_raw(merged_df)
    merge_raw = self.app.merge_state.merge_raw
    #  build pop-up window
    if merge_raw is not None and not merge_raw.empty:
      return self.app.comp_fact.build_popup_wd(wd_title="Preview Table Options",
                                               target_df=merge_raw,
                                               popup_title=f"Merged Table".title(),
                                               popup_content=self.app.comp_fact.build_table_view(target_df=merge_raw))
    err_msg: str = "Please ensure merged tables have been selected."
    self.app.comp_fact.build_reminder_box(title="Error", 
                                          txt_msg=err_msg)
    logger.warning(err_msg)
    
    
  def reset_merge_page(self) -> None:
    #  TODO: UI is required to be reset
    self.temp_merge_dataset = None
    self.merge_state.reset_merge_ds()
    print("activated on reset merge page method")