import sqlite3 as sq
class SQLDataBase(object):
    #�������� ������, ���� �� ���
    def __init__(self, pathName):
        self.path = pathName
        with sq.connect(path) as con
            self.cur = con.cursor()
            #���� ���� �����
            cur.execute("""CREATE TABLE IF NOT EXIST expenseCat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL)""")
            #���� ����� �����
            cur.execute("""CREATE TABLE IF NOT EXIST incomeCat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL)""")
            #���� ��� ��������
            cur.execute("""CREATE TABLE IF NOT EXIST expense(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exp_id INTEGER,
            expDate DATE,
            sum MONEY,
            com TEXT NOT NULL)""")
            #���� ��� ������� 
            cur.execute("""CREATE TABLE IF NOT EXIST income(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inc_id INTEGER,
            incDate DATE,
            sum MONEY,
            com TEXT NOT NULL)""")
    
    #+ ����/��� �����
    def addExpCat(self, catName):
        cur.execute("INSERT INTO expenseCat(name) VALUES(?)", catName)


    def addIncCat(self, catName):
        cur.execute("INSERT INTO incomeCat(name) VALUES(?)", catName)

    #+ ����/��� ������
    def addExpense(self, exp_id, _date, sum, com): #+without com
        cur.execute("INSERT INTO expense(exp_id, expDate, sum, com) VALUES(?,?,?,?)", exp_id, _date, sum, com)


    def addIncome(self, inc_id, _date, sum, com): #-=-
        cur.execute("INSERT INTO income(inc_id, incDate, sum, com) VALUES(?,?,?,?)", inc_id, _date, sum, com)
    
    #- ����/��� �����
    def delExpCat(self, exp_id):
        cur.execute("DELETE FROM expenseCat WHERE exp_id == ?", exp_id)

    
    def delIncCat(self, inc_id):
        cur.execute("DELETE FROM incomeCat WHERE inc_id == ?", inc_id)


