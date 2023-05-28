# -*- coding: Windows-1251 -*-
from ipaddress import v4_int_to_packed
import os
import datetime
import matplotlib.pyplot as mp

from tkinter import *
from PIL import Image, ImageTk
from SQLData import SQLDataBase
from tkcalendar import Calendar  # включи при себе
from matplotlib.widgets import RadioButtons
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from calendar import monthrange

path = os.getcwd() + r"\tables.db"
conn = SQLDataBase(path)


class Aplication:
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
        self.plus_input = None
        self.minus_input = None

        self.names_categories = []
        self.data_base = {}

        self.selected_period = 'week'
        self.categories = ["Все", "Инвестиции", "Здоровье", "Аренда"]

        self.categories = [x['name'] for x in conn.selectExpCat()]
        # выгрузить категории из бд

        self.current_category = StringVar()
        self.current_category.set(self.categories[0])

        self.current_date = datetime.datetime.today()

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

        plus_sv = StringVar()
        plus_sv.trace("w", lambda name, index, mode, sv=plus_sv: self.OnValueChanged())
        self.plus_input = Entry(self.bottom_frame, textvariable=plus_sv, background='#DAFDBA')
        self.plus_input.place(relx=0.3, rely=0.55)

        minus_sv = StringVar()
        minus_sv.trace("w", lambda name, index, mode, sv=minus_sv: self.OnValueChanged())
        self.minus_input = Entry(self.bottom_frame, textvariable=minus_sv, background='#DAFDBA')
        self.minus_input.place(relx=0.6, rely=0.55)

    def OpenCategoriesWindow(self):
        # ///////////////////////////// обновлять график другой категории
        self.priceLine = None
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

        Button(categories_frame, text="+", command=self.OpenAddCategoryWindow).pack(pady=10)
        for category in self.categories:
            Button(categories_frame, text=category, command=lambda x=category: self.ChangeCategory(x)).pack(
                pady=10, padx=100)

        categories_canvas.update_idletasks()
        categories_canvas.configure(scrollregion=categories_canvas.bbox("all"))

    def ChangeCategory(self, category):
        global categories_window
        self.current_category.set(category)
        self.RenderBottom()
        self.categories_window.destroy()
        self.selected_button()

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
        Button(categories_frame, text=category, command=lambda x=category: self.ChangeCategory(x)).pack(
            pady=10, padx=100)
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
        self.SaveRecord()
        #
        self.current_date = datetime.datetime.strptime(self.calendar.get_date(), '%m/%d/%y')  # дата измен
        self.calendar_window.destroy()
        self.selected_button()
        # [done]запись в БД прошлого дня, если ячейки пустые null?
        self.RenderBottom()

    def SaveRecord(self):  # ++сохранение записи при изменении даты, !!!!!!!!!!!!!!!!выход из приложения - обработать
        try:
            float(self.minus_input.get())
            float(self.plus_input.get())
        except ValueError:
            pass  # print("Не число")
        else:
            _expId = conn.findExpCatId(self.current_category.get())
            conn.addExpense(_expId, self.current_date, float(self.minus_input.get()))
            conn.addIncome(_expId, self.current_date, float(self.plus_input.get()))  # +incomecat

    def ChangeCurDate(self, days=0):
        global current_date
        self.SaveRecord()
        self.current_date += datetime.timedelta(days=days)
        # self.plus_input.delete(0, END)
        # self.minus_input.delete(0, END)
        self.selected_button()
        # [done]запись в БД прошлого дня, если ячейки пустые null?

        self.RenderBottom()

    def OnValueChanged(self):

        value = 0
        try:
            value += int(self.plus_input.get())  # пришел доход
            print(int(self.plus_input.get()))

        except ValueError:
            pass

        try:
            value -= int(self.minus_input.get())  # пришел расход
            print(int(self.minus_input.get()))
        except ValueError:
            pass

        #  где то тут при стирании значения, данные лишний раз сохраняются

        if (self.current_date.strftime("%d %B %Y") in self.data_base.keys()):

            print("value = ", value)

            value += self.data_base[self.current_date.strftime("%d %B %Y")]
            self.data_base[self.current_date.strftime("%d %B %Y")] = value

            print("В базу данных добавлено значение " + str(value) + " для даты " + self.current_date.strftime(
                "%d %B %Y"))

            print("db[date] = ", self.data_base[self.current_date.strftime("%d %B %Y")])
        else:
            # value += self.data_base[self.current_date.strftime("%d %B %Y")]

            self.data_base.update({self.current_date.strftime("%d %B %Y"): value})
            print("внесено значение " + str(value) + " для даты " + self.current_date.strftime("%d %B %Y"))

        # value = 0

        self.selected_button()

    def selected_button(self):
        i_dict = {
            "week": 0,
            "month": 1,
            "year": 2,
            "all time": 3
        }
        self.selected_period = i_dict.get(self.selected_period, 0)
        self.render_lines()
        self.canvas.draw()

    def render_lines(self):
        self.ax.clear()
        self.ax.grid()
        self.priceLine = []
        self.timeLine = []
        self.length = []
        maxMarks = None
        print(self.selected_period)
        if self.selected_period == 0:  # week
            maxMarks = 7
            self.start = self.current_date - datetime.timedelta(
                days=self.current_date.weekday())  # Начинаем с понедельника
            self.timeLine = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        elif self.selected_period == 1:  # month
            maxMarks = monthrange(self.current_date.year, self.current_date.month)[1]  # сколько дней в месяце
            self.start = datetime.datetime(self.current_date.year, self.current_date.month, 1)  # Начинаем с 1 числа
            self.timeLine = [str(i + 1) for i in range(maxMarks)]

        elif self.selected_period == 2:  # year
            maxMarks = 12
            self.start = self.current_date - datetime.timedelta(
                days=self.current_date.weekday())  # datetime.datetime(self.current_date.year, 1, 1)
            self.timeLine = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec']

        elif self.selected_period == 3:  # all time
            maxMarks = len(self.priceLine)
            self.start = datetime.datetime(self.current_date.year, self.current_date.month, 1)
            self.timeLine = [str(i + 1) for i in range(maxMarks)]

        for i in range(maxMarks):
            self.priceLine = mp.np.append(self.priceLine,
                                          self.data_base.get(
                                              (self.start + datetime.timedelta(days=i)).strftime("%d %B %Y"), 0))
        print(self.priceLine, '\n')
        # ???

        maxMarks = 15
        if self.selected_period == 3:
            self.ax.xaxis.set_major_locator(mp.MaxNLocator(maxMarks))
        self.ax.yaxis.set_major_locator(mp.MaxNLocator(maxMarks))

        for j in range(len(self.priceLine)):
            self.length = mp.np.append(self.length, j)

        # maybe these string should be below
        z = mp.np.polyfit(self.length, self.priceLine, 1)
        p = mp.np.poly1d(z)

        # $(t) and trend line

        ##self.ax.plot(conn.sumExpenseByDays().fetchall(),
        # выгрузить на график

        self.ax.plot(self.timeLine, self.priceLine, label=self.current_category.get(), color="#45C4B0", marker=".",
                     linestyle="-")
        self.ax.plot(self.timeLine, p(self.length), label='trend line', color="y", linestyle=":")
        self.ax.legend(loc='lower center')

    # визуализация графика
    def RenderGraph(self):
        self.figure = mp.Figure(figsize=(15, 1), dpi=130, facecolor="#45C4B0")
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.canvas = FigureCanvasTkAgg(self.figure, self.main_window)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        self.ax_dop = self.figure.add_subplot(3, 7, 7)
        self.radio_buttons = RadioButtons(self.ax_dop, ['week', 'month', 'year', 'all time'], 0, activecolor='black')
        self.radio_buttons.on_clicked(self.selected_button)

        self.ax_dop1 = self.figure.add_subplot(6, 20, 1)
        self.help_bot = mp.Button(self.ax_dop1, "?")
        self.help_bot.on_clicked(lambda x: self.open_image())
        self.help_bot.hovercolor = "grey"

        # Button(self.bottom_frame, text="?", command=lambda: self.open_image1).place(x=0, y=0)

        self.selected_button()

    def open_image(self):
        image = Image.open("11.png")
        image = image.resize((380, 290))
        # text_img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
        # text_img.paste(image, (200, 100), mask=image)
        image = ImageTk.PhotoImage(image)

        label = Label(self.main_window, image=image)
        label.image_names = image
        label.place(relx=1.0, rely=1.0, anchor='se')
        label.bind("<Button-1>", lambda event: label.destroy())


apl = Aplication()

apl.RenderGraph()
apl.RenderBottom()

apl.main_window.mainloop()
