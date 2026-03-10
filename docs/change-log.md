<!--

Learnt:

The CHANGRLOG.md file records the version-based changes of the system. It
store the trace that how the development teams add, edit, fix and remove
in each release.

While Git commit messages records the details of subsequent changes; however,
this files groups relevant changes into a clearer and human-recognisable
summaries for further maintenance.

-->

# CHANGELOG

This file records the major version changes of the projects.

<br/>


## [1.0.1] - Mar 10, 2026

### Added 

-  Added `test/` folder for unit testing
-  Added new unit tests for data cleaning methods
                     
### Edited
-  Refined `readme.md` and `developer-guide.md` documents
-  Updated `requirements.txt` with new implemented libraries

### Fixed
-  Refined data cleaning methods based on the failed tests at edge cases


<br/>


## [1.0.8] - Mar 07, 2026

-  First minimum viable product released.

<br/>


## [0.1.7] - Mar 07, 2026

### Added 

- Added AnalyseState for managing analysing options
                    
### Edited

- Restructured analysing logic at PageAnalyse
- Update page-specific criteria of back button triggering at NavController

### Fixed

- Fixed parameter input missing in AnalyseState
- Fixed missing value checkboxes in metric tabs, PageAnalyse
- Update page-specific criteria of back button triggering at NavController

### Delete

- Removed graph visualization for the current version.

<br/>


## [0.1.6] - Dec 28, 2026
                    
### Edited

- Implemebted controller events into PageFE's components
- Restructured feature engineering logic at PageFE

### Fixed

- Resolved bug of duplicate state at root UI and PageClean

<br/>


## [0.1.5] - Dec 18, 2025

### Added 

- Added PageFE and PageAnalyse UI
- Added MergeStates and MergeDataState

### Edited

- Renamed cleaning-related state classes
- Refine buttons and tabs with pointer cursor
- Refine sidebar dataset list with status updates (dataset only)
- Refactorised reused component groups in ComponentFactory
- Refactorised relationship between views and ValidController
- Implemented controllers events to PageMerge's components
- Updated developer guide and changelog

### Fixed

- Enabled cleaned dataset to be temporarily stored into CleanDataState
- Resolved refreshing bugs to ensure up-to-date options for dropdown widgets
- Fixed circular import issue by deferred ValidController loading temporarily

### Removed

- Remove unused dependencies

<br/>


## [0.1.4] - Dec 5, 2025

### Added

- Added PageFE step into the workflow for handling feature-engineering tasks
- Added PageClean and PageMerge UI
- Added instructions of adding new pages in developer-guide
- Added project structure and architecture in architecture and readme documents

## Edited

- Refactored cleaning with tab switching issues for preventing redundent codes
- Implemented controller events into PageClean's components

## Fixed

- Fixed UI refresh and event binding bugs

<br/>


## [0.1.3] - Nov 29, 2025

### Added

- Added tabs structure for reusable sub-pages setting
- Added states folder for global state management
- Added project structure, workflow and user guide in readme.md

### Edited

- Updated documentation

### Fixed

- Fixed earlier component generation bugs

### Removed

- Deleted script folder, considering models logic need to be adjusted for UI

<br/>


## [0.1.2] - Nov 22, 2025

### Added

- Implemented DebugLogger for application-wide logging
- Added ValidController for validation methods
- Added DataController for connecting models and views

### Edited

- Completed PageImport workflow and UI integration
- Updated documentation
- Refactored one-off codes into scripts folder

<br/>


## [0.1.1] - Nov 16, 2025

### Added

- Added documentation files
- Added MVC structure for logic seperation

### Edited

- Updated README
- Refactored pages classes for modularisation
- Refactored events into controllers for MVC structure

### Fixed

- Fixed app crash during page switching with reset

### Removed

- Deleted unused and deprecated dependencies and modules

<br/>


## [0.1.0] - Oct 19, 2025

### Added

- Initialised the project
