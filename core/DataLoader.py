import os
import dataframe_image as dfi
import pandas as pd


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
      

  def convert_dataset(self, dataframe: pd.DataFrame, fileType: str, fileName: str, destination: str = "output/") -> None:

    #  check job types
    type_r = fileType.strip().lower()
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
    print("[DataLoader] convert files successfully.")
    return None
