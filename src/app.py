import sys, os
from pathlib import Path
from datetime import datetime

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from main_window import Ui_Form
from stock_data import StockData

class Main(qtw.QWidget, Ui_Form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		# button connections
		self.loadCSVButton.clicked.connect(self.load_data)
		self.updateWindowButton.clicked.connect(self.update_graphics)

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
			print(self.stock_data.data)
			print(f"data loaded from {filepath}")
		except:
			print("filepath provided is invalid.")

	def update_graphics(self):
		"""
		Given inputted date string of format YYYY-MM-DD, creates a date object from it.
		Then, use it to slice a copy of loaded stock_date to be used to update graphics.
		Error handling:
		- Invalid date format: prompts user
		- Non-existent stock_data: prompts user
		"""
		date_format = '%Y-%m-%d'

		try:
			start_date = datetime.strptime(self.startDateEdit.text(), date_format).date()
			end_date = datetime.strptime(self.endDateEdit.text(), date_format).date()
			period = f"{start_date} to {end_date}"
			print(f"Time period specified as: {period}")

			try:
				self.selected_stock_data = self.stock_data.get_data(start_date, end_date)
				print(self.selected_stock_data)

				# update graphics here

			except AttributeError:
				print("Stock data has not been loaded. Please specify filepath of relevant .csv file.")

		except ValueError as e:
			print("Time period has not been specified or does not match YYYY-MM-DD format")


if __name__ == "__main__":
	app = qtw.QApplication([])
	main = Main()
	main.show()
	sys.exit(app.exec_())
