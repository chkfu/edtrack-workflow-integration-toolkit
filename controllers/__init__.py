from controllers.AppController import AppController
from controllers.NavController import NavController
from controllers.FileController import FileController
from controllers.ValidController import ValidController
from controllers.CleanController import CleanController



#  MAIN

#  learnt: __init__ manage info. globally, no longer entry pt. since Py3.3
__all__ = ["AppController",
           "NavController",
           "FileController",
           "ValidController",
           "CleanController"]