# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditReviewDialog(object):
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

        self.label_product_id = QtWidgets.QLabel(Dialog)
        self.label_product_id.setObjectName("label_product_id")
        self.lineEdit_product_id = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_product_id.setObjectName("lineEdit_product_id")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_product_id)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_product_id)

        self.label_rating = QtWidgets.QLabel(Dialog)
        self.label_rating.setObjectName("label_rating")
        self.comboBox_rating = QtWidgets.QComboBox(Dialog)
        self.comboBox_rating.setObjectName("comboBox_rating")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_rating)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_rating)

        self.label_review_text = QtWidgets.QLabel(Dialog)
        self.label_review_text.setObjectName("label_review_text")
        self.textEdit_review_text = QtWidgets.QTextEdit(Dialog)
        self.textEdit_review_text.setMaximumHeight(100)
        self.textEdit_review_text.setObjectName("textEdit_review_text")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_review_text)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.textEdit_review_text)

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
        Dialog.setWindowTitle(_translate("Dialog", "Редактировать отзыв"))
        self.label_title.setText(_translate("Dialog", "Редактирование отзыва"))
        self.label_user_id.setText(_translate("Dialog", "ID пользователя:"))
        self.label_product_id.setText(_translate("Dialog", "ID товара:"))
        self.label_rating.setText(_translate("Dialog", "Рейтинг:"))
        self.label_review_text.setText(_translate("Dialog", "Текст отзыва:"))
        self.pushButton_cancel.setText(_translate("Dialog", "Отмена"))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить"))