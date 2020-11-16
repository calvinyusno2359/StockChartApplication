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

## Team & Project Information
The project is public, all source code, ipython notebooks and the application itself are available for download at: https://github.com/heavensward-argentlux/StockChartApplication

SMU QF205 G2 Team 3
1. YUSNOVERI CALVIN
2. YANG JIAXIN
3. PANG BO HAO EDWIN
4. LIM ZHI XIN CASPER
5. LIM WEI YANG

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
    4. Using `Path` from `pathlib` to parse `filepath`
    5. Preventing Crashes with `try... except...`
    6. Setting `Widget` Values Programmatically
    7. Parsing date `string` using `datetime`
    8. Getting `Checkbox Widget` Value
    9. `matplotlib` plot format `strings`
    10. Clearing Axes
    11. Preventing Crashes with assert
    12. The "Standard Way" of Plotting Using matplotlib
    13. Anatomy `matplotlib`'s `Figure`
    14. Connecting `Widgets` to `functions`
    15. Compiling Python Modules into an `.exe`

