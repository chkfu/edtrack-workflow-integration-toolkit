from views import UserInterface
from infra.DebugLogger import DebugLogger
from scripts.script_fullAnalysis import run_full_analysis


#  LOGGING

logger = DebugLogger().setup_app_logger(file_name="debug.log")


#  MAIN

def main():
  
  #  UI -  PyQt5
  user_interface = UserInterface()
  user_interface.run_app()
  
  #  PIPELINE - Diagrams
  #  remarks: generate diagrams for analysis, lower priority to prevent UI delay
  run_full_analysis()
  
#  OUTPUT
if __name__ == "__main__":
  main()