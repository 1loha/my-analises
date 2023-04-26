import sqlite3 as sq


class SQLDataBase(object):
    # создание таблиц, если не сущ
    def __init__(self, pathName):
        self.path = pathName
        with sq.connect(self.path) as con:
            # извлеч данные хран как словарь
            con.row_factory = sq.Row

            self.cur = con.cursor()
            # табл расх катег
            self.cur.execute("""CREATE TABLE IF NOT EXISTS expenseCat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL)""")
            # табл доход катег
            self.cur.execute("""CREATE TABLE IF NOT EXISTS incomeCat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL)""")
            # табл общ расходов
            self.cur.execute("""CREATE TABLE IF NOT EXISTS expense(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exp_id INTEGER,
            expDate DATE,
            cash MONEY,
            com TEXT NOT NULL)""")
            # табл общ доходов
            self.cur.execute("""CREATE TABLE IF NOT EXISTS income(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inc_id INTEGER,
            incDate DATE,
            cash MONEY,
            com TEXT NOT NULL)""")

    # + расх/дох катег
    def addExpCat(self, catName):
        self.cur.execute("INSERT INTO expenseCat(name) VALUES(?)", catName)

    def addIncCat(self, catName):
        self.cur.execute("INSERT INTO incomeCat(name) VALUES(?)", catName)

    # + расх/дох запись
    def addExpense(self, exp_id, _date, cash, com):  # +without com
        self.cur.execute("INSERT INTO expense(exp_id, expDate, cash, com) VALUES(?,?,?,?)", exp_id, _date, cash, com)

    def addIncome(self, inc_id, _date, cash, com):  # -=-
        self.cur.execute("INSERT INTO income(inc_id, incDate, cash, com) VALUES(?,?,?,?)", inc_id, _date, cash, com)

    def addExpense(self, exp_id, _date, cash, com):  # +without com
        self.cur.execute("INSERT INTO expense(exp_id, expDate, sum, com) VALUES(?,?,?,?)", exp_id, _date, cash, com)

    def addIncome(self, inc_id, _date, cash, com):  # -=-
        self.cur.execute("INSERT INTO income(inc_id, incDate, sum, com) VALUES(?,?,?,?)", inc_id, _date, cash, com)

    # - расх/дох катег
    def delExpCat(self, exp_id):
        self.cur.execute("DELETE FROM expenseCat WHERE exp_id == ?", exp_id)

    def delIncCat(self, inc_id):
        self.cur.execute("DELETE FROM incomeCat WHERE inc_id == ?", inc_id)

    # для графика -- сумма трат по дням без учета категорий за период времени, словарь -- результир данные, отсорт по возраст даты
    def sumExpenseByDays(self, dateBegin, dateEnd):  # 1.04 - 4.04
        res = self.cur.execute("""SELECT (expDate, sum(cash) as sumCash) 
        FROM expense 
        GROUP BY expDate 
        WHERE (expDate >= ? AND expDate <= ?) 
        ORDER BY expDate ASC""", dateBegin, dateEnd)
        return res

    # -=- доходов
    def sumIncomeByDays(self, dateBegin, dateEnd):  # 1.04 - 4.04
        res = self.cur.execute("""SELECT (incDate, sum(cash) as sumCash) 
        FROM income 
        GROUP BY incDate
        WHERE (incDate >= ? AND incDate <= ?) 
        ORDER BY incDate ASC""", dateBegin, dateEnd)
        return res

    # сумма по каждой из категорий за временной промежуток, вывод по убыванию суммы
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
