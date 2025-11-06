# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddOrderDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 400)
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

        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")

        self.label_user = QtWidgets.QLabel(Dialog)
        self.label_user.setObjectName("label_user")
        self.comboBox_user = QtWidgets.QComboBox(Dialog)
        self.comboBox_user.setObjectName("comboBox_user")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_user)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_user)

        self.label_date = QtWidgets.QLabel(Dialog)
        self.label_date.setObjectName("label_date")
        self.dateEdit = QtWidgets.QDateEdit(Dialog)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_date)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dateEdit)

        self.label_status = QtWidgets.QLabel(Dialog)
        self.label_status.setObjectName("label_status")
        self.comboBox_status = QtWidgets.QComboBox(Dialog)
        self.comboBox_status.setObjectName("comboBox_status")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_status)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_status)

        self.label_sum = QtWidgets.QLabel(Dialog)
        self.label_sum.setObjectName("label_sum")
        self.lineEdit_sum = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_sum.setObjectName("lineEdit_sum")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_sum)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_sum)

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
        Dialog.setWindowTitle(_translate("Dialog", "Добавить заказ"))
        self.label_title.setText(_translate("Dialog", "Добавление заказа"))
        self.label_user.setText(_translate("Dialog", "Пользователь:"))
        self.label_date.setText(_translate("Dialog", "Дата:"))
        self.label_status.setText(_translate("Dialog", "Статус:"))
        self.label_sum.setText(_translate("Dialog", "Сумма:"))
        self.pushButton_cancel.setText(_translate("Dialog", "Отмена"))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить"))