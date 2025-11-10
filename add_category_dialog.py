from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt5 import QtCore


class Ui_AddCategoryDialog(object):
    def setupUi(self, AddCategoryDialog):
        AddCategoryDialog.setObjectName("AddCategoryDialog")
        AddCategoryDialog.resize(400, 300)
        AddCategoryDialog.setMinimumSize(400, 300)
        AddCategoryDialog.setMaximumSize(500, 400)

        self.verticalLayout = QVBoxLayout(AddCategoryDialog)
        self.verticalLayout.setObjectName("verticalLayout")

        # Название категории
        self.label_name = QLabel(AddCategoryDialog)
        self.label_name.setObjectName("label_name")
        self.verticalLayout.addWidget(self.label_name)

        self.lineEdit_name = QLineEdit(AddCategoryDialog)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_name.setPlaceholderText("Введите название категории")
        self.verticalLayout.addWidget(self.lineEdit_name)

        # Описание категории
        self.label_description = QLabel(AddCategoryDialog)
        self.label_description.setObjectName("label_description")
        self.verticalLayout.addWidget(self.label_description)

        self.textEdit_description = QTextEdit(AddCategoryDialog)
        self.textEdit_description.setObjectName("textEdit_description")
        self.textEdit_description.setPlaceholderText("Введите описание категории")
        self.textEdit_description.setMaximumHeight(120)
        self.verticalLayout.addWidget(self.textEdit_description)

        # Кнопки
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton_save = QPushButton(AddCategoryDialog)
        self.pushButton_save.setObjectName("pushButton_save")
        self.pushButton_save.setMinimumSize(100, 30)
        self.horizontalLayout.addWidget(self.pushButton_save)

        self.pushButton_cancel = QPushButton(AddCategoryDialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(100, 30)
        self.horizontalLayout.addWidget(self.pushButton_cancel)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(AddCategoryDialog)

    def retranslateUi(self, AddCategoryDialog):
        _translate = QtCore.QCoreApplication.translate  # Исправлено здесь
        AddCategoryDialog.setWindowTitle(_translate("AddCategoryDialog", "Добавить категорию"))
        self.label_name.setText(_translate("AddCategoryDialog", "Название категории:"))
        self.label_description.setText(_translate("AddCategoryDialog", "Описание:"))
        self.pushButton_save.setText(_translate("AddCategoryDialog", "Сохранить"))
        self.pushButton_cancel.setText(_translate("AddCategoryDialog", "Отмена"))