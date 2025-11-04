import os
import pandas as pd
from dotenv import load_dotenv
from core import DataLoader, SQLConnector, DataManager, DataCleaner, DataPreprocessor
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
  data_preproc = DataPreprocessor(data_manager=data_manager)
  
  #  1.  merge the dataset to be analysed
  merged_df = data_manager.merge_tables(target_df_left=df_users, 
                                        target_df_right=df_activities, 
                                        target_col_left="User Full Name *Anonymized", 
                                        target_col_right="User Full Name *Anonymized")
  
  #  2.  clean data
  merged_df = data_cleaner.first_data_cleaning(target_df=merged_df,
                                              drop_duplicated=True,
                                              drop_missing=True,
                                              na_subset_col=None,
                                              sort_item="date",
                                              sort_ascending=True)
  
  
  merged_df = data_cleaner.second_data_cleaning(target_df=merged_df)
  
  data_loader.convert_dataset(dataframe=merged_df, 
                              fileType="csv", 
                              fileName="table_merged", 
                              destination="data/processed/")
  
  #  PRE-PROCESSING
  
  processed_df = data_preproc.remove_time_col(target_df=merged_df, 
                                              time_col="time")
  
  processed_df = data_preproc.hash_name_col(target_df=processed_df, 
                                            name_col="User Full Name *Anonymized")
  
  processed_df = data_manager.rename_col(target_df=processed_df,
                                         target_col="User Full Name *Anonymized", 
                                         new_name="User")
  
  processed_df = data_preproc.encode_component_col(target_df=processed_df, 
                                                   target_col="component", 
                                                   code_df=df_components, 
                                                   dict_idx="component", 
                                                   dict_val="code")
  
  processed_df = data_preproc.encode_component_col(target_df=processed_df, 
                                                   target_col="target", 
                                                   code_df=df_components, 
                                                   dict_idx="component", 
                                                   dict_val="code")
  
  processed_df = data_preproc.regulate_actions(target_df=processed_df, 
                                               target_col="action")
  
  processed_df = data_preproc.revise_target_col(target_df=processed_df, 
                                                target_col="target")
 
  data_loader.convert_dataset(dataframe=processed_df, 
                              fileType="csv", 
                              fileName="table_preprocessed", 
                              destination="data/processed/")
  
  
  #  DATA MANIPULATION
  
  #  task: remove "sys" and "fold" from component column
  processed_df = data_manager.remove_rows(target_df=processed_df, target_col="component", target_rows=["sys", "fold"])
  print(processed_df["Target"].unique().tolist())
  #  task: restructure a pivot table
  #  1. to understand how events interact one another
  reshaped_1 = data_manager.reshape_pivot(target_df=processed_df, 
                             target_cols=["component"], 
                             target_rows=["target"], 
                             target_val="user",
                             target_aggfunc=pd.Series.nunique,
                             target_filling=0)
  #  2. to understand how many actions has been done to component events
  reshaped_2 = data_manager.reshape_pivot(target_df=processed_df, 
                             target_cols=["component"], 
                             target_rows=["action"], 
                             target_val="user",
                             target_aggfunc="count",
                             target_filling=0)
  #  3. to understand how many actions has been done to target events (by days)
  reshaped_3 = data_manager.reshape_pivot(target_df=processed_df, 
                             target_cols=["target"], 
                             target_rows=["action"], 
                             target_val="user",
                             target_aggfunc="count",
                             target_filling=0)
  #  4. to understand how users prefer to engage in component events (by days)
  reshaped_4 = data_manager.reshape_pivot(target_df=processed_df, 
                             target_cols=["component"], 
                             target_rows=["user"], 
                             target_val="date",
                             target_aggfunc=pd.Series.nunique,
                             target_filling=0)
  #  5. to understand how users prefer to engage in target events
  reshaped_5 = data_manager.reshape_pivot(target_df=processed_df, 
                             target_cols=["target"], 
                             target_rows=["user"], 
                             target_val="date",
                             target_aggfunc=pd.Series.nunique,
                             target_filling=0)
  #  6. to understand how users prefer to act
  reshaped_6 = data_manager.reshape_pivot(target_df=processed_df, 
                             target_cols=["action"], 
                             target_rows=["user"], 
                             target_val="date",
                             target_aggfunc=pd.Series.nunique,
                             target_filling=0)
  
  data_loader.convert_dataset(dataframe=reshaped_1, 
                              fileType="png", 
                              fileName="table_reshaped_EventCorrelation", 
                              destination="output/tables/")
  
  data_loader.convert_dataset(dataframe=reshaped_2, 
                              fileType="png", 
                              fileName="table_reshaped_ActionPattern", 
                              destination="output/tables/")
  
  data_loader.convert_dataset(dataframe=reshaped_3, 
                              fileType="png", 
                              fileName="table_reshaped_TaskBehavior", 
                              destination="output/tables/")
  
  data_loader.convert_dataset(dataframe=reshaped_4, 
                              fileType="png", 
                              fileName="table_reshaped_ContentEngagement", 
                              destination="output/tables/")
  
  data_loader.convert_dataset(dataframe=reshaped_5, 
                              fileType="png", 
                              fileName="table_reshaped_TargetEngagement", 
                              destination="output/tables/")

  data_loader.convert_dataset(dataframe=reshaped_6, 
                              fileType="png", 
                              fileName="table_reshaped_UserBehavior", 
                              destination="output/tables/")
  
  #  Testing
  # print(processed_df)
  

  
  
#  OUTPUT

if __name__ == "__main__":
  main()