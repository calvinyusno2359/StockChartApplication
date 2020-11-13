import sys
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from main_window import Ui_Form
from stock_data import StockData

class Main(qtw.QWidget, Ui_Form):
	"""
	handles user interaction, loads data and updates GUI

	Attributes
	.figure : Figure
		matplotlib Figure object to contain the Axes object(s) and the FigureCanvas object
	.ax : Axes
		matplotlib Axes object is the 'plot' itself, the region of the image which contains the data
	.canvas : FigureCanvas
		matplotlib FigureCanvas is the area onto which the figure is drawn
	.toolbar : NavigationToolbar
		matplotlib NavigationToolbar is the UI that users can use to interact with the drawn plot
	.canvasLayout : QVBoxLayout
		PyQt5's object used to demark the location and contain the FigureCanvas and NavigationToolbar
	.loadCSVButton : QPushButton
		PyQt5's object that user can push to activate the load_data() function
	.updateWindowButton : QPushButton
		PyQt5's object that user can push to activate the update_canvas() function
	.SMA1Checkbox : QCheckBox
		PyQt5's object that user can tick to specify whether to include SMA1 plot in the canvas
	.SMA2Checkbox : QCheckBox
		PyQt5's object that user can tick to specify whether to include SMA2 plot in the canvas
	.scrollWidget : QWidget
		PyQt5's base object for that receives user inputs, as such it is interactable on the screen
	.scrollLayout : QVBoxLayout
		PyQt5's object used to demark the location and contain the QScrollArea
	.scrollArea : QScrollArea
		PyQt5's object's scrollable area on which status reports of the GUI actions are written
	.filePathEdit : QLineEdit
		PyQt5's object used to create a box into which user can input filepath (e.g. ../data/GOOG.csv)
	.startDateEdit : QLineEdit
		PyQt5's object used to create a box into which user can input start date (YYYY-MM-DD)
	.endDateEdit : QLineEdit
		PyQt5's object used to create a box into which user can input end date (YYYY-MM-DD)
	.SMA1Edit : QLineEdit
		PyQt5's object used to create a box into which user can input SMA1 window value (e.g. 15)
	.SMA2Edit : QLineEdit
		PyQt5's object used to create a box into which user can input SMA2 window value (e.g. 50)
	.periodEdit : QLineEdit
		PyQt5's object used to create a box which user can use to see the period used for the graph
	"""
	def __init__(self):
		"""
		initializes and sets up GUI widgets and its connections
		"""
		super().__init__()
		self.setupUi(self)
		self.setWindowTitle("Stock Chart & Moving Average Application")

		# sets up a new figure to plot on, then instantiates a canvas and toolbar object
		self.figure, self.ax = plt.subplots()
		self.canvas = FigureCanvas(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, self)

		# attaches the toolbar and canvas to the canvas layout
		self.canvasLayout.addWidget(self.toolbar)
		self.canvasLayout.addWidget(self.canvas)

		# sets up a scroll area to display GUI statuses
		self.scrollWidget = qtw.QWidget()
		self.scrollLayout = qtw.QVBoxLayout()
		self.scrollWidget.setLayout(self.scrollLayout)
		self.scrollArea.setWidget(self.scrollWidget)

		# button & checkbox connections
		self.loadCSVButton.clicked.connect(self.load_data)
		self.updateWindowButton.clicked.connect(self.update_canvas)
		self.SMA1Checkbox.stateChanged.connect(self.update_canvas)
		self.SMA2Checkbox.stateChanged.connect(self.update_canvas)

		# auto-complete feauture
		self.filePathEdit.setText("../data/GOOG.csv")

	def load_data(self):
		"""
		loads stock data .csv from inputted filepath string on the GUI as StockData object,
		also autocompletes all inputs using information provided by the csv.

		Error handling
			invalid filepath :
				empty filepath or file could not be found or opened.
			invalid .csv :
				.csv file is empty, missing date column, etc.
		"""
		filepath = Path(self.filePathEdit.text())

		try:
			self.stock_data = StockData(filepath)
			start_date, end_date = self.stock_data.get_period()
			period = f"{start_date} to {end_date}"

			# auto-complete feauture
			self.startDateEdit.setText(start_date)
			self.endDateEdit.setText(end_date)
			self.periodEdit.setText(period)
			self.SMA1Edit.setText("15")
			self.SMA2Edit.setText("50")
			self.SMA1Checkbox.setChecked(False)
			self.SMA2Checkbox.setChecked(False)

			self.report(f"Data loaded from {filepath}; period auto-selected: {start_date} to {end_date}.")
			print(self.stock_data.data)

		except IOError as e:
			self.report(f"Filepath provided is invalid or fail to open .csv file. {e}")

		except TypeError as e:
			self.report(f"The return tuple is probably (nan, nan) because .csv is empty")

	def update_canvas(self):
		"""
		creates a datetime object from the inputted date string of format YYYY-MM-DD.
		uses it to slice a copy of loaded stock_data to be used to update graphics.
		checks checkboxes first to see if SMA1, SMA2, Buya and Sell plots need to be drawn.
		finally, updates graphic accordingly

		Error handling
		invalid date format:
			date format inside the .csv file is not of form YYYY-MM-DD
		non-existent stock_data :
			the selected range results in an empty dataframe or end date < start date
		non-existent data point :
			data of that date does not exist, or maybe because it is Out-Of-Bound
		raised exceptions :
			SMA1 and SMA2 values are the same, or other exceptions raised
		"""
		self.ax.clear()
		self.date_format = '%Y-%m-%d'

		try:
			start_date = str(datetime.strptime(self.startDateEdit.text(), self.date_format).date())
			end_date = str(datetime.strptime(self.endDateEdit.text(), self.date_format).date())
			period = f"{start_date} to {end_date}"
			self.periodEdit.setText(period)

			# builds a list of graphs to plot by checking the tickboxes
			column_headers = ['Close']
			formats = ['k-']

			if self.SMA1Checkbox.isChecked():
				self.stock_data._calculate_SMA(int(self.SMA1Edit.text()))
				column_headers.append(f"SMA{self.SMA1Edit.text()}")
				formats.append('b-')
			if self.SMA2Checkbox.isChecked():
				self.stock_data._calculate_SMA(int(self.SMA2Edit.text()))
				column_headers.append(f"SMA{self.SMA2Edit.text()}")
				formats.append('c-')
			if len(column_headers) == 3:
				self.stock_data._calculate_crossover(column_headers[1], column_headers[2], column_headers[1])
				column_headers.append('Sell')
				formats.append('rv')
				column_headers.append('Buy')
				formats.append('g^')

			self.selected_stock_data = self.stock_data.get_data(start_date, end_date)
			self.plot_graph(column_headers, formats)

			self.report(f"Plotting {column_headers} data from period: {start_date} to {end_date}.")
			print(self.selected_stock_data)

		except ValueError as e:
			self.report(f"Time period has not been specified or does not match YYYY-MM-DD format, {e}.")

		except AssertionError as e:
			self.report(f"Selected range is empty, {e}")

		except KeyError as e:
			self.report(f"Data for this date does not exist: {e}")

		except Exception as e:
			self.report(f"Exception encountered: {e}")

	def plot_graph(self, column_headers, formats):
		"""
		plots graphs specified under columnd_headers using the formats specified

		Parameters
		column_headers : [str, str, ...]
			a list containing column header names whose data are to be plotted
		formats : [str, str, ...]
			a list of matplotlib built-in style strings to indicate whether to plot line or scatterplot
			and the colours corresponding to each value in col_headers (hence, must be same length)

		Error handling
		empty dataframe :
			selected dataframe is empty
		"""
		self.ax.clear()
		assert not self.selected_stock_data.empty

		# matplotlib has its own internal representation of datetime
		# date2num converts datetime.datetime to this internal representation
		x_data = list(mdates.date2num(
		                              [datetime.strptime(dates, self.date_format).date()
		                              for dates in self.selected_stock_data.index.values]
		                              ))

		colors = ['black', 'blue', 'orange', 'red', 'green']
		for i in range(len(column_headers)):
			if column_headers[i] in self.selected_stock_data.columns:
				y_data = list(self.selected_stock_data[column_headers[i]])
				self.ax.plot(x_data, y_data, formats[i], label=column_headers[i], color=colors[i])
				self.report(f"{column_headers[i]} data is being plotted.")
			else: self.report(f"{column_headers[i]} data does not exist.")

		# formatting
		months_locator = mdates.MonthLocator()
		months_format = mdates.DateFormatter('%b %Y')
		self.ax.xaxis.set_major_locator(months_locator)
		self.ax.xaxis.set_major_formatter(months_format)
		self.ax.format_xdata = mdates.DateFormatter(self.date_format)
		self.ax.format_ydata = lambda y: '$%1.2f' % y
		self.ax.grid(True)
		self.figure.autofmt_xdate()
		self.figure.legend()
		self.figure.tight_layout()
		self.canvas.draw()

	def report(self, string):
		"""
		given a report (string), update the scroll area with this report

		Parameters
		string : str
			string of the report, usually the error message itself.
		"""
		report_text = qtw.QLabel(string)
		self.scrollLayout.addWidget(report_text)
		print(string)

	def center(self):
		"""
		centers the fixed main window size according to user screen size
		"""
		screen = qtw.QDesktopWidget().screenGeometry()
		main_window = self.geometry()
		x = (screen.width() - main_window.width()) / 2
		y = (screen.height() - main_window.height()) / 2 - 50	# pulls the window up slightly (arbitrary)
		self.setFixedSize(main_window.width(), main_window.height())
		self.move(x, y)

if __name__ == "__main__":
	app = qtw.QApplication([])
	main = Main()
	main.center()
	main.show()
	sys.exit(app.exec_())
