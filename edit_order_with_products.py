# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditOrderWithProductsDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 500)
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

        # ID заказа
        self.label_order_id = QtWidgets.QLabel(Dialog)
        self.label_order_id.setObjectName("label_order_id")
        self.label_order_id_value = QtWidgets.QLabel(Dialog)
        self.label_order_id_value.setObjectName("label_order_id_value")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_order_id)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_order_id_value)

        self.label_user = QtWidgets.QLabel(Dialog)
        self.label_user.setObjectName("label_user")
        self.label_user_value = QtWidgets.QLabel(Dialog)
        self.label_user_value.setObjectName("label_user_value")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_user)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_user_value)

        self.label_status = QtWidgets.QLabel(Dialog)
        self.label_status.setObjectName("label_status")
        self.comboBox_status = QtWidgets.QComboBox(Dialog)
        self.comboBox_status.setObjectName("comboBox_status")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_status)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_status)

        self.label_date = QtWidgets.QLabel(Dialog)
        self.label_date.setObjectName("label_date")
        self.label_date_value = QtWidgets.QLabel(Dialog)
        self.label_date_value.setObjectName("label_date_value")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_date)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_date_value)

        self.label_total = QtWidgets.QLabel(Dialog)
        self.label_total.setObjectName("label_total")
        self.label_total_value = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_total_value.setFont(font)
        self.label_total_value.setObjectName("label_total_value")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_total)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.label_total_value)

        self.verticalLayout.addLayout(self.formLayout)

        # Секция товаров в заказе
        self.label_products = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(12)
        self.label_products.setFont(font)
        self.label_products.setObjectName("label_products")
        self.verticalLayout.addWidget(self.label_products)

        # Таблица товаров в заказе (только для просмотра)
        self.tableWidget_products = QtWidgets.QTableWidget(Dialog)
        self.tableWidget_products.setObjectName("tableWidget_products")
        self.tableWidget_products.setColumnCount(4)
        self.tableWidget_products.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Только чтение
        self.verticalLayout.addWidget(self.tableWidget_products)

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
        self.label_order_id.setText(_translate("Dialog", "Номер заказа:"))
        self.label_user.setText(_translate("Dialog", "Пользователь:"))
        self.label_status.setText(_translate("Dialog", "Статус:"))
        self.label_date.setText(_translate("Dialog", "Дата заказа:"))
        self.label_total.setText(_translate("Dialog", "Итоговая сумма:"))
        self.label_products.setText(_translate("Dialog", "Товары в заказе:"))
        self.pushButton_cancel.setText(_translate("Dialog", "Отмена"))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить изменения"))