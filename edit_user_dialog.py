# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditUserDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 550)
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

        self.label_first_name = QtWidgets.QLabel(Dialog)
        self.label_first_name.setObjectName("label_first_name")
        self.lineEdit_first_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_first_name.setObjectName("lineEdit_first_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_first_name)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_first_name)

        self.label_last_name = QtWidgets.QLabel(Dialog)
        self.label_last_name.setObjectName("label_last_name")
        self.lineEdit_last_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_last_name.setObjectName("lineEdit_last_name")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_last_name)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_last_name)

        self.label_third_name = QtWidgets.QLabel(Dialog)
        self.label_third_name.setObjectName("label_third_name")
        self.lineEdit_third_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_third_name.setObjectName("lineEdit_third_name")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_third_name)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_third_name)

        self.label_login = QtWidgets.QLabel(Dialog)
        self.label_login.setObjectName("label_login")
        self.lineEdit_login = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_login.setObjectName("lineEdit_login")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_login)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_login)

        self.label_password = QtWidgets.QLabel(Dialog)
        self.label_password.setObjectName("label_password")
        self.lineEdit_password = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_password)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password)

        self.label_phone = QtWidgets.QLabel(Dialog)
        self.label_phone.setObjectName("label_phone")
        self.lineEdit_phone = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_phone.setObjectName("lineEdit_phone")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_phone)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_phone)

        self.label_email = QtWidgets.QLabel(Dialog)
        self.label_email.setObjectName("label_email")
        self.lineEdit_email = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_email.setObjectName("lineEdit_email")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_email)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lineEdit_email)

        self.label_address = QtWidgets.QLabel(Dialog)
        self.label_address.setObjectName("label_address")
        self.lineEdit_address = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_address.setObjectName("lineEdit_address")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_address)
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.lineEdit_address)

        self.verticalLayout.addLayout(self.formLayout)

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
        Dialog.setWindowTitle(_translate("Dialog", "Редактировать пользователя"))
        self.label_title.setText(_translate("Dialog", "Редактирование пользователя"))
        self.label_first_name.setText(_translate("Dialog", "Имя:"))
        self.label_last_name.setText(_translate("Dialog", "Фамилия:"))
        self.label_third_name.setText(_translate("Dialog", "Отчество:"))
        self.label_login.setText(_translate("Dialog", "Логин:"))
        self.label_password.setText(_translate("Dialog", "Пароль:"))
        self.label_phone.setText(_translate("Dialog", "Телефон:"))
        self.label_email.setText(_translate("Dialog", "Email:"))
        self.label_address.setText(_translate("Dialog", "Адрес:"))
        self.pushButton_cancel.setText(_translate("Dialog", "Отмена"))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить"))