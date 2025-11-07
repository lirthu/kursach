import sys
import sqlite3

from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem, QMenu
from PyQt5 import QtCore

from authorize import Ui_Auth_Form
from registration import Ui_Reg_Form
from admin_panel import Ui_Admin_Form
from profile import Ui_Profile_Form
from catalog import Ui_Catalog_Form
from shopping_cart import Ui_Cart_Form
from c_application import Ui_Create_Application_Form
from order import Ui_Order_Form
from order_content import Ui_Content_Form
from application_view import Ui_Application_Form
from add_product_dialog import Ui_AddProductDialog
from add_order_dialog import Ui_AddOrderDialog
from add_review_dialog import Ui_AddReviewDialog
from add_application_dialog import Ui_AddApplicationDialog
from add_user_dialog import Ui_AddUserDialog
from add_employee_dialog import Ui_AddEmployeeDialog
from edit_product_dialog import Ui_EditProductDialog
from edit_user_dialog import Ui_EditUserDialog
from edit_employee_dialog import Ui_EditEmployeeDialog
from edit_order_dialog import Ui_EditOrderDialog
from edit_review_dialog import Ui_EditReviewDialog
from edit_application_dialog import Ui_EditApplicationDialog

def get_connection():
    connect = sqlite3.connect('database.db')
    c = connect.cursor()
    c.execute("PRAGMA foreign_keys = ON;")  # подключает внешние ключи (чтобы  можно было делать связи между таблицами)
    c.row_factory = sqlite3.Row
    return connect

class MainWindow(QDialog, Ui_Auth_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_2.clicked.connect(self.open_register_window)
        self.pushButton.clicked.connect(self.clicked_login)

    def clicked_login(self):
        connect  = get_connection()
        c = connect.cursor()
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите все данные!")
            return

        c.execute('''SELECT id FROM user WHERE login = ? AND password = ?''', (login, password))
        result = c.fetchone()

        if result:
            self.current_user_id = result[0]
            self.open_main_catalog()
            return

        c.execute('''SELECT id FROM employee WHERE login = ? AND password = ?''', (login, password))
        result = c.fetchone()

        if result:
            self.current_user_id = result[0]
            self.open_admin_panel()
            return

        QMessageBox.warning(self, "Ошибка", "Пользователь не найден!")

    def open_main_catalog(self):
        self.close()
        self.win = CatalogWin(self.current_user_id)
        self.win.show()

    def open_register_window(self):
        self.close()
        self.win = RegisterWin()
        self.win.show()

    def open_admin_panel(self):
        self.close()
        self.win = AdminPanel(self.current_user_id)
        self.win.show()

class RegisterWin(QDialog, Ui_Reg_Form):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.pushButton.clicked.connect(self.registration)
        self.pushButton_2.clicked.connect(self.open_main_window_return)

    def registration(self):
        connect = get_connection()
        c = connect.cursor()
        try:
            name = self.lineEdit_2.text().strip()
            last_name = self.lineEdit.text().strip()
            third_name = self.lineEdit_3.text().strip()
            login = self.lineEdit_7.text().strip()
            password = self.lineEdit_8.text().strip()
            return_password = self.lineEdit_9.text().strip()
            phone = self.lineEdit_4.text().strip()
            email = self.lineEdit_6.text().strip()
            address = self.lineEdit_5.text().strip()


            if not name or not last_name or not login or not password or not return_password:
                QMessageBox.warning(self, "Внимание", "Заполните все поля.")
                return
            if password != return_password:
                QMessageBox.critical(self, "Ошибка", "Пароли не совпадают.")
                return

            c.execute('''INSERT INTO user (first_name, last_name, third_name, login, password, phone, email, address) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (name, last_name, third_name, login, password, email, phone, address))

            connect.commit()
            self.open_main_window(login)

        except Exception as e:
            print(e)

    def open_main_catalog(self):
        self.close()
        self.win = CatalogWin()
        self.win.show()

    def open_main_window_return(self):
        self.close()
        self.win = MainWindow()
        self.win.show()

    def open_main_window(self,login):
        self.close()
        self.win = MainWindow()
        self.win.lineEdit.setText(login)
        self.win.lineEdit_2.setFocus()
        self.win.show()

class CatalogWin(QDialog, Ui_Catalog_Form):
    def __init__(self, user_id = None):
        super().__init__()
        self.setupUi(self)
        self.user_id = user_id

        menu_manager = ProfileMenuManager(user_id, 'user')
        self.pushButton.setMenu(menu_manager.create_profile_menu(self))

class ProfileWin(QDialog, Ui_Profile_Form):
    def __init__(self, user_id = None, user_type = 'user'):
        super().__init__()
        self.setupUi(self)
        self.user_id = user_id
        self.user_type = user_type

        self.load_user_data()

        self.pushButton.clicked.connect(self.save_changes)

    def load_user_data(self):
        conn = get_connection()
        c = conn.cursor()
        # Получаем данные пользователя

        if self.user_type == 'user':
            c.execute('''SELECT first_name, last_name, third_name, login, password, phone, email, 
            address FROM user 
                        WHERE id = ?''', (self.user_id,))
        else:
            c.execute('''SELECT first_name, last_name, third_name, login, password, phone, email, 
            address FROM employee 
                        WHERE id = ?''', (self.user_id,))

        user_data = c.fetchone()
        conn.close()

        if user_data:
            # Заполняем поля данными из БД
            self.lineEdit.setText(user_data[1] if user_data[1] else "")  # фамилия
            self.lineEdit_2.setText(user_data[0] if user_data[0] else "") # имя
            self.lineEdit_3.setText(user_data[2] if user_data[2] else "") # отчество
            self.lineEdit_4.setText(user_data[3] if user_data[3] else "") # логин
            self.lineEdit_5.setText(user_data[4] if user_data[4] else "") # пароль
            self.lineEdit_6.setText(user_data[6] if user_data[6] else "") # телефон
            self.lineEdit_7.setText(user_data[5] if user_data[5] else "") # почта
            self.lineEdit_8.setText(user_data[7] if user_data[7] else "") # адрес

    def save_changes(self):
        conn = get_connection()
        c = conn.cursor()
        try:
            # Получаем текущие значения из полей
            first_name = self.lineEdit_2.text()
            last_name = self.lineEdit.text()
            third_name = self.lineEdit_3.text()
            login = self.lineEdit_4.text()
            password = self.lineEdit_5.text()
            phone = self.lineEdit_6.text()
            email = self.lineEdit_7.text()
            address = self.lineEdit_8.text()

            # Обновляем данные пользователя в БД

            if self.user_type == 'user':
                c.execute('''UPDATE user 
                             SET first_name = ?, last_name = ?, third_name = ?, 
                                 login = ?, password = ?, phone = ?, email = ?,
                                 address = ? 
                             WHERE id = ?''',
          (first_name, last_name, third_name, login, password, phone, email, address, self.user_id))
            else:
                c.execute('''UPDATE employee 
                             SET first_name = ?, last_name = ?, third_name = ?, 
                                 login = ?, password = ?, phone = ?, email = ?,
                                 address = ? 
                             WHERE id = ?''',
          (first_name, last_name, third_name, login, password, phone, email, address, self.user_id))
            conn.commit()
            QMessageBox.information(self,'Успешно', 'Данные успешно сохранены')
        except Exception as e:
            print(e)

class ProfileMenuManager:
    def __init__(self, user_id, user_type='user'):
        self.user_id = user_id
        self.user_type = user_type

    def create_profile_menu(self, parent_window):
        """Создаем выпадающее меню для кнопки Профиль"""
        profile_menu = QMenu()

        menu_font = profile_menu.font()
        menu_font.setFamily("Segoe Print")
        menu_font.setPointSize(10)
        profile_menu.setFont(menu_font)

        # Добавляем пункты меню
        open_profile_menu = profile_menu.addAction("Личные данные")
        open_order_menu = profile_menu.addAction("Заказы")
        application = profile_menu.addAction("Заявки")
        profile_menu.addSeparator()
        back_to_log = profile_menu.addAction("Выйти")

        open_profile_menu.triggered.connect(lambda: self.open_profile_menu(parent_window))
        open_order_menu.triggered.connect(lambda: self.open_order_menu(parent_window))
        back_to_log.triggered.connect(lambda: self.open_main_window_return(parent_window))
        application.triggered.connect(lambda: self.open_application_menu(parent_window))
        return profile_menu

    def open_profile_menu(self, parent_window):
        parent_window.win = ProfileWin(self.user_id, self.user_type)
        parent_window.win.show()

    def open_order_menu(self, parent_window):
        parent_window.close()
        parent_window.win = OrderWin(self.user_id)
        parent_window.win.show()

    def open_application_menu(self, parent_window):
        parent_window.close()
        parent_window.win = Application(self.user_id)
        parent_window.win.show()

    def open_main_window_return(self, parent_window):
        parent_window.close()
        parent_window.win = MainWindow()
        parent_window.win.show()

class OrderWin(QDialog, Ui_Order_Form):
    def __init__(self, user_id = None):
        super().__init__()
        self.setupUi(self)

        menu_manager = ProfileMenuManager(user_id, 'user')
        self.pushButton.setMenu(menu_manager.create_profile_menu(self))

class OrderContent(QDialog, Ui_Content_Form):
    def __init__(self, user_id = None):
        super().__init__()
        self.setupUi(self)

class Application(QDialog, Ui_Application_Form):
    def __init__(self, user_id = None):
        super().__init__()
        self.setupUi(self)
        self.user_id = user_id
        menu_manager = ProfileMenuManager(user_id, 'user')
        self.pushButton.setMenu(menu_manager.create_profile_menu(self))

        self.pushButton_6.clicked.connect(self.open_main_window_return)

    def open_main_window_return(self):
        self.close()
        self.win = CatalogWin(self.user_id)
        self.win.show()

class CreateApplication(QDialog, Ui_Create_Application_Form):
    def __init__(self, user_id = None):
        super().__init__()
        self.setupUi(self)

class ShoppingCart(QDialog, Ui_Cart_Form):
    def __init__(self, user_id = None):
        super().__init__()
        self.setupUi(self)


class AdminPanel(QDialog, Ui_Admin_Form):
    def __init__(self, user_id = None):
        super().__init__()
        self.setupUi(self)
        self.current_user_id = user_id
        self.load_users_to_table()
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

        self.pushButton_2.clicked.connect(self.add_item)
        self.pushButton_3.clicked.connect(self.delete_item)
        self.pushButton_4.clicked.connect(self.edit_item)

        self.create_profile_menu()

    def add_item(self):
        """Добавление элемента в зависимости от активной вкладки"""
        current_tab = self.tabWidget.currentIndex()

        if current_tab == 0:  # Заказы
            self.add_order()
        elif current_tab == 1:  # Товары
            self.add_product()
        elif current_tab == 2:  # Отзывы
            self.add_review()
        elif current_tab == 3:  # Клиенты
            self.add_user()
        elif current_tab == 4:  # Сотрудники
            self.add_employee()
        elif current_tab == 5:  # Заявки
            self.add_application()

    def add_product(self):
        """Открывает диалог добавления товара"""
        dialog = AddProductDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Обновляем таблицу товаров после добавления
            self.load_products_to_table()

    def add_order(self):
        dialog = AddOrderDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_orders_to_table()

    def add_review(self):
        dialog = AddReviewDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_reviews_to_table()

    def add_application(self):
        dialog = AddApplicationDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_applications_to_table()

    def add_user(self):
        dialog = AddUserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users_to_table()

    def add_employee(self):
        dialog = AddEmployeeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_employees_to_table()

    def edit_item(self):
        """Редактирование выбранного элемента"""
        current_tab = self.tabWidget.currentIndex()

        if current_tab == 0:  # Заказы
            self.edit_order()
        elif current_tab == 1:  # Товары
            self.edit_product()
        elif current_tab == 2:  # Отзывы
            self.edit_review()
        elif current_tab == 3:  # Клиенты
            self.edit_user()
        elif current_tab == 4:  # Сотрудники
            self.edit_employee()
        elif current_tab == 5:  # Заявки
            self.edit_application()

    def edit_product(self):
        """Редактирование выбранного товара"""
        table_widget = self.tableWidget_2
        current_row = table_widget.currentRow()

        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для редактирования")
            return

        product_id = table_widget.item(current_row, 0).text()
        product_name = table_widget.item(current_row, 1).text()

        # Открываем диалог редактирования
        dialog = EditProductDialog(self, product_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_products_to_table()

    def edit_user(self):
        """Редактирование выбранного пользователя"""
        table_widget = self.tableWidget_4
        current_row = table_widget.currentRow()

        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для редактирования")
            return

        user_id = table_widget.item(current_row, 0).text()

        dialog = EditUserDialog(self, user_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users_to_table()

    def edit_employee(self):
        """Редактирование выбранного сотрудника"""
        table_widget = self.tableWidget_5
        current_row = table_widget.currentRow()

        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для редактирования")
            return

        employee_id = table_widget.item(current_row, 0).text()

        dialog = EditEmployeeDialog(self, employee_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_employees_to_table()

    def edit_order(self):
        """Редактирование выбранного заказа"""
        table_widget = self.tableWidget
        current_row = table_widget.currentRow()

        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для редактирования")
            return

        order_id = table_widget.item(current_row, 0).text()

        dialog = EditOrderDialog(self, order_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_orders_to_table()

    def edit_review(self):
        """Редактирование выбранного отзыва"""
        table_widget = self.tableWidget_3
        current_row = table_widget.currentRow()

        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите отзыв для редактирования")
            return

        review_id = table_widget.item(current_row, 0).text()

        dialog = EditReviewDialog(self, review_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_reviews_to_table()

    def edit_application(self):
        """Редактирование выбранной заявки"""
        table_widget = self.tableWidget_6
        current_row = table_widget.currentRow()

        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите заявку для редактирования")
            return

        application_id = table_widget.item(current_row, 0).text()

        dialog = EditApplicationDialog(self, application_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_applications_to_table()

    def delete_item(self):
        """Удаление выбранного элемента"""
        current_tab = self.tabWidget.currentIndex()

        if current_tab == 0:  # Заказы
            self.delete_order()
        elif current_tab == 1:  # Товары
            self.delete_product()
        elif current_tab == 2:  # Отзывы
            self.delete_review()
        elif current_tab == 3:  # Клиенты
            self.delete_user()
        elif current_tab == 4:  # Сотрудники
            self.delete_employee()
        elif current_tab == 5:  # Заявки
            self.delete_application()

    def delete_product(self):
        """Удаление выбранного товара"""
        table_widget = self.tableWidget_2
        current_row = table_widget.currentRow()

        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для удаления")
            return

        product_id = table_widget.item(current_row, 0).text()
        product_name = table_widget.item(current_row, 1).text()

        reply = QMessageBox.question(self, "Подтверждение",
                                     f"Вы уверены, что хотите удалить товар '{product_name}'?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            conn = get_connection()
            c = conn.cursor()
            try:
                c.execute("DELETE FROM product WHERE id = ?", (product_id,))
                conn.commit()
                self.load_products_to_table()
                QMessageBox.information(self, "Успех", "Товар удален")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить товар: {str(e)}")
            finally:
                conn.close()

    def delete_order(self):
        table_widget = self.tableWidget
        current_row = table_widget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для удаления")
            return

        order_id = table_widget.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Подтверждение", "Удалить выбранный заказ?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            conn = get_connection()
            c = conn.cursor()
            try:
                c.execute("DELETE FROM user_order WHERE id = ?", (order_id,))
                conn.commit()
                self.load_orders_to_table()
                QMessageBox.information(self, "Успех", "Заказ удален")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить заказ: {str(e)}")
            finally:
                conn.close()

    def delete_review(self):
        table_widget = self.tableWidget_3
        current_row = table_widget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите отзыв для удаления")
            return

        review_id = table_widget.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Подтверждение", "Удалить выбранный отзыв?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            conn = get_connection()
            c = conn.cursor()
            try:
                c.execute("DELETE FROM review WHERE id = ?", (review_id,))
                conn.commit()
                self.load_reviews_to_table()
                QMessageBox.information(self, "Успех", "Отзыв удален")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить отзыв: {str(e)}")
            finally:
                conn.close()

    def delete_application(self):
        table_widget = self.tableWidget_6
        current_row = table_widget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите заявку для удаления")
            return

        application_id = table_widget.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Подтверждение", "Удалить выбранную заявку?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            conn = get_connection()
            c = conn.cursor()
            try:
                c.execute("DELETE FROM application WHERE id = ?", (application_id,))
                conn.commit()
                self.load_applications_to_table()
                QMessageBox.information(self, "Успех", "Заявка удалена")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить заявку: {str(e)}")
            finally:
                conn.close()

    def delete_user(self):
        table_widget = self.tableWidget_4
        current_row = table_widget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для удаления")
            return

        user_id = table_widget.item(current_row, 0).text()
        user_name = f"{table_widget.item(current_row, 1).text()} {table_widget.item(current_row, 2).text()}"

        reply = QMessageBox.question(self, "Подтверждение", f"Удалить пользователя {user_name}?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            conn = get_connection()
            c = conn.cursor()
            try:
                c.execute("DELETE FROM user WHERE id = ?", (user_id,))
                conn.commit()
                self.load_users_to_table()
                QMessageBox.information(self, "Успех", "Пользователь удален")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить пользователя: {str(e)}")
            finally:
                conn.close()

    def delete_employee(self):
        table_widget = self.tableWidget_5
        current_row = table_widget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для удаления")
            return

        employee_id = table_widget.item(current_row, 0).text()
        employee_name = f"{table_widget.item(current_row, 1).text()} {table_widget.item(current_row, 2).text()}"

        reply = QMessageBox.question(self, "Подтверждение", f"Удалить сотрудника {employee_name}?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            conn = get_connection()
            c = conn.cursor()
            try:
                c.execute("DELETE FROM employee WHERE id = ?", (employee_id,))
                conn.commit()
                self.load_employees_to_table()
                QMessageBox.information(self, "Успех", "Сотрудник удален")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить сотрудника: {str(e)}")
            finally:
                conn.close()

    def create_profile_menu(self):
        """Создаем выпадающее меню для кнопки Профиль"""
        self.profile_menu = QMenu()

        menu_font = self.profile_menu.font()
        menu_font.setFamily("Segoe Print")  # Ваш шрифт
        menu_font.setPointSize(10)  # Размер текста
        self.profile_menu.setFont(menu_font)

        # Добавляем пункты меню
        open_profile_menu = self.profile_menu.addAction("Личные данные")
        self.profile_menu.addSeparator()
        back_to_log = self.profile_menu.addAction("Выйти")

        open_profile_menu.triggered.connect(self.open_profile_menu)
        back_to_log.triggered.connect(self.open_main_window_return)

        self.pushButton.setMenu(self.profile_menu)

    def open_profile_menu(self):
        self.win = ProfileWin(self.current_user_id, user_type="employee")
        self.win.show()

    def open_main_window_return(self):
        self.close()
        self.win = MainWindow()
        self.win.show()

    def load_reviews_to_table(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute('''SELECT id, user_id, product_id, rating, review_text, date 
                                     FROM review''')
        data = c.fetchall()
        conn.close()

        table_widget = self.tableWidget_3
        self.populate_reviews_table(table_widget, data)

    def load_products_to_table(self):
        """Загрузка товаров в таблицу"""
        conn = get_connection()
        c = conn.cursor()
        c.execute('''SELECT id, name, brand, description, price 
                                     FROM product''')
        data = c.fetchall()
        conn.close()

        table_widget = self.tableWidget_2
        self.populate_product_table(table_widget, data)

    def load_orders_to_table(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute('''SELECT id, user_id, date, status, sum 
                                     FROM user_order''')
        data = c.fetchall()
        conn.close()

        table_widget = self.tableWidget
        self.populate_orders_table(table_widget, data)

    def load_employees_to_table(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute('''SELECT * FROM employee''')
        data = c.fetchall()
        conn.close()

        table_widget = self.tableWidget_5
        self.populate_table(table_widget, data)

    def load_users_to_table(self):
        conn = get_connection()
        c = conn.cursor()  # Исправлено: было connect.cursor()
        c.execute('''SELECT * FROM user''')
        data = c.fetchall()
        conn.close()

        table_widget = self.tableWidget_4
        self.populate_table(table_widget, data)

    def load_applications_to_table(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute('''SELECT id, user_id, employee_id, status, date, description
                                     FROM application''')
        data = c.fetchall()
        conn.close()

        table_widget = self.tableWidget_6
        self.populate_applications_table(table_widget, data)

    def populate_orders_table(self, table_widget, data):
        if not data:
            table_widget.setRowCount(0)
            table_widget.setColumnCount(0)
            return

        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]))

        headers = ['ID', 'Пользователь', 'Дата', 'Статус', 'Сумма']
        table_widget.setHorizontalHeaderLabels(headers)

        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                table_widget.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))

        table_widget.verticalHeader().setVisible(False)
        table_widget.resizeColumnsToContents()

    def populate_reviews_table(self, table_widget, data):
        if not data:
            table_widget.setRowCount(0)
            table_widget.setColumnCount(0)
            return

        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]))

        headers = ['ID', 'Пользователь', 'Товар', 'Рейтинг', 'Текст отзыва', 'Дата']
        table_widget.setHorizontalHeaderLabels(headers)

        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                table_widget.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))

        table_widget.verticalHeader().setVisible(False)
        table_widget.resizeColumnsToContents()

    def populate_product_table(self, table_widget, data):
        """Заполнение таблицы товаров"""
        if not data:
            table_widget.setRowCount(0)
            table_widget.setColumnCount(0)
            return

        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]))

        headers = ['ID', 'Название', 'Категория', 'Бренд', 'Описание', 'Цена']
        table_widget.setHorizontalHeaderLabels(headers)

        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                table_widget.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))

        table_widget.verticalHeader().setVisible(False)
        table_widget.resizeColumnsToContents()

    def populate_table(self, table_widget, data):
        if not data:
            table_widget.setRowCount(0)
            table_widget.setColumnCount(0)
            return

        table_widget.setRowCount(len(data))  # кол-во строк и столбцов
        table_widget.setColumnCount(len(data[0]))

        headers = ['ID', 'Имя', 'Фамилия', 'Отчество', 'Логин', 'Пароль', 'Телефон', 'Email', 'Адрес']
        table_widget.setHorizontalHeaderLabels(headers)

        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                table_widget.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))

        table_widget.verticalHeader().setVisible(False)
        table_widget.resizeColumnsToContents()

    def populate_applications_table(self, table_widget, data):
        if not data:
            table_widget.setRowCount(0)
            table_widget.setColumnCount(0)
            return

        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]))

        headers = ['ID', 'Пользователь', 'Сотрудник', 'Статус', 'Дата', 'Описание']
        table_widget.setHorizontalHeaderLabels(headers)

        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                table_widget.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))

        table_widget.verticalHeader().setVisible(False)
        table_widget.resizeColumnsToContents()

    def on_tab_changed(self, index):
        """Обработчик смены вкладки"""
        try:
            if index == 0:  # Заказы
                self.load_orders_to_table()
            elif index == 1:  # Товары
                self.load_products_to_table()
            elif index == 2:  # Отзывы
                self.load_reviews_to_table()
            elif index == 3:  # Клиенты
                self.load_users_to_table()
            elif index == 4:  # Сотрудники
                self.load_employees_to_table()
            elif index == 5:  # Заявки
                self.load_applications_to_table()

            # Принудительное обновление интерфейса
            self.repaint()
            QApplication.processEvents()

        except Exception as e:
            print(f"Ошибка при смене вкладки: {e}")

    def save_changes(self):
        """Сохранение изменений в таблице"""
        current_tab = self.tabWidget.currentIndex()

        if current_tab == 1:  # Товары
            self.save_products_changes()
        # Можно добавить сохранение для других вкладок

    def save_products_changes(self):
        """Сохранение изменений в таблице товаров"""
        QMessageBox.information(self, "Информация", "Изменения сохранены")

    def close_event(self, event):
        """Закрытие подключения к БД при закрытии окна"""
        if hasattr(self, 'db_connection'):
            self.db_connection.close()
        event.accept()

class AddProductDialog(QDialog, Ui_AddProductDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Подключаем кнопки
        self.pushButton_save.clicked.connect(self.save_product)
        self.pushButton_cancel.clicked.connect(self.reject)

        # Загружаем категории из БД
        self.load_categories_from_db()

    def load_categories_from_db(self):
        """Загружаем категории из базы данных"""
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT id, name FROM category")
            categories = c.fetchall()
            self.comboBox_category.clear()
            self.comboBox_category.addItem("")  # Пустой элемент
            for category in categories:
                self.comboBox_category.addItem(category[1], category[0])  # name как текст, id как данные
        except Exception as e:
            print(f"Ошибка загрузки категорий: {e}")
        finally:
            conn.close()

    def save_product(self):
        # Получаем данные из полей
        name = self.lineEdit_name.text().strip()
        description = self.textEdit_description.toPlainText().strip()
        price = self.lineEdit_price.text().strip()
        category_id = self.comboBox_category.currentData()
        brand = self.lineEdit_brand.text().strip()

        # Валидация
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название товара")
            return
        if not price or not self.is_valid_price(price):
            QMessageBox.warning(self, "Ошибка", "Введите корректную цену")
            return
        if not category_id:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию")
            return

        # Сохраняем товар в БД
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO product 
                        (name, description, price, category_id, brand) 
                        VALUES (?, ?, ?, ?, ?)''',
                      (name, description, float(price), category_id, brand))

            conn.commit()
            QMessageBox.information(self, "Успех", "Товар успешно добавлен")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить товар: {str(e)}")
            print(f"Ошибка добавления товара: {e}")
        finally:
            conn.close()

    def is_valid_price(self, price):
        """Проверяет валидность цены"""
        try:
            float(price)
            return True
        except ValueError:
            return False


class AddOrderDialog(QDialog, Ui_AddOrderDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pushButton_save.clicked.connect(self.save_order)
        self.pushButton_cancel.clicked.connect(self.reject)

        self.load_users_from_db()
        self.setup_status_combo()
        self.dateEdit.setDate(QtCore.QDate.currentDate())

    def load_users_from_db(self):
        """Загружаем пользователей из базы данных"""
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT id, first_name, last_name FROM user")
            users = c.fetchall()
            self.comboBox_user.clear()
            self.comboBox_user.addItem("")
            for user in users:
                self.comboBox_user.addItem(f"{user[1]} {user[2]}", user[0])
        except Exception as e:
            print(f"Ошибка загрузки пользователей: {e}")
        finally:
            conn.close()

    def setup_status_combo(self):
        """Заполняем статусы заказов"""
        self.comboBox_status.clear()
        self.comboBox_status.addItems(["Оформлен", "Доставляется", "Выполнен", "Отменен"])

    def save_order(self):
        user_id = self.comboBox_user.currentData()
        date = self.dateEdit.date().toString("yyyy-MM-dd")
        status = self.comboBox_status.currentText()
        sum_value = self.lineEdit_sum.text().strip()

        if not user_id:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return
        if not sum_value or not self.is_valid_price(sum_value):
            QMessageBox.warning(self, "Ошибка", "Введите корректную сумму")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO user_order (user_id, date, status, sum) 
                        VALUES (?, ?, ?, ?)''',
                      (user_id, date, status, float(sum_value)))
            conn.commit()
            QMessageBox.information(self, "Успех", "Заказ успешно добавлен")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить заказ: {str(e)}")
        finally:
            conn.close()

    def is_valid_price(self, price):
        try:
            float(price)
            return True
        except ValueError:
            return False


class AddReviewDialog(QDialog, Ui_AddReviewDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pushButton_save.clicked.connect(self.save_review)
        self.pushButton_cancel.clicked.connect(self.reject)

        self.load_users_from_db()
        self.load_products_from_db()
        self.setup_rating_combo()

    def load_users_from_db(self):
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT id, first_name, last_name FROM user")
            users = c.fetchall()
            self.comboBox_user.clear()
            self.comboBox_user.addItem("")
            for user in users:
                self.comboBox_user.addItem(f"{user[1]} {user[2]}", user[0])
        except Exception as e:
            print(f"Ошибка загрузки пользователей: {e}")
        finally:
            conn.close()

    def load_products_from_db(self):
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT id, name FROM product")
            products = c.fetchall()
            self.comboBox_product.clear()
            self.comboBox_product.addItem("")
            for product in products:
                self.comboBox_product.addItem(product[1], product[0])
        except Exception as e:
            print(f"Ошибка загрузки товаров: {e}")
        finally:
            conn.close()

    def setup_rating_combo(self):
        self.comboBox_rating.clear()
        for i in range(1, 6):
            self.comboBox_rating.addItem(str(i), i)

    def save_review(self):
        user_id = self.comboBox_user.currentData()
        product_id = self.comboBox_product.currentData()
        rating = self.comboBox_rating.currentData()
        review_text = self.textEdit_review.toPlainText().strip()

        if not user_id:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return
        if not product_id:
            QMessageBox.warning(self, "Ошибка", "Выберите товар")
            return
        if not rating:
            QMessageBox.warning(self, "Ошибка", "Выберите рейтинг")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            from datetime import datetime
            current_date = datetime.now().strftime("%Y-%m-%d")

            c.execute('''INSERT INTO review (user_id, product_id, rating, review_text, date) 
                        VALUES (?, ?, ?, ?, ?)''',
                      (user_id, product_id, rating, review_text, current_date))
            conn.commit()
            QMessageBox.information(self, "Успех", "Отзыв успешно добавлен")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить отзыв: {str(e)}")
        finally:
            conn.close()


class AddApplicationDialog(QDialog, Ui_AddApplicationDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pushButton_save.clicked.connect(self.save_application)
        self.pushButton_cancel.clicked.connect(self.reject)

        self.load_users_from_db()
        self.load_employees_from_db()
        self.setup_status_combo()

    def load_users_from_db(self):
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT id, first_name, last_name FROM user")
            users = c.fetchall()
            self.comboBox_user.clear()
            self.comboBox_user.addItem("")
            for user in users:
                self.comboBox_user.addItem(f"{user[1]} {user[2]}", user[0])
        except Exception as e:
            print(f"Ошибка загрузки пользователей: {e}")
        finally:
            conn.close()

    def load_employees_from_db(self):
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT id, first_name, last_name FROM employee")
            employees = c.fetchall()
            self.comboBox_employee.clear()
            self.comboBox_employee.addItem("")
            for employee in employees:
                self.comboBox_employee.addItem(f"{employee[1]} {employee[2]}", employee[0])
        except Exception as e:
            print(f"Ошибка загрузки сотрудников: {e}")
        finally:
            conn.close()

    def setup_status_combo(self):
        self.comboBox_status.clear()
        self.comboBox_status.addItems(["Новая", "В обработке", "Выполнена", "Отклонена"])

    def save_application(self):
        user_id = self.comboBox_user.currentData()
        employee_id = self.comboBox_employee.currentData()
        status = self.comboBox_status.currentText()
        description = self.textEdit_description.toPlainText().strip()

        if not user_id:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return
        if not employee_id:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            from datetime import datetime
            current_date = datetime.now().strftime("%Y-%m-%d")

            c.execute('''INSERT INTO application (user_id, employee_id, status, date, description) 
                        VALUES (?, ?, ?, ?, ?)''',
                      (user_id, employee_id, status, current_date, description))
            conn.commit()
            QMessageBox.information(self, "Успех", "Заявка успешно добавлена")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить заявку: {str(e)}")
        finally:
            conn.close()


class AddUserDialog(QDialog, Ui_AddUserDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pushButton_save.clicked.connect(self.save_user)
        self.pushButton_cancel.clicked.connect(self.reject)

    def save_user(self):
        first_name = self.lineEdit_first_name.text().strip()
        last_name = self.lineEdit_last_name.text().strip()
        third_name = self.lineEdit_third_name.text().strip()
        login = self.lineEdit_login.text().strip()
        password = self.lineEdit_password.text().strip()
        phone = self.lineEdit_phone.text().strip()
        email = self.lineEdit_email.text().strip()
        address = self.lineEdit_address.text().strip()

        if not all([first_name, last_name, login, password, phone, email, address]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO user (first_name, last_name, third_name, login, password, phone, email, address) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (first_name, last_name, third_name, login, password, phone, email, address))
            conn.commit()
            QMessageBox.information(self, "Успех", "Пользователь успешно добавлен")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить пользователя: {str(e)}")
        finally:
            conn.close()


class AddEmployeeDialog(QDialog, Ui_AddEmployeeDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pushButton_save.clicked.connect(self.save_employee)
        self.pushButton_cancel.clicked.connect(self.reject)

    def save_employee(self):
        first_name = self.lineEdit_first_name.text().strip()
        last_name = self.lineEdit_last_name.text().strip()
        third_name = self.lineEdit_third_name.text().strip()
        login = self.lineEdit_login.text().strip()
        password = self.lineEdit_password.text().strip()
        phone = self.lineEdit_phone.text().strip()
        email = self.lineEdit_email.text().strip()
        address = self.lineEdit_address.text().strip()

        if not all([first_name, last_name, login, password, phone, email, address]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO employee (first_name, last_name, third_name, login, password, phone, email, address) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (first_name, last_name, third_name, login, password, phone, email, address))
            conn.commit()
            QMessageBox.information(self, "Успех", "Сотрудник успешно добавлен")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить сотрудника: {str(e)}")
        finally:
            conn.close()


class EditProductDialog(QDialog, Ui_EditProductDialog):
    def __init__(self, parent=None, product_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.product_id = product_id

        self.pushButton_save.clicked.connect(self.save_changes)
        self.pushButton_cancel.clicked.connect(self.reject)

        self.load_product_data()

    def load_product_data(self):
        """Загружаем данные товара"""
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT name, description, price, brand FROM product WHERE id = ?", (self.product_id,))
            product_data = c.fetchone()

            if product_data:
                self.lineEdit_name.setText(product_data[0] or "")
                self.textEdit_description.setPlainText(product_data[1] or "")
                self.lineEdit_price.setText(str(product_data[2]) if product_data[2] else "")
                self.lineEdit_brand.setText(product_data[3] or "")

        except Exception as e:
            print(f"Ошибка загрузки данных товара: {e}")
        finally:
            conn.close()

    def save_changes(self):
        """Сохраняем изменения"""
        name = self.lineEdit_name.text().strip()
        description = self.textEdit_description.toPlainText().strip()
        price = self.lineEdit_price.text().strip()
        brand = self.lineEdit_brand.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название товара")
            return

        try:
            float(price)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректную цену")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''UPDATE product SET name=?, description=?, price=?, brand=?
                        WHERE id=?''',
                      (name, description, float(price), brand, self.product_id))
            conn.commit()
            QMessageBox.information(self, "Успех", "Товар успешно обновлен")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить товар: {str(e)}")
        finally:
            conn.close()


class EditUserDialog(QDialog, Ui_EditUserDialog):
    def __init__(self, parent=None, user_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.user_id = user_id

        self.pushButton_save.clicked.connect(self.save_changes)
        self.pushButton_cancel.clicked.connect(self.reject)

        self.load_user_data()

    def load_user_data(self):
        """Загружаем данные пользователя"""
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "SELECT first_name, last_name, third_name, login, password, phone, email, address FROM user WHERE id = ?",
                (self.user_id,))
            user_data = c.fetchone()

            if user_data:
                self.lineEdit_first_name.setText(user_data[0] or "")
                self.lineEdit_last_name.setText(user_data[1] or "")
                self.lineEdit_third_name.setText(user_data[2] or "")
                self.lineEdit_login.setText(user_data[3] or "")
                self.lineEdit_password.setText(user_data[4] or "")
                self.lineEdit_phone.setText(user_data[5] or "")
                self.lineEdit_email.setText(user_data[6] or "")
                self.lineEdit_address.setText(user_data[7] or "")

        except Exception as e:
            print(f"Ошибка загрузки данных пользователя: {e}")
        finally:
            conn.close()

    def save_changes(self):
        """Сохраняем изменения"""
        first_name = self.lineEdit_first_name.text().strip()
        last_name = self.lineEdit_last_name.text().strip()
        third_name = self.lineEdit_third_name.text().strip()
        login = self.lineEdit_login.text().strip()
        password = self.lineEdit_password.text().strip()
        phone = self.lineEdit_phone.text().strip()
        email = self.lineEdit_email.text().strip()
        address = self.lineEdit_address.text().strip()

        if not all([first_name, last_name, login, password, phone, email, address]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''UPDATE user SET first_name=?, last_name=?, third_name=?, 
                        login=?, password=?, phone=?, email=?, address=?
                        WHERE id=?''',
                      (first_name, last_name, third_name, login, password, phone, email, address, self.user_id))
            conn.commit()
            QMessageBox.information(self, "Успех", "Пользователь успешно обновлен")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить пользователя: {str(e)}")
        finally:
            conn.close()


class EditEmployeeDialog(QDialog, Ui_EditEmployeeDialog):
    def __init__(self, parent=None, employee_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.employee_id = employee_id

        self.pushButton_save.clicked.connect(self.save_changes)
        self.pushButton_cancel.clicked.connect(self.reject)

        self.load_employee_data()

    def load_employee_data(self):
        """Загружаем данные сотрудника"""
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "SELECT first_name, last_name, third_name, login, password, phone, email, address FROM employee WHERE id = ?",
                (self.employee_id,))
            employee_data = c.fetchone()

            if employee_data:
                self.lineEdit_first_name.setText(employee_data[0] or "")
                self.lineEdit_last_name.setText(employee_data[1] or "")
                self.lineEdit_third_name.setText(employee_data[2] or "")
                self.lineEdit_login.setText(employee_data[3] or "")
                self.lineEdit_password.setText(employee_data[4] or "")
                self.lineEdit_phone.setText(employee_data[5] or "")
                self.lineEdit_email.setText(employee_data[6] or "")
                self.lineEdit_address.setText(employee_data[7] or "")

        except Exception as e:
            print(f"Ошибка загрузки данных сотрудника: {e}")
        finally:
            conn.close()

    def save_changes(self):
        """Сохраняем изменения"""
        first_name = self.lineEdit_first_name.text().strip()
        last_name = self.lineEdit_last_name.text().strip()
        third_name = self.lineEdit_third_name.text().strip()
        login = self.lineEdit_login.text().strip()
        password = self.lineEdit_password.text().strip()
        phone = self.lineEdit_phone.text().strip()
        email = self.lineEdit_email.text().strip()
        address = self.lineEdit_address.text().strip()

        if not all([first_name, last_name, login, password, phone, email, address]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''UPDATE employee SET first_name=?, last_name=?, third_name=?, 
                        login=?, password=?, phone=?, email=?, address=?
                        WHERE id=?''',
                      (first_name, last_name, third_name, login, password, phone, email, address, self.employee_id))
            conn.commit()
            QMessageBox.information(self, "Успех", "Сотрудник успешно обновлен")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить сотрудника: {str(e)}")
        finally:
            conn.close()


class EditOrderDialog(QDialog, Ui_EditOrderDialog):
    def __init__(self, parent=None, order_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.order_id = order_id

        self.pushButton_save.clicked.connect(self.save_changes)
        self.pushButton_cancel.clicked.connect(self.reject)

        self.setup_status_combo()
        self.load_order_data()

    def setup_status_combo(self):
        """Заполняем статусы заказов"""
        self.comboBox_status.clear()
        self.comboBox_status.addItems(["Оформлен", "Доставляется", "Выполнен", "Отменен"])

    def load_order_data(self):
        """Загружаем данные заказа"""
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT user_id, date, status, sum FROM user_order WHERE id = ?", (self.order_id,))
            order_data = c.fetchone()

            if order_data:
                self.lineEdit_user_id.setText(str(order_data[0]) if order_data[0] else "")
                self.lineEdit_date.setText(order_data[1] or "")

                # Устанавливаем статус
                index = self.comboBox_status.findText(order_data[2] or "")
                if index >= 0:
                    self.comboBox_status.setCurrentIndex(index)

                self.lineEdit_sum.setText(str(order_data[3]) if order_data[3] else "")

        except Exception as e:
            print(f"Ошибка загрузки данных заказа: {e}")
        finally:
            conn.close()

    def save_changes(self):
        """Сохраняем изменения"""
        user_id = self.lineEdit_user_id.text().strip()
        date = self.lineEdit_date.text().strip()
        status = self.comboBox_status.currentText()
        sum_value = self.lineEdit_sum.text().strip()

        if not all([user_id, date, sum_value]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля")
            return

        try:
            int(user_id)
            float(sum_value)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "ID пользователя должно быть числом, сумма - числом")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''UPDATE user_order SET user_id=?, date=?, status=?, sum=?
                        WHERE id=?''',
                      (int(user_id), date, status, float(sum_value), self.order_id))
            conn.commit()
            QMessageBox.information(self, "Успех", "Заказ успешно обновлен")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить заказ: {str(e)}")
        finally:
            conn.close()


class EditReviewDialog(QDialog, Ui_EditReviewDialog):
    def __init__(self, parent=None, review_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.review_id = review_id

        self.pushButton_save.clicked.connect(self.save_changes)
        self.pushButton_cancel.clicked.connect(self.reject)

        self.setup_rating_combo()
        self.load_review_data()

    def setup_rating_combo(self):
        """Заполняем рейтинги"""
        self.comboBox_rating.clear()
        for i in range(1, 6):
            self.comboBox_rating.addItem(str(i), i)

    def load_review_data(self):
        """Загружаем данные отзыва"""
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT user_id, product_id, rating, review_text FROM review WHERE id = ?", (self.review_id,))
            review_data = c.fetchone()

            if review_data:
                self.lineEdit_user_id.setText(str(review_data[0]) if review_data[0] else "")
                self.lineEdit_product_id.setText(str(review_data[1]) if review_data[1] else "")

                # Устанавливаем рейтинг
                index = self.comboBox_rating.findData(review_data[2])
                if index >= 0:
                    self.comboBox_rating.setCurrentIndex(index)

                self.textEdit_review_text.setPlainText(review_data[3] or "")

        except Exception as e:
            print(f"Ошибка загрузки данных отзыва: {e}")
        finally:
            conn.close()

    def save_changes(self):
        """Сохраняем изменения"""
        user_id = self.lineEdit_user_id.text().strip()
        product_id = self.lineEdit_product_id.text().strip()
        rating = self.comboBox_rating.currentData()
        review_text = self.textEdit_review_text.toPlainText().strip()

        if not all([user_id, product_id, rating]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля")
            return

        try:
            int(user_id)
            int(product_id)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "ID пользователя и ID товара должны быть числами")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''UPDATE review SET user_id=?, product_id=?, rating=?, review_text=?
                        WHERE id=?''',
                      (int(user_id), int(product_id), rating, review_text, self.review_id))
            conn.commit()
            QMessageBox.information(self, "Успех", "Отзыв успешно обновлен")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить отзыв: {str(e)}")
        finally:
            conn.close()


class EditApplicationDialog(QDialog, Ui_EditApplicationDialog):
    def __init__(self, parent=None, application_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.application_id = application_id

        self.pushButton_save.clicked.connect(self.save_changes)
        self.pushButton_cancel.clicked.connect(self.reject)

        self.setup_status_combo()
        self.load_application_data()

    def setup_status_combo(self):
        """Заполняем статусы заявок"""
        self.comboBox_status.clear()
        self.comboBox_status.addItems(["Новая", "В обработке", "Выполнена", "Отклонена"])

    def load_application_data(self):
        """Загружаем данные заявки"""
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT user_id, employee_id, status, date, description FROM application WHERE id = ?",
                      (self.application_id,))
            app_data = c.fetchone()

            if app_data:
                self.lineEdit_user_id.setText(str(app_data[0]) if app_data[0] else "")
                self.lineEdit_employee_id.setText(str(app_data[1]) if app_data[1] else "")

                # Устанавливаем статус
                index = self.comboBox_status.findText(app_data[2] or "")
                if index >= 0:
                    self.comboBox_status.setCurrentIndex(index)

                self.lineEdit_date.setText(app_data[3] or "")
                self.textEdit_description.setPlainText(app_data[4] or "")

        except Exception as e:
            print(f"Ошибка загрузки данных заявки: {e}")
        finally:
            conn.close()

    def save_changes(self):
        """Сохраняем изменения"""
        user_id = self.lineEdit_user_id.text().strip()
        employee_id = self.lineEdit_employee_id.text().strip()
        status = self.comboBox_status.currentText()
        date = self.lineEdit_date.text().strip()
        description = self.textEdit_description.toPlainText().strip()

        if not all([user_id, employee_id, date]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля")
            return

        try:
            int(user_id)
            int(employee_id)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "ID пользователя и ID сотрудника должны быть числами")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''UPDATE application SET user_id=?, employee_id=?, status=?, date=?, description=?
                        WHERE id=?''',
                      (int(user_id), int(employee_id), status, date, description, self.application_id))
            conn.commit()
            QMessageBox.information(self, "Успех", "Заявка успешно обновлена")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить заявку: {str(e)}")
        finally:
            conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())