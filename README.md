## EdTrack - Data Integration Toolkit

<br/>


### I. Overview

A refactored version of my earlier coursework rebuilt into a modularised Python application. Redesigned the client-side workflow with a new PyQt5 interface, together with the server-side data-processing pipelines with modules of import/export, cleaning, transforming and visualising student activities logs.

It is designed to tailor-made a standard workflow for analysing student engagement and supports exporting processed datasets into designated format and storing persistent data in a SQL database.

<br/>

## II. Features

- Import/export datasets and connect to a SQL database
- Form modular data-processing pipeline (Loader, Cleaner, Transformer, Visualiser, etc.)
- Basic data visualisation with Matplotlib heatmaps and pivot tables

<br/>

## III. Demonstration

*Browse and preview dataset*
![UI Demo](docs/demo/demo_import-export_1.gif)


<br/>

## IV. Architecture


<br/>

## V. Project Structure

The application adopts an MVC pattern.

Each module only specialises in single responsibility to maintain the clean and independent system, making future testing maintenance and extension simpler.

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

<br/>

## VI. Workflow

### A. High-level Overview

Controllers bridge between the views and the models, handling user instruction and forwarding tasks to data or state operations.

```
[Action]  ->  [Views]  ->  [Controllers]  ->  [Models]  ->  [Controllers]  ->  [Views]
 (user)        (widgets)    (controller)    (data pipeline)                 
```

### B. Models - Data Pipelines

The Data Pipelines processes data with staged modules which enables data handling procedures to be flexibly swapped, extended and reused without breaking the workflow.

```
[Loader]  ->  [Cleaner]  ->  [Manager]  ->  [Preprocessor]  ->  [Manager]  ->  [Visualiser]  ->  [Loader]
(import)      (cleaning)      (merge)      (feature engineer)  (transform)      (visualise)      (export)
```

### C. Views - User Interface

The User Interface applies a four-tier layer to integrate the layouts, pages, and reusable components together in the decoupled and modularised structure.

```
[UserInterface]  -> [LayoutFactory]  ->  [PageFactory]  ->  [ComponentFactory]
 (main window)                                                 (component)
```

<br/>

## VII. Installation

 <i> Clone the Project </i>

```
$ git clone https://github.com/chkfu/Practice_student-activities.git
$ cd Practice_student-activities
```

 <i> Build Virtual Environment </i>

```bash
$ python -m venv .venv

# macOS / Linux
$ source .venv/bin/activate
# Windows
$ .venv\Scripts\activate
```

 <i> Install Dependencies and run the program: </i>
```
$ pip install -r requirements.txt
```
```
$ python3 app.py
```

<br/>

## VIII. Usage Guide

### A. Initialise the Program

Run the command:
```
$ python3 app.py
```

### B. Navigation Bar

The Navigation Bar handling user behabior which is relevant to application lifecycle:

(1) Reset button: Clears all temporary states and restores global default settings.<br/>
(2) Exit button: Safely shuts down all running processes.<br/>

### C. Side Bar

The Side Bar display the workflow progress and the dataset status.

### D. Content

The Content is the work panel for the application, enabling users to adjust the configurations for data transformation and further analysis.

(1) Browse button: Opens a file dialog to select an input dataset.<br/>
(2) Preview button: Displays a pop-up window with tables or diagrams, including export options.<br/>
(3) Export Button: Opens a file dialog to choose an output destination.<br/>
(4) Navigation Button: Moves between workflow pages.<br/>
(5) Reset Button: Restores the current page to default settings.<br/>

<br/>

## IX. Dependencies
- Python 3.10
- pandas 2.3.3
- numpy 2.3.4
- PyQt5 5.15.11
- matplotlib 3.10.7

See `requirements.txt` for the full package list.

<br/>

<i> Author: kchan </i>
</br>
<i> Last Updated: Nov 27, 2025 </i>