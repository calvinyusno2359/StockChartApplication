import sys, os
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from main_window import Ui_Form

class Main(qtw.QWidget, Ui_Form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		# button connections
		self.loadCSVButton.clicked.connect(self.load_data)
		self.updateWindowButton.clicked.connect(self.update_graphics)

	def load_data(self):
		filepath = self.filePathEdit.text()
		print(f"data loaded from {filepath}")

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
