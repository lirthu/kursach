import os
import sys
import sqlite3

from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem, QMenu
from PyQt5 import QtCore, QtGui, QtWidgets

from authorize import Ui_Auth_Form
from registration import Ui_Reg_Form
from admin_panel import Ui_Admin_Form
from profile import Ui_Profile_Form
from catalog import Ui_Catalog_Form
from shopping_cart import Ui_Cart_Form
from order import Ui_Order_Form
from add_product_dialog import Ui_AddProductDialog
from add_order_with_products import Ui_AddOrderWithProductsDialog
from add_user_dialog import Ui_AddUserDialog
from add_employee_dialog import Ui_AddEmployeeDialog
from add_category_dialog import Ui_AddCategoryDialog
from edit_order_with_products import Ui_EditOrderWithProductsDialog
from edit_product_dialog import Ui_EditProductDialog
from edit_user_dialog import Ui_EditUserDialog
from edit_category_dialog import Ui_EditCategoryDialog
from edit_employee_dialog import Ui_EditEmployeeDialog

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
        self.checkBox.stateChanged.connect(self.toggle_password_visibility)

    def toggle_password_visibility(self, state):
        """Переключение видимости пароля"""
        if state == QtCore.Qt.Checked:
            # Показываем пароль
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            # Скрываем пароль (точки)
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

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
        self.checkBox.stateChanged.connect(self.toggle_password_visibility)

    def toggle_password_visibility(self, state):
        """Переключение видимости пароля"""
        if state == QtCore.Qt.Checked:
            # Показываем пароль
            self.lineEdit_11.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.lineEdit_12.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            # Скрываем пароль (точки)
            self.lineEdit_11.setEchoMode(QtWidgets.QLineEdit.Password)
            self.lineEdit_12.setEchoMode(QtWidgets.QLineEdit.Password)

    def registration(self):
        connect = get_connection()
        c = connect.cursor()
        try:
            name = self.lineEdit_1.text().strip()
            last_name = self.lineEdit.text().strip()
            third_name = self.lineEdit_2.text().strip()
            login = self.lineEdit_10.text().strip()
            password = self.lineEdit_11.text().strip()
            return_password = self.lineEdit_12.text().strip()
            phone = self.lineEdit_3.text().strip()
            email = self.lineEdit_9.text().strip()
            address = self.lineEdit_4.text().strip()

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
    def __init__(self, user_id=None):
        super().__init__()
        self.setupUi(self)
        self.user_id = user_id

        self.setWindowState(QtCore.Qt.WindowMaximized)  # Развернуть на весь экран
        self.showMaximized()

        # Получаем ссылку на widget для отображения товаров
        self.products_widget = self.widget
        self.products_layout = QtWidgets.QVBoxLayout(self.products_widget)
        self.products_widget.setLayout(self.products_layout)

        menu_manager = MenuManager(user_id, 'user')
        self.pushButton.setMenu(menu_manager.create_profile_menu(self))
        self.pushButton_2.clicked.connect(self.open_cart_window)

        self.load_products()

    def open_cart_window(self):
        self.close()
        self.win = ShoppingCart(self.user_id)
        self.win.show()

    def load_products(self):
        """Загрузка товаров из базы данных"""
        try:
            # Очищаем виджет перед загрузкой новых товаров
            conn = get_connection()
            c = conn.cursor()
            c.execute('''SELECT id, name, brand, description, price, image_path 
                         FROM product''')
            products = c.fetchall()
            conn.close()

            self.display_products(products)

        except Exception as e:
            print(f"Ошибка загрузки товаров: {e}")

    def display_products(self, products):
        """Отображение товаров в виде карточек"""
        # Очищаем предыдущие карточки
        if not products:
            # Если товаров нет, показываем сообщение
            no_products_label = QtWidgets.QLabel("Товары не найдены")
            no_products_label.setAlignment(QtCore.Qt.AlignCenter)
            no_products_label.setStyleSheet("font-size: 16px; color: gray; font-family: 'Segoe Print';")
            self.products_layout.addWidget(no_products_label)
            return

        # Создаем сетку для карточек (3 колонки)
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(25)  # Увеличил расстояние между карточками

        row = 0
        col = 0

        for product in products:
            product_id, name, brand, description, price, image_path = product

            # Создаем карточку товара
            card = self.create_product_card(product_id, name, brand, price, image_path, description)

            # Добавляем в сетку
            grid_layout.addWidget(card, row, col)

            # Переходим к следующей ячейке
            col += 1
            if col >= 7:  # 3 колонки
                col = 0
                row += 1

        # Добавляем сетку в основной layout
        self.products_layout.addLayout(grid_layout)

        # Добавляем растягивающийся элемент чтобы карточки были вверху
        self.products_layout.addStretch(1)

    def create_product_card(self, product_id, name, brand, price, image_path, description):
        """Создание карточки товара"""
        # Основная карточка
        card = QtWidgets.QGroupBox()
        card.setMinimumSize(200, 320)  # Увеличил минимальную высоту
        card.setMaximumSize(220, 400)  # Увеличил максимальную высоту
        card.setStyleSheet("""
            QGroupBox {
                border: 2px solid #cccccc;
                border-radius: 10px;
                margin: 5px;
                padding: 10px;
                background-color: white;
            }
            QGroupBox:hover {
                border: 2px solid #0078d7;
            }
        """)

        layout = QtWidgets.QVBoxLayout(card)
        layout.setSpacing(6)  # Уменьшил расстояние между элементами
        layout.setContentsMargins(8, 8, 8, 8)  # Уменьшил отступы

        # Изображение товара - фиксированная высота
        image_label = QtWidgets.QLabel()
        image_label.setFixedSize(150, 150)  # Фиксированный размер вместо min/max
        image_label.setAlignment(QtCore.Qt.AlignCenter)
        image_label.setStyleSheet("""
            QLabel {
                border: 1px solid #dddddd;
                border-radius: 5px;
                background-color: #f8f8f8;
            }
        """)

        if image_path and os.path.exists(image_path):
            try:
                pixmap = QtGui.QPixmap(image_path)
                if not pixmap.isNull():
                    # Масштабируем изображение
                    scaled_pixmap = pixmap.scaled(140, 140, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                    image_label.setPixmap(scaled_pixmap)
                else:
                    image_label.setText("Нет\nизображения")
                    image_label.setStyleSheet("color: gray; font-size: 10px; font-family: 'Segoe Print';")
            except Exception as e:
                print(f"Ошибка загрузки изображения: {e}")
                image_label.setText("Ошибка\nзагрузки")
                image_label.setStyleSheet("color: red; font-size: 10px; font-family: 'Segoe Print';")
        else:
            image_label.setText("Нет\nизображения")
            image_label.setStyleSheet("color: gray; font-size: 10px; font-family: 'Segoe Print';")

        # Название товара - ограничиваем высоту
        name_label = QtWidgets.QLabel(name)
        name_label.setWordWrap(True)
        name_label.setMaximumHeight(40)  # Ограничиваем высоту названия
        name_label.setAlignment(QtCore.Qt.AlignCenter)
        name_label.setStyleSheet("""
            font-weight: bold; 
            font-size: 12px; 
            font-family: 'Segoe Print';
            margin-top: 5px;
        """)

        # Бренд
        brand_label = QtWidgets.QLabel(brand if brand else "Бренд не указан")
        brand_label.setMaximumHeight(20)  # Ограничиваем высоту
        brand_label.setAlignment(QtCore.Qt.AlignCenter)
        brand_label.setStyleSheet("""
            color: #666666; 
            font-size: 11px; 
            font-family: 'Segoe Print';
        """)

        # Цена
        price_label = QtWidgets.QLabel(f"{float(price):.2f} руб.")
        price_label.setMaximumHeight(25)  # Ограничиваем высоту
        price_label.setAlignment(QtCore.Qt.AlignCenter)
        price_label.setStyleSheet("""
            font-weight: bold; 
            font-size: 14px; 
            color: #000000;
            padding: 3px;
            font-family: 'Segoe Print';
            margin: 2px 0;
        """)

        # Контейнер для кнопок
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setSpacing(5)

        # Кнопка "В корзину"
        cart_button = QtWidgets.QPushButton("В корзину")
        cart_button.setMinimumHeight(30)  # Фиксированная высота кнопки
        cart_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #000000;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-weight: bold;
                font-family: 'Segoe Print';
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border: 1px solid #999999;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        cart_button.clicked.connect(lambda checked, pid=product_id: self.add_to_cart(pid))

        # Кнопка "Подробнее"
        details_button = QtWidgets.QPushButton("Подробнее")
        details_button.setMinimumHeight(30)  # Фиксированная высота кнопки
        details_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #000000;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-weight: bold;
                font-family: 'Segoe Print';
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border: 1px solid #999999;
            }
        """)
        details_button.clicked.connect(lambda checked, pid=product_id: self.show_product_details(pid))

        # Добавляем кнопки в горизонтальный layout
        buttons_layout.addWidget(cart_button)
        buttons_layout.addWidget(details_button)

        # Добавляем все элементы в карточку
        layout.addWidget(image_label)
        layout.addWidget(name_label)
        layout.addWidget(brand_label)
        layout.addWidget(price_label)
        layout.addLayout(buttons_layout)

        return card

    def add_to_cart(self, product_id):
        """Добавление товара в корзину"""
        try:
            if not self.user_id:
                QMessageBox.warning(self, "Ошибка", "Необходимо авторизоваться для добавления в корзину")
                return

            conn = get_connection()
            c = conn.cursor()

            # Проверяем, есть ли у пользователя корзина
            c.execute("SELECT id FROM cart WHERE user_id = ?", (self.user_id,))
            cart = c.fetchone()

            if not cart:
                # Создаем корзину если ее нет
                from datetime import datetime
                current_date = datetime.now().strftime("%Y-%m-%d")
                c.execute("INSERT INTO cart (user_id, created_date) VALUES (?, ?)",
                          (self.user_id, current_date))
                cart_id = c.lastrowid
            else:
                cart_id = cart[0]

            # Проверяем, есть ли уже этот товар в корзине
            c.execute("SELECT id, quantity FROM cart_item WHERE cart_id = ? AND product_id = ?",
                      (cart_id, product_id))
            existing_item = c.fetchone()

            if existing_item:
                # Увеличиваем количество
                new_quantity = existing_item[1] + 1
                c.execute("UPDATE cart_item SET quantity = ? WHERE id = ?",
                          (new_quantity, existing_item[0]))
            else:
                # Добавляем новый товар
                c.execute("INSERT INTO cart_item (cart_id, product_id, quantity) VALUES (?, ?, ?)",
                          (cart_id, product_id, 1))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Товар добавлен в корзину!")

        except Exception as e:
            print(f"Ошибка добавления в корзину: {e}")
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить товар в корзину")

    def show_product_details(self, product_id):
        """Показ подробной информации о товаре"""
        try:
            conn = get_connection()
            c = conn.cursor()

            # Получаем основную информацию о товаре
            c.execute('''SELECT name, brand, description, price, image_path 
                         FROM product WHERE id = ?''', (product_id,))
            product = c.fetchone()

            if product:
                # Правильное обращение к данным через индексы
                name = product[0] if product[0] else ""
                brand = product[1] if product[1] else ""
                description = product[2] if product[2] else ""
                price = product[3] if product[3] else 0
                image_path = product[4] if product[4] else ""

                # Создаем диалог с подробной информацией
                detail_dialog = QtWidgets.QDialog(self)
                detail_dialog.setWindowTitle(f"Товар: {name}")
                detail_dialog.resize(450, 550)

                layout = QtWidgets.QVBoxLayout(detail_dialog)

                # Изображение
                image_label = QtWidgets.QLabel()
                image_label.setAlignment(QtCore.Qt.AlignCenter)
                if image_path and os.path.exists(image_path):
                    pixmap = QtGui.QPixmap(image_path)
                    scaled_pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                    image_label.setPixmap(scaled_pixmap)
                else:
                    image_label.setText("Изображение отсутствует")
                    image_label.setStyleSheet("color: gray; font-size: 12px; font-family: 'Segoe Print';")

                # Информация о товаре
                info_text = f"<h2 style='font-family: \"Segoe Print\"'>{name}</h2>"
                if brand:
                    info_text += f"<p><b>Бренд:</b> {brand}</p>"

                info_text += f"<p><b>Цена:</b> <span style='color: #0078d7; font-weight: bold;'>{float(price):.2f} руб.</span></p>"
                if description:
                    info_text += f"<p><b>Описание:</b><br>{description}</p>"

                info_label = QtWidgets.QLabel(info_text)
                info_label.setWordWrap(True)
                info_label.setStyleSheet("font-family: 'Segoe Print'; font-size: 12px; line-height: 1.4;")

                # Кнопка закрытия
                close_btn = QtWidgets.QPushButton("Закрыть")
                close_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f0f0f0;
                        color: #000000;
                        border: 1px solid #cccccc;
                        border-radius: 5px;
                        font-weight: bold;
                        font-family: 'Segoe Print';
                        font-size: 12px;
                        padding: 8px 16px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                        border: 1px solid #999999;
                    }
                """)
                close_btn.clicked.connect(detail_dialog.close)

                layout.addWidget(image_label)
                layout.addWidget(info_label)
                layout.addWidget(close_btn)

                detail_dialog.exec_()

        except Exception as e:
            print(f"Ошибка показа деталей товара: {e}")

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

class MenuManager:
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
        profile_menu.addSeparator()
        back_to_log = profile_menu.addAction("Выйти")

        open_profile_menu.triggered.connect(lambda: self.open_profile_menu(parent_window))
        open_order_menu.triggered.connect(lambda: self.open_order_menu(parent_window))
        back_to_log.triggered.connect(lambda: self.open_main_window_return(parent_window))
        return profile_menu

    def open_profile_menu(self, parent_window):
        parent_window.win = ProfileWin(self.user_id, self.user_type)
        parent_window.win.show()

    def open_order_menu(self, parent_window):
        parent_window.close()
        parent_window.win = OrderWin(self.user_id)
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

        self.setWindowState(QtCore.Qt.WindowMaximized)  # Развернуть на весь экран
        self.showMaximized()

        menu_manager = MenuManager(user_id, 'user')
        self.pushButton.setMenu(menu_manager.create_profile_menu(self))
        self.pushButton_6.clicked.connect(self.exit_to_catalog)

        # Загружаем заказы пользователя
        self.load_user_orders()

    def exit_to_catalog(self):
        self.close()
        self.win = CatalogWin(self.user_id)
        self.win.show()

    def load_user_orders(self):
        """Загрузка заказов пользователя из БД"""
        try:
            conn = get_connection()
            c = conn.cursor()

            # Получаем заказы пользователя
            c.execute('''
                SELECT id, date, status, sum 
                FROM user_order 
                WHERE user_id = ?
                ORDER BY date DESC
            ''', (self.user_id,))
            orders = c.fetchall()

            conn.close()

            self.display_orders(orders)

        except Exception as e:
            print(f"Ошибка загрузки заказов: {e}")
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить заказы")

    def display_orders(self, orders):
        """Отображение заказов в таблице"""
        if not orders:
            # Если заказов нет, показываем сообщение
            self.tableWidget.setRowCount(1)
            self.tableWidget.setColumnCount(1)
            no_orders_item = QtWidgets.QTableWidgetItem("Заказы не найдены")
            no_orders_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(0, 0, no_orders_item)
            return

        # Настраиваем таблицу
        self.tableWidget.setRowCount(len(orders))
        self.tableWidget.setColumnCount(4)

        # Устанавливаем заголовки
        headers = ['ID заказа', 'Дата', 'Статус', 'Сумма']
        self.tableWidget.setHorizontalHeaderLabels(headers)

        # Заполняем таблицу данными
        for row, order in enumerate(orders):
            order_id, date, status, total_sum = order

            # ID заказа
            id_item = QtWidgets.QTableWidgetItem(str(order_id))
            self.tableWidget.setItem(row, 0, id_item)

            # Дата
            date_item = QtWidgets.QTableWidgetItem(date)
            self.tableWidget.setItem(row, 1, date_item)

            # Статус
            status_item = QtWidgets.QTableWidgetItem(status)
            self.tableWidget.setItem(row, 2, status_item)

            # Сумма
            sum_item = QtWidgets.QTableWidgetItem(f"{float(total_sum):.2f} руб.")
            sum_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(row, 3, sum_item)

        # Настраиваем внешний вид таблицы
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        # Устанавливаем сортировку по дате (новые сверху)
        self.tableWidget.sortItems(1, QtCore.Qt.DescendingOrder)

class ShoppingCart(QDialog, Ui_Cart_Form):
    def __init__(self, user_id=None):
        super().__init__()
        self.setupUi(self)

        self.setWindowState(QtCore.Qt.WindowMaximized)  # Развернуть на весь экран
        self.showMaximized()

        self.user_id = user_id
        self.cart_items_data = {}  # Словарь для хранения данных о товарах {row: cart_item_id}

        menu_manager = MenuManager(user_id, 'user')

        self.pushButton.setMenu(menu_manager.create_profile_menu(self))
        self.pushButton_2.clicked.connect(self.open_cart_window)
        self.pushButton_5.clicked.connect(self.create_order)
        self.pushButton_6.clicked.connect(self.exit_to_catalog)
        self.pushButton_3.clicked.connect(self.search_products)

        # Загружаем данные корзины
        self.load_cart_data()

        # Настраиваем таблицу
        self.setup_table()

    def open_cart_window(self):
        self.close()
        self.win = ShoppingCart(self.user_id)
        self.win.show()

    def setup_table(self):
        """Настройка таблицы корзины"""
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Товар", "Количество", "Цена", "Стоимость", "Удалить"])
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def load_cart_data(self):
        """Загрузка данных корзины из БД"""
        try:
            conn = get_connection()
            c = conn.cursor()

            # Получаем ID корзины пользователя
            c.execute("SELECT id FROM cart WHERE user_id = ?", (self.user_id,))
            cart_result = c.fetchone()

            if not cart_result:
                # Если корзины нет, создаем пустую
                self.tableWidget.setRowCount(0)
                self.label_3.setText("0.00")
                return

            cart_id = cart_result[0]

            # Получаем товары в корзине
            c.execute('''
                SELECT ci.id, p.name, p.price, ci.quantity, p.image_path 
                FROM cart_item ci 
                JOIN product p ON ci.product_id = p.id 
                WHERE ci.cart_id = ?
            ''', (cart_id,))
            cart_items = c.fetchall()

            conn.close()

            self.display_cart_items(cart_items)

        except Exception as e:
            print(f"Ошибка загрузки корзины: {e}")
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить корзину")

    def display_cart_items(self, cart_items):
        """Отображение товаров в корзине"""
        self.tableWidget.setRowCount(len(cart_items))
        self.cart_items_data.clear()  # Очищаем словарь данных

        total_sum = 0

        for row, item in enumerate(cart_items):
            cart_item_id, product_name, price, quantity, image_path = item
            item_total = price * quantity
            total_sum += item_total

            # Сохраняем ID элемента корзины для этой строки
            self.cart_items_data[row] = cart_item_id

            # Название товара
            name_item = QtWidgets.QTableWidgetItem(product_name)
            self.tableWidget.setItem(row, 0, name_item)

            # Количество с возможностью редактирования
            quantity_widget = QtWidgets.QSpinBox()
            quantity_widget.setMinimum(1)
            quantity_widget.setMaximum(100)
            quantity_widget.setValue(quantity)
            quantity_widget.valueChanged.connect(lambda value, row=row: self.update_quantity(row, value))
            self.tableWidget.setCellWidget(row, 1, quantity_widget)

            # Цена за единицу
            price_item = QtWidgets.QTableWidgetItem(f"{float(price):.2f}")
            price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(row, 2, price_item)

            # Общая стоимость
            total_item = QtWidgets.QTableWidgetItem(f"{float(item_total):.2f}")
            total_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(row, 3, total_item)

            # Кнопка удаления
            delete_button = QtWidgets.QPushButton("Удалить")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff4444;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-family: 'Segoe Print';
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #cc0000;
                }
            """)
            delete_button.clicked.connect(lambda checked, row=row: self.delete_item_by_row(row))
            self.tableWidget.setCellWidget(row, 4, delete_button)

        # Обновляем итоговую сумму
        self.label_3.setText(f"{total_sum:.2f}")

        # Автоподбор ширины столбцов
        self.tableWidget.resizeColumnsToContents()

    def update_quantity(self, row, new_quantity):
        """Обновление количества товара в корзине"""
        try:
            # Получаем cart_item_id из словаря данных
            cart_item_id = self.cart_items_data.get(row)
            if not cart_item_id:
                return

            conn = get_connection()
            c = conn.cursor()

            # Обновляем количество в БД
            c.execute("UPDATE cart_item SET quantity = ? WHERE id = ?", (new_quantity, cart_item_id))
            conn.commit()
            conn.close()

            # Пересчитываем стоимость строки
            price_text = self.tableWidget.item(row, 2).text()
            price = float(price_text)
            new_total = price * new_quantity

            total_item = QtWidgets.QTableWidgetItem(f"{new_total:.2f}")
            total_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(row, 3, total_item)

            # Пересчитываем общую сумму
            self.calculate_total_sum()

        except Exception as e:
            print(f"Ошибка обновления количества: {e}")

    def delete_item_by_row(self, row):
        """Удаление товара из корзины по номеру строки"""
        try:
            cart_item_id = self.cart_items_data.get(row)
            if not cart_item_id:
                return

            reply = QMessageBox.question(
                self,
                "Подтверждение",
                "Вы уверены, что хотите удалить товар из корзины?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                conn = get_connection()
                c = conn.cursor()
                c.execute("DELETE FROM cart_item WHERE id = ?", (cart_item_id,))
                conn.commit()
                conn.close()

                # Перезагружаем корзину
                self.load_cart_data()

                QMessageBox.information(self, "Успех", "Товар удален из корзины")

        except Exception as e:
            print(f"Ошибка удаления товара: {e}")
            QMessageBox.warning(self, "Ошибка", "Не удалось удалить товар из корзины")

    def calculate_total_sum(self):
        """Пересчет общей суммы заказа"""
        total_sum = 0
        for row in range(self.tableWidget.rowCount()):
            total_item = self.tableWidget.item(row, 3)
            if total_item:
                total_sum += float(total_item.text())

        self.label_3.setText(f"{total_sum:.2f}")

    def create_order(self):
        """Оформление заказа из корзины"""
        try:
            # Проверяем, есть ли товары в корзине
            if self.tableWidget.rowCount() == 0:
                QMessageBox.warning(self, "Ошибка", "Корзина пуста. Добавьте товары перед оформлением заказа.")
                return

            conn = get_connection()
            c = conn.cursor()

            # Получаем ID корзины пользователя
            c.execute("SELECT id FROM cart WHERE user_id = ?", (self.user_id,))
            cart_result = c.fetchone()

            if not cart_result:
                QMessageBox.warning(self, "Ошибка", "Корзина не найдена")
                return

            cart_id = cart_result[0]

            # Получаем товары из корзины
            c.execute('''
                SELECT ci.product_id, ci.quantity, p.price 
                FROM cart_item ci 
                JOIN product p ON ci.product_id = p.id 
                WHERE ci.cart_id = ?
            ''', (cart_id,))
            cart_items = c.fetchall()

            if not cart_items:
                QMessageBox.warning(self, "Ошибка", "В корзине нет товаров")
                return

            # Рассчитываем общую сумму заказа
            total_sum = sum(item[1] * item[2] for item in cart_items)

            # Создаем заказ
            from datetime import datetime
            current_date = datetime.now().strftime("%Y-%m-%d")

            c.execute('''INSERT INTO user_order (user_id, date, status, sum) 
                        VALUES (?, ?, ?, ?)''',
                      (self.user_id, current_date, "Оформлен", total_sum))

            # Получаем ID созданного заказа
            order_id = c.lastrowid

            # Добавляем товары в заказ
            for product_id, quantity, price in cart_items:
                c.execute('''INSERT INTO order_position (order_id, product_id, quantity, price_at_time) 
                            VALUES (?, ?, ?, ?)''',
                          (order_id, product_id, quantity, price))

            # Очищаем корзину после оформления заказа
            c.execute("DELETE FROM cart_item WHERE cart_id = ?", (cart_id,))

            conn.commit()
            conn.close()

            # Показываем сообщение об успешном оформлении
            order_message = f"Заказ успешно оформлен!\n\nID заказа: {order_id}\nСумма заказа: {total_sum:.2f} руб.\nСтатус: Оформлен"
            QMessageBox.information(self, "Заказ оформлен", order_message)

            # Открываем окно заказов
            self.open_orders_window()

        except Exception as e:
            print(f"Ошибка оформления заказа: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось оформить заказ: {str(e)}")

    def open_orders_window(self):
        """Открытие окна заказов"""
        self.close()
        self.win = OrderWin(self.user_id)
        self.win.show()

    def search_products(self):
        """Поиск товаров в корзине"""
        search_text = self.lineEdit.text().strip().lower()

        if not search_text:
            # Если поле поиска пустое, показываем все товары
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.setRowHidden(row, False)
            return

        # Скрываем строки, которые не соответствуют поисковому запросу
        for row in range(self.tableWidget.rowCount()):
            product_name_item = self.tableWidget.item(row, 0)
            if product_name_item:
                product_name = product_name_item.text().lower()
                if search_text in product_name:
                    self.tableWidget.setRowHidden(row, False)
                else:
                    self.tableWidget.setRowHidden(row, True)

    def exit_to_catalog(self):
        """Выход в каталог"""
        self.close()
        self.win = CatalogWin(self.user_id)
        self.win.show()


class AdminPanel(QDialog, Ui_Admin_Form):
    def __init__(self, user_id = None):
        super().__init__()
        self.setupUi(self)

        self.setWindowState(QtCore.Qt.WindowMaximized)  # Развернуть на весь экран
        self.showMaximized()

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
        elif current_tab == 2:  # Клиенты
            self.add_user()
        elif current_tab == 3:  # Сотрудники
            self.add_employee()
        elif current_tab == 4:  # Категории
            self.add_category()

    def add_product(self):
        """Открывает диалог добавления товара"""
        dialog = AddProductDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Обновляем таблицу товаров после добавления
            self.load_products_to_table()

    def add_order(self):
        dialog = AddOrderWithProductsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_orders_to_table()

    def add_user(self):
        dialog = AddUserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users_to_table()

    def add_employee(self):
        dialog = AddEmployeeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_employees_to_table()

    def add_category(self):
        """Открывает диалог добавления категории"""
        dialog = AddCategoryDialog(self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.load_categories_to_table()

    def edit_item(self):
        """Редактирование выбранного элемента"""
        current_tab = self.tabWidget.currentIndex()

        if current_tab == 0:  # Заказы
            self.edit_order()
        elif current_tab == 1:  # Товары
            self.edit_product()
        elif current_tab == 2:  # Клиенты
            self.edit_user()
        elif current_tab == 3:  # Сотрудники
            self.edit_employee()
        elif current_tab == 4:  # Категории
            self.edit_category()

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

        dialog = EditOrderWithProductsDialog(self, order_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_orders_to_table()

    def edit_category(self):
        """Редактирование выбранной категории"""
        table_widget = self.tableWidget_7
        current_row = table_widget.currentRow()

        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для редактирования")
            return

        category_id = table_widget.item(current_row, 0).text()
        category_name = table_widget.item(current_row, 1).text()

        # Открываем диалог редактирования
        dialog = EditCategoryDialog(self, category_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_categories_to_table()

    def delete_item(self):
        """Удаление выбранного элемента"""
        current_tab = self.tabWidget.currentIndex()

        if current_tab == 0:  # Заказы
            self.delete_order()
        elif current_tab == 1:  # Товары
            self.delete_product()
        elif current_tab == 2:  # Клиенты
            self.delete_user()
        elif current_tab == 3:  # Сотрудники
            self.delete_employee()
        elif current_tab == 4:  # Категории
            self.delete_category()

    def delete_product(self):
        """Удаление выбранного товара"""
        try:
            table_widget = self.tableWidget_2
            current_row = table_widget.currentRow()

            if current_row == -1:
                QMessageBox.warning(self, "Ошибка", "Выберите товар для удаления")
                return

            # Безопасное получение ID товара
            id_item = table_widget.item(current_row, 0)
            if not id_item:
                QMessageBox.warning(self, "Ошибка", "Не удалось получить ID товара")
                return

            product_id = id_item.text()
            if not product_id.isdigit():
                QMessageBox.warning(self, "Ошибка", "Некорректный ID товара")
                return

            # Получаем название товара для подтверждения
            name_item = table_widget.item(current_row, 1)
            product_name = name_item.text() if name_item else "Неизвестный товар"

            reply = QMessageBox.question(
                self,
                "Подтверждение",
                f"Вы уверены, что хотите удалить товар '{product_name}'?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                conn = get_connection()
                c = conn.cursor()
                try:
                    # Проверяем, есть ли связанные записи в order_position
                    c.execute("SELECT COUNT(*) FROM order_position WHERE product_id = ?", (product_id,))
                    order_count = c.fetchone()[0]

                    if order_count > 0:
                        QMessageBox.warning(
                            self,
                            "Ошибка",
                            f"Нельзя удалить товар '{product_name}'. "
                            f"Он содержится в {order_count} заказах. "
                            f"Сначала удалите связанные заказы."
                        )
                        return

                    # Проверяем, есть ли товар в корзинах
                    c.execute("SELECT COUNT(*) FROM cart_item WHERE product_id = ?", (product_id,))
                    cart_count = c.fetchone()[0]

                    if cart_count > 0:
                        QMessageBox.warning(
                            self,
                            "Ошибка",
                            f"Нельзя удалить товар '{product_name}'. "
                            f"Он находится в {cart_count} корзинах."
                        )
                        return

                    # Удаляем товар
                    c.execute("DELETE FROM product WHERE id = ?", (product_id,))
                    conn.commit()

                    # Обновляем таблицу
                    self.load_products_to_table()
                    QMessageBox.information(self, "Успех", "Товар удален")

                except sqlite3.IntegrityError as e:
                    QMessageBox.critical(
                        self,
                        "Ошибка",
                        f"Не удалось удалить товар из-за связей с другими таблицами: {str(e)}"
                    )
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось удалить товар: {str(e)}")
                finally:
                    conn.close()

        except Exception as e:
            print(f"Общая ошибка при удалении товара: {e}")
            QMessageBox.critical(self, "Ошибка", f"Произошла непредвиденная ошибка: {str(e)}")

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
                c.execute("DELETE FROM order_position WHERE order_id = ?", (order_id,))
                c.execute("DELETE FROM user_order WHERE id = ?", (order_id,))
                conn.commit()
                self.load_orders_to_table()
                QMessageBox.information(self, "Успех", "Заказ удален")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить заказ: {str(e)}")
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

    def delete_category(self):
        """Удаление выбранной категории"""
        table_widget = self.tableWidget_7
        current_row = table_widget.currentRow()

        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для удаления")
            return

        category_id = table_widget.item(current_row, 0).text()
        category_name = table_widget.item(current_row, 1).text()

        reply = QMessageBox.question(self, "Подтверждение",
                                     f"Вы уверены, что хотите удалить категорию '{category_name}'?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            conn = get_connection()
            c = conn.cursor()
            try:
                # Проверяем, есть ли товары в этой категории
                c.execute("SELECT COUNT(*) FROM product WHERE category_id = ?", (category_id,))
                product_count = c.fetchone()[0]

                if product_count > 0:
                    QMessageBox.warning(self, "Ошибка",
                                        f"Нельзя удалить категорию '{category_name}'. "
                                        f"В ней содержится {product_count} товар(ов). "
                                        f"Сначала удалите или переместите товары.")
                    return

                c.execute("DELETE FROM category WHERE id = ?", (category_id,))
                conn.commit()
                self.load_categories_to_table()
                QMessageBox.information(self, "Успех", "Категория удалена")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить категорию: {str(e)}")
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

    def load_products_to_table(self):
        """Загрузка товаров в таблицу"""
        conn = get_connection()
        c = conn.cursor()
        # Упрощенный запрос - только данные из таблицы product
        c.execute('''SELECT id, name, brand, description, price, image_path 
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

    def load_categories_to_table(self):
        """Загрузка категорий в таблицу"""
        conn = get_connection()
        c = conn.cursor()
        c.execute('''SELECT id, name, description FROM category''')
        data = c.fetchall()
        conn.close()

        table_widget = self.tableWidget_7
        self.populate_categories_table(table_widget, data)

    def populate_categories_table(self, table_widget, data):
        """Заполнение таблицы категорий"""
        if not data:
            table_widget.setRowCount(0)
            table_widget.setColumnCount(0)
            return

        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]))

        # Правильные заголовки для категорий
        headers = ['ID', 'Название', 'Описание']
        table_widget.setHorizontalHeaderLabels(headers)

        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                table_widget.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))

        table_widget.verticalHeader().setVisible(False)
        table_widget.resizeColumnsToContents()

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

    def populate_product_table(self, table_widget, data):
        """Заполнение таблицы товаров"""
        if not data:
            table_widget.setRowCount(0)
            table_widget.setColumnCount(0)
            return

        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]))

        # Упрощенные заголовки
        headers = ['ID', 'Название', 'Бренд', 'Описание', 'Цена', 'Изображение']
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

    def on_tab_changed(self, index):
        """Обработчик смены вкладки"""
        try:
            if index == 0:  # Заказы
                self.load_orders_to_table()
            elif index == 1:  # Товары
                self.load_products_to_table()
            elif index == 2:  # Клиенты
                self.load_users_to_table()
            elif index == 3:  # Сотрудники
                self.load_employees_to_table()
            elif index == 4:  # Категории
                self.load_categories_to_table()

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
        self.pushButton_browse.clicked.connect(self.browse_image)

        # Загружаем категории из БД
        self.load_categories_from_db()

    def browse_image(self):
        """Выбор файла изображения"""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Выберите изображение товара",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_name:
            self.lineEdit_image.setText(file_name)
            self.show_image_preview(file_name)

    def show_image_preview(self, image_path):
        """Показ превью изображения"""
        try:
            pixmap = QtGui.QPixmap(image_path)
            if not pixmap.isNull():
                # Масштабируем изображение для превью
                scaled_pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.label_image_preview.setPixmap(scaled_pixmap)
            else:
                self.label_image_preview.setText("Неверный формат\nизображения")
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.label_image_preview.setText("Ошибка\nзагрузки")

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
        image_path = self.lineEdit_image.text().strip()

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
                           (name, description, price, category_id, brand, image_path) 
                           VALUES (?, ?, ?, ?, ?, ?)''',
                      (name, description, float(price), category_id, brand, image_path))

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

class AddOrderWithProductsDialog(QDialog, Ui_AddOrderWithProductsDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.selected_products = []  # Список выбранных товаров: [product_id, name, price, quantity]

        self.pushButton_save.clicked.connect(self.save_order)
        self.pushButton_cancel.clicked.connect(self.reject)
        self.pushButton_add_product.clicked.connect(self.add_product_to_list)

        self.load_users_from_db()
        self.load_products_from_db()
        self.setup_status_combo()

        # Настраиваем таблицу
        self.tableWidget_products.setColumnCount(4)
        self.tableWidget_products.setHorizontalHeaderLabels(["Товар", "Цена", "Количество", "Сумма"])

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

    def load_products_from_db(self):
        """Загружаем товары из базы данных"""
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT id, name, price FROM product WHERE price > 0")
            products = c.fetchall()
            self.comboBox_product.clear()
            self.comboBox_product.addItem("")
            for product in products:
                self.comboBox_product.addItem(f"{product[1]} - {product[2]} руб.", product[0])
        except Exception as e:
            print(f"Ошибка загрузки товаров: {e}")
        finally:
            conn.close()

    def setup_status_combo(self):
        """Заполняем статусы заказов"""
        self.comboBox_status.clear()
        self.comboBox_status.addItems(["Оформлен", "Доставляется", "Выполнен", "Отменен"])

    def add_product_to_list(self):
        """Добавляем выбранный товар в список"""
        product_index = self.comboBox_product.currentIndex()
        if product_index == 0:  # Пустой элемент
            QMessageBox.warning(self, "Ошибка", "Выберите товар")
            return

        product_id = self.comboBox_product.currentData()
        product_text = self.comboBox_product.currentText()
        quantity = self.spinBox_quantity.value()

        # Извлекаем название и цену из текста
        product_parts = product_text.split(" - ")
        product_name = product_parts[0]
        price = float(product_parts[1].replace(" руб.", ""))

        # Проверяем, не добавлен ли уже этот товар
        for i, item in enumerate(self.selected_products):
            if item[0] == product_id:
                # Увеличиваем количество
                self.selected_products[i][3] += quantity
                self.update_products_table()
                return

        # Добавляем новый товар
        self.selected_products.append([product_id, product_name, price, quantity])
        self.update_products_table()

    def update_products_table(self):
        """Обновляем таблицу выбранных товаров и итоговую сумму"""
        self.tableWidget_products.setRowCount(len(self.selected_products))

        total_sum = 0

        for row, product in enumerate(self.selected_products):
            product_id, name, price, quantity = product
            sum_price = price * quantity
            total_sum += sum_price

            # Товар
            self.tableWidget_products.setItem(row, 0, QTableWidgetItem(name))
            # Цена
            self.tableWidget_products.setItem(row, 1, QTableWidgetItem(f"{price:.2f}"))
            # Количество
            self.tableWidget_products.setItem(row, 2, QTableWidgetItem(str(quantity)))
            # Сумма
            self.tableWidget_products.setItem(row, 3, QTableWidgetItem(f"{sum_price:.2f}"))

        # Обновляем итоговую сумму
        self.label_total.setText(f"Итоговая сумма: {total_sum:.2f} руб.")

        # Автоподбор ширины столбцов
        self.tableWidget_products.resizeColumnsToContents()

    def save_order(self):
        """Сохраняем заказ и позиции заказа"""
        user_id = self.comboBox_user.currentData()
        status = self.comboBox_status.currentText()

        if not user_id:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return

        if not self.selected_products:
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы один товар в заказ")
            return

        # Рассчитываем итоговую сумму
        total_sum = sum(product[2] * product[3] for product in self.selected_products)

        conn = get_connection()
        c = conn.cursor()
        try:
            from datetime import datetime
            current_date = datetime.now().strftime("%Y-%m-%d")

            # Создаем заказ
            c.execute('''INSERT INTO user_order (user_id, date, status, sum) 
                        VALUES (?, ?, ?, ?)''',
                      (user_id, current_date, status, total_sum))

            # Получаем ID созданного заказа
            order_id = c.lastrowid

            # Добавляем позиции заказа
            for product in self.selected_products:
                product_id, name, price, quantity = product
                c.execute('''INSERT INTO order_position (order_id, product_id, quantity, price_at_time) 
                            VALUES (?, ?, ?, ?)''',
                          (order_id, product_id, quantity, price))

            conn.commit()
            QMessageBox.information(self, "Успех", f"Заказ успешно создан!\nИтоговая сумма: {total_sum:.2f} руб.")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать заказ: {str(e)}")
            conn.rollback()
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

class AddCategoryDialog(QDialog, Ui_AddCategoryDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Подключаем кнопки
        self.pushButton_save.clicked.connect(self.save_category)
        self.pushButton_cancel.clicked.connect(self.reject)

    def save_category(self):
        name = self.lineEdit_name.text().strip()
        description = self.textEdit_description.toPlainText().strip()

        if not name or not description:
            QMessageBox.warning(self, "Ошибка", "Введите данные для добавления категории")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO category (name, description) 
                        VALUES (?, ?)''', (name, description))
            conn.commit()
            QMessageBox.information(self, "Успех", "Категория успешно добавлена")
            self.accept()
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Ошибка", "Категория с таким названием уже существует")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить категорию: {str(e)}")
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
                "SELECT first_name, last_name, third_name, phone, email, address FROM user WHERE id = ?",
                (self.user_id,))
            user_data = c.fetchone()

            if user_data:
                self.lineEdit_first_name.setText(user_data[0] or "")
                self.lineEdit_last_name.setText(user_data[1] or "")
                self.lineEdit_third_name.setText(user_data[2] or "")
                self.lineEdit_phone.setText(user_data[3] or "")
                self.lineEdit_email.setText(user_data[4] or "")
                self.lineEdit_address.setText(user_data[5] or "")

        except Exception as e:
            print(f"Ошибка загрузки данных пользователя: {e}")
        finally:
            conn.close()

    def save_changes(self):
        """Сохраняем изменения"""
        first_name = self.lineEdit_first_name.text().strip()
        last_name = self.lineEdit_last_name.text().strip()
        third_name = self.lineEdit_third_name.text().strip()
        phone = self.lineEdit_phone.text().strip()
        email = self.lineEdit_email.text().strip()
        address = self.lineEdit_address.text().strip()

        if not all([first_name, last_name, phone, email, address]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''UPDATE user SET first_name=?, last_name=?, third_name=?, 
                        phone=?, email=?, address=?
                        WHERE id=?''',
                      (first_name, last_name, third_name, phone, email, address, self.user_id))
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
                "SELECT first_name, last_name, third_name, phone, email, address FROM employee WHERE id = ?",
                (self.employee_id,))
            employee_data = c.fetchone()

            if employee_data:
                self.lineEdit_first_name.setText(employee_data[0] or "")
                self.lineEdit_last_name.setText(employee_data[1] or "")
                self.lineEdit_third_name.setText(employee_data[2] or "")
                self.lineEdit_phone.setText(employee_data[3] or "")
                self.lineEdit_email.setText(employee_data[4] or "")
                self.lineEdit_address.setText(employee_data[5] or "")

        except Exception as e:
            print(f"Ошибка загрузки данных сотрудника: {e}")
        finally:
            conn.close()

    def save_changes(self):
        """Сохраняем изменения"""
        first_name = self.lineEdit_first_name.text().strip()
        last_name = self.lineEdit_last_name.text().strip()
        third_name = self.lineEdit_third_name.text().strip()
        phone = self.lineEdit_phone.text().strip()
        email = self.lineEdit_email.text().strip()
        address = self.lineEdit_address.text().strip()

        if not all([first_name, last_name, phone, email, address]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''UPDATE employee SET first_name=?, last_name=?, third_name=?, 
                        phone=?, email=?, address=?
                        WHERE id=?''',
                      (first_name, last_name, third_name, phone, email, address, self.employee_id))
            conn.commit()
            QMessageBox.information(self, "Успех", "Сотрудник успешно обновлен")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить сотрудника: {str(e)}")
        finally:
            conn.close()


class EditOrderWithProductsDialog(QDialog, Ui_EditOrderWithProductsDialog):
    def __init__(self, parent=None, order_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.order_id = order_id

        self.pushButton_save.clicked.connect(self.save_changes)
        self.pushButton_cancel.clicked.connect(self.reject)

        self.setup_status_combo()
        self.setup_products_table()

        self.load_order_data()

    def setup_status_combo(self):
        """Заполняем статусы заказов"""
        self.comboBox_status.clear()
        self.comboBox_status.addItems(["Оформлен", "Доставляется", "Выполнен", "Отменен"])

    def setup_products_table(self):
        """Настраиваем таблицу товаров (только для просмотра)"""
        self.tableWidget_products.setColumnCount(4)
        self.tableWidget_products.setHorizontalHeaderLabels(["Товар", "Цена", "Количество", "Сумма"])
        self.tableWidget_products.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Только чтение

    def load_order_data(self):
        """Загружаем данные заказа и его товары"""
        conn = get_connection()
        c = conn.cursor()
        try:
            # Загружаем основную информацию о заказе
            c.execute('''SELECT user_id, date, status, sum 
                         FROM user_order WHERE id = ?''', (self.order_id,))
            order_data = c.fetchone()

            if order_data:
                user_id, date, status, total_sum = order_data

                # Устанавливаем номер заказа
                self.label_order_id_value.setText(str(self.order_id))

                # Устанавливаем пользователя (только для просмотра)
                c.execute('''SELECT first_name, last_name FROM user WHERE id = ?''', (user_id,))
                user_data = c.fetchone()
                if user_data:
                    user_name = f"{user_data[0]} {user_data[1]}"
                    self.label_user_value.setText(user_name)

                # Устанавливаем статус (для редактирования)
                index = self.comboBox_status.findText(status)
                if index >= 0:
                    self.comboBox_status.setCurrentIndex(index)

                # Устанавливаем дату и сумму (только для просмотра)
                self.label_date_value.setText(date)
                self.label_total_value.setText(f"{total_sum:.2f} руб.")

            # Загружаем товары в заказе (только для просмотра)
            c.execute('''SELECT p.name, op.price_at_time, op.quantity
                         FROM order_position op
                         JOIN product p ON op.product_id = p.id
                         WHERE op.order_id = ?''', (self.order_id,))
            order_products = c.fetchall()

            self.display_order_products(order_products)

        except Exception as e:
            print(f"Ошибка загрузки данных заказа: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные заказа: {str(e)}")
        finally:
            conn.close()

    def display_order_products(self, order_products):
        """Отображаем товары заказа в таблице (только для просмотра)"""
        self.tableWidget_products.setRowCount(len(order_products))

        for row, product in enumerate(order_products):
            name, price, quantity = product
            sum_price = price * quantity

            # Товар
            self.tableWidget_products.setItem(row, 0, QTableWidgetItem(name))
            # Цена
            self.tableWidget_products.setItem(row, 1, QTableWidgetItem(f"{price:.2f}"))
            # Количество
            self.tableWidget_products.setItem(row, 2, QTableWidgetItem(str(quantity)))
            # Сумма
            self.tableWidget_products.setItem(row, 3, QTableWidgetItem(f"{sum_price:.2f}"))

        # Автоподбор ширины столбцов
        self.tableWidget_products.resizeColumnsToContents()

    def save_changes(self):
        """Сохраняем изменения статуса заказа"""
        status = self.comboBox_status.currentText()

        if not status:
            QMessageBox.warning(self, "Ошибка", "Выберите статус заказа")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            # Обновляем только статус заказа
            c.execute('''UPDATE user_order SET status=?
                        WHERE id=?''',
                      (status, self.order_id))

            conn.commit()
            QMessageBox.information(self, "Успех", "Статус заказа успешно обновлен")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить статус заказа: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

class EditCategoryDialog(QDialog, Ui_EditCategoryDialog):
    def __init__(self, parent=None, category_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.category_id = category_id

        self.pushButton_save.clicked.connect(self.save_changes)
        self.pushButton_cancel.clicked.connect(self.reject)

        self.load_category_data()

    def load_category_data(self):
        """Загружаем данные категории"""
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT name, description FROM category WHERE id = ?", (self.category_id,))
            category_data = c.fetchone()

            if category_data:
                self.lineEdit_name.setText(category_data[0] or "")
                self.textEdit_description.setPlainText(category_data[1] or "")

        except Exception as e:
            print(f"Ошибка загрузки данных категории: {e}")
        finally:
            conn.close()

    def save_changes(self):
        """Сохраняем изменения категории"""
        name = self.lineEdit_name.text().strip()
        description = self.textEdit_description.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название категории")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''UPDATE category SET name=?, description=? WHERE id=?''',
                      (name, description, self.category_id))

            conn.commit()
            QMessageBox.information(self, "Успех", "Категория успешно обновлена")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить категорию: {str(e)}")
        finally:
            conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())