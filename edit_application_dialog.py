# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditApplicationDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 450)
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
        self.label_user_name = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_user_name.setFont(font)
        self.label_user_name.setObjectName("label_user_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_user)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_user_name)

        self.label_date = QtWidgets.QLabel(Dialog)
        self.label_date.setObjectName("label_date")
        self.label_date_value = QtWidgets.QLabel(Dialog)
        self.label_date_value.setObjectName("label_date_value")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_date)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_date_value)

        self.label_employee = QtWidgets.QLabel(Dialog)
        self.label_employee.setObjectName("label_employee")
        self.comboBox_employee = QtWidgets.QComboBox(Dialog)
        self.comboBox_employee.setObjectName("comboBox_employee")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_employee)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_employee)

        self.label_status = QtWidgets.QLabel(Dialog)
        self.label_status.setObjectName("label_status")
        self.comboBox_status = QtWidgets.QComboBox(Dialog)
        self.comboBox_status.setObjectName("comboBox_status")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_status)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.comboBox_status)

        self.label_description = QtWidgets.QLabel(Dialog)
        self.label_description.setObjectName("label_description")
        self.textEdit_description = QtWidgets.QTextEdit(Dialog)
        self.textEdit_description.setMaximumHeight(100)
        self.textEdit_description.setObjectName("textEdit_description")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_description)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.textEdit_description)

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
        Dialog.setWindowTitle(_translate("Dialog", "Редактировать заявку"))
        self.label_title.setText(_translate("Dialog", "Редактирование заявки"))
        self.label_user.setText(_translate("Dialog", "Пользователь:"))
        self.label_date.setText(_translate("Dialog", "Дата создания:"))
        self.label_employee.setText(_translate("Dialog", "Ответственный сотрудник:"))
        self.label_status.setText(_translate("Dialog", "Статус:"))
        self.label_description.setText(_translate("Dialog", "Описание:"))
        self.pushButton_cancel.setText(_translate("Dialog", "Отмена"))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить"))