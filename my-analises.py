import datetime

from matplotlib.pyplot import *
from tkinter import *
# from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import Calendar

# matplotlib.use("TkAgg")


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
graph_width = 640
graph_height = 240
graph_line_width = 2

# Глобальные переменные
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


def cm_to_inch(value):
    return value / 2.54


# визуализация графика
def RenderGraph():
    value = [4, 5, 2, 6, 8, 2, 1]
    days = ['mon', 'tue', 'wed', 'thur', 'frid', 'sut', 'sun']

    sum_x = (1 + 7) * len(days) / 2
    sr_x = sum_x / 7
    sr_xx = sr_x ** 2

    sum_y = sum(value)
    sr_y = sum_y / len(value)

    sum_xy, sum_xx = 0, 0
    trend_line = []

    for i in range(0, len(value)):
        sum_xx += value[i] ** 2
        sum_xy += value[i] * i + 1

    b = (sum_xy - len(value) * sr_x * sr_y) / (sum_xx - len(value) * sr_xx)
    a = sr_y - b * sr_x
    for i in range(0, len(value)):
        trend_line.append(a + b * (i + 1))

    figure = Figure(figsize=(cm_to_inch(25), cm_to_inch(4)), dpi=130, facecolor="#45C4B0")
    plot = figure.add_subplot(1, 1, 1)
    plot.grid()

    plot.plot(days, value, color="#45C4B0", marker=".", linestyle="-")
    plot.plot(trend_line, color="y", marker="o", linestyle=":")

    canv = FigureCanvasTkAgg(figure, main_window)
    canv.get_tk_widget().grid(row=0, column=0, sticky='nsew')


RenderBottom()
RenderGraph()

main_window.mainloop()
