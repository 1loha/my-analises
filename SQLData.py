import sqlite3 as sq


class SQLDataBase:
    # �������� ������, ���� �� ���
    def __init__(self, pathName):
        self.path = pathName
        with sq.connect(self.path) as self.con:
            # ������ ������ ���� ��� �������
            self.con.row_factory = sq.Row

            self.cur = self.con.cursor()
            # ���� ���� �����
            self.cur.execute("""CREATE TABLE IF NOT EXISTS expenseCat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL)""")
            # ���� ����� �����
            self.cur.execute("""CREATE TABLE IF NOT EXISTS incomeCat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL)""")
            # ���� ��� ��������
            self.cur.execute("""CREATE TABLE IF NOT EXISTS expense(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exp_id INTEGER,
            expDate DATE,
            cash MONEY)""")
            # ���� ��� �������
            self.cur.execute("""CREATE TABLE IF NOT EXISTS income(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inc_id INTEGER,
            incDate DATE,
            cash MONEY)""")

    # + ����/��� �����
    def addExpCat(self, catName):
        self.cur.execute("INSERT INTO expenseCat(name) VALUES(?)", [catName])
        self.con.commit()

    def addIncCat(self, catName):
        self.cur.execute("INSERT INTO incomeCat(name) VALUES(?)", [catName])
        self.con.commit()
    # + ����/��� ������
    #def addExpense(self, exp_id, _date, cash, com):  # +without com
        #self.cur.execute("INSERT INTO expense(exp_id, expDate, cash, com) VALUES(?,?,?,?)", (exp_id, _date, cash, com))
        #self.con.commit()

    #def addIncome(self, inc_id, _date, cash, com):  # -=-
        #self.cur.execute("INSERT INTO income(inc_id, incDate, cash, com) VALUES(?,?,?,?)", (inc_id, _date, cash, com))

    def addExpense(self, exp_id, _date, cash):  # +without com
        self.cur.execute("INSERT INTO expense(exp_id, expDate, cash) VALUES(?,?,?)", (exp_id, _date, cash))
        self.con.commit()

    def addIncome(self, inc_id, _date, cash):  # -=-
        self.cur.execute("INSERT INTO income(inc_id, incDate, cash) VALUES(?,?,?)", (inc_id, _date, cash))
        self.con.commit()

    # - ����/��� �����
    def delExpCat(self, exp_id):
        self.cur.execute("DELETE FROM expenseCat WHERE exp_id == ?", [exp_id])
        self.con.commit()

    def delIncCat(self, inc_id):
        self.cur.execute("DELETE FROM incomeCat WHERE inc_id == ?", [inc_id])
        self.con.commit()

    # ��� ������� -- ����� ���� �� ���� ��� ����� ��������� �� ������ �������, ������� -- ��������� ������, ������ �� ������� ����
    def sumExpenseByDays(self, dateBegin, dateEnd):  # 1.04 - 4.04
        res = self.cur.execute("""SELECT expDate, SUM(cash) AS sumCash 
        FROM expense 
        WHERE (expDate >= ? AND expDate <= ?) 
        GROUP BY expDate 
        ORDER BY expDate ASC""", (dateBegin, dateEnd))
        self.con.commit()
        return res

    # -=- �������
    def sumIncomeByDays(self, dateBegin, dateEnd):  # 1.04 - 4.04
        res = self.cur.execute("""SELECT (incDate, sum(cash) as sumCash) 
        FROM income 
        WHERE (incDate >= ? AND incDate <= ?) 
        GROUP BY incDate
        ORDER BY incDate ASC""", (dateBegin, dateEnd))
        self.con.commit()
        return res

    # ����� �� ������ �� ��������� �� ��������� ����������, ����� �� �������� �����
    def sumExpenseByCateg(self, dateBegin, dateEnd):#############
        res = self.cur.execute("""SELECT exp_id, SUM(cash) AS sumCash
        FROM expense
        WHERE (expDate >= ? AND expDate <= ?)
        GROUP BY exp_id
        ORDER BY sumCash DESC""", (dateBegin, dateEnd))
        self.con.commit()
        return res

    def sumIncomeByCateg(self, dateBegin, dateEnd):
        res = self.cur.execute("""SELECT inc_id, sum(cash)
        FROM income
        WHERE (incDate >= ? AND incDate <= ?) 
        GROUP BY inc_id
        ORDER BY sum(cash) DESC""", (dateBegin, dateEnd))
        self.con.commit()
        return res
    def findExpCatId(self, catName):#����� �� ����� id ���������
        numRec = self.cur.execute("""SELECT id FROM expenseCat WHERE name == ?""", [str(catName)])
        return numRec.fetchone()[0]

        
    
    def selectExpCat(self):
        categ = self.cur.execute("SELECT name FROM expenseCat")
        return categ

    def deleteAllRecords(self):
        self.cur.execute("""DELETE FROM expense""")
        self.cur.execute("""DELETE FROM income""")
        self.con.commit()

    #����. ������
    #������� ��� ������
    #�������� ��������� -> �������� � ��� �������
    #������� ��� ��������� ?? -> ������� ��� ������
