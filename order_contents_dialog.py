# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OrderContentsDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 500)
        Dialog.setMinimumSize(QtCore.QSize(600, 400))
        Dialog.setStyleSheet("background-color: #ECF0F1;")

        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        # Заголовок с информацией о заказе
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.label_order_info = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_order_info.setFont(font)
        self.label_order_info.setStyleSheet("color: #2C3E50;")
        self.label_order_info.setObjectName("label_order_info")
        self.horizontalLayout.addWidget(self.label_order_info)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Таблица с товарами
        self.tableWidget_products = QtWidgets.QTableWidget(Dialog)
        self.tableWidget_products.setObjectName("tableWidget_products")
        self.tableWidget_products.setColumnCount(4)
        self.tableWidget_products.setRowCount(0)

        # Настройка таблицы (только для чтения)
        self.tableWidget_products.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_products.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_products.setAlternatingRowColors(True)
        self.tableWidget_products.setStyleSheet("QTableWidget {\n"
"    background-color: white;\n"
"    border: 1px solid #BDC3C7;\n"
"    border-radius: 4px;\n"
"    gridline-color: #ECF0F1;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #2C3E50;\n"
"    color: white;\n"
"    padding: 6px;\n"
"    border: none;\n"
"    font-family: 'Segoe Print';\n"
"}")
        self.verticalLayout.addWidget(self.tableWidget_products)

        # Итоговая сумма
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.label_total = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_total.setFont(font)
        self.label_total.setStyleSheet("color: #2C3E50;")
        self.label_total.setObjectName("label_total")
        self.horizontalLayout_2.addWidget(self.label_total)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        # Кнопка закрытия
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)

        self.pushButton_close = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(11)
        font.setUnderline(False)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    color: #3498DB;\n"
"    border: 1px solid #3498DB;\n"
"    padding: 8px 16px;\n"
"    border-radius: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3498DB;\n"
"    color: white;\n"
"}")
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout_3.addWidget(self.pushButton_close)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Содержимое заказа"))
        self.label_order_info.setText(_translate("Dialog", "Содержимое заказа"))
        self.label_total.setText(_translate("Dialog", "Итоговая сумма: 0.00 руб."))
        self.pushButton_close.setText(_translate("Dialog", "Закрыть"))