from views import UserInterface
from infra.DebugLogger import DebugLogger


#  LOGGING

logger = DebugLogger().setup_app_logger(file_name="debug.log")


#  MAIN

def main():
  
  #  UI -  PyQt5
  user_interface = UserInterface()
  user_interface.run_app()
  
#  OUTPUT
if __name__ == "__main__":
  main()