from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFrame, \
    QSpacerItem, QSizePolicy
from PyQt5 import QtCore, QtGui


class Ui_AddCategoryDialog(object):
    def setupUi(self, AddCategoryDialog):
        AddCategoryDialog.setObjectName("AddCategoryDialog")
        AddCategoryDialog.resize(500, 400)
        AddCategoryDialog.setStyleSheet("background-color: #ECF0F1;")
        self.verticalLayout = QVBoxLayout(AddCategoryDialog)
        self.verticalLayout.setObjectName("verticalLayout")

        # Заголовок
        self.label_title = QLabel(AddCategoryDialog)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(16)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color: #2C3E50;")
        self.label_title.setObjectName("label_title")
        self.verticalLayout.addWidget(self.label_title)

        # Разделительная линия
        self.line = QFrame(AddCategoryDialog)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setStyleSheet("color: #BDC3C7;")
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        # Форма с полями
        self.formLayout = QVBoxLayout()
        self.formLayout.setObjectName("formLayout")

        # Название категории
        self.label_name = QLabel(AddCategoryDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(12)
        self.label_name.setFont(font)
        self.label_name.setStyleSheet("color: #2C3E50;")
        self.label_name.setObjectName("label_name")
        self.formLayout.addWidget(self.label_name)

        self.lineEdit_name = QLineEdit(AddCategoryDialog)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_name.setPlaceholderText("Введите название категории")
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
        self.formLayout.addWidget(self.lineEdit_name)

        # Добавляем отступ между полями
        spacer_item1 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.formLayout.addItem(spacer_item1)

        # Описание категории
        self.label_description = QLabel(AddCategoryDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(12)
        self.label_description.setFont(font)
        self.label_description.setStyleSheet("color: #2C3E50;")
        self.label_description.setObjectName("label_description")
        self.formLayout.addWidget(self.label_description)

        self.textEdit_description = QTextEdit(AddCategoryDialog)
        self.textEdit_description.setObjectName("textEdit_description")
        self.textEdit_description.setPlaceholderText("Введите описание категории (необязательно)")
        self.textEdit_description.setMaximumHeight(120)
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
        self.formLayout.addWidget(self.textEdit_description)

        self.verticalLayout.addLayout(self.formLayout)

        # Горизонтальный спейсер для растягивания формы
        vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(vertical_spacer)

        # Кнопки
        self.horizontalLayout_buttons = QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")

        # Горизонтальный спейсер для выравнивания кнопок вправо
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_buttons.addItem(spacer_item)

        self.pushButton_cancel = QPushButton(AddCategoryDialog)
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

        self.pushButton_save = QPushButton(AddCategoryDialog)
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

        self.retranslateUi(AddCategoryDialog)
        QtCore.QMetaObject.connectSlotsByName(AddCategoryDialog)

    def retranslateUi(self, AddCategoryDialog):
        _translate = QtCore.QCoreApplication.translate
        AddCategoryDialog.setWindowTitle(_translate("AddCategoryDialog", "Добавить категорию"))
        self.label_title.setText(_translate("AddCategoryDialog", "Добавление категории"))
        self.label_name.setText(_translate("AddCategoryDialog", "Название категории:"))
        self.label_description.setText(_translate("AddCategoryDialog", "Описание:"))
        self.pushButton_cancel.setText(_translate("AddCategoryDialog", "Отмена"))
        self.pushButton_save.setText(_translate("AddCategoryDialog", "Сохранить"))