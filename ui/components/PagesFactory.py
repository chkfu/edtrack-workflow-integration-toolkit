from typing import Callable
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QPushButton, QStackedWidget


#  CLASS

class PagesFactory:
  
  #  Constructor
  
  def __init__(self):
    super().__init__()
    print("[PagesFactory] initialised successfully.") 
    
    
  #  METHODS - PAGE SETUPS
  
  def create_page_step_1(self) -> QStackedWidget:
    page_step_1 = QStackedWidget()
    print()
    
  
  def create_page_step_2(self) -> QStackedWidget:
    page_step_2 = QStackedWidget()
    print()
    

  def create_page_step_3(self) -> QStackedWidget:
    page_step_3 = QStackedWidget()
    print()
    

  def create_page_step_4(self) -> QStackedWidget:
    page_step_4 = QStackedWidget()
    print()
    
    
  def create_page_step_5(self) -> QStackedWidget:
    page_step_5 = QStackedWidget()
    print()
  

  def create_page_step_6(self) -> QStackedWidget:
    page_step_6 = QStackedWidget()
    print()
