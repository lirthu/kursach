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

        self.label_user_id = QtWidgets.QLabel(Dialog)
        self.label_user_id.setObjectName("label_user_id")
        self.lineEdit_user_id = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_user_id.setObjectName("lineEdit_user_id")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_user_id)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_user_id)

        self.label_employee_id = QtWidgets.QLabel(Dialog)
        self.label_employee_id.setObjectName("label_employee_id")
        self.lineEdit_employee_id = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_employee_id.setObjectName("lineEdit_employee_id")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_employee_id)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_employee_id)

        self.label_status = QtWidgets.QLabel(Dialog)
        self.label_status.setObjectName("label_status")
        self.comboBox_status = QtWidgets.QComboBox(Dialog)
        self.comboBox_status.setObjectName("comboBox_status")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_status)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_status)

        self.label_date = QtWidgets.QLabel(Dialog)
        self.label_date.setObjectName("label_date")
        self.lineEdit_date = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_date.setObjectName("lineEdit_date")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_date)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_date)

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
        self.label_user_id.setText(_translate("Dialog", "ID пользователя:"))
        self.label_employee_id.setText(_translate("Dialog", "ID сотрудника:"))
        self.label_status.setText(_translate("Dialog", "Статус:"))
        self.label_date.setText(_translate("Dialog", "Дата:"))
        self.label_description.setText(_translate("Dialog", "Описание:"))
        self.pushButton_cancel.setText(_translate("Dialog", "Отмена"))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить"))