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

The application adopts MVC pattern. 

```
models/        # Data layer: database management, data transformation 
views/         # UI layer: all UI components and structure
controllers/   # logic layer: bridge views and models, manage user workflow 
docs/          # internal documentation and architectural diagrams
infra/         # Infrastructure: logging
scripts/       # One-off or less important codes 
output/        # File generation: exported files and reports
data/          # Raw input or interim processed data
```

Each modules therefore specialise their own duties and logically grouped, supporting the principle of "high cohersion" and "low coupling". This methods helps developers to save time and effort on future maintenance and testing, and enhances system's consistency and reliability with minimal impacts one another.


___


## IV. UI Guide

### A. Rationale

PyQt5 interfaces constructed by layers of widgets and layouts. Layout manages geometry, while widget manage appearance of styling. Widgets can adopt one layout, and the layout therein contains the subordinated widgets.

The below codes is the minimal example to show how to build a container with a "Next" button inside:

```
def create_btn_container(self):
    btn = QPushButton("Next")
    box = QFrame()
    layout = QHBoxLayout()
    layout.addWidget(btn)   # ✅ assign the button into layout
    box.setLayout(layout)   # ✅ widget adopt the layout
    return box
```

However, widget is unable to adopt another widget, as well as layout
```
def create_btn_container(self):
    btn = QPushButton("Next")
    box = QFrame()

    box.addWidget(btn)   # ❌ widget has no .addWidget method
    box.setLayout(btn)   # ❌ btn is not a layout
    
    layout_1 = QHBoxLayout()
    layout_2 = QVBoxLayout()
    layout_1.addWidget(box_layout_2)  # ❌ layout_2 is not a widget
    layout_1.setLayout()  # ❌ layout has no .setLayout method
    return box
```


### B. Return Widget that being added

Returning an adopted widget will be resulted in an error, as those items will be gone with no trace. Make sure that the outest widget (highest level) should be returned:

```
def create_btn_container(self):
    btn = QPushButton("Next")
    box = QFrame()
    layout = QHBoxLayout()
    layout.addWidget(btn) 
    box.setLayout(layout) 
    return btn   # ❌ the btn is no longer existed
```


### C. Table Missing Values

PyQt5 tables requires stringify data for visualisation; otherwise, the values will be gone missing.  Convert all values into string before you add them into the table body.

```
item = str(target_df.iloc[row, col])  # ✅ convert the value to string first
table.setItem(row, col, QTableWidgetItem(item))
```

___


## V. Error Handling

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
logger = logging.getLogger("APPLICATION")
logger.error(f"[AppController] failed to reset applicaiton - {ex}", exc_info=True)
```

3. Logging Criteria 

Our practice based on the application workflow: 
1. logging in script 
2. reminding user with UI notifications 
3. raising critical errors, terminating the workflow. 

Among various moduls, the criteria:
- models: both logging and raised error, ensure accurate data transformation 
- views: UI notification preferred for tency, except logging for system crashes. 
- controllers: logging cross-domain events preferred. Preventing the intersection beteen different logics impacted the board services consistencies. 
- i/o: logging all pass and failed conditions, enabling further tracing errors that happened in the system entry and exit points.


4. Logging Management

The logger is packaged into a reusable module in the infra folder.  It prevents to create duplicated codes across the system, as well as considering future maintainece and expansion of the system structure.

The log sheet will be store in the same folder for the logical file management.

___


## VI. Trouble-shooting

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
from core.config.monthList import MONTH_LIST

#  After change:
from models.config.monthList import MONTH_LIST
```

3.  Testing

Please run the program again and see whether the error is still existed.
```
python3 app.py
```

___


## VII. Limitation



___


## VIII. Future Improvements