import sqlite3
from account import Account as Acc

account = Acc('database.db')
class UserAccount:
    
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def register_user(self, username, password):
        
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        self.existing_user = self.cursor.fetchone()
        
        if self.existing_user:
            print("Пользователь с таким именем уже существует")
        else:
            self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, 'user'))
            self.cursor.execute("INSERT INTO loyalty (username) VALUES (?)", (username))
            self.conn.commit()
            self.conn.close()
            print("Регистрация прошла успешно")
            

    def login_user(self, username, password):

        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        self.user = self.cursor.fetchone()
        
        if self.user != None:
            self.cursor.execute("SELECT role FROM users WHERE username=?",(username,))
            role = self.cursor.fetchone()
            match role[0]:
                case "admin":
                    account.admin(username)
                case "cashier":
                    account.cashier(username)
                case "user":
                    account.user(username)
        else:
            print("Неверное имя пользователя или пароль")

