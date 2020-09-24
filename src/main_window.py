# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1122, 861)
        self.appTitleLabel = QtWidgets.QLabel(Form)
        self.appTitleLabel.setGeometry(QtCore.QRect(4, 20, 1111, 101))
        font = QtGui.QFont()
        font.setPointSize(31)
        self.appTitleLabel.setFont(font)
        self.appTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.appTitleLabel.setObjectName("appTitleLabel")
        self.loadCSVButton = QtWidgets.QPushButton(Form)
        self.loadCSVButton.setGeometry(QtCore.QRect(10, 140, 361, 111))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.loadCSVButton.setFont(font)
        self.loadCSVButton.setObjectName("loadCSVButton")
        self.filePathEdit = QtWidgets.QLineEdit(Form)
        self.filePathEdit.setGeometry(QtCore.QRect(380, 140, 731, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.filePathEdit.setFont(font)
        self.filePathEdit.setObjectName("filePathEdit")
        self.periodEdit = QtWidgets.QLineEdit(Form)
        self.periodEdit.setGeometry(QtCore.QRect(380, 200, 731, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.periodEdit.setFont(font)
        self.periodEdit.setObjectName("periodEdit")
        self.updateWindowButton = QtWidgets.QPushButton(Form)
        self.updateWindowButton.setGeometry(QtCore.QRect(380, 270, 471, 111))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateWindowButton.setFont(font)
        self.updateWindowButton.setObjectName("updateWindowButton")
        self.startDateEdit = QtWidgets.QLineEdit(Form)
        self.startDateEdit.setGeometry(QtCore.QRect(140, 270, 231, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.startDateEdit.setFont(font)
        self.startDateEdit.setObjectName("startDateEdit")
        self.endDateEdit = QtWidgets.QLineEdit(Form)
        self.endDateEdit.setGeometry(QtCore.QRect(140, 330, 231, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.endDateEdit.setFont(font)
        self.endDateEdit.setObjectName("endDateEdit")
        self.startDateLabel = QtWidgets.QLabel(Form)
        self.startDateLabel.setGeometry(QtCore.QRect(20, 270, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.startDateLabel.setFont(font)
        self.startDateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.startDateLabel.setObjectName("startDateLabel")
        self.endDateLabel = QtWidgets.QLabel(Form)
        self.endDateLabel.setGeometry(QtCore.QRect(20, 330, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.endDateLabel.setFont(font)
        self.endDateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.endDateLabel.setObjectName("endDateLabel")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 390, 1101, 461))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.canvasLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.canvasLayout.setContentsMargins(0, 0, 0, 0)
        self.canvasLayout.setObjectName("canvasLayout")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.appTitleLabel.setText(_translate("Form", "Stock Chart & Moving Average Crossover"))
        self.loadCSVButton.setText(_translate("Form", "Load CSV File"))
        self.periodEdit.setPlaceholderText(_translate("Form", "YYYY-MM-DD to YYYY-MM-DD"))
        self.updateWindowButton.setText(_translate("Form", "Update Window"))
        self.startDateEdit.setPlaceholderText(_translate("Form", "YYYY-MM-DD"))
        self.endDateEdit.setPlaceholderText(_translate("Form", "YYYY-MM-DD"))
        self.startDateLabel.setText(_translate("Form", "Start Date"))
        self.endDateLabel.setText(_translate("Form", "End Date"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

