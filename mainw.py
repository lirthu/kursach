import sys
import sqlite3

from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem, QMenu


from authorize import Ui_Auth_Form
from registration import Ui_Reg_Form
from catalog import Ui_Catalog_Form
from admin_panel import Ui_Admin_Form
from profile import Ui_Profile_Form
from shopping_cart import Ui_Cart_Form
from c_application import Ui_Create_Application_Form
from order import Ui_Order_Form
from history_order import Ui_History_Order_Form
from order_content import Ui_Content_Form
from application_view import Ui_Application_Form



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
        self.pushButton_2.clicked.connect(self.open_main_window_return)

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

    def open_main_window_return(self):
        self.close()
        if self.user_type == 'user':
            self.win = CatalogWin(self.user_id)
        else:
            self.win = AdminPanel(self.user_id)
        self.win.show()


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
        open_history_menu = profile_menu.addAction("История покупок")
        application = profile_menu.addAction("Заявки")
        profile_menu.addSeparator()
        back_to_log = profile_menu.addAction("Выйти")

        open_profile_menu.triggered.connect(lambda: self.open_profile_menu(parent_window))
        open_order_menu.triggered.connect(lambda: self.open_order_menu(parent_window))
        back_to_log.triggered.connect(lambda: self.open_main_window_return(parent_window))
        application.triggered.connect(lambda: self.open_application_menu(parent_window))
        return profile_menu

    def open_profile_menu(self, parent_window):
        parent_window.close()
        parent_window.win = ProfileWin(self.user_id, self.user_type)
        parent_window.win.show()

    def open_order_menu(self, parent_window):
        parent_window.close()
        parent_window.win = OrderWin(self.user_id)
        parent_window.win.show()

    def open_history_menu(self, parent_window):
        parent_window.close()
        parent_window.win = HistoryOrder(self.user_id)
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

class HistoryOrder(QDialog, Ui_History_Order_Form):
    def __init__(self, user_id = None):
        super().__init__()
        self.setupUi(self)

        menu_manager = ProfileMenuManager(user_id, 'user')
        self.pushButton_8.setMenu(menu_manager.create_profile_menu(self))

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

        self.create_profile_menu()

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
        self.close()
        self.win = ProfileWin(self.current_user_id, user_type="employee")
        self.win.show()

    def open_main_window_return(self):
        self.close()
        self.win = MainWindow()
        self.win.show()

    def load_reviews_to_table(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM review''')
        data = c.fetchall()
        conn.close()

        table_widget = self.tableWidget_3
        self.populate_table(table_widget, data)

    def load_products_to_table(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM product''')
        data = c.fetchall()
        conn.close()

        table_widget = self.tableWidget_2
        self.populate_table(table_widget, data)

    def load_orders_to_table(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM user_order''')
        data = c.fetchall()
        conn.close()

        table_widget_5 = self.tableWidget
        self.populate_table(table_widget_5, data)

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
        c.execute('''SELECT * FROM application''')
        data = c.fetchall()
        conn.close()

        table_widget = self.tableWidget_6  # Правильный виджет для заявок
        self.populate_table(table_widget, data)

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

    def on_tab_changed(self, index):
        """Обработчик смены вкладки"""
        # if index == 0:  # Вкладка "Заказы"
        #     self.load_orders_to_table()
        # elif index == 1:  # Вкладка "Товары"
        #     self.load_products_to_table()
        # elif index == 2:  # Вкладка "Отзывы"
        #     self.load_reviews_to_table()
        if index == 3:  # Вкладка "Клиенты"
            self.load_users_to_table()
        elif index == 4:  # Вкладка "Сотрудники"
            self.load_employees_to_table()
        # elif index == 5:  # Вкладка "Заявки"
        #     self.load_applications_to_table()

    def close_event(self, event):
        """Закрытие подключения к БД при закрытии окна"""
        if hasattr(self, 'db_connection'):
            self.db_connection.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())