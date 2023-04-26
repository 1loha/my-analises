import sqlite3 as sq


class SQLDataBase(object):
    # �������� ������, ���� �� ���
    def __init__(self, pathName):
        self.path = pathName
        with sq.connect(self.path) as con:
            # ������ ������ ���� ��� �������
            con.row_factory = sq.Row

            self.cur = con.cursor()
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
            cash MONEY,
            com TEXT NOT NULL)""")
            # ���� ��� �������
            self.cur.execute("""CREATE TABLE IF NOT EXISTS income(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inc_id INTEGER,
            incDate DATE,
            cash MONEY,
            com TEXT NOT NULL)""")

    # + ����/��� �����
    def addExpCat(self, catName):
        self.cur.execute("INSERT INTO expenseCat(name) VALUES(?)", catName)

    def addIncCat(self, catName):
        self.cur.execute("INSERT INTO incomeCat(name) VALUES(?)", catName)

    # + ����/��� ������
    def addExpense(self, exp_id, _date, cash, com):  # +without com
        self.cur.execute("INSERT INTO expense(exp_id, expDate, cash, com) VALUES(?,?,?,?)", exp_id, _date, cash, com)

    def addIncome(self, inc_id, _date, cash, com):  # -=-
        self.cur.execute("INSERT INTO income(inc_id, incDate, cash, com) VALUES(?,?,?,?)", inc_id, _date, cash, com)

    def addExpense(self, exp_id, _date, cash, com):  # +without com
        self.cur.execute("INSERT INTO expense(exp_id, expDate, sum, com) VALUES(?,?,?,?)", exp_id, _date, cash, com)

    def addIncome(self, inc_id, _date, cash, com):  # -=-
        self.cur.execute("INSERT INTO income(inc_id, incDate, sum, com) VALUES(?,?,?,?)", inc_id, _date, cash, com)

    # - ����/��� �����
    def delExpCat(self, exp_id):
        self.cur.execute("DELETE FROM expenseCat WHERE exp_id == ?", exp_id)

    def delIncCat(self, inc_id):
        self.cur.execute("DELETE FROM incomeCat WHERE inc_id == ?", inc_id)

    # ��� ������� -- ����� ���� �� ���� ��� ����� ��������� �� ������ �������, ������� -- ��������� ������, ������ �� ������� ����
    def sumExpenseByDays(self, dateBegin, dateEnd):  # 1.04 - 4.04
        res = self.cur.execute("""SELECT (expDate, sum(cash) as sumCash) 
        FROM expense 
        GROUP BY expDate 
        WHERE (expDate >= ? AND expDate <= ?) 
        ORDER BY expDate ASC""", dateBegin, dateEnd)
        return res

    # -=- �������
    def sumIncomeByDays(self, dateBegin, dateEnd):  # 1.04 - 4.04
        res = self.cur.execute("""SELECT (incDate, sum(cash) as sumCash) 
        FROM income 
        GROUP BY incDate
        WHERE (incDate >= ? AND incDate <= ?) 
        ORDER BY incDate ASC""", dateBegin, dateEnd)
        return res

    # ����� �� ������ �� ��������� �� ��������� ����������, ����� �� �������� �����
    def sumExpenseByCateg(self, dateBegin, dateEnd):
        res = self.cur.execute("""SELECT (exp_id, sum(cash) as sumCash)
        FROM execute
        GROUP BY exp_id
        WHERE (expDate >= ? AND expDate <= ?) 
        ORDER BY sumCash DESC""", dateBegin, dateEnd)
        return res

    def sumIncomeByCateg(self, dateBegin, dateEnd):
        res = self.cur.execute("""SELECT (inc_id, sum(cash) as sumCash)
        FROM income
        GROUP BY inc_id
        WHERE (incDate >= ? AND incDate <= ?) 
        ORDER BY sumCash DESC""", dateBegin, dateEnd)
        return res
