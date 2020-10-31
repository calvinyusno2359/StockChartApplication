import sys, os
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
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setWindowTitle("Stock Chart & Moving Average Application")

		# sets up a new figure to plot on, then instantiates a canvas and toolbar object
		self.figure, self.ax = plt.subplots()
		self.canvas = FigureCanvas(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, self)

		# attaches the toolbar and canvas
		self.canvasLayout.addWidget(self.toolbar)
		self.canvasLayout.addWidget(self.canvas)

		# button & checkbox connections
		self.loadCSVButton.clicked.connect(self.load_data)
		self.updateWindowButton.clicked.connect(self.update_canvas)
		self.SMA1Checkbox.stateChanged.connect(self.update_canvas)
		self.SMA2Checkbox.stateChanged.connect(self.update_canvas)

		self.scrollwidget = qtw.QWidget()
		self.scrollLayout = qtw.QVBoxLayout()
		self.scrollwidget.setLayout(self.scrollLayout)
		self.scrollArea.setWidget(self.scrollwidget)

		# auto-complete feauture
		self.filePathEdit.setText("../data/GOOG.csv")

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

			self.report(f"Data loaded from {filepath}; period auto-selected: {start_date} to {end_date}.")
			print(self.stock_data.data)

		except:
			self.report("Filepath provided is invalid.")

	def update_canvas(self):
		"""
		Given inputted date string of format YYYY-MM-DD, creates a date object from it.
		Then, use it to slice a copy of loaded stock_data to be used to update graphics.
		Checks checkboxes first to see if SMA1 and SMA2 lines need to be drawn.
		Error handling:
		- Invalid date format: prompts user
		- Non-existent stock_data: prompts user
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
			style = ['k-']

			if self.SMA1Checkbox.isChecked():
				self.stock_data._calculate_SMA(int(self.SMA1Edit.text()))
				column_headers.append(f"SMA{self.SMA1Edit.text()}")
				style.append('b-')
			if self.SMA2Checkbox.isChecked():
				self.stock_data._calculate_SMA(int(self.SMA2Edit.text()))
				column_headers.append(f"SMA{self.SMA2Edit.text()}")
				style.append('c-')
			if len(column_headers) == 3:
				self.stock_data._calculate_crossover(column_headers[1], column_headers[2], column_headers[1])
				column_headers.append('Sell')
				style.append('rv')
				column_headers.append('Buy')
				style.append('g^')

			self.selected_stock_data = self.stock_data.get_data(start_date, end_date)
			self.stock_data.plot_graph(column_headers, style=style, ax=self.ax, show=False)
			self.figure.tight_layout()
			self.canvas.draw()

		except ValueError as e:
			self.report(f"Time period has not been specified or does not match YYYY-MM-DD format, {e}.")

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
