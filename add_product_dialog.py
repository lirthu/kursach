# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddProductDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 550)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        # Заголовок
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

        # Основная форма
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(15)
        self.formLayout.setObjectName("formLayout")

        # Название товара
        self.label_name = QtWidgets.QLabel(Dialog)
        self.label_name.setObjectName("label_name")
        self.lineEdit_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_name)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_name)

        # Описание
        self.label_description = QtWidgets.QLabel(Dialog)
        self.label_description.setObjectName("label_description")
        self.textEdit_description = QtWidgets.QTextEdit(Dialog)
        self.textEdit_description.setMaximumHeight(80)
        self.textEdit_description.setObjectName("textEdit_description")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_description)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.textEdit_description)

        # Цена
        self.label_price = QtWidgets.QLabel(Dialog)
        self.label_price.setObjectName("label_price")
        self.lineEdit_price = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_price.setObjectName("lineEdit_price")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_price)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_price)

        # Категория
        self.label_category = QtWidgets.QLabel(Dialog)
        self.label_category.setObjectName("label_category")
        self.comboBox_category = QtWidgets.QComboBox(Dialog)
        self.comboBox_category.setObjectName("comboBox_category")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_category)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.comboBox_category)

        # Бренд
        self.label_brand = QtWidgets.QLabel(Dialog)
        self.label_brand.setObjectName("label_brand")
        self.lineEdit_brand = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_brand.setObjectName("lineEdit_brand")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_brand)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_brand)

        self.verticalLayout.addLayout(self.formLayout)

        # Добавьте после поля "Бренд" в setupUi:

        # Изображение
        self.label_image = QtWidgets.QLabel(Dialog)
        self.label_image.setObjectName("label_image")
        self.horizontalLayout_image = QtWidgets.QHBoxLayout()
        self.horizontalLayout_image.setObjectName("horizontalLayout_image")
        self.lineEdit_image = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_image.setObjectName("lineEdit_image")
        self.lineEdit_image.setReadOnly(True)  # Только для отображения
        self.pushButton_browse = QtWidgets.QPushButton(Dialog)
        self.pushButton_browse.setObjectName("pushButton_browse")
        self.pushButton_browse.setText("Обзор...")
        self.horizontalLayout_image.addWidget(self.lineEdit_image)
        self.horizontalLayout_image.addWidget(self.pushButton_browse)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_image)
        self.formLayout.setLayout(5, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_image)

        # Превью изображения
        self.label_image_preview = QtWidgets.QLabel(Dialog)
        self.label_image_preview.setMinimumSize(200, 200)
        self.label_image_preview.setMaximumSize(200, 200)
        self.label_image_preview.setFrameShape(QtWidgets.QFrame.Box)
        self.label_image_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image_preview.setText("Нет изображения")
        self.label_image_preview.setObjectName("label_image_preview")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.label_image_preview)

        # Кнопки
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
        Dialog.setWindowTitle(_translate("Dialog", "Добавить товар"))
        self.label_title.setText(_translate("Dialog", "Добавление нового товара"))
        self.label_name.setText(_translate("Dialog", "Название:"))
        self.label_description.setText(_translate("Dialog", "Описание:"))
        self.label_price.setText(_translate("Dialog", "Цена:"))
        self.label_category.setText(_translate("Dialog", "Категория:"))
        self.label_brand.setText(_translate("Dialog", "Бренд:"))
        self.label_image.setText(_translate("Dialog", "Изображение:"))
        self.pushButton_cancel.setText(_translate("Dialog", "Отмена"))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить"))
