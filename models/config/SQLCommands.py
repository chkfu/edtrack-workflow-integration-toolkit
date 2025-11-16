SQL_COMMANDS = {
  
  #  CREATE
  
  "create_database":
    """
      CREATE DATABASE IF NOT EXISTS student_activities;
    """,
    
  "create_table_users": 
    """ 
      CREATE TABLE IF NOT EXISTS Users (
        user_id         INT           AUTO_INCREMENT PRIMARY KEY,
        user_name       VARCHAR(20)   NOT NULL,
        date            DATETIME      NOT NULL
      );
    """,
    
  "create_table_activities": 
    """ 
      CREATE TABLE IF NOT EXISTS Activities (
        activity_id     INT           AUTO_INCREMENT PRIMARY KEY,
        user_name       VARCHAR(20)   NOT NULL,
        component       VARCHAR(20)   NOT NULL,
        action          VARCHAR(20)   NOT NULL,
        target          VARCHAR(20)   NOT NULL
      );
    """,
    
  "create_table_components": 
    """ 
      CREATE TABLE IF NOT EXISTS Components (
        component       VARCHAR(20)   NOT NULL,
        code            VARCHAR(20)   NOT NULL
      );
    """,
    
    
  #  DELETE 
  
  "drop_database":
    """
      DROP DATABASE IF EXISTS student_activities;
    """,
    
  "drop_table_users":
    """
      DROP TABLE USERS;
    """,
    
  "drop_table_activities":
    """
      DROP TABLE ACTIVITIES;
    """,
    
  "drop_table_components":
    """
      DROP TABLE COMPOENETS;
    """
    
}
