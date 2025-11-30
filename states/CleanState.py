import pandas as pd
import logging
from states.DatasetState import DatasetState
from views.components.config.views_config import DATASET_LIST



#  LOGGING

logger = logging.getLogger("PAGE_MERGE")


#  CLASS

#  Learnt: managing different datasets, for cleaning options
#          centialised control in CleanState
class CleanState:
  
  def __init__(self):
    
    #  identify curr state
    self.opt_list = [item["data"] for item in DATASET_LIST[1:4]]
    self.clean_target = self.opt_list[0]
    
    #  setup DatasetState to be managed
    self.dataset_states = {
      self.opt_list[0]: DatasetState(state_name=self.opt_list[0]),
      self.opt_list[1]: DatasetState(state_name=self.opt_list[1]),
      self.opt_list[2]: DatasetState(state_name=self.opt_list[2])
    }
    
    
  #  methods - switching datasets
  
  def get_clean_target(self):
    return self.dataset_states[self.clean_target]
  
    
  def set_clean_target(self, target_index: int)  -> None:
    #  validate index
    if target_index < 0 or target_index >= len(self.opt_list):
      err_msg: str = "Input index exceed the range of dataset list"
      logger.error(err_msg, exc_info=True)
      raise ValueError(err_msg)
    #  change state
    self.clean_target = self.opt_list[target_index]
    return
    
  
  #  methods - reset
  def reset_all_ds(self):
    for ds in self.dataset_states.values():
      ds.reset_ds()