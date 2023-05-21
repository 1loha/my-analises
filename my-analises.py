import os
import datetime
import matplotlib.pyplot as mp

from tkinter import *
from SQLData import SQLDataBase
from tkcalendar import Calendar
from matplotlib.widgets import RadioButtons
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        self.categories = []
        self.names_categories = []

        self.plus_inputs = []
        self.minus_inputs = []

        self.current_date = datetime.datetime.today()

        for i in range(4):
            self.bottom_frame.rowconfigure(i, weight=1)
        for i in range(6):
            self.bottom_frame.columnconfigure(i, weight=1)

    # дизайн нижней части окна
    def RenderBottom(self):
        Button(self.bottom_frame, text="<---", command=lambda: self.ChangeCurDate(days=-1)).grid(row=0, column=1)
        Label(self.bottom_frame, text=self.current_date.strftime("%d %B %Y")).grid(row=0, column=2)
        # Button(bottom_frame, text="Render Graph", command=RenderGraph).grid(row=0, column=3)
        Button(self.bottom_frame, text="Выбрать дату", command=self.OpenCalendar).grid(row=0, column=4)
        Button(self.bottom_frame, text="--->", command=lambda: self.ChangeCurDate(days=1)).grid(row=0, column=5)

        Label(self.bottom_frame, text="Категории").grid(row=1, column=0)
        Label(self.bottom_frame, text="Доход").grid(row=2, column=0)
        Label(self.bottom_frame, text="Расход").grid(row=3, column=0)

        for i in range(5):
            self.categories.append(Entry(self.bottom_frame))
            self.categories[i].grid(row=1, column=i + 1)

            self.plus_inputs.append(Entry(self.bottom_frame))
            self.plus_inputs[i].grid(row=2, column=i + 1)

            self.minus_inputs.append(Entry(self.bottom_frame))
            self.minus_inputs[i].grid(row=3, column=i + 1)

    def OpenCalendar(self):
        global calendar_window
        self.calendar_window = Toplevel()
        self.calendar_window.grab_set()
        self.calendar_window.title("Input date")
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
        self.RenderBottom()

    def ChangeCurDate(self, days=0):
        global current_date
        self.current_date += datetime.timedelta(days=days)
        self.RenderBottom()

    def selected_button(self, label):
        i_dict = {
            "week": 0,
            "month": 1,
            "year": 2,
            "all time": 3
        }
        i = i_dict.get(label, 0)
        self.render_lines(i)
        self.canvas.draw()

    def render_lines(self, i):
        self.ax.clear()
        self.ax.grid()
        self.priceLine = []
        self.timeLine = []
        self.length = []
        maxMarks = None

        if i == 0:  # week
            maxMarks = 7

            for p_i in self.plus_inputs:  # values on price axis
                self.priceLine = mp.np.append(self.priceLine, int(p_i.get()))
            self.timeLine = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        elif i == 1:  # month
            maxMarks = 10

            for p_i in self.plus_inputs:  # values on price axis
                self.priceLine = mp.np.append(self.priceLine, int(p_i.get()))
            self.timeLine = ['first week', 'second week', 'third week', 'last week']

        elif i == 2:  # year
            maxMarks = 12

            for p_i in self.plus_inputs:  # values on price axis
                self.priceLine = mp.np.append(self.priceLine, int(p_i.get()))
            self.timeLine = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec']

        elif i == 3:  # all time
            maxMarks = 15

            for p_i in self.plus_inputs:  # values on price axis
                self.priceLine = mp.np.append(self.priceLine, int(p_i.get()))
            self.timeLine = ['first quarter', 'second quarter', 'third quarter', 'last quarter']

        lenX = len(self.priceLine)
        lenY = len(self.timeLine)
        # newPriceLine = [0]*lenY
        # indexStep = lenX // lenY
        # out = 0

        # must not be more than maxMarks
        if lenX >= lenY:
            newIndexes = mp.np.linspace(0, lenX - 1, lenY)

            # Вычисляем новый массив с использованием пропорциональной интерполяции
            newPriceLine = mp.np.interp(newIndexes, mp.np.arange(lenX), self.priceLine)

            # newPriceLine = mp.np.round(newPriceLine, 0)
            # print(newPriceLine)
            # print(sum(newPriceLine))

            # Масштабируем новый массив, чтобы сохранить сумму
            newPriceLine *= self.priceLine.sum() / newPriceLine.sum()

            # newPriceLine = mp.np.round(newPriceLine, 0)
            # print(newPriceLine)
            # print(sum(newPriceLine))

            self.priceLine = newPriceLine  # copy a new array in priceLine
        else:
            self.timeLine = []
            for k in range(1, lenX + 1):  # length of timeline selected dynamically
                self.timeLine = mp.np.append(self.timeLine, f'{k}/{lenX}')
            self.ax.xaxis.set_major_locator(mp.MaxNLocator(lenX))
        self.ax.yaxis.set_major_locator(mp.MaxNLocator(maxMarks))

        for j in range(len(self.priceLine)):
            self.length = mp.np.append(self.length, j)

        print(type(self.length), " - ", self.length)
        print(type(self.priceLine), " - ", self.priceLine)
        print(type(self.timeLine), " - ", self.timeLine)
        # maybe these string should be below
        z = mp.np.polyfit(self.length, self.priceLine, 1)
        p = mp.np.poly1d(z)

        if lenX > lenY:
            pass  # self.priceLine = self.priceLine[:lenY]
        else:
            # self.priceLine = mp.np.append(self.priceLine, [None] * (len(self.timeLine) - len(self.priceLine)))
            self.timeLine = self.timeLine[:lenX]

        # Removes duplicate legends
        if self.executed:
            self.ax.plot(self.timeLine, self.priceLine, label='cost', color="#45C4B0", marker=".", linestyle="-")
            self.ax.plot(self.timeLine, p(self.length), label='trend line', color="y", linestyle=":")
            self.ax.legend(loc='lower center')
            self.executed = False
            return

        # $(t) and trend line
        self.ax.plot(self.timeLine, self.priceLine, color="#45C4B0", marker=".", linestyle="-")
        self.ax.plot(self.timeLine, p(self.length), color="y", linestyle=":")

    # визуализация графика
    def RenderGraph(self):
        self.figure = mp.Figure(figsize=(15, 1), dpi=130, facecolor="#45C4B0")
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.canvas = FigureCanvasTkAgg(self.figure, self.main_window)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        self.ax_dop = self.figure.add_subplot(3, 7, 7)
        self.radio_buttons = RadioButtons(self.ax_dop, ['week', 'month', 'year', 'all time'], 0, activecolor='black')
        self.radio_buttons.on_clicked(self.selected_button)


apl = Aplication()
apl.RenderGraph()
apl.RenderBottom()

apl.main_window.mainloop()
