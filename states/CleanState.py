import pandas as pd
import logging
from states.DatasetState import DatasetState
from views.components.config.views_config import DATASET_LIST



#  LOGGING

logger = logging.getLogger("CLEAN_STATE")


#  CLASS

#  Learnt: managing different datasets, for cleaning options
#          centialised control in CleanState
class CleanState:
  
  def __init__(self):
    
    #  identify curr state
    self.opt_list = [item["data"] for item in DATASET_LIST[1:]]
    self.clean_target = self.opt_list[0]
    
    #  setup DatasetState to be managed
    self.dataset_states = {
      self.opt_list[0]: DatasetState(state_name=self.opt_list[0]),  # users
      self.opt_list[1]: DatasetState(state_name=self.opt_list[1]),  # activities
      self.opt_list[2]: DatasetState(state_name=self.opt_list[2])  # components
    }
    
    
  #  methods - switching datasets

  
  def get_clean_target(self):
    return self.dataset_states[self.clean_target]
  
  
  def get_spec_dataframe(self, target_name: str):
    valid_keys = [item["data"] for item in DATASET_LIST[1:4]]
    if target_name not in valid_keys:
      err_msg = f"Failed to get specific dataframe {target_name} at CleanState."
      logger.error(err_msg, exc_info=True)
      raise KeyError(err_msg)
    return self.dataset_states[target_name]
  
  
  def get_clean_ds_validity(self) -> dict:
    output: dict = {}
    for index, dataset in self.dataset_states.items():
      output[index] = self.get_spec_dataframe(index).data_raw is not None
    return output
  
  
  def set_raw_data(self, dataset_name: str, df: pd.DataFrame):
    if dataset_name not in self.dataset_states:
        err_msg = f"Dataset State {dataset_name} is not found"
        logger.error(err_msg, exc_info=True)
        raise KeyError(err_msg)
    self.dataset_states[dataset_name].set_data_raw(df)
  

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
    #  clean state
    self.clean_target = self.opt_list[0]
    #  dataset state
    for ds in self.dataset_states.values():
      ds.reset_ds()