## Overview

A refactored version of my earlier coursework rebuilt into a modularised Python application. Redesigned the client-side workflow with a new PyQt5 interface, together with the server-side data-processing pipelines with modules of import/export, cleaning, transforming and visualising student activities logs.

It is designed to tailor-made a standard workflow for analysing student engagement and supports to export processed datasets into designated format and store persistent data in a SQL database.

</br>
</br>

## Features

- Import/export datasets and connect to a SQL database
- Form modular data-processing pipeline (Loader, Cleaner, Transformer, Visualiser, etc.)
- Basic data visualisation with Matplotlib heatmaps and pivot tables

</br>
</br>

## Dependencies

- python==3.10
- pandas==2.3.3
- numpy==2.3.4
- PyQt5==5.15.11
- mysql-connector-python==9.5.0
- matplotlib==3.10.7

</br>
</br>

## Initialise the Project

#### <i> 1. Clone the Project </i>

```bash
git clone https://github.com/chkfu/Practice_student-activities.git
cd Practice_student-activities
```

#### <i> 2. Build Virtual Environment </i>

```bash

python -m venv .venv

# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

```

#### <i> 3. Install Dependencies </i>

```bash
pip install -r requirements.txt
```

#### <i> 4. Run the Script </i>

```bash
python3 app.py
```

</br>
</br>

## Project Structure

</br>
</br>

## Demos

</br>
</br>


---

<i> Author: kchan </i>
</br>
<i> Last Updated: 16 November 2025 </i>
