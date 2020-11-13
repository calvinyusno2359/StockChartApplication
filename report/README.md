# Student Notes

## How to Merge IPython Notebooks
First install nbmerge:
```
pip install nbmerge
```
To merge documents use the following commands on the current `report` directory (not root):
```
nbmerge main_window.ipynb app.ipynb appendix.ipynb > "Python Programming and Its Applications in Stock Chart & Moving Average (MA) Crossover.ipynb"
```

## Converting IPython Notebook via LaTeX
1. Open jupyter notebook to convert using anaconda prompt on `root` folder
2. Navigate to the `.ipynb` to be converted and open it
3. Ensure that all images and cells load properly
4. Click `File > Download As > PDF via LaTeX` on the top left hand corner
5. (Optional) if prompted to install a module, simply follow the instructions

## Table of Contents
1. User Manual
    1. Overview
    2. direction (if basic 2, 3, else 4,5,6)
2. Python Basics
    1.
3. Python Packages
    1. Import Statements
    2. Pandas
    3. Numpy
    4. Datetime
4. stock_data.py
5. main_window.py
    1. Installing `Qt Designer`
    2. Building `main_window.ui` Using `Qt Designer`
        1. Defining the GUI
        2. Defining the Widgets
    3. Installing PyQt5
    4. Compiling `main_window.ui`into `main_window.py`
6. app.py

## Learning Points
1. `stock_data.py`
2. `main_window.py`
    1. `Qt Designer` + `PyQt5` Template
    2. `Qt Designer` + `PyQt5 Widget` Types
    3. `Qt Designer` + `PyQt5 Widget` Attributes
3. `app.py`
    1. Inheriting Widgets from `main_window.py`
    2. Defining & Adding Widgets programmatically
    3. Getting `Line Edit Widget` Value
    4. Preventing Crashes with `try... except...`
    5. Setting `Widget` Values Programmatically

