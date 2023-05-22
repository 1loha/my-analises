import os
import datetime
import matplotlib.pyplot as mp

from tkinter import *
from SQLData import SQLDataBase
from tkcalendar import Calendar
from matplotlib.widgets import RadioButtons
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from calendar import monthrange

path = os.getcwd() + r"\tables.db"
conn = SQLDataBase(path)


class Aplication:
    # Инициализация окна
    def __init__(self):
        self.main_window = Tk()
        self.main_window.title('Cash App')
        self.main_window.geometry('1280x720')
        self.main_window.minsize(800, 600)
        self.main_window.maxsize(1920, 1080)
        [self.main_window.columnconfigure(i, weight=1) for i in range(2)]
        [self.main_window.rowconfigure(i, weight=1) for i in range(2)]

        self.graph_frame = Frame(self.main_window, background='#FFFFFF')
        self.graph_frame.grid(row=0, column=0, sticky="nsew")

        self.bottom_frame = Frame(self.main_window, background='#DAFDBA')
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
        self.selected_period = 'week'
        self.data_base = {}

        self.names_categories = []

        self.plus_input = None
        self.minus_input = None
        self.categories = ["Все", "Инвестиции", "Здоровье", "Аренда"]
        self.current_category = StringVar()
        self.current_category.set(self.categories[0])


        self.current_date = datetime.datetime.today()

        for i in range(4):
            self.bottom_frame.rowconfigure(i, weight=1)
        for i in range(6):
            self.bottom_frame.columnconfigure(i, weight=1)

    # дизайн нижней части окна
    def RenderBottom(self):
        Label(self.bottom_frame, textvariable=self.current_category).grid(row=0, column=2)

        Button(self.bottom_frame, text="Выбрать дату", command=self.OpenCalendar).grid(row=1, column=0)
        Button(self.bottom_frame, text="<---", command=lambda: self.ChangeCurDate(days=-1)).grid(row=1, column=1)
        Label(self.bottom_frame, text=self.current_date.strftime("%d %B %Y")).grid(row=1, column=2)
        Button(self.bottom_frame, text="--->", command=lambda: self.ChangeCurDate(days=1)).grid(row=1, column=3)

        Label(self.bottom_frame, text="Доход").grid(row=2, column=0)
        Label(self.bottom_frame, text="Расход").grid(row=2, column=2)

        plus_sv = StringVar()
        plus_sv.trace("w", lambda name, index, mode, sv=plus_sv: self.OnValueChanged())
        self.plus_input = Entry(self.bottom_frame, textvariable=plus_sv)
        self.plus_input.grid(row=2, column=1)

        minus_sv = StringVar()
        minus_sv.trace("w", lambda name, index, mode, sv=minus_sv: self.OnValueChanged())
        self.minus_input = Entry(self.bottom_frame, textvariable=minus_sv)
        self.minus_input.grid(row=2, column=3)

        Button(self.bottom_frame, text="Сменить категорию", command=self.OpenCategoriesWindow).grid(row=2, column=4)

    def OpenCategoriesWindow(self):
        global categories_window
        self.categories_window = Toplevel()
        # self.categories_window.grab_set()
        self.categories_window.title("Выбор категории")
        self.categories_window.geometry("400x500")
        self.categories_window.resizable(False, False)

        scrollbar = Scrollbar(self.categories_window, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        for category in self.categories:
            Button(self.categories_window, text=category, command=lambda x=category: self.ChangeCategory(x)).pack(
                pady=10)

        Button(self.categories_window, text="+", command=self.OpenAddCategoryWindow).pack(pady=10)

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
        Button(self.add_categoty_window, text="Ok", command=lambda:self.AddCategory(new_category.get())).pack(pady=10)


    def AddCategory(self, category):
        global add_categoty_window
        self.categories.append(category)
        self.categories_window.destroy()
        self.add_categoty_window.destroy()
        self.OpenCategoriesWindow()


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
        self.current_date = datetime.datetime.strptime(self.calendar.get_date(), '%m/%d/%y')
        self.calendar_window.destroy()
        self.selected_button(self.selected_period)
        self.RenderBottom()

    def ChangeCurDate(self, days=0):
        global current_date
        self.current_date += datetime.timedelta(days=days)
        self.plus_input.delete(0, END)
        self.minus_input.delete(0, END)
        self.selected_button(self.selected_period)
        self.RenderBottom()

    def OnValueChanged(self):
        value = 0

        try:
            value += int(self.plus_input.get())
        except ValueError:
            print("Не число")

        try:
            value -= int(self.minus_input.get())
        except ValueError:
            print("Не число")

        if (self.current_date.strftime("%d %B %Y") in self.data_base.keys()):
            print("В базу данных добавлено значение " +
                  str(value) + " для даты " +
                  self.current_date.strftime("%d %B %Y"))
            self.data_base[self.current_date.strftime("%d %B %Y")] = value
        else:
            self.data_base.update({self.current_date.strftime("%d %B %Y"): value})
            print("В базу данных изменено значение " +
                  str(value) + " для даты " +
                  self.current_date.strftime("%d %B %Y"))

        self.selected_button(self.selected_period)

    def selected_button(self, label):
        i_dict = {
            "week": 0,
            "month": 1,
            # "year": 2,
            # "all time": 3
        }
        i = i_dict.get(label, 0)
        self.selected_period = label
        self.render_lines(i)
        self.canvas.draw()

    def render_lines(self, selected_period):
        self.ax.clear()
        self.ax.grid()
        self.priceLine = []
        self.timeLine = []
        self.length = []
        maxMarks = None

        if selected_period == 0:  # week
            maxMarks = 7
            self.start = self.current_date - datetime.timedelta(
                days=self.current_date.weekday())  # Начинаем с понедельника
            self.timeLine = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        elif selected_period == 1:  # month
            maxMarks = monthrange(self.current_date.year, self.current_date.month)[1]  # сколько дней в месяце
            self.start = datetime.datetime(self.current_date.year, self.current_date.month, 1)  # Начинаем с 1 числа
            self.timeLine = [str(i + 1) for i in range(maxMarks)]
        # elif selected_period == 2:  # year
        #     maxMarks = 12
        #     self.timeLine = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec']
        # elif selected_period == 3:  # all time
        #     maxMarks = 15
        #     start = datetime.datetime(self.current_date.year, self.current_date.month, 1)
        #     self.timeLine = ['first quarter', 'second quarter', 'third quarter', 'last quarter']

        for i in range(maxMarks):
            self.priceLine = mp.np.append(self.priceLine,
                                          self.data_base.get(
                                              (self.start + datetime.timedelta(days=i)).strftime("%d %B %Y"), 0))
        # lenX = len(self.priceLine)
        # lenY = len(self.timeLine)

        # if lenX < 2:
        #     return

        # must not be more than maxMarks
        # if lenX >= lenY:
        #     newIndexes = mp.np.linspace(0, lenX - 1, lenY)  # equal location of elements
        #     newPriceLine = mp.np.interp(newIndexes, mp.np.arange(lenX), self.priceLine)  # proportional interpolation
        #     print(self.priceLine)
        #     print(newPriceLine)
        #     newPriceLine *= self.priceLine.sum() / newPriceLine.sum()  # to return the lost value
        #     newPriceLine = mp.np.round(newPriceLine, 0)
        #     self.priceLine = newPriceLine  # copy a new array in priceLine
        # else:
        #     self.timeLine = []
        #     for k in range(1, lenX + 1):  # length of timeline selected dynamically
        #         self.timeLine = mp.np.append(self.timeLine, f'{k}/{lenX}')
        #     self.ax.xaxis.set_major_locator(mp.MaxNLocator(lenX))
        self.ax.yaxis.set_major_locator(mp.MaxNLocator(15))

        for j in range(len(self.priceLine)):
            self.length = mp.np.append(self.length, j)

        # maybe these string should be below
        z = mp.np.polyfit(self.length, self.priceLine, 1)
        p = mp.np.poly1d(z)

        # Removes duplicate legends
        # if self.executed:
        #     self.ax.plot(self.timeLine, self.priceLine, label='cost', color="#45C4B0", marker=".", linestyle="-")
        #     self.ax.plot(self.timeLine, p(self.length), label='trend line', color="y", linestyle=":")
        #     self.ax.legend(loc='lower center')
        #     self.executed = False
        #     return

        # $(t) and trend line
        self.ax.plot(self.timeLine, self.priceLine, label='cost', color="#45C4B0", marker=".", linestyle="-")
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


apl = Aplication()
apl.RenderGraph()
apl.RenderBottom()

apl.main_window.mainloop()
