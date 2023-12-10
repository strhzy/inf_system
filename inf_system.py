import sqlite3
from database import SQLiteDatabase
from user import UserAccount
from account import Account

db_name = 'database.db'

db = SQLiteDatabase(db_name)
UserAccount.db_name = db_name
user = UserAccount(db_name)
Account.db_name = db_name
account = Account(db_name)
while True:
    choice = input("1.Регистрация\n2.Вход\n3.Выход\n")
    match choice:
        case "1": 
            print("Регистрация")
            username = input("Введите логин: ")
            password = input("Введите пароль: ")
            user.register_user(username, password)
            Choose()
        case "2":
            print("Вход")
            username = input("Введите логин: ")
            password = input("Введите пароль: ")
            user.login_user(username, password)
        case "3":
            exit()
        case _:
            print("Неправильно введенные данные")


