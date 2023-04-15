import sqlite3
import hashlib

DATABASE = 'database.db'
con = sqlite3.connect(DATABASE)
def create_users_table():
    con.execute("CREATE TABLE IF NOT EXISTS users(username, mon, tue, wed, thu, fri, sat, sun)")
    con.execute("CREATE TABLE IF NOT EXISTS employee(id integer, username, password, wages)")
    con.execute("CREATE TABLE IF NOT EXISTS admin(id integer, username, password)")
    con.execute("CREATE TABLE IF NOT EXISTS mon(username, time, position)")
    con.execute("CREATE TABLE IF NOT EXISTS tue(username, time, position)")
    con.execute("CREATE TABLE IF NOT EXISTS wed(username, time, position)")
    con.execute("CREATE TABLE IF NOT EXISTS thu(username, time, position)")
    con.execute("CREATE TABLE IF NOT EXISTS fri(username, time, position)")
    con.execute("CREATE TABLE IF NOT EXISTS sat(username, time, position)")
    con.execute("CREATE TABLE IF NOT EXISTS sun(username, time, position)")
    con.close()

def init_admin():
    admin = 'admin'
    pin = '1qaz!QAZ'
    con.execute("INSERT INTO admin(?, ?, ?)",
                0, 
                hashlib.sha256(admin.encode()).hexdigest(),
                hashlib.sha256(pin.encode()).hexdigest()
                )
    
