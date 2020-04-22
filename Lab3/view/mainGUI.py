# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread, QThreadPool

from view.secondaryGUI import Ui_Form


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(401, 177)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.psoButton = QtWidgets.QPushButton(self.centralwidget)
        self.psoButton.setObjectName("psoButton")
        self.horizontalLayout.addWidget(self.psoButton)
        self.adamEvaButton = QtWidgets.QPushButton(self.centralwidget)
        self.adamEvaButton.setObjectName("adamEvaButton")
        self.adamEvaButton.setText("Adam and Evas")
        self.eaButton = QtWidgets.QPushButton(self.centralwidget)
        self.eaButton.setObjectName("eaButton")
        self.horizontalLayout.addWidget(self.eaButton)
        self.hcButton = QtWidgets.QPushButton(self.centralwidget)
        self.hcButton.setObjectName("hcButton")
        self.horizontalLayout.addWidget(self.hcButton)
        self.horizontalLayout.addWidget(self.adamEvaButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 401, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.psoButton.clicked.connect(PSO)
        self.eaButton.clicked.connect(EA)
        self.hcButton.clicked.connect(hillClimb)
        self.adamEvaButton.clicked.connect(adamEva)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Population Size"))
        self.label_2.setText(_translate("MainWindow", "Individual Size"))
        self.label_3.setText(_translate("MainWindow", "Iterations"))
        self.psoButton.setText(_translate("MainWindow", "PSO"))
        self.eaButton.setText(_translate("MainWindow", "EA"))
        self.hcButton.setText(_translate("MainWindow", "Hill Climb"))



if __name__ == "__main__":
    import sys
    import threading

    def getParams(ui):
        pSize = ui.lineEdit.text()
        iSize = ui.lineEdit_2.text()
        iterations = ui.lineEdit_3.text()
        return pSize, iSize, iterations

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()

    @pyqtSlot(name="PSO")
    def PSO():
        newWindow = Ui_Form()
        t1 = threading.Thread(target=newWindow.run, args=('pso', getParams(ui)))
        t1.start()
        t1.join()

    @pyqtSlot(name="EA")
    def EA():
        newWindow = Ui_Form()
        t1 = threading.Thread(target=newWindow.run, args=('ea', getParams(ui)))
        t1.start()
        t1.join()

    @pyqtSlot(name="hillCLimb")
    def hillClimb():
        newWindow = Ui_Form()
        t1 = threading.Thread(target=newWindow.run, args=('hc', getParams(ui)))
        t1.start()
        t1.join()

    @pyqtSlot(name="adamEva")
    def adamEva():
        newWindow = Ui_Form()
        t1 = threading.Thread(target=newWindow.run, args=('ae', getParams(ui)))
        t1.start()
        t1.join()

    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
