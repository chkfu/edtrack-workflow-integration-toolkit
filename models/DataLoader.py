import os
import logging
import dataframe_image as dfi
import pandas as pd
from matplotlib.figure import Figure


#  LOGGING

logger = logging.getLogger("DATA_LOADER")


#  CLASS

class DataLoader:

  #  Constructor

  def __init__(self):
    logger.info("initialised successfully.")


  #  Methods

  def import_dataset(self, path: str) -> pd.DataFrame:
    try:
      #  check validity
      if not os.path.exists(path):
        raise FileNotFoundError("import_dataset - the data path is not valid.")
      fileFormat: str = os.path.splitext(path)[-1].lower()    #  learnt: to detect file format
      
      #  check job type
      if fileFormat == ".csv":
        output: pd.DataFrame = pd.read_csv(path)
      elif fileFormat == ".json":
        output: pd.DataFrame  = pd.read_json(path)
      elif fileFormat == ".xml":
        output: pd.DataFrame = pd.read_xml(path)
      else:
        raise ValueError(f"import_dataset - data path format is not .csv, .xml, or .json.")
      
      #  output
      logger.info("imported files successfully.")
      return output
    
    except Exception as ex:
      logger.error("Failed to upload the selected file.")
      

  def convert_dataset(self, dataframe: pd.DataFrame, fileType: str, destination: str) -> None:

    try:
      if dataframe is None or dataframe.empty:
        raise ValueError("failed to export diagram. pandas dataframe is missing.")
      
      type_r = fileType.strip().lower()
      if type_r not in [".csv", ".xml", ".json", ".png"]:
        err_msg = "incorrect file type has been provided. please try again."
        logger.warning(err_msg)
        raise ValueError(err_msg)
      
      #  check job types
      if type_r == ".csv":
        dataframe.to_csv(destination, index=False)
      elif type_r == ".xml":
        dataframe.to_xml(destination, index=False)
      elif type_r == ".json":
        #  learnt: orient="records" for dict type (json-like)
        dataframe.to_json(destination, orient="records", indent=4) 
      elif type_r == ".png":
        dfi.export(dataframe, destination)
      else:
        raise ValueError("Data path format is not .csv, .xml, or .json.")
      
      #  output
      logger.info("Convert dataset successfully.")
      return
    
    except Exception as ex:
      logger.error(f"Failed to convert diagram - {ex}", exc_info=True)
      raise Exception(f"{ex}")

  
  
  def convert_diagram(self, plt_figure: Figure, fileType: str, fileName: str, destination: str, target_dpi: int=300) -> None:
    
    if plt_figure is None:
      raise ValueError("failed to export diagram. matplotlib figure is missing.")
    
    type_r = fileType.strip().lower()
    if type_r not in ["png", "jpg", "tiff", "bmp"]:
      err_msg = "incorrect file type has been provided. please try again."
      logger.warning(err_msg)
      raise ValueError(err_msg)
    
    
    try:
      if type_r == "png":
        plt_figure.savefig(destination + fileName + ".png", dpi=target_dpi)
      elif type_r == "jpg":
        plt_figure.savefig(destination + fileName + ".jpg", dpi=target_dpi)
      elif type_r  == "tiff":
        plt_figure.savefig(destination + fileName + ".tiff", dpi=target_dpi)
      elif type_r == "bmp":
        plt_figure.savefig(destination + fileName + ".bmp", dpi=target_dpi)
      else:
        raise ValueError("import_dataset - data path format is not .png, .jpg, .tiff, .bmp")
      
      logger.info("convert diagram successfully.")
      return
      
    except Exception as ex:
      logger.error(f"failed to convert diagram - {ex}")

