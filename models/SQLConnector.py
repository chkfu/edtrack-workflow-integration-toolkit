import re
import logging
import mysql.connector
from mysql.connector import Error
from models.config.SQLCommands import SQL_COMMANDS
import pandas as pd


#  LOGGING
logger = logging.getLogger("SQL_CONNECTOR")


#  CLASS

class SQLConnector:
  
  #  Constructor
  
  def __init__(self, user, password, database, host, port):
      #  learnt: store config first for reuse
      self.config = {
          "user": user,
          "password": password,
          "host": host,
          "port": port
      }
      self.db_name = database
      self.initialise_database()
      self.initialise_tables()


  #  METHODS - SQL OPERATION

  def connect_db(self, use_db=False):
      try:
          config = self.config.copy()
          if use_db:
              config["database"] = self.db_name
          #  learnt: **config, for dict. unpacking
          connection = mysql.connector.connect(**config)  
          if not connection:
              err_msg = "Failed to connect to the database. Please ensure the connection pipeliines."
              logger.into(err_msg)
              raise ConnectionError(err_msg)
          cursor = connection.cursor()
          return connection, cursor
      except Error as err:
          logger.error(f"Connection error: {err}", exc_info=True)
          return None, None

 
  def terminate_db(self, connection, cursor):
      if cursor:
          cursor.close()
      if connection:
          connection.close()
          logger.info("terminated MySQL connection.")
          

  #  learnt: the fn as wrappper, bringing simplicity with sql code adopted
  def execute_db(self, sql, db_initialised=False):
    #  learnt: extract connection and cursor
    #  connection
    connection, cursor = self.connect_db(db_initialised)
    if not connection:
        return
    #  execution
    try:
        cursor.execute(sql)
        connection.commit()
    except Error as ex:
        logger.error(f"Execution error: {ex}", exc_info=True)
        raise
    #  disconnection
    finally:
        self.terminate_db(connection, cursor)



  # METHODS - COMMAND-BASED (CRUD concepts)


  #  create methods


  def initialise_database(self, db_init=False):
    try:
        self.execute_db(SQL_COMMANDS["create_database"], db_initialised=db_init)
        logger.info("Database is created.")
    except Exception as ex:
        logger.error(f"failed to create database - {ex}", exc_info=True)



  def initialise_tables(self, db_init=True):
    try:
        self.execute_db(SQL_COMMANDS["create_table_users"], db_initialised=db_init)
        self.execute_db(SQL_COMMANDS["create_table_activities"], db_initialised=db_init)
        self.execute_db(SQL_COMMANDS["create_table_components"], db_initialised=db_init)
        logger.info("Tables are created.")
    except Exception as ex:
        logger.error(f"failed to create tables - {ex}", exc_info=True)
    

  def validate_sql_table(self, target_table: str) -> str:
      table_r = re.sub(r'[^a-zA-Z]', "", target_table).lower()
      if table_r not in ["users", "activities", "components"]:
          raise ValueError(f"\"{table_r}\" is not valid.")
      return table_r
    
  #  delete methods

  
  def drop_database(self, db_init=False):
      self.execute_db(SQL_COMMANDS["drop_database"], db_initialised=db_init)
      logger.info("Database is dropped.")
      
      
  def drop_tables(self, table: str, db_init=True):
    
    table_r = self.validate_sql_table(target_table=table)
    if (table_r == "users"):
        self.execute_db(SQL_COMMANDS["drop_table_users"], db_initialised=db_init)
        logger.info(f"drop_tables: \"{table_r}\" is dropped.")
    elif (table_r == "activities"):
        self.execute_db(SQL_COMMANDS["drop_table_activities"], db_initialised=db_init)
        logger.info(f"drop_tables: \"{table_r}\" is dropped.")
    elif (table_r == "components"):
        self.execute_db(SQL_COMMANDS["drop_table_components"], db_initialised=db_init)
        logger.info(f"drop_tables: \"{table_r}\" is dropped.")
    else:
        err_msg = "drop_tables: table name does not match."
        logger.error(err_msg, exc_info=True)
        raise ValueError(err_msg)
    
    
  def import_dataframe(self, 
                    target_table: str, 
                    target_df = pd.DataFrame) -> None:
    
    
    SCHEMA_COLS = {
        "users": {
            "User Full Name *Anonymized": "user_name",
            "Date": "date",
            "Time": "time"
        },

        "activities": {
            "User Full Name *Anonymized": "user_name",
            "Component": "component",
            "Action": "action",
            "Target": "target"
        },

        "components": {
            "Component": "component",
            "Code": "code"
        }
    }

    
    #  1. validation
    table_r = self.validate_sql_table(target_table=target_table)

    if target_df is None or target_df.empty:
        err_msg: str = "The dataframe to be imported is invalid. Failed to transfer to SQL."
        logger.error(err_msg, exc_info=True)
        raise ValueError(err_msg)
    #  remarks: for safety, check types seriously for sql related actions (easy to crash)
    if not isinstance(target_df, pd.DataFrame):
        err_msg: str = "The provided tabular data is not a pandas dataframe. Failed to transfer to SQL."
        logger.error(err_msg, exc_info=True)
        raise TypeError(err_msg)
    
    #  2. apply transformation
    if target_table not in SCHEMA_COLS:
        err_msg = f"The table {target_table} is not found. Please ensure the table name."
        logger.error(err_msg)
        raise KeyError(err_msg)

    #  Learnt: pandas rename required dict format, trans np.list to dict
    standard_cols = SCHEMA_COLS[target_table]
    target_df_r = target_df.rename(columns=standard_cols)
            
    #  3. import data
    connection, cursor = self.connect_db(use_db=True)
    #  execution
    try:
        #  transform data form
        columns = ", ".join(target_df_r.columns)
        #  Learnt: take placeholders, replacing with update
        values = ", ".join(["%s"] * len(target_df_r.columns))
        command = f"INSERT INTO {table_r} ({columns}) VALUES ({values})"
        #  Learnt: convert to the 2D array which can be accepted by SQL
        #          because it takes [tuple(row) for row in target_df.to_numpy()]
        transformed_data = [tuple(row) for row in target_df_r.to_numpy()]
        #  import to SQL
        cursor.executemany(command, transformed_data)
        connection.commit()
        logger.info("Imported data into SQL sucessfully.")
        
    #  still allow data transformation without SQL sync
    except Exception as ex:
        err_msg: str = f"Failed to import the designated dataset - {ex}. SQL database will not be updated."
        logger.warning(err_msg)
        raise Exception(f"{ex}")
    
    finally:
        self.terminate_db(connection, cursor)