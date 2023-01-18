import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget


class AddCoffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.setWindowTitle("Добавить")
        self.pushButton.clicked.connect(self.add)

    def add(self):
        con = sqlite3.connect("coffee.db")
        cur = con.cursor()

        name = self.lineEdit.text()
        degree = self.lineEdit_2.text()
        type = self.lineEdit_3.text()
        taste = self.lineEdit_4.text()
        price = self.spinBox.value()
        size = self.spinBox_2.value()
        cur.execute(f"""
        INSERT INTO coffee(name, degreeOfRoasting, type, taste, price, size)
        VALUES('{name}', '{degree}', '{type}', '{taste}', {int(price)}, {int(size)})""")
        con.commit()
        con.close()
        ex.loadTable()
        self.close()


class EditCoffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.setWindowTitle("Изменить")
        self.current_elem = ""
        self.pushButton.clicked.connect(self.edit)

    def initUI(self):
        con = sqlite3.connect("coffee.db")
        cur = con.cursor()
        data = cur.execute(f"""SELECT * FROM coffee WHERE name = '{self.current_elem}'""").fetchone()
        con.close()
        self.lineEdit.setText(data[1])
        self.lineEdit_2.setText(data[2])
        self.lineEdit_3.setText(data[3])
        self.lineEdit_4.setText(data[4])
        self.spinBox.setValue(data[5])
        self.spinBox_2.setValue(data[6])

    def edit(self):
        con = sqlite3.connect("coffee.db")
        cur = con.cursor()

        name = self.lineEdit.text()
        degree = self.lineEdit_2.text()
        type = self.lineEdit_3.text()
        taste = self.lineEdit_4.text()
        price = self.spinBox.value()
        size = self.spinBox_2.value()

        cur.execute(f"""UPDATE coffee
                        SET name='{name}', degreeOfRoasting='{degree}', type='{type}', taste='{taste}', price={price}, size={size}
                        WHERE name='{self.current_elem}'""")

        con.commit()
        con.close()
        ex.loadTable()
        self.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.setWindowTitle("Эспрессо")
        self.loadTable()
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.update_coffee)
        self.tableWidget.cellClicked.connect(self.cellClick)
        self.add = AddCoffee()
        self.edit = EditCoffee()

    def cellClick(self):
        self.edit.current_elem = self.tableWidget.item(self.tableWidget.currentRow(), 1).text()

    def add(self):
        self.add.show()

    def update_coffee(self):
        self.edit.initUI()
        self.edit.show()

    def loadTable(self):
        con = sqlite3.connect("coffee.db")
        cur = con.cursor()
        reader = cur.execute("""SELECT * FROM coffee""").fetchall()
        con.close()
        title = ["ID", "название сорта", "степень обжарки", "молотый/в зернах",
                 "описание вкуса", "цена", "объем упаковки"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(reader):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())