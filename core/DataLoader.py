import os
import dataframe_image as dfi
import pandas as pd
from matplotlib.figure import Figure


#  CLASS

class DataLoader:

  #  Constructor

  def __init__(self):
    print("[DataLoader] initialised successfully.")


  #  Methods

  def import_dataset(self, path: str) -> pd.DataFrame:

      #  check validity
      if not os.path.exists(path):
        raise FileNotFoundError("[DataLoader] import_dataset - the data path is not valid.")
      fileFormat: str = os.path.splitext(path)[-1].lower()    #  learnt: to detect file format
      
      #  check job type
      if fileFormat == ".csv":
        output: pd.DataFrame = pd.read_csv(path)
      elif fileFormat == ".json":
        output: pd.DataFrame  = pd.read_json(path)
      elif fileFormat == ".xml":
        output: pd.DataFrame = pd.read_xml(path)
      else:
        raise ValueError(f"[DataLoader] import_dataset - data path format is not .csv, .xml, or .json.")
      
      #  output
      print("[DataLoader] upload files successfully.")
      return output
      

  def convert_dataset(self, dataframe: pd.DataFrame, fileType: str, fileName: str, destination: str = "output/tables/") -> None:

    try:
      if dataframe is None or dataframe.empty:
        raise ValueError("DataLoader] failed to export diagram. pandas dataframe is missing.")
      
      type_r = fileType.strip().lower()
      if type_r not in ["csv", "xml", "json", "png"]:
        raise ValueError("[DataLoader] incorrect file type has been provided. please try again.")
      
      #  check job types
      if type_r == "csv":
        dataframe.to_csv(destination + fileName + ".csv", index=False)
      elif type_r == "xml":
        dataframe.to_xml(destination + fileName + ".xml", index=False)
      elif type_r == "json":
        #  learnt: orient="records" for dict type (json-like)
        dataframe.to_json(destination + fileName + ".json", orient="records", indent=4) 
      elif type_r == "png":
        dfi.export(dataframe, destination + fileName + ".png")
      else:
        raise ValueError("[DataLoader] import_dataset - data path format is not .csv, .xml, or .json.")
      
      #  output
      print("[DataLoader] convert dataset successfully.")
      return
    
    except Exception as ex:
      raise Exception(f"[DataLoader] failed to convert diagram - {ex}")

  
  
  def convert_diagram(self, plt_figure: Figure, fileType: str, fileName: str, destination: str="output/diagrams/", target_dpi: int=300) -> None:
    
    if plt_figure is None:
      raise ValueError("[DataLoader] failed to export diagram. matplotlib figure is missing.")
    
    type_r = fileType.strip().lower()
    if type_r not in ["png", "jpg", "tiff", "bmp"]:
      raise ValueError("[DataLoader] incorrect file type has been provided. please try again.")
    
    
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
        raise ValueError("[DataLoader] import_dataset - data path format is not .png, .jpg, .tiff, .bmp")
      
      print("[DataLoader] convert diagram successfully.")
      return
      
    except Exception as ex:
      raise Exception(f"[DataLoader] failed to convert diagram - {ex}")

