import re
import logging
import mysql.connector
from mysql.connector import Error
from models.config.SQLCommands import SQL_COMMANDS


#  LOGGING

logger = logging.getLogger("APPLICATION")


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
          cursor = connection.cursor()
          return connection, cursor
      except Error as err:
          logger.error(f"[SQLConnector] Connection error: {err}", exc_info=True)
          return None, None

 
  def terminate_db(self, connection, cursor):
      if cursor:
          cursor.close()
      if connection:
          connection.close()
          logger.info("[SQLConnector] terminated MySQL connection.")
          

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
        logger.error(f"[SQLConnector] Execution error: {ex}", exc_info=True)
        raise
    #  disconnection
    finally:
        self.terminate_db(connection, cursor)



  # METHODS - COMMAND-BASED (CRUD concepts)


  #  create methods


  def initialise_database(self, db_init=False):
    try:
        self.execute_db(SQL_COMMANDS["create_database"], db_initialised=db_init)
        logger.info("[SQLConnector] Database is created.")
    except Exception as ex:
        logger.error(f"failed to create database - {ex}", exc_info=True)



  def initialise_tables(self, db_init=True):
    try:
        self.execute_db(SQL_COMMANDS["create_table_users"], db_initialised=db_init)
        self.execute_db(SQL_COMMANDS["create_table_activities"], db_initialised=db_init)
        self.execute_db(SQL_COMMANDS["create_table_components"], db_initialised=db_init)
        logger.info("[SQLConnector] Tables are created.")
    except Exception as ex:
        logger.error(f"failed to create tables - {ex}", exc_info=True)
    
      
      
  #  delete methods
  
  
  def drop_database(self, db_init=False):
      self.execute_db(SQL_COMMANDS["drop_database"], db_initialised=db_init)
      logger.info("[SQLConnector] Database is dropped.")
      
      
  def drop_tables(self, table: str, db_init=True):
    
    table_r = re.sub(r'[^a-zA-Z]', "", table).lower()
    if table_r not in ["users", "activities", "components"]:
        raise ValueError(f"[SQLConnector] \"{table_r}\" is not valid.")
    
    if (table_r == "users"):
        self.execute_db(SQL_COMMANDS["drop_table_users"], db_initialised=db_init)
        logger.info(f"[SQLConnector] drop_tables: \"{table_r}\" is dropped.")
    elif (table_r == "activities"):
        self.execute_db(SQL_COMMANDS["drop_table_activities"], db_initialised=db_init)
        logger.info(f"[SQLConnector] drop_tables: \"{table_r}\" is dropped.")
    elif (table_r == "components"):
        self.execute_db(SQL_COMMANDS["drop_table_components"], db_initialised=db_init)
        logger.info(f"[SQLConnector] drop_tables: \"{table_r}\" is dropped.")
    else:
        err_msg = "[SQLConnector] drop_tables: table name does not match."
        logger.error(err_msg, exc_info=True)
        raise ValueError(err_msg)
    
