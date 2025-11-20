from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditCategoryDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 400)
        Dialog.setStyleSheet("background-color: #ECF0F1;")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_title = QtWidgets.QLabel(Dialog)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(16)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color: #2C3E50;")
        self.label_title.setObjectName("label_title")
        self.verticalLayout.addWidget(self.label_title)

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")

        self.label_name = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(12)
        self.label_name.setFont(font)
        self.label_name.setStyleSheet("color: #2C3E50;")
        self.label_name.setObjectName("label_name")

        self.lineEdit_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_name.setStyleSheet("QLineEdit {\n"
                                         "    background-color: white;\n"
                                         "    border: 2px solid #BDC3C7;\n"
                                         "    border-radius: 4px;\n"
                                         "    padding: 8px;\n"
                                         "    color: #2C3E50;\n"
                                         "    font-family: 'Segoe Print';\n"
                                         "}\n"
                                         "QLineEdit:focus {\n"
                                         "    border-color: #3498DB;\n"
                                         "}")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_name)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_name)

        self.label_description = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(12)
        self.label_description.setFont(font)
        self.label_description.setStyleSheet("color: #2C3E50;")
        self.label_description.setObjectName("label_description")

        self.textEdit_description = QtWidgets.QTextEdit(Dialog)
        self.textEdit_description.setMaximumHeight(150)
        self.textEdit_description.setObjectName("textEdit_description")
        self.textEdit_description.setStyleSheet("QTextEdit {\n"
                                                "    background-color: white;\n"
                                                "    border: 2px solid #BDC3C7;\n"
                                                "    border-radius: 4px;\n"
                                                "    padding: 8px;\n"
                                                "    color: #2C3E50;\n"
                                                "    font-family: 'Segoe Print';\n"
                                                "}\n"
                                                "QTextEdit:focus {\n"
                                                "    border-color: #3498DB;\n"
                                                "}")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_description)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.textEdit_description)

        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout_buttons = QtWidgets.QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_buttons.addItem(spacerItem)

        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.pushButton_cancel.setStyleSheet("QPushButton {\n"
                                             "    background-color: transparent;\n"
                                             "    color: #E74C3C;\n"
                                             "    border: 1px solid #E74C3C;\n"
                                             "    padding: 8px 16px;\n"
                                             "    border-radius: 5px;\n"
                                             "    font-family: 'Segoe Print';\n"
                                             "}\n"
                                             "QPushButton:hover {\n"
                                             "    background-color: #E74C3C;\n"
                                             "    color: white;\n"
                                             "}")
        self.horizontalLayout_buttons.addWidget(self.pushButton_cancel)

        self.pushButton_save = QtWidgets.QPushButton(Dialog)
        self.pushButton_save.setObjectName("pushButton_save")
        self.pushButton_save.setStyleSheet("QPushButton {\n"
                                           "    background-color: transparent;\n"
                                           "    color: #3498DB;\n"
                                           "    border: 1px solid #3498DB;\n"
                                           "    padding: 8px 16px;\n"
                                           "    border-radius: 5px;\n"
                                           "    font-family: 'Segoe Print';\n"
                                           "}\n"
                                           "QPushButton:hover {\n"
                                           "    background-color: #3498DB;\n"
                                           "    color: white;\n"
                                           "}")
        self.horizontalLayout_buttons.addWidget(self.pushButton_save)

        self.verticalLayout.addLayout(self.horizontalLayout_buttons)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Редактировать категорию"))
        self.label_title.setText(_translate("Dialog", "Редактирование категории"))
        self.label_name.setText(_translate("Dialog", "Название:"))
        self.label_description.setText(_translate("Dialog", "Описание:"))
        self.pushButton_cancel.setText(_translate("Dialog", "Отмена"))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить"))