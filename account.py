import sqlite3
from database import SQLiteDatabase
import time
import user_account

database = SQLiteDatabase('database.db')



class Account:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def admin(self,username):
        adm = user_account.Admin('database.db',username)
        adm.login(username)

    def cashier(self,username):
        usr = user_account.User('database.db',username)
        usr.login(username)

    def user(self,username):
        usr = user_account.User('database.db',username)
        usr.login(username)
