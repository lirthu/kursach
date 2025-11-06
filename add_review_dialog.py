# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddReviewDialog(object):
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

        self.label_product = QtWidgets.QLabel(Dialog)
        self.label_product.setObjectName("label_product")
        self.comboBox_product = QtWidgets.QComboBox(Dialog)
        self.comboBox_product.setObjectName("comboBox_product")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_product)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_product)

        self.label_rating = QtWidgets.QLabel(Dialog)
        self.label_rating.setObjectName("label_rating")
        self.comboBox_rating = QtWidgets.QComboBox(Dialog)
        self.comboBox_rating.setObjectName("comboBox_rating")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_rating)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_rating)

        self.label_review = QtWidgets.QLabel(Dialog)
        self.label_review.setObjectName("label_review")
        self.textEdit_review = QtWidgets.QTextEdit(Dialog)
        self.textEdit_review.setMaximumHeight(100)
        self.textEdit_review.setObjectName("textEdit_review")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_review)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.textEdit_review)

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
        Dialog.setWindowTitle(_translate("Dialog", "Добавить отзыв"))
        self.label_title.setText(_translate("Dialog", "Добавление отзыва"))
        self.label_user.setText(_translate("Dialog", "Пользователь:"))
        self.label_product.setText(_translate("Dialog", "Товар:"))
        self.label_rating.setText(_translate("Dialog", "Рейтинг:"))
        self.label_review.setText(_translate("Dialog", "Текст отзыва:"))
        self.pushButton_cancel.setText(_translate("Dialog", "Отмена"))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить"))