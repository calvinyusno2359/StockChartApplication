import sys, os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pathlib import Path
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from main_window import Ui_Form
from stock_data import StockData

class Main(qtw.QWidget, Ui_Form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setWindowTitle("Stock Chart & Moving Average Application")

		# sets up a new figure to plot on, then instantiates a canvas and toolbar object
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, self)

		# attaches the toolbar and canvas
		self.canvasLayout.addWidget(self.toolbar)
		self.canvasLayout.addWidget(self.canvas)

		# button connections
		self.loadCSVButton.clicked.connect(self.load_data)
		self.updateWindowButton.clicked.connect(self.update_graphics)

		self.scrollwidget = qtw.QWidget()
		self.scrollLayout = qtw.QVBoxLayout()
		self.scrollwidget.setLayout(self.scrollLayout)
		self.scrollArea.setWidget(self.scrollwidget)

	def load_data(self):
		"""
		Given inputted filepath (str), loads stock data from csv as object StockData.
		Error handling:
		- Empty filepath: do nothing
		- Invalid filepath: prompts user
		"""
		filepath = Path(self.filePathEdit.text())

		try:
			self.stock_data = StockData(filepath)

			start_date, end_date = self.stock_data.get_period()
			period = f"{start_date} to {end_date}"
			self.startDateEdit.setText(start_date)
			self.endDateEdit.setText(end_date)
			self.periodEdit.setText(period)
			self.SMA1Edit.setText("15")
			self.SMA2Edit.setText("50")

			self.report(f"Data loaded from {filepath}; period auto-selected: {start_date} to {end_date}")
			print(self.stock_data.data)

		except:
			self.report("Filepath provided is invalid.")

	def update_graphics(self):
		"""
		Given inputted date string of format YYYY-MM-DD, creates a date object from it.
		Then, use it to slice a copy of loaded stock_data to be used to update graphics.
		Error handling:
		- Invalid date format: prompts user
		- Non-existent stock_data: prompts user
		"""
		self.date_format = '%Y-%m-%d'

		try:
			start_date = datetime.strptime(self.startDateEdit.text(), self.date_format).date()
			end_date = datetime.strptime(self.endDateEdit.text(), self.date_format).date()
			period = f"{start_date} to {end_date}"
			self.report(f"Time period specified as: {period}. Plotting...")

			try:
				self.selected_stock_data = self.stock_data.get_data(start_date, end_date)
				print(self.selected_stock_data)
				self.plot_graph('Close')

			except AssertionError as e:
				self.report(f"Selected range is empty, {e}")

			except AttributeError as e:
				self.report(f"Stock data has not been loaded. Please specify filepath of relevant .csv file, {e}")

		except ValueError as e:
			self.report(f"Time period has not been specified or does not match YYYY-MM-DD format, {e}")

	def plot_graph(self, column_head):
		"""
		Given non-empty selected_stock_data and a specified column_head name,
		plots the graph in the canvas
		Error handling:
		- Empty y_data: raise AssertionError
		"""
		self.figure.clear()

		assert not self.selected_stock_data.empty
		ax = self.figure.add_subplot(111)
		# matplotlib has its own internal representation of datetime
		# date2num converts datetime.datetime to this internal representation

		x_data = list(mdates.date2num(
		                              [datetime.strptime(dates, self.date_format).date()
		                              for dates in self.selected_stock_data.index.values]
		                              ))
		y_data = list(self.selected_stock_data[column_head])
		ax.plot(x_data, y_data)

		# formatting
		months_locator = mdates.MonthLocator()
		months_format = mdates.DateFormatter('%b %Y')
		ax.xaxis.set_major_locator(months_locator)
		ax.xaxis.set_major_formatter(months_format)
		ax.format_xdata = mdates.DateFormatter(self.date_format)
		ax.format_ydata = lambda y: '$%1.2f' % y
		ax.grid(True)
		self.figure.autofmt_xdate()

		self.canvas.draw()

	def report(self, string):
		report_text = qtw.QLabel(string)
		self.scrollLayout.addWidget(report_text)

		# scrolls to the latest report
		latest_index = self.scrollLayout.count()-1
		print(latest_index)
		self.scrollArea.ensureWidgetVisible(self.scrollLayout.itemAt(latest_index).widget())
		print(string)

if __name__ == "__main__":
	app = qtw.QApplication([])
	main = Main()
	main.show()
	sys.exit(app.exec_())
