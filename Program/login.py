import sqlite3
from time import time
from hashlib import sha256
database = 'users.db'
try:
    conn = sqlite3.connect(database, check_same_thread=False)
except Exception as e:
    print(f"Error connecting to database: {e}")

def check(username, password):

    sql_cmd = '''SELECT pass_hash, pass_salt FROM USERS'''
    cur = conn.cursor()
    cur.execute(sql_cmd)
    pre_hashed_password, salt = cur.fetchone()
    if pre_hashed_password == sha256((password+salt).encode('ascii')).hexdigest():
        print("Login Success!")
        return True
    else:
        print("Login Fail!")
        return False



def register(username, password):
    salt = str(int(time()))
    to_hash = password+salt
    hashed_password = sha256(to_hash.encode()).hexdigest()
    sql_cmd = '''INSERT INTO USERS(username, pass_hash, pass_salt) VALUES(?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql_cmd, (username, hashed_password, salt))
    conn.commit()
    cur.close()
