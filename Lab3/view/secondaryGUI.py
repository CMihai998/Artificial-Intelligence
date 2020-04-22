# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'secondary.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!
from copy import deepcopy
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

from controller.controller import Controller

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 465)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.fitnessResultLabel = QtWidgets.QLabel(Form)
        self.fitnessResultLabel.setText("")
        self.fitnessResultLabel.setObjectName("fitnessResultLabel")
        self.horizontalLayout.addWidget(self.fitnessResultLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(4)
        self._controller = None
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Fitness:"))

    def run(self, option, params):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Form = QtWidgets.QWidget()
        ui = Ui_Form()
        ui.setupUi(Form)
        iterations, individualSize = self.createController(params)
        ui.tableWidget.setColumnCount(individualSize)
        ui.tableWidget.setRowCount(individualSize)

        if option == 'pso':
            self.handlePSO(ui, iterations)
        elif option == 'ea':
            self.handleEA(ui, iterations)
        elif option == 'hc':
            self.handleHC(ui, individualSize, iterations)
        elif option == 'ae':
            self.handleAE(ui, 0, individualSize)

        Form.show()
        sys.exit(app.exec_())



    def createController(self, args):
        populationSize = 100
        individualSize = 4
        if args[0] != '':
            populationSize = int(args[0])
        if args[1] != '':
            individualSize = int(args[1])
        self._controller = Controller(populationSize, individualSize)
        if args[2] != '':
            return int(args[2]), individualSize
        return 500, individualSize

    def fillMeUp(self, ui, data):
        actualData = data.getChromosome()
        tableData = []
        for i in range(data.getSize()):
            row = []
            for j in range(data.getSize()):
                elem = str(str(actualData[i][j]) + ', ' + str(actualData[i + data.getSize()][j]))
                row.append(elem)
            tableData.append(deepcopy(row))
        for row in range(data.getSize()):
            for column in range(data.getSize()):
                ui.tableWidget.setItem(row, column, QTableWidgetItem(tableData[row][column]))
        ui.fitnessResultLabel.setText(str(data.fitness()))

    def handlePSO(self, ui,  iterations):
        self.fillMeUp(ui, self._controller.particleSwarnOptimisation(iterations)[0])

    def handleEA(self, ui,  iterations):
        self.fillMeUp(ui, self._controller.evolutionaryAlgorithm(iterations)[-2])

    def handleHC(self, ui, individualSize, iterations):
        self.fillMeUp(ui, self._controller.hillClimb(individualSize, iterations))

    def handleAE(self, ui, param, individualSize):
        self.fillMeUp(ui, self._controller.AdamAndEvas(param, individualSize))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
