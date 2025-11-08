# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditOrderWithProductsDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_title = QtWidgets.QLabel(Dialog)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(16)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        self.verticalLayout.addWidget(self.label_title)

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")

        self.label_user = QtWidgets.QLabel(Dialog)
        self.label_user.setObjectName("label_user")
        self.comboBox_user = QtWidgets.QComboBox(Dialog)
        self.comboBox_user.setObjectName("comboBox_user")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_user)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_user)

        self.label_status = QtWidgets.QLabel(Dialog)
        self.label_status.setObjectName("label_status")
        self.comboBox_status = QtWidgets.QComboBox(Dialog)
        self.comboBox_status.setObjectName("comboBox_status")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_status)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_status)

        self.label_date = QtWidgets.QLabel(Dialog)
        self.label_date.setObjectName("label_date")
        self.label_date_value = QtWidgets.QLabel(Dialog)
        self.label_date_value.setObjectName("label_date_value")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_date)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_date_value)

        self.label_total = QtWidgets.QLabel(Dialog)
        self.label_total.setObjectName("label_total")
        self.label_total_value = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_total_value.setFont(font)
        self.label_total_value.setObjectName("label_total_value")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_total)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_total_value)

        self.verticalLayout.addLayout(self.formLayout)

        # Секция управления товарами
        self.label_products = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(12)
        self.label_products.setFont(font)
        self.label_products.setObjectName("label_products")
        self.verticalLayout.addWidget(self.label_products)

        self.horizontalLayout_products = QtWidgets.QHBoxLayout()
        self.horizontalLayout_products.setObjectName("horizontalLayout_products")

        self.comboBox_product = QtWidgets.QComboBox(Dialog)
        self.comboBox_product.setObjectName("comboBox_product")
        self.horizontalLayout_products.addWidget(self.comboBox_product)

        self.spinBox_quantity = QtWidgets.QSpinBox(Dialog)
        self.spinBox_quantity.setMinimum(1)
        self.spinBox_quantity.setMaximum(100)
        self.spinBox_quantity.setObjectName("spinBox_quantity")
        self.horizontalLayout_products.addWidget(self.spinBox_quantity)

        self.pushButton_add_product = QtWidgets.QPushButton(Dialog)
        self.pushButton_add_product.setObjectName("pushButton_add_product")
        self.horizontalLayout_products.addWidget(self.pushButton_add_product)

        self.verticalLayout.addLayout(self.horizontalLayout_products)

        # Таблица товаров в заказе
        self.tableWidget_products = QtWidgets.QTableWidget(Dialog)
        self.tableWidget_products.setObjectName("tableWidget_products")
        self.tableWidget_products.setColumnCount(5)
        self.verticalLayout.addWidget(self.tableWidget_products)

        # Кнопка удаления товара
        self.pushButton_remove_product = QtWidgets.QPushButton(Dialog)
        self.pushButton_remove_product.setObjectName("pushButton_remove_product")
        self.verticalLayout.addWidget(self.pushButton_remove_product)

        self.horizontalLayout_buttons = QtWidgets.QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_buttons.addItem(spacerItem)

        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout_buttons.addWidget(self.pushButton_cancel)

        self.pushButton_save = QtWidgets.QPushButton(Dialog)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout_buttons.addWidget(self.pushButton_save)

        self.verticalLayout.addLayout(self.horizontalLayout_buttons)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Редактировать заказ"))
        self.label_title.setText(_translate("Dialog", "Редактирование заказа"))
        self.label_user.setText(_translate("Dialog", "Пользователь:"))
        self.label_status.setText(_translate("Dialog", "Статус:"))
        self.label_date.setText(_translate("Dialog", "Дата заказа:"))
        self.label_total.setText(_translate("Dialog", "Итоговая сумма:"))
        self.label_products.setText(_translate("Dialog", "Товары в заказе:"))
        self.pushButton_add_product.setText(_translate("Dialog", "Добавить товар"))
        self.pushButton_remove_product.setText(_translate("Dialog", "Удалить выбранный товар"))
        self.pushButton_cancel.setText(_translate("Dialog", "Отмена"))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить изменения"))