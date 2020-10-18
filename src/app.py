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
		Also autocompletes all inputs using information provided by the csv.
		Error handling:
		- Empty filepath: do nothing
		- Invalid filepath: prompts user
		"""
		filepath = Path(self.filePathEdit.text())

		try:
			self.stock_data = StockData(filepath)

			# auto-complete feauture
			start_date, end_date = self.stock_data.get_period()
			period = f"{start_date} to {end_date}"
			self.startDateEdit.setText(start_date)
			self.endDateEdit.setText(end_date)
			self.periodEdit.setText(period)
			self.SMA1Edit.setText("15")
			self.SMA2Edit.setText("50")
			self.SMA1Checkbox.setChecked()
			self.SMA2Checkbox.setChecked()

			self.report(f"Data loaded from {filepath}; period auto-selected: {start_date} to {end_date}.")
			print(self.stock_data.data)

		except:
			self.report("Filepath provided is invalid.")

	def update_graphics(self):
		"""
		Given inputted date string of format YYYY-MM-DD, creates a date object from it.
		Then, use it to slice a copy of loaded stock_data to be used to update graphics.
		Checks checkboxes first to see if SMA1 and SMA2 lines need to be drawn.
		Error handling:
		- Invalid date format: prompts user
		- Non-existent stock_data: prompts user
		"""
		self.date_format = '%Y-%m-%d'

		try:
			start_date = datetime.strptime(self.startDateEdit.text(), self.date_format).date()
			end_date = datetime.strptime(self.endDateEdit.text(), self.date_format).date()
			period = f"{start_date} to {end_date}"
			self.periodEdit.setText(period)

			# builds a list of graphs to plot by checking the tickboxes
			column_headers = ['Close']
			if self.SMA1Checkbox.isChecked():
				column_headers.append("SMA" + self.SMA1Edit.text())
				self.stock_data.calculate_SMA(int(self.SMA1Edit.text()))
			if self.SMA2Checkbox.isChecked():
				column_headers.append("SMA" + self.SMA2Edit.text())
				self.stock_data.calculate_SMA(int(self.SMA2Edit.text()))

			self.report(f"Time period specified as: {period}. Plotting...")

			try:
				if len(column_headers) == 3:
					self.stock_data.calculate_crossover(column_headers[1], column_headers[2])

				self.selected_stock_data = self.stock_data.get_data(start_date, end_date)
				print(self.selected_stock_data)
				self.plot_graph(column_headers)
				self.plot_signals()

			except AssertionError as e:
				self.report(f"Selected range is empty, {e}.")

			except AttributeError as e:
				self.report(f"Stock data has not been loaded. Please specify filepath of relevant *.csv file, {e}.")

		except ValueError as e:
			self.report(f"Time period has not been specified or does not match YYYY-MM-DD format, {e}.")

	def plot_graph(self, column_headers):
		"""
		Given non-empty selected_stock_data and a specified column_head name,
		plots the graph in the canvas
		Error handling:
		- Empty y_data: raise AssertionError
		"""
		self.figure.clear()
		assert not self.selected_stock_data.empty

		# matplotlib has its own internal representation of datetime
		# date2num converts datetime.datetime to this internal representation
		x_data = list(mdates.date2num(
		                              [datetime.strptime(dates, self.date_format).date()
		                              for dates in self.selected_stock_data.index.values]
		                              ))

		idx = 0
		colors = ['black', 'blue', 'orange']
		for column_head in column_headers:
			if column_head in self.selected_stock_data.columns:
				ax = self.figure.add_subplot(111)
				y_data = list(self.selected_stock_data[column_head])
				ax.plot(x_data, y_data, label=column_head, color=colors[idx])
				self.report(f"{column_head} data is being plotted.")
			else: self.report(f"{column_head} data does not exist.")
			idx += 1

		# formatting
		months_locator = mdates.MonthLocator()
		months_format = mdates.DateFormatter('%b %Y')
		ax.xaxis.set_major_locator(months_locator)
		ax.xaxis.set_major_formatter(months_format)
		ax.format_xdata = mdates.DateFormatter(self.date_format)
		ax.format_ydata = lambda y: '$%1.2f' % y
		ax.grid(True)
		self.figure.autofmt_xdate()
		self.figure.legend()
		self.figure.tight_layout()
		self.canvas.draw()

	def plot_signals(self):
		# matplotlib has its own internal representation of datetime
		# date2num converts datetime.datetime to this internal representation
		isChecked = self.SMA1Checkbox.isChecked() and self.SMA2Checkbox.isChecked()
		if 'Buy' and 'Sell' in self.selected_stock_data.columns:
			x_data = list(mdates.date2num(
			                              [datetime.strptime(dates, self.date_format).date()
			                              for dates in self.selected_stock_data.index.values]
			                              ))
			ybuy_data = list(self.selected_stock_data['Buy'])
			ysell_data = list(self.selected_stock_data['Sell'])
			ax = self.figure.add_subplot(111)
			ax.scatter(x_data, ybuy_data, label='Buy', color='green')
			ax.scatter(x_data, ysell_data, label='Sell', color='red')

			self.figure.legend()
			self.figure.tight_layout()
			self.canvas.draw()

	def report(self, string):
		"""
		Given a report (string), update the scroll area with this report
		"""
		report_text = qtw.QLabel(string)
		self.scrollLayout.addWidget(report_text)

		# scrolls to the latest report
		latest_index = self.scrollLayout.count()-1
		self.scrollArea.ensureWidgetVisible(self.scrollLayout.itemAt(latest_index).widget())
		print(string)

	def center(self):
		"""
		Centers the fixed main window size according to user screen size
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
