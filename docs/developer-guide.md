<!--

Learnt:

The developer-guide.md file use to educate the future developers internally on
how to edit, expand and append the new elements.

It ensures future developers could make changes on the system within the
specific structure.

-->

# DEVELOPMENT GUIDE

[TOC]

___


## I. Environment Setup
Run the project with Python 13.3+ version.

### A. Create the virtual environment:
```
$ python3 -m venv .venv
```

### B. Activate the virtual environment:
```
$ source .venv/bin/activate
```

### C. Install dependencies at first attempt:
```
$ pip install -r requirements.txt
```

___



## II. Architecture Rationale

### A. Design principles

### B. File Management - MVC Structure

### C. Modular Logic - OOP

### D. State Management

### E. Technology Choice



___


## III。Project Structure




___


## IV. Error Handling

### A. Logging 

1. Using Logging, prevent print 

Logging records important information in a log sheet, helping developers to traceback potential issues with designated checkpoint and timeline. It enables to categorise the logged items in different levels for debugging. 

In turn, printing helps to identify the location of the errors temporarily, but it is unable to support programmers with concrete details. 

2. Logger Setup 

For logging the error, specifically, ensure the logger has been set up at app.py entry point.
```
from infra.DebugLogger import DebugLogger
logger = DebugLogger().setup_app_logger(file_name="debug.log")
```

You also need to call the logger again before you place the log in specific modules. For error logging, make sure 'exc_info=True' for trace message:
```
import logging
log = logging.getLogger("APPLICATION")
log.error(f"[AppController] failed to reset applicaiton - {ex}", exc_info=True)
```

3. Logging Criteria 

Our practice based on the application workflow: 
1. logging in script 
2. reminding user with UI notifications 
3. raising critical errors, terminating the workflow. 

Among various moduls, the criteria:
- models: both logging and raised error, ensure accurate data transformation 
- views: UI notification preferred for consisstency, except logging for system crashes. 
- controllers: logging cross-domain events preferred. Preventing the intersection beteen different logics impacted the board services consistencies. 
- i/o: logging all pass and failed conditions, enabling further tracing errors that happened in the system entry and exit points.


4. Logging Management

The logger is packaged into a reusable module in the infra folder.  It prevents to create duplicated codes across the system, as well as considering future maintainece and expansion of the system structure.

The log sheet will be store in the same folder for the logical file management.

___



## V. Trouble-shooting

### A. Missing imports (dependencies, eg. PyQt5)

If you encounter the warning message:

"Import "pandas" could not be resolved."

1. Check whether Python 13.3+ has been installed, and re-install the dependencies:
```
$ pip install -r requirements.txt
```

2. Check whether the dependencies are installed, for example:
```
$ python3 -c "import PyQt5; print('PyQt5 installed')"
```

If the warning still exists, select the correct interpreter.

1. Open VS code, and press:
    -  macOS: Cmd + Shift + P
    -  Windows: Ctrl + Shift + P 
2. Select "Python: Select Interpreter"
3. Select "Python 3.13.0 (.venv)"

Import warnings should disappear if correct version has been selected.


### B. Missing Module


After renaming, the ModuleNotFoundError may exist if the files still refer to the old path name. 


1.  Case 1  -  changes not adopted

Make sure the new name has been adopted and save completely.
```
ModuleNotFoundError: No module named 'core'
```

You may save and close all of the files. The issue will be resolved once the change has been made sucessfully. 


2.  Case 2 - imported path not updated

If a module has been renamed, but the import paths may not automatically updated and refer to the old name. Please check and ensure the new path name has been applied in these statements.

```
#  Before change:
from core.config.monthList import MONNTH_LIST

#  After change:
from models.config.monthList import MONNTH_LIST
```

3.  Testing

Please run the program again and see whether the error is still existed.
```
python3 app.py
```


___


## VI. Limitation



___


## V. Future Improvements