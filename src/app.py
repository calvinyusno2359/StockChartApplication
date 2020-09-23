import sys, os
from pathlib import Path

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
		if filepath:
			try:
				stock_data = StockData(filepath)
				print(stock_data.data)
				print(f"data loaded from {filepath}")
			except:
				print("filepath provided is invalid.")

	def update_graphics(self):
		start_date = self.startDateEdit.text()
		end_date = self.endDateEdit.text()
		period = f"{start_date} to {end_date}"

		print(f"graphics updated from {period}")

if __name__ == "__main__":
	app = qtw.QApplication([])
	main = Main()
	main.show()
	sys.exit(app.exec_())
