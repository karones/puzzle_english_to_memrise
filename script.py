#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
from multiprocessing import Process

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QApplication, QPushButton, QMessageBox)


from puzzle import puzzle


class Window_ok(QWidget):
    def __init__(self):
        super(Window_ok, self).__init__()
        self.setWindowTitle('Window2')
        self.setMinimumWidth(10)
        self.setMinimumHeight(10)



class main(QWidget):


    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        field_1 = QLabel('Логин Puzzle English')
        field_2 = QLabel('Пароль  Puzzle English')
        field_3 = QLabel('Название колоды')
        field_4 = QLabel('Логин Memrise')
        field_5 = QLabel('Пароль Memrise')
        field_6 = QLabel('Ссылка на колоду Memrise')
        self.field_7 = QLabel('Идет процесс')

        button = QPushButton('Отправить')
        button.clicked.connect(self.run)

        self.field_Edit1 = QLineEdit()
        self.field_Edit2 = QLineEdit()
        self.field_Edit3 = QLineEdit()
        self.field_Edit4 = QLineEdit()
        self.field_Edit5 = QLineEdit()
        self.field_Edit6 = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(4)

        grid.addWidget(field_1, 1, 0)
        grid.addWidget(self.field_Edit1, 1, 1)

        grid.addWidget(field_2, 2, 0)
        grid.addWidget(self.field_Edit2, 2, 1)

        grid.addWidget(field_3, 3, 0)
        grid.addWidget(self.field_Edit3, 3, 1)


        grid.addWidget(field_4, 4, 0)
        grid.addWidget(self.field_Edit4, 4, 1)

        grid.addWidget(field_5, 5, 0)
        grid.addWidget(self.field_Edit5, 5, 1)

        grid.addWidget(field_6, 6, 0)
        grid.addWidget(self.field_Edit6, 6, 1)

        grid.addWidget(self.field_7, 7, 2)
        self.field_7.hide()
        grid.addWidget(button, 7, 0)

        self.setLayout(grid)

        self.setGeometry(300, 300, 600, 300)
        self.setWindowTitle('Puzzle To Memrise')
        self.show()

    def run(self):
        test = False
        print(type(test))
     #   sender = self.sender()

        puz = puzzle()

        try:


            puz.work(self.field_Edit1.text(), self.field_Edit2.text(), self.field_Edit3.text(),
                     self.field_Edit4.text(), self.field_Edit5.text(), self.field_Edit6.text())

        except Exception as ex:
            print(ex)
            self.field_7.hide()
            choice = QMessageBox.question(self, 'Error!',
                                                str(ex),
                                                QMessageBox.Ok)


            return
        QMessageBox.question(self, 'Ok!',

                                            "Успешное добавление в колоду",
                                            QMessageBox.Ok)
        self.field_7.hide()







if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = main()


    sys.exit(app.exec_())
