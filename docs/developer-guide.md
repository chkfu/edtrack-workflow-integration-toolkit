<!--

Learnt:

The developer-guide.md file use to educate the future developers internally on
how to edit, expand and append the new elements.

It ensures future developers could make changes on the system within the
specific structure.

-->

# DEVELOPMENT GUIDE

[TOC]


## I. Environment Setup
Run the project with Python 13.3+ version.

### 1. Create the virtual environment:
```
$ python3 -m venv .venv
```

### 2. Activate the virtual environment:
```
$ source .venv/bin/activate
```


## II. Trouble-shooting

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
