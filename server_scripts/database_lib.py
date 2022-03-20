from __main__ import app
from __main__ import mysql
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import datetime
import hashlib

def create_account(username, password, email, gender, birthday):
    if str(gender) == "2":
        gendertype = "male"
    elif str(gender) == "3":
        gendertype = "female"
    else:
        gendertype = "homosexual"
    
    hashedpassword = hashlib.md5(password.encode())

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, NULL, %s, %s)', (username, hashedpassword, email, 0, 15, "Yeah...", 0, 0, gendertype, str(birthday)))
    mysql.connection.commit()

def check_existing_account_by_name(username):
    # Check if account exists using MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
    account = cursor.fetchone()
    
    if account:
        return True
    else:
        return False

def check_account_login(username, password):
    # Check if account exists using MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
    account = cursor.fetchone()
    
    if account:
        if account['password'] == hashlib.md5(password.encode()):
            return True
        else:
            return False
    else:
        return False

def get_account_login_data(username):
    # Check if account exists using MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
    account = cursor.fetchone()
    
    if account:
        logindata = [account['username'], account['id'], account['money']]
        return logindata
    else:
        return False
