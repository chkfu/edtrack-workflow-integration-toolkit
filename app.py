import os
from datetime import datetime
from dotenv import load_dotenv
from core import DataLoader, SQLConnector, DataManager, DataCleaner
from core.config.paths import PATH_DATA_USER, PATH_DATA_ACTIVITY, PATH_DATA_COMPONENT


#  ENVIRONMENT

load_dotenv("config.env")
db_user = os.getenv("DB_USER")
db_pw= os.getenv("DB_PW")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")


#  MAIN

def main():
  
  #  Data Loader
  
  data_loader = DataLoader()
  df_users = data_loader.import_dataset(path=PATH_DATA_USER)
  df_activities = data_loader.import_dataset(path=PATH_DATA_ACTIVITY)
  df_components = data_loader.import_dataset(path=PATH_DATA_COMPONENT)
  
  
  # SQL Connector
  
  sql_connector = SQLConnector(user=db_user,
                               password=db_pw, 
                               database=db_name, 
                               host=db_host, 
                               port=db_port)
  sql_connector.initialise_database()
  sql_connector.initialise_tables("users")
  sql_connector.initialise_tables("activities")
  sql_connector.initialise_tables("components")
  
  
  #  Data Manager
  

  data_manager = DataManager()
  data_cleaner = DataCleaner()
  
  #  1.  merge the dataset to be analysed
  merged_df = data_manager.merge_tables(target_df_left=df_users, 
                                        target_df_right=df_activities, 
                                        target_col_left="User Full Name *Anonymized", 
                                        target_col_right="User Full Name *Anonymized")
  
  #  2.  update the emerged dataset for consistency
  data_loader.convert_dataset(dataframe=df_activities, fileType="csv", fileName=f"task3_merge")
  
  #  3.  clean data
  print(type(merged_df))
  
  merged_df = data_cleaner.first_data_cleaning(target_df=merged_df,
                                            drop_missing=True,
                                            na_subset_col=None,
                                            sort_item="date",
                                            sort_ascending=True)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
#   #  task 4: reshape
  
#   #  a.  analyse how users interact in different component  ->  user participation
#   reshaped_df = data_manager.reshape_pivot(target_df=merged_df, 
#                                            target_cols=["component"],
#                                            target_rows=["user_id"], 
#                                            target_val="target", 
#                                            target_aggfunc="count", 
#                                            target_filling=0)
#   # print(reshaped_df)
#   data_loader.convert_dataset(dataframe=reshaped_df, 
#                               fileType="csv", 
#                               fileName=f"task4_reshape-01_user-participation")

#   #  b.  analyse how users act in different component  ->  user engagement pattern
#   reshaped_df = data_manager.reshape_pivot(target_df=merged_df, 
#                                            target_cols=["action"], 
#                                            target_rows=["user_id"], 
#                                            target_val="target", 
#                                            target_aggfunc="count", 
#                                            target_filling=0)
#   # print(reshaped_df)
#   data_loader.convert_dataset(dataframe=reshaped_df, 
#                               fileType="csv", 
#                               fileName=f"task4_reshape-02_user-engagement-pattern")
  
#   #  c.  analyse what user perform in different target  ->  user intention
#   reshaped_df = data_manager.reshape_pivot(target_df=merged_df, 
#                                            target_cols=["target"], 
#                                            target_rows=["user_id"], 
#                                            target_val="action", 
#                                            target_aggfunc="count", 
#                                            target_filling=0)
#   # print(reshaped_df)
#   data_loader.convert_dataset(dataframe=reshaped_df, 
#                               fileType="csv", 
#                               fileName=f"task4_reshape-03_user-intention")
  
#   #  d.  analyse the most interacted target in different components  ->  target significance
#   reshaped_df = data_manager.reshape_pivot(target_df=merged_df, 
#                                            target_cols=["target"], 
#                                            target_rows=["component"], 
#                                            target_val="user_id", 
#                                            target_aggfunc="count", 
#                                            target_filling=0)
#   # print(reshaped_df)
#   data_loader.convert_dataset(dataframe=reshaped_df, 
#                               fileType="csv", 
#                               fileName=f"task4_reshape-04_target-significance")
  
#   #  e.  analyse the vaired performed action in different components  -> behavior distribution
#   reshaped_df = data_manager.reshape_pivot(target_df=merged_df, 
#                                            target_cols=["action"], 
#                                            target_rows=["component"], 
#                                            target_val="user_id", 
#                                            target_aggfunc="count", 
#                                            target_filling=0)
#   # print(reshaped_df)
#   data_loader.convert_dataset(dataframe=reshaped_df, 
#                               fileType="csv", 
#                               fileName=f"task4_reshape-05_behavior-distribution")
  
#   #  f.  analyse varied performed actions in different target  ->  action-target linkage
#   reshaped_df = data_manager.reshape_pivot(target_df=merged_df, 
#                                            target_cols=["target"], 
#                                            target_rows=["action"], 
#                                            target_val="user_id", 
#                                            target_aggfunc="count", 
#                                            target_filling=0)
#   # print(reshaped_df)
#   data_loader.convert_dataset(dataframe=reshaped_df, 
#                               fileType="csv", 
#                               fileName=f"task4_reshape-06_action-target")
  
  
#  OUTPUT

if __name__ == "__main__":
  main()