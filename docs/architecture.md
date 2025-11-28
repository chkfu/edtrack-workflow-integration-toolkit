<!--

Learnt:

The architecture.md file use to explain the principle of the system design,
answering the questions why certain layer and modules has been built.

The documents will insert the Lucid charts with few lines of descrition,
helping future developer to understanding the system rationale and maintain
efficient codes practice, and follow the established architectural practices.

-->

#  ARCHITECTURE


##  I.  Architecture Rationale

###  A.  Overall Architecture Design

The program follows the principles of low coupling and high cohesion, by separating job responsibilities into clarified and independent logical layers.  Additionally, modular components constructed complex visual layout, while the data pipeline is formed with replaceable processes which enabling flexible and extendable analysis,


###  B.  MVC Layered Structure

The application adopts layered structure for clarifying the division of  business logic, data management and visualisation.  

It defines the boundaries between layers, enabling their role to be more understandable, while preventing unnecessary cross-layer interactions with mess. Clearer boundaries therefore make the system structure being more organised and predictable which help developers to trace, maintain and extend the current codes.


###  C.  Object-oriented Programming

With the OOP principles, it helps to divide data management and business workflow into smaller and independent modules, and these modules thereby specialise in single responsibility. In this design, the encapsulation pattern helps to reduce the dependence between modules, while enabling them to construct complex products with easy scaling and adjustments. 

Class abstraction and inheritance also enable modules to replace or extend or override existing functionalities without affecting the original structure. It is able to simplify complex operation into easy-manageable parts and therefore support flexible extensions and modification for new requirements.


<br/>

##  II. Overall Architecture

##  A. Project Structure

```
|----  controllers/                       #  Workflow logic
 |----  data/                             #  Raw and interim datasets
 |----  docs/                             #  Documentation and design
 |----  infra/                            #  System Infrastructure, i.e. Logging
 |    |----    DebugLogger.py
 |----    models/                         #  Data pipeline collection
 |    |----  DataLoader.py
 |       |----  DataCleaner.py
 |       |----  DataManager.py
 |       |----  DataPreprocessor.py
 |       |----  DataVisualiser.py
 |       |----  SQLConnector.py
 |----  output/                           #  Export tables and diagram examples
 |      |----  diagrams/
 |      |----   tables/
 |----  state/                            #  Global state management
 |----  views/                            #  User Interface
 |----  config.env                        #  Environment config
 |----  requirements.txt                  #  List of dependencies
 |----  README.md
 |----  app.py                            #  Entry Point
```

###  B.  Layer Responsibility

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

### C. High-level Overview

Controllers bridge between the views and the models, handling user instruction and forwarding tasks to data or state operations.

```
[Action]  ->  [Views]  ->  [Controllers]  ->  [Models]  ->  [Controllers]  ->  [Views]
 (user)        (widgets)    (controller)    (data pipeline)                 
```


<br/>

##  III.  Layers Architecture

###  A. Models - Data Pipeline Modules

```
| Module       | Responsibility                                                                             |
|----------------|---------------------------------------------------------------------------------------------|
| Loader | Imports raw datasets, validates structure and converts into pandas DataFrames. |
| Cleaner | Handles missing values, duplicates and inconsistent / unmatched formats. |
| Manager | Manages DataFrame structures, merging, and interim dataset organisation. |
| Preprocessor | Establishes feature engineering and prepares data for later analysis. |
| Visualiser | Produces preview diagrams for visual display. |
```

###  B. Models - Data Pipelines

The Data Pipelines processes data with staged modules which enables data handling procedures to be flexibly swapped, extended and reused without breaking the workflow.

```
[Loader]  ->  [Cleaner]  ->  [Manager]  ->  [Preprocessor]  ->  [Manager]  ->  [Visualiser]  ->  [Loader]
(import)      (cleaning)      (merge)      (feature engineer)  (transform)      (visualise)      (export)
```

###  C.  Views - UI Composition

```
| Module         | Responsibility                                                                             |
|----------------|---------------------------------------------------------------------------------------------|
| UIApplication |  Manages the overall interface and workflow, including the main window and the application's lifecycle.  |
| LayoutFactory | Constructs standardised layout sections to organise the structure of each page consistently. |
| PagesFactory | Generates page layouts for each workflow step, handling the arrangement and presentation of content. |
| ComponentFactory | Creates reusable UI components and grouped toolkits to maintain visual and behavioural consistency. |
```

###  D.  Views - User Interface

The User Interface applies a four-tier layer to integrate the layouts, pages, and reusable components together in the decoupled and modularised structure.

```
[UserInterface]  -> [LayoutFactory]  ->  [PageFactory]  ->  [ComponentFactory]
 (main window)                                                 (component)
```
```
[PageFactory]  ->  [PageTemplate]  ->  [Page___]
 (router)       (base class for UI)   (concrete class)
                                            |------> [Qt Components]
                                                     (page object(s))
```

