from tests.test_data_cleaner_basic import TestDataCleanerBasic
from tests.test_data_cleaner_types import TestDataCleanerTypes


"""
****   Guideline to run Pytest    ****


(1) run the tests:

"TestDataCleanerBasic":  pytest tests/test_data_cleaner_basic.py -v
"TestDataCleanerTypes":  pytest tests/test_data_cleaner_types.py -v


(2) receive report:

"TestDataCleanerBasic":  tests/test_data_cleaner_basic.py | grep -n "def 
"TestDataCleanerTypes":  tests/test_data_cleaner_types.py | grep -n "def 

"""


#  MAIN

__all__ = [
    "TestDataCleanerBasic",
    "TestDataCleanerTypes"
]