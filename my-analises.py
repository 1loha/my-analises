# -*- coding: UTF-8 -*-
import os
import datetime
import matplotlib.pyplot as mp

from tkinter import *
from PIL import Image, ImageTk
from SQLData import SQLDataBase
from tkcalendar import Calendar
from matplotlib.widgets import RadioButtons
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from calendar import monthrange

path = os.getcwd() + r"\tables.db"
conn = SQLDataBase(path)


class Application:
    # Инициализация окна
    def __init__(self):
        self.main_window = Tk()
        self.main_window.title('Cash App')
        self.main_window.geometry('1280x720')
        self.main_window.resizable(width=False, height=False)
        [self.main_window.columnconfigure(i, weight=1) for i in range(2)]
        [self.main_window.rowconfigure(i, weight=1) for i in range(2)]

        self.graph_frame = Frame(self.main_window, background='#FFFFFF')
        self.graph_frame.grid(row=0, column=0, sticky="nsew")

        self.bottom_frame = Frame(self.main_window)
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")

        self.length = None
        self.executed = True
        self.figure = None
        self.ax = None
        self.canvas = None
        self.ax_dop = None
        self.radio_buttons = None
        self.priceLine = None
        self.timeLine = None
        self.start = None
        self.ax_dop1 = None
        self.help_bot = None
        self.tmp = True
        self.selected_period = 'week'
        self.daysCashDict = {}

        self.names_categories = []

        self.plus_input = None
        self.minus_input = None
        # conn.addExpCat('Все')
        self.categories = [x['name'] for x in conn.selectExpCat()]
        # conn.deleteAllRecords()

        # self.categories.insert(0, 'Все')
        # выгрузить категории из бд

        self.current_category = StringVar()
        if len(self.categories) == 0:
            conn.addExpCat('Все')
            self.categories.append('Все')
        self.current_category.set(self.categories[0])

        self.current_date = datetime.datetime.today()

        for i in range(4):
            self.bottom_frame.rowconfigure(i, weight=1)
        for i in range(6):
            self.bottom_frame.columnconfigure(i, weight=1)

    # дизайн нижней части окна
    def RenderBottom(self):
        Button(self.bottom_frame, text="Выбрать дату", command=self.OpenCalendar,
               background='#DAFDBA').place(relx=0.46, rely=0.2)
        Button(self.bottom_frame, text="<---", command=lambda: self.ChangeCurDate(days=-1),
               background='#DAFDBA').place(relx=0.42, rely=0.1)
        Label(self.bottom_frame, text=self.current_date.strftime("%d %B %Y"),
              background='#DAFDBA').place(relx=0.465, rely=0.11)
        Button(self.bottom_frame, text="--->", command=lambda: self.ChangeCurDate(days=1),
               background='#DAFDBA').place(relx=0.53, rely=0.1)

        Label(self.bottom_frame, textvariable=self.current_category,
              background='#DAFDBA').place(relx=0.2, rely=0.11)
        Button(self.bottom_frame, text="Сменить категорию", command=self.OpenCategoriesWindow,
               background='#DAFDBA').place(relx=0.1, rely=0.1)

        Label(self.bottom_frame, text="Доход", background='#DAFDBA').place(relx=0.32, rely=0.45)
        Label(self.bottom_frame, text="Расход", background='#DAFDBA').place(relx=0.62, rely=0.45)
        Button(self.bottom_frame, text="Ок", command=lambda: self.OnValueChanged()).place(relx=0.47, rely=0.55)

        plus_sv = StringVar()
        self.plus_input = Entry(self.bottom_frame, textvariable=plus_sv, background='#DAFDBA')
        self.plus_input.place(relx=0.3, rely=0.55)
        # plus_sv.trace("w", lambda name, index, mode, sv=plus_sv: self.OnValueChanged())

        minus_sv = StringVar()
        self.minus_input = Entry(self.bottom_frame, textvariable=minus_sv, background='#DAFDBA')
        self.minus_input.place(relx=0.6, rely=0.55)
        # minus_sv.trace("w", lambda name, index, mode, sv=minus_sv: self.OnValueChanged())

        def clear_entry(event):
            event.widget.delete(0, 'end')

        # self.plus_input.bind('<FocusOut>', clear_entry)
        # self.minus_input.bind('<FocusOut>', clear_entry)




    def OpenCategoriesWindow(self):
        # выгрузка категорий из бд - сделать функцию
        global categories_window
        global categories_frame
        global categories_canvas
        self.categories_window = Toplevel()
        # self.categories_window.grab_set()
        self.categories_window.title("Выбор категории")
        self.categories_window.geometry("300x300")
        self.categories_window.resizable(False, False)

        categories_canvas = Canvas(self.categories_window, borderwidth=0, background="#ffffff")
        categories_frame = Frame(categories_canvas, background="#ffffff")
        scrollbar = Scrollbar(self.categories_window, orient="vertical", command=categories_canvas.yview)
        categories_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        categories_canvas.pack(side="left", fill="both", expand=True)
        categories_canvas.create_window((4, 4), window=categories_frame, anchor="nw")

        Button(categories_frame, text="+", command=self.OpenAddCategoryWindow).grid()
        for i in range(len(self.categories)):
            Button(categories_frame, text=self.categories[i], command=lambda x=self.categories[i]: self.ChangeCategory(x)).grid(row=i+1, column=0)
            Button(categories_frame, text="-", command=lambda x=self.categories[i]: self.ChangeCategory(x)).grid(row=i+1, column = 1)
        # for category in self.categories:
        #     Button(categories_frame, text=category, command=lambda x=category: self.ChangeCategory(x)).grid(row=1)
        #     Button(categories_frame, text="-", command=lambda x=category: self.ChangeCategory(x)).grid(row=1)

        categories_canvas.update_idletasks()
        categories_canvas.configure(scrollregion=categories_canvas.bbox("all"))

    def ChangeCategory(self, category):
        global categories_window
        self.current_category.set(category)
        self.RenderBottom()
        self.categories_window.destroy()
        self.selected_button(self.selected_period)

    def OpenAddCategoryWindow(self):
        global add_categoty_window
        self.add_categoty_window = Toplevel()
        # self.categories_window.grab_set()
        self.add_categoty_window.title("Добавить категорию")
        self.add_categoty_window.geometry("200x200")
        self.add_categoty_window.resizable(False, False)
        new_category = Entry(self.add_categoty_window)
        new_category.pack(pady=10)
        Button(self.add_categoty_window, text="Ok", command=lambda: self.AddCategory(new_category.get())).pack(pady=10)

        # [done]добавление категории в БД addcat

    def AddCategory(self, category):
        global add_categoty_window
        global categories_frame
        global categories_canvas
        self.categories.append(category)
        #
        conn.addExpCat(category)  # expense
        #
        Button(categories_frame, text=category, command=lambda x=category: self.ChangeCategory(x)).grid(row=len(self.categories), column= 0)
        Button(categories_frame, text="-").grid(row=len(self.categories), column= 1)
        categories_canvas.update_idletasks()
        categories_canvas.configure(scrollregion=categories_canvas.bbox("all"))
        self.add_categoty_window.destroy()

    def OpenCalendar(self):
        global calendar_window
        self.calendar_window = Toplevel()
        self.calendar_window.grab_set()
        self.calendar_window.title("Выбор даты")
        self.calendar_window.geometry("300x300")
        self.calendar_window.resizable(False, False)
        global calendar
        self.calendar = Calendar(self.calendar_window,
                                 selectmode='day',
                                 year=self.current_date.year,
                                 month=self.current_date.month,
                                 day=self.current_date.day)
        self.calendar.pack(pady=20)

        Button(self.calendar_window, text="Ok", command=self.SelectDate).pack(pady=20)

    def SelectDate(self):
        global current_date
        global calendar_window
        #
        # self.SaveRecord()
        #
        self.current_date = datetime.datetime.strptime(self.calendar.get_date(), '%m/%d/%y')  # дата измен
        self.calendar_window.destroy()
        self.selected_button(self.selected_period)
        # [done]запись в БД прошлого дня, если ячейки пустые null?
        self.RenderBottom()

    def SaveRecord(self, plus, minus):  # ++сохранение записи при изменении даты, !!!!!!!!!!!!!!!!выход из приложения - обработать
        # try:
        #     self.plus_input.get() ########################################################################################
        # except ValueError:
        #     pass
        #
        # try:
        #     self.minus_input.get()
        # except ValueError:
        #     pass

        # else:
        _expId = conn.findExpCatId(self.current_category.get())
        conn.addExpense(_expId, self.current_date.strftime("%Y-%m-%d"), minus)  # self.minus_input.get())
        conn.addIncome(_expId, self.current_date.strftime("%Y-%m-%d"), plus)   # self.plus_input.get())  # +incomecat

    def ChangeCurDate(self, days=0):
        global current_date
        #
        # self.SaveRecord()
        #
        self.current_date += datetime.timedelta(days=days)
        self.selected_button(self.selected_period)

        self.RenderBottom()

    def OnValueChanged(self):
        value, plus, minus = 0, 0, 0
        try:
            plus += int(self.plus_input.get())  # пришел доход
            print("plus =", plus)
        except ValueError:
            pass

        try:
            minus -= int(self.minus_input.get())  # пришел расход
            print("value =", minus)
        except ValueError:
            pass

        self.SaveRecord(plus, minus)
         #  не сохраняет доход в 30 числе
        #  непраавильно работает, если значения есть и в доходе, и в расходе
        # все идет в доход..
        value += plus + minus

        if (self.current_date.strftime("%Y-%m-%d") in self.daysCashDict.keys()):
            print("++++++++++++++++++++++++++++++++++++++++++++++++")
            # print("В базу данных добавлено значение " + str(value) + " для даты " + self.current_date.strftime(
            #     "%Y-%m-%d"))
            self.daysCashDict[self.current_date.strftime("%Y-%m-%d")] += value
            print("db[date] = ", self.daysCashDict[self.current_date.strftime("%Y-%m-%d")])
        else:
            print("------------------------------------------------")
            # self.daysCashDict.update({self.current_date.strftime("%Y-%m-%d"): 0})
            self.daysCashDict[self.current_date.strftime("%Y-%m-%d")] += value
            # print("внесено значение " + str(value) + " для даты " + self.current_date.strftime("%Y-%m-%d"))

        self.plus_input.delete(0, END)
        self.minus_input.delete(0, END)
        self.selected_button(self.selected_period)

    def selected_button(self, label):
        i_dict = {
            "week": 0,
            "month": 1
        }
        i = i_dict.get(label, 0)
        self.selected_period = i
        self.render_lines(i)
        self.canvas.draw()

    def render_lines(self, selected_period):
        self.ax.clear()
        self.ax.grid()
        self.priceLine = []
        self.timeLine = []
        self.length = []
        maxMarks = 0

        if selected_period == 0:  # week

            # количество меток для недели
            maxMarks = 7

            # Начинаем с понедельника
            self.start = self.current_date - datetime.timedelta(days=self.current_date.weekday())

            if self.tmp:
                # запрос данных БД за неделю
                tempCursor = conn.sumExpenseByDays(self.start.strftime("%Y-%m-%d"),
                                                   (self.start + datetime.timedelta(days=maxMarks)).strftime("%Y-%m-%d"))
                # занести словарем key-value
                self.daysCashDict = dict((day, cash) for day, cash in tempCursor.fetchall())
                self.tmp = False

            # проинициализировать нулями пустые значения
            for iDay in range(maxMarks):
                keyDict = (self.start + datetime.timedelta(days=iDay)).strftime("%Y-%m-%d")
                if keyDict not in self.daysCashDict:
                    self.daysCashDict[keyDict] = 0

            self.timeLine = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        elif selected_period == 1:  # month
            maxMarks = monthrange(self.current_date.year, self.current_date.month)[1]  # сколько дней в месяце
            self.start = datetime.datetime(self.current_date.year, self.current_date.month, 1)  # Начинаем с 1 числа
            #
            # добавить daysCashDict
            #
            self.timeLine = [str(i + 1) for i in range(maxMarks)]



        # вынести из словаря БД значения в обычный массив за каждый день
        for i in range(maxMarks):
            self.priceLine = mp.np.append(self.priceLine, self.daysCashDict.get(
                                              (self.start + datetime.timedelta(days=i)).strftime("%Y-%m-%d"), 0))

        print("priceLine =", self.priceLine, '\n')

        # по оси y установить ограничение в 15 значений
        self.ax.yaxis.set_major_locator(mp.MaxNLocator(maxMarks))

        # приравнять количество меток по оси x относительно y
        for j in range(len(self.daysCashDict)):
            self.length = mp.np.append(self.length, j)

        # построить линию тренда
        z = mp.np.polyfit(self.length, self.priceLine, 1)
        p = mp.np.poly1d(z)

        # построить графики
        self.ax.plot(self.timeLine, self.priceLine, label=self.current_category.get(), color="#45C4B0", marker=".", linestyle="-")
        self.ax.plot(self.timeLine, p(self.length), label='trend line', color="y", linestyle=":")
        self.ax.legend(loc='lower center')

    # визуализация графика
    def RenderGraph(self):
        self.figure = mp.Figure(figsize=(15, 1), dpi=130, facecolor="#45C4B0")
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.canvas = FigureCanvasTkAgg(self.figure, self.main_window)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        self.ax_dop = self.figure.add_subplot(3, 7, 7)
        self.radio_buttons = RadioButtons(self.ax_dop, ['week', 'month'], 0, activecolor='black')
        self.radio_buttons.on_clicked(self.selected_button)

        self.ax_dop1 = self.figure.add_subplot(6, 20, 1)
        self.help_bot = mp.Button(self.ax_dop1, "?")
        self.help_bot.on_clicked(lambda x: self.open_image())
        self.help_bot.hovercolor = "grey"

        # Button(self.bottom_frame, text="?", command=lambda: self.open_image1).place(x=0, y=0)

        self.selected_button(self.selected_period)

    def open_image(self):
        image = Image.open("11.png")
        image = image.resize((380, 290))
        image = ImageTk.PhotoImage(image)

        label = Label(self.main_window, image=image)
        label.image_names = image
        label.place(relx=1.0, rely=1.0, anchor='se')
        label.bind("<Button-1>", lambda event: label.destroy())


apl = Application()
apl.RenderGraph()
apl.RenderBottom()
apl.main_window.mainloop()
