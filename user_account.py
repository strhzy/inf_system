import sqlite3
from database import SQLiteDatabase


db = SQLiteDatabase('database.db')

class Base:
    def __init__(self, db_name, username):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.username = username
    
    def login(self,username):
        print(f"Вы вошли как {username}")

class Admin(Base):
    def __init__(self, db_name, username):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.username = username
    
    def login(self,username):
        print(f"Вы вошли как {username}")
        while True:
            choice = string(input("1.Изменение роли\n2.Добавление товаров\n3.Удаление пользователей\n4.Выход из аккаунта\n"))
            match choice:
                case "1":
                    usern = input("Введите имя пользователя: ")
                    condition = ('username = ?',(usern,))
                    db.select_data('users',(condition,))
                    result = self.cursor.fetchone()
                    print(f"Роль {result[1]}")
                    choice = input("Изменить роль\n1.да\n2.нет")
                    match choice:
                        case "1":
                            newrole = input("Выберите роль\n1.admin\n2.cashier\n3.user\n")
                            query2 = (f"SELECT id FROM users WHERE username=?")
                            self.cursor.execute(query2,(usern,))
                            ID = self.cursor.fetchone()
                            match newrole:
                                case "1":
                                    role = {
                                        "role":"admin"
                                    }
                                case "2":
                                    role = {
                                        "role":"cashier"
                                    }
                                case "3":
                                    role = {
                                        "role":"user"
                                    }
                            db.update_data('users',role,f'id={ID[0]}')
                            db.close_connection()
                        case "2":
                            pass
                case "2":
                    product = input("Введите продукт для добавления: ")
                    count = int(input("Введите количество товара: "))
                    data = {
                        'product':product,
                        'count':count
                    }
                    db.insert_data('storage',data)
                    db.close_connection()
                case "3":
                    usern = input("Введите имя пользователя: ")
                    db.delete_data('users',('username = ?',(usern)))
                    print("Пользователь удален")
                case "4":
                    exit()
                case _:
                    print("Неправильно введенные данные")

class User(Base):
    def __init__(self, db_name, username):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.username = username                         
    
    def login(self,username):
        print(f"Вы вошли как {username}")
        while True:
            choice = string(input("1.Посмотреть баллы лояльности\n2.Поменять пароль\n3.Поменять логин\n4.Выход из аккаунта\n"))
            match choice:
                case "1":
                    result = db.select_data('loyalty',('username = ?',(username)))
                    print(f"Количество е-баллов: {result[2]}")
                    db.close_connection()
                case "2":
                    data = {
                        'password':input("Введите новый пароль")
                    }
                    db.update_data('users',data,f'username = {username}')
                case "3":
                    data = {
                        'username':input("Введите новый логин")
                    }
                    db.update_data('users',data,f'username = {username}')
                case "4":
                    exit()
                case _:
                    print("Неправильно введенные данные")

class Cashier(Base):
    def __init__(self, db_name, username):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.username = username                         
    
    def login(self,username):
        print(f"Вы вошли как {username}")
        while True:
            choice = string(input("1.Касса\n2.Выход\n"))
            match choice:
                case "1":
                    print("Меню кассы")
                    Kassa()
                case "2":
                    exit()
                case _:
                    print("Неправильно введенные данные")
    def Kassa(self):
        zakaz = []
        cost = int
        try:
            id_usr = int(input("Введите ID покупателя"))
            self.cursor.execute("SELECT username FROM users WHERE id = ?",(id_usr))
            name_usr = self.cursor.fetchone()
        except:
            print("Ошибка ввода данных. Попробуйте еще раз.")
            Kassa()
        while True:
            choice = string(input("1.Пробить товар\n2.Оплата"))
            if choice == "1":
                try:
                    id_gds = int(input("ID товара"))
                    query1 = ("SELECT product FROM storage WHERE id = ?",(id_gds))
                    self.cursor.execute(query1)
                    name = self.cursor.fetchone()
                    zakaz.append(name)
                    query2 = ("SELECT cost FROM storage WHERE id = ?",(id_gds))
                    self.cursor.execute(query2)
                    cost_db = self.cursor.fetchone()
                    cost =+ cost_db
                    self.cursor.execute("SELECT count FROM storage WHERE id = ?",(id_gds))
                    count = self.cursor.fetchone()
                    data = {
                        "count":count-1
                    }
                    db.update_data("storage",data,("id = ?",(id_gds)))
                except:
                    print("Ошибка ввода данных. Попробуйте еще раз.")
            elif choice == "2":
                if len(zakaz) == 0:
                    print("Корзина пуста. Сначала добавьте товары")
                else:
                    query = ("SELECT points FROM loyalty WHERE username = ?",(name_usr))
                    self.cursor.execute(query)
                    points = self.cursor.fetchone()
                    print(f"Количество баллов у {name_usr}: {points}")
                    choice2 = string(input("1.Списать баллы\n2.Начислить баллы"))
                    match choice2:
                        case "1":
                            if points<cost:
                                cost=-points
                                print(f"Итог {cost} рублей")
                            else:
                                cost = 0
                                print(f"Итог {cost} рублей")
                        case "2":
                            points =+ cost/10
                            print(f"Итог {cost} рублей")
                        case _:
                            print("Неправильно введенные данные")
            else:
                print("Неправильно введенные данные")
                    