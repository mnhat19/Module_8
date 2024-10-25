from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

from FileFactory import FileFactory
from MainWindow import Ui_MainWindow
from Customer import Customer


class MainWindowEx(Ui_MainWindow):
    def __init__(self):
        self.customers=[]
        self.selectedCustomer=None
        self.fileFactory=FileFactory()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.customers = self.fileFactory.readData("database.json",Customer)
        self.loadDataIntoTableWidget()
        self.pushButtonAdd.clicked.connect(self.processNew)
        self.pushButtonSave.clicked.connect(self.processSave)
        self.tableWidget.itemSelectionChanged.connect(self.processItemSelection)
        self.pushButtonRemove.clicked.connect(self.processDelete)

    def loadDataIntoTableWidget(self):
        self.tableWidget.setRowCount(0)
        for i in range(len(self.customers)):
            customer = self.customers[i]
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(customer.FullName)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(customer.Email)))
            itemNumber = QTableWidgetItem()
            itemNumber.setText(str(customer.Number))
            self.tableWidget.setItem(row, 2, itemNumber)

    def processNew(self):
        self.lineEditFullname.setText("")
        self.lineEditEmail.setText("")
        self.lineEditNumber.setText("")
        self.lineEditFullname.setFocus()
        self.selectedCustomer = None

    def processSave(self):
        customer = Customer(self.lineEditFullname.text(), self.lineEditEmail.text(),
                          str(self.lineEditNumber.text()))
        if self.selectedCustomer == None:
            self.customers.append(customer)
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
        else:
            row = self.customers.index(self.selectedCustomer)
        self.selectedCustomer = customer
        self.customers[row] = self.selectedCustomer
        self.tableWidget.setItem(row, 0, QTableWidgetItem(str(customer.FullName)))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(str(customer.Email)))
        itemNumber = QTableWidgetItem()
        itemNumber.setText(str(customer.Number))
        self.tableWidget.setItem(row, 2, itemNumber)
        self.fileFactory.writeData("database.json", self.customers)

    def processItemSelection(self):
        row = self.tableWidget.currentRow()
        if row == -1 or row >= len(self.customers):
            return
        # fullname=self.tableWidget.item(row,0).text()
        # email=self.tableWidget.item(row,1).text()
        # number = self.tableWidget.item(row, 2).text()
        customer = self.customers[row]
        self.selectedCustomer = customer
        name = customer.FullName
        email = customer.Email
        number = customer.Number
        self.lineEditFullname.setText(str(name))
        self.lineEditEmail.setText(str(email))
        self.lineEditNumber.setText(str(number))

    def processDelete(self):
        dlg = QMessageBox(self.MainWindow)
        if self.selectedCustomer == None:
            dlg.setWindowTitle("Deleteing error")
            dlg.setIcon(QMessageBox.Icon.Critical)
            dlg.setText("You have to select a Customer to delete")
            dlg.exec()
            return
        dlg.setWindowTitle("Confirmation Deleting")
        dlg.setText("Are you sure you want to delete?")
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        dlg.setStandardButtons(buttons)
        button = dlg.exec()
        if button == QMessageBox.StandardButton.Yes:
            row = self.customers.index(self.selectedCustomer)
            self.customers.remove(self.selectedCustomer)
            self.selectedCustomer = None
            self.tableWidget.removeRow(row)
            self.processNew()
            self.fileFactory.writeData("database.json", self.customers)

    def show(self):
        self.MainWindow.show()
