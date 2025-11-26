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


## I. Overview

This guide provides the project's scope, architecture, structure and the workflow decisions of the EdTrack system. 

It is a desktop application to be utilised for cleaning and transforming student-activity datasets through the standard workflow. Specifically, this toolkit enables importing/exporting files, browse and preview tables, data processing and diagram visualisation.  


## II. Environment Setup

Run the project with Python 13.3+ version.

### A. Create the virtual environment:
```
#  step 1:  create the virtual environment
$ python3 -m venv .venv

#  step 2:  activate the virtual environment (if macOS)
$ source .venv/bin/activate

#  step 3:  install dependencies at first attempt
$ pip install -r requirements.txt

#  step 4:  run the program
$ python app.py

```

___


## II. Architecture Rationale


___


## III。Project Structure

The application adopts MVC pattern. 

```
controllers/   # logic layer: bridge views and models, manage user
data/          # Raw input or interim processed data
docs/          # internal documentation and architectural diagrams
infra/         # Infrastructure: logging
models/        # Data layer: database management, data transformation
output/        # File generation: exported files and reports
state/         # State management: handle state for cross-modules
views/         # UI layer: all UI components and structure workflow
```

Each module groups logically and specialises their own duties, separating a clear layer structure with the principle of high cohesion and low coupling.  This arrangement helps to prevent cross-dependent logic with complex relations, improving future maintenance and testing with module reusability and system consistency.


___


## IV.  Workflow Logic

This section explains how the workflow logic operates after activating the application.

### A.  Activate the application

Run the code below in the virtual environment:
```
$ python3 app.py
```

Once the application is activated, the code initialises the application and loads its user interface - a window with its home page.

### B. Managing Visual Display (User Interface)

Modularised in OOP structure, the file `UserInterface.py` is the root of the `views/` folder that manages the main window. It encapsulates all Qt components in different layer structures.

Factory classes assist to integrate different components into large component sets, constructing the Application's section, page, and even small widget layouts. Indeed, they only create objects in layers structure but the classes themselves are not interdependent on one another. 

```
[UserInterface]  -> [LayoutFactory]  ->  [PageFactory]  ->  [ComponentFactory]
 (main window)                                                 (component)
```

Pages-related structure performs in abstraction and inheritance relationship with OOP pattern.  `PageFactory` manages the page-switching logic with state management, while `PageTemplate` only manages the user interface by building shared components for the page classes. 

As children, `Page__` classes inherit the parent's behaviors, while being able to override parent's behavior for customisation.

```
[PageFactory]  ->  [PageTemplate]  ->  [Page___]
 (router)       (base class for UI)   (concrete class)
                                            |------> [Qt Components]
                                                     (page object(s))
```

### C. Managing Behaviors (Events)

Under MVC structure, the Application's logic, behavior and display perform independently. The `controller` module connects different parts: (1) receive request from view, (2) trigger model functions if needed, and (3) return the result back to the display.

```
[Action]  ->  [Widget]  ->  [Validation]  ->  [Data Handling]  ->  [Result]  ->  [Updated Widget]
 (user)        (view)       (controller)       (model, if need)  (controller)         (view)   
```

#### (1) Button Events

For example, when users try to preview a dataset in `PageImport`, they firstly click on the "Browse" button, thereby triggering the `preview_dataset` method in `FileController`.

The controller firstly validates the inputs and then proceeds the action itself, processing the new call to pop-up window, and thereby receiving the result and returning the requested data.  

Finally, the pop-up window will display the diagram based on the data result, completing the request-response cycle.


___


## V. User Interface Guide

### A. Rationale

PyQt5 interfaces constructed by layers of widgets and layouts. Layout manages geometry, while widget manages appearance of styling. Widgets can adopt one layout, and the layout therein contains the subordinated widgets.

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

Returning an adopted widget will result in an error, as those items will be gone with no trace. Make sure that the outest widget (highest level) should be returned:

```
def create_btn_container(self):
    btn = QPushButton("Next")
    box = QFrame()
    layout = QHBoxLayout()
    layout.addWidget(btn)
    box.setLayout(layout)
    return   # ❌ the btn is no longer existed
```


### C. Table Missing Values

PyQt5 tables require stringify data for visualisation; otherwise, the values will be gone missing.  Convert all values into string before you add them into the table body.

```
item = str(target_df.iloc[row, col])  # ✅ convert the value to string first
table.setItem(row, col, QTableWidgetItem(item))
```

___


## VI Error Handling

### A. Logging

#### (1) Using Logging, prevent print

Logging records important information in a log sheet, helping developers to traceback potential issues with designated checkpoint and timeline. It enables categorising the logged items in different levels for debugging.

In turn, printing helps to identify the location of the errors temporarily, but it is unable to support programmers with concrete details.


#### (2) Logger Setup

For logging the error, specifically, ensure the logger has been set up at app.py entry point.
```
from infra.DebugLogger import DebugLogger
logger = DebugLogger().setup_app_logger(file_name="debug.log")
```

You also need to call the logger again before you place the log in specific modules. For error logging, make sure 'exc_info=True' for trace message:
```
import logging
logger = logging.getLogger("APPLICATION")
logger.error(f"[AppController] failed to reset application - {ex}", exc_info=True)
```


#### (3) Logging Criteria

Our practice based on the application workflow:
(a) logging in script, and
(b) reminding user with UI notifications, and
(c) raising critical errors, terminating the workflow.

Among various modules, the criteria:
- models: both logging and raised error, ensure accurate data transformation
- views: UI notification preferred for tency, except logging for system crashes.
- controllers: logging cross-domain events preferred. Preventing the intersection between different logics impacted the board services' consistencies.
- i/o: logging all pass and failed conditions, enabling further tracing errors that happened in the system entry and exit points.


#### (4) Logging Management

The logger is packaged into a reusable module in the infra folder.  It prevents duplicated codes across the system, as well as considering future maintenance and expansion of the system structure.

The log sheet will be stored in the same folder for logical file management.

___


## VII. Trouble-shooting

### A. Missing imports (dependencies, eg. PyQt5)

If you encounter the warning message:

"Import "pandas" could not be resolved."

#### (1) Check whether Python 13.3+ has been installed, and re-install the dependencies:
```
$ pip install -r requirements.txt
```

#### (2) Check whether the dependencies are installed, for example:
```
$ python3 -c "import PyQt5; print('PyQt5 installed')"
```

If the warning still exists, select the correct interpreter.

(a) Open VS code, and press:
\-  macOS: Cmd + Shift + P
\-  Windows: Ctrl + Shift + P
(b) Select "Python: Select Interpreter"
(c) Select "Python 3.13.0 (.venv)"

Import warnings should disappear if the correct version has been selected.

### B. Missing Module

After renaming, the ModuleNotFoundError may exist if the files still refer to the old path name.

#### (1)  Case 1  -  changes not adopted

Make sure the new name has been adopted and saved completely.
```
ModuleNotFoundError: No module named 'core'
```

You may save and close all of the files. The issue will be resolved once the change has been made successfully.

#### (2)  Case 2 - imported path not updated

If a module has been renamed, but the import paths may not automatically update and refer to the old name. Please check and ensure the new path name has been applied in these statements.

```
#  Before change:
from core.config.monthList import MONTH_LIST

#  After change:
from models.config.monthList import MONTH_LIST
```

##### (3) Testing

Please run the program again and see whether the error still exists.
```
python3 app.py
```

___


## VII. Limitation



___


## VIII. Future Improvements