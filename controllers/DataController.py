"""
This controller bridges the models and views.
It specific become the wrapper of models' methods, enabling minor adjustment
and prevent directly changes to the data transformation logic.
"""


import logging


#  LOGGING

logger = logging.getLogger("DATA_CONTROLLER")


# CLASS

class DataController:
  
  #  CONSTRUCTOR
  
  def __init__(self, app_ref):
    self.app = app_ref
    logger.info("[FileController] initialised sucessfully.")