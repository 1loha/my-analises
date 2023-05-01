import datetime
import os
from tkinter import *
from tkcalendar import Calendar

from SQLData import SQLDataBase
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as mp

#
path = os.getcwd() + r"\tables.db"
conn = SQLDataBase(path)

# Инициализация окна
main_window = Tk()
main_window.title('Cash App')
main_window.geometry('1280x720')
main_window.minsize(800, 600)
main_window.maxsize(1920, 1080)
main_window.columnconfigure(0, weight=1)
main_window.rowconfigure(0, weight=1)
main_window.columnconfigure(1, weight=1)
main_window.rowconfigure(1, weight=1)

# Настройки
graphWidth = 640
graphHeight = 240
graphLineWidth = 2

## Глобальные переменные
сategories = []
plus_inputs = []
minus_inputs = []
current_date = datetime.datetime.today()

# рамки, сейчас они просто в оперативке
graph_frame = Frame(main_window, background='#FFFFFF')
bottom_frame = Frame(main_window, background='#DAFDBA')

# Настройка строк и столбцов в нижней половине
for i in range(4):
    bottom_frame.rowconfigure(i, weight=1)
for i in range(6):
    bottom_frame.columnconfigure(i, weight=1)

# фиксируем их на плоскость с помощью упаковщиков
graph_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")


# дизайн нижней части окна
def RenderBottom():
    Button(bottom_frame, text="<---", command=lambda: ChangeCurDate(days=-1)).grid(row=0, column=1)
    Label(bottom_frame, text=current_date.strftime("%d %B %Y")).grid(row=0, column=2)
    Button(bottom_frame, text="Render Graph", command=RenderGraph).grid(row=0, column=3)
    Button(bottom_frame, text="Выбрать дату", command=OpenCalendar).grid(row=0, column=4)
    Button(bottom_frame, text="--->", command=lambda: ChangeCurDate(days=1)).grid(row=0, column=5)

    Label(bottom_frame, text="Категории").grid(row=1, column=0)
    Label(bottom_frame, text="Доход").grid(row=2, column=0)
    Label(bottom_frame, text="Расход").grid(row=3, column=0)

    for i in range(5):
        сategories.append(Entry(bottom_frame))
        сategories[i].grid(row=1, column=i + 1)

        plus_inputs.append(Entry(bottom_frame))
        plus_inputs[i].grid(row=2, column=i + 1)

        minus_inputs.append(Entry(bottom_frame))
        minus_inputs[i].grid(row=3, column=i + 1)


def OpenCalendar():
    global calendar_window
    calendar_window = Toplevel()
    calendar_window.grab_set()
    calendar_window.title("Input date")
    calendar_window.geometry("300x300")
    calendar_window.resizable(False, False)
    global calendar
    calendar = Calendar(calendar_window, selectmode='day',
                        year=current_date.year, month=current_date.month,
                        day=current_date.day)
    calendar.pack(pady=20)

    Button(calendar_window, text="Ok",
           command=SelectDate).pack(pady=20)


def SelectDate():
    global current_date
    global calendar_window
    current_date = datetime.datetime.strptime(calendar.get_date(), '%m/%d/%y')
    calendar_window.destroy()
    RenderBottom()


def ChangeCurDate(days=0):
    global current_date
    current_date += datetime.timedelta(days=days)
    RenderBottom()


def choose_date(clicks):
    return [7, 10, 20]


def on_button_click():
    print('Button clicked')


def create_buttons(figure):
    coordinates = [[0 for j in range(4)] for h in range(4)]
    button_ax = [0 for p in range(4)]
    button = [0 for q in range(4)]
    x, y, w, h = 0.91, 0.18, 0.08, 0.1

    # кнопки для смены периода
    for butt in range(4):
        coordinates[butt] = [x, y * (butt + 1), w, h]

    times = ['anywhere', 'year', 'month', 'week']

    for i in range(len(coordinates)):
        button_ax[i] = figure.add_axes(coordinates[i])
        button[i] = mp.Button(button_ax[i], times[i])

    # button[0].on_clicked(on_button_click)
    return button


# визуализация графика
def RenderGraph():
    figure = mp.Figure(figsize=(15, 1), dpi=130, facecolor="#45C4B0")
    ax = figure.add_subplot(1, 1, 1)
    ax.grid()

    # аля считывание с бд
    cost = mp.np.array([154, 19, 13, 11, 14, 8, 6])
    days = mp.np.array([1, 2, 3, 4, 5, 6, 7])

    # $(t)
    ax.plot(days, cost, label='cost', color="#45C4B0", marker=".", linestyle="-")

    # trend line
    z = mp.np.polyfit(days, cost, 1)
    p = mp.np.poly1d(z)
    ax.plot(days, p(days), label='trend line', color="y", linestyle=":")

    # lines name
    ax.legend(loc='lower center')

    clicks = create_buttons(figure)

    # количество отметок на осях
    choose = choose_date(clicks)

    ax.yaxis.set_major_locator(mp.LinearLocator(5))
    ax.xaxis.set_major_locator(mp.LinearLocator(10))

    canv = FigureCanvasTkAgg(figure, main_window)
    canv.get_tk_widget().grid(row=0, column=0, sticky='nsew')

RenderBottom()
RenderGraph()
# Button(valuesFrame, "+", AddValue).grid(column=37, row=40)

main_window.mainloop()
