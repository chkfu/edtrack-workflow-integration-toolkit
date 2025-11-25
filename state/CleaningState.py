import pandas as pd
import logging
from state.DatasetState import DatasetState
from views.components.config.views_config import DATASET_LIST


#  CLASS

#  Learnt: managing different datasets, for cleaning options
#          centialised control in CleanState
class CleaningState:
  
  def __init__(self):
    
    #  setup DatasetState to be managed
    self.ds_users = DatasetState()
    self.ds_activities = DatasetState()
    self.ds_components = DatasetState()
    
    #  identify curr state
    opt_list = [item["data"] for item in DATASET_LIST[1:4]]
    self.clean_target = opt_list[0]
    
    #  methods - switching datasets
    def get_clean_target(self) -> str:
      if self.clean_target == opt_list[0]:
        return self.ds_users
      elif self.clean_target == opt_list[1]:
        return self.ds_activities
      elif self.ds_components == opt_list[2]:
        return self.ds_components
      else:
        raise ValueError("Data cleaning target is not found.")
    
    
    def set_clean_target(self, target_ds: str)  -> None:
      target_ds_r = str(target_ds).strip().lower()
      if target_ds not in ["users", "activities", "components"]:
        raise ValueError("Invalid datasetState option cannot be set.")
      self.clean_target = target_ds_r
      
    
    #  methods - reset
    def reset_all_ds(self):
      self.users.reset_ds()
      self.activities.reset_ds()
      self.components.reset_ds()