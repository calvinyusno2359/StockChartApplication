import sys, os
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from main_window import Ui_Form

class Main(qtw.QWidget, Ui_Form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

if __name__ == "__main__":
	app = qtw.QApplication([])
	main = Main()
	main.show()
	sys.exit(app.exec_())
