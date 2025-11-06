import sys
import sqlite3

from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem, QMenu
from PyQt5 import QtWidgets, QtGui

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

class UserDataWin(QDialog, Ui_Profile_Form):
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
        parent_window.win = UserDataWin(self.user_id, self.user_type)
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
    def __init__(self, user_id=None):
        super().__init__()
        self.setupUi(self)
        self.user_id = user_id
        menu_manager = ProfileMenuManager(user_id, 'user')
        self.pushButton.setMenu(menu_manager.create_profile_menu(self))

        self.load_orders()

        self.pushButton_6.clicked.connect(self.open_main_window_return)

    def load_orders(self):
        """Загрузка заказов пользователя из БД"""
        conn = get_connection()
        c = conn.cursor()

        # Получаем заказы пользователя
        c.execute('''SELECT id, date, status, sum 
                     FROM user_order 
                     WHERE user_id = ? 
                     ORDER BY date DESC''', (self.user_id,))
        orders = c.fetchall()
        conn.close()

        self.tableWidget.setRowCount(len(orders))
        self.tableWidget.setColumnCount(5)

        # Устанавливаем заголовки
        headers = ['Номер', 'Дата', 'Содержимое', 'Статус', 'Стоимость']
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for row, order in enumerate(orders):
            order_id, date, status, total = order

            # Номер заказа
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(order_id)))
            # Дата
            self.tableWidget.setItem(row, 1, QTableWidgetItem(date))

            # Кнопка для просмотра содержимого
            details_btn = QtWidgets.QPushButton("Просмотреть")
            details_btn.clicked.connect(lambda checked, ord_id=order_id: self.show_order_details(ord_id))
            self.tableWidget.setCellWidget(row, 2, details_btn)

            # Статус
            status_item = QTableWidgetItem(status)
            self.tableWidget.setItem(row, 3, status_item)

            # Устанавливаем цвет в зависимости от статуса
            if status == 'Выполнен':
                status_item.setBackground(QtGui.QColor(144, 238, 144))  # Светло-зеленый
            elif status == 'Отменен':
                status_item.setBackground(QtGui.QColor(255, 182, 193))  # Светло-красный
            elif status == 'Доставляется':
                status_item.setBackground(QtGui.QColor(173, 216, 230))  # Светло-голубой

            # Стоимость
            self.tableWidget.setItem(row, 4, QTableWidgetItem(f"{total:.2f} руб."))

        # Настраиваем внешний вид таблицы
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

    def show_order_details(self, order_id):
        """Показать содержимое заказа"""
        self.order_content_win = OrderContent(self.user_id, order_id)
        self.order_content_win.show()

    def open_main_window_return(self):
        self.close()
        self.win = CatalogWin(self.user_id)
        self.win.show()


class OrderContent(QDialog, Ui_Content_Form):
    def __init__(self, user_id=None, order_id=None):
        super().__init__()
        self.setupUi(self)
        self.user_id = user_id
        self.order_id = order_id

        self.load_order_content()

        # Настраиваем окно
        self.setWindowTitle(f"Содержимое заказа №{order_id}")
        self.resize(800, 400)

    def load_order_content(self):
        """Загрузка содержимого заказа"""
        conn = get_connection()
        c = conn.cursor()

        try:
            # Получаем позиции заказа с информацией о товарах
            c.execute('''
                SELECT p.name, p.brand, op.quantity, op.price_at_time, 
                       (op.quantity * op.price_at_time) as total
                FROM order_position op
                JOIN product p ON op.product_id = p.id
                WHERE op.order_id = ?
            ''', (self.order_id,))

            order_items = c.fetchall()

            if not order_items:
                QMessageBox.information(self, "Информация", "Заказ пуст или не найден")
                return

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные заказа: {str(e)}")
            print(f"Ошибка при загрузке заказа: {e}")  # Для отладки
            return
        finally:
            conn.close()

        # Настраиваем таблицу
        self.tableWidget.setRowCount(len(order_items))
        self.tableWidget.setColumnCount(5)

        headers = ['Товар', 'Бренд', 'Количество', 'Цена за шт.', 'Общая стоимость']
        self.tableWidget.setHorizontalHeaderLabels(headers)

        total_order_sum = 0

        for row, item in enumerate(order_items):
            name, brand, quantity, price, total = item

            # Название товара
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(name)))
            # Бренд
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(brand) if brand else "-"))
            # Количество
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(quantity)))
            # Цена за штуку
            self.tableWidget.setItem(row, 3, QTableWidgetItem(f"{float(price):.2f} руб."))
            # Общая стоимость позиции
            self.tableWidget.setItem(row, 4, QTableWidgetItem(f"{float(total):.2f} руб."))

            total_order_sum += float(total)

        # Добавляем итоговую строку
        if order_items:
            self.tableWidget.setRowCount(len(order_items) + 1)
            total_row = len(order_items)

            # Объединяем ячейки для итоговой строки
            self.tableWidget.setItem(total_row, 0, QTableWidgetItem("ИТОГО:"))
            self.tableWidget.setSpan(total_row, 0, 1, 4)  # Объединяем первые 4 колонки
            self.tableWidget.setItem(total_row, 4, QTableWidgetItem(f"{total_order_sum:.2f} руб."))

            # Выделяем итоговую строку жирным
            font = QtGui.QFont()
            font.setBold(True)
            for col in range(5):
                item = self.tableWidget.item(total_row, col)
                if item:
                    item.setFont(font)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

    # Удалите метод open_cart если кнопки pushButton_2 нет в UI
    # def open_cart(self):
    #     self.close()
    #     self.win = ShoppingCart(self.user_id)
    #     self.win.show()

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

        self.pushButton_7.clicked.connect(self.create_order)

    def create_order(self):
        """Создание заказа из корзины"""
        if not hasattr(self, 'cart_items') or not self.cart_items:
            QMessageBox.warning(self, "Ошибка", "Корзина пуста!")
            return

        connect = get_connection()
        c = connect.cursor()

        try:
            # Рассчитываем общую сумму заказа
            total_sum = sum(item['price'] * item['quantity'] for item in self.cart_items)

            # Создаем заказ
            from datetime import date
            today = date.today().isoformat()

            c.execute('''INSERT INTO user_order (user_id, date, status, sum) 
                         VALUES (?, ?, ?, ?)''',
                      (self.user_id, today, 'Оформлен', total_sum))

            order_id = c.lastrowid

            # Добавляем позиции заказа
            for item in self.cart_items:
                c.execute('''INSERT INTO order_position (order_id, product_id, quantity, price_at_time) 
                             VALUES (?, ?, ?, ?)''',
                          (order_id, item['product_id'], item['quantity'], item['price']))

            # Очищаем корзину
            self.cart_items = []
            self.update_cart_display()

            connect.commit()
            QMessageBox.information(self, "Успех", f"Заказ №{order_id} успешно оформлен!")

            # Переходим к просмотру заказов
            self.open_order_window()

        except Exception as e:
            connect.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось оформить заказ: {str(e)}")
        finally:
            connect.close()

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
        self.win = UserDataWin(self.current_user_id, user_type="employee")
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

        table_widget = self.tableWidget
        self.populate_table(table_widget, data)

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
        if index == 0:  # Вкладка "Заказы"
            self.load_orders_to_table()
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