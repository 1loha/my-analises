import datetime
import os
from tkinter import *
<<<<<<< HEAD
from tkinter import ttk

from SQLData import SQLDataBase
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import *

#
path = os.getcwd() + r"\tables.db"
conn = SQLDataBase(path)
=======
# from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import Calendar

# matplotlib.use("TkAgg")

>>>>>>> b96a6692629f3c66174ed9969e49f31c1fa3451e

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

<<<<<<< HEAD
    # Button(valuesFrame, "Render Graph", RenderGraph).grid()

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
        coordinates[butt] = [x, y*(butt+1), w, h]

    times = ['anywhere', 'year', 'month', 'week']

    for i in range(len(coordinates)):
        button_ax[i] = figure.add_axes(coordinates[i])
        button[i] = Button(button_ax[i], times[i])

    # button[0].on_clicked(on_button_click)
    return button
=======

def cm_to_inch(value):
    return value / 2.54

>>>>>>> b96a6692629f3c66174ed9969e49f31c1fa3451e

# визуализация графика
def RenderGraph():
    figure = Figure(figsize=(15, 1), dpi=130, facecolor="#45C4B0")
    ax = figure.add_subplot(1, 1, 1)
    ax.grid()

    # аля считывание с бд
    cost = np.array([15, 19, 13, 11, 14, 8, 6])
    days = np.array([1, 2, 3, 4, 5, 6, 7])

    # $(t)
    ax.plot(days, cost, label='cost', color="#45C4B0", marker=".", linestyle="-")

    # trend line
    z = np.polyfit(days, cost, 1)
    p = np.poly1d(z)
    ax.plot(days, p(days), label='trend line', color="y", linestyle=":")

<<<<<<< HEAD
    # lines name
    ax.legend(loc='lower center')
=======
    for i in range(0, len(value)):
        sum_xx += value[i] ** 2
        sum_xy += value[i] * i + 1
>>>>>>> b96a6692629f3c66174ed9969e49f31c1fa3451e


    clicks = create_buttons(figure)

<<<<<<< HEAD


    # количество отметок на осях
    choose = choose_date(clicks)
=======
    figure = Figure(figsize=(cm_to_inch(25), cm_to_inch(4)), dpi=130, facecolor="#45C4B0")
    plot = figure.add_subplot(1, 1, 1)
    plot.grid()
>>>>>>> b96a6692629f3c66174ed9969e49f31c1fa3451e

    ax.yaxis.set_major_locator(LinearLocator(5))
    ax.xaxis.set_major_locator(LinearLocator(10))

    canv = FigureCanvasTkAgg(figure, main_window)
    canv.get_tk_widget().grid(row=0, column=0, sticky='nsew')


<<<<<<< HEAD




def click_date_button(value):
    global date
    date = str(value)
    current_date.config(text="Selected date: " + date + " " + month_value)

def check(event):
    i = 0
    value = 1
    day = 1
    global date
    for button in buttonsArray:
        button.grid_forget()
    # buttonsArray.clear()
    global month_value
    month_value = event.widget.get()
    if month_value in ["January", "March", "May", "July", "August", "October", "December"]:
        for r in range(3, 6):
            for col in range(10):
                value_button = ttk.Button(add_value_window, text=f"{value}", width=23, command=lambda c=day: click_date_button(c))
                value += 1
                buttonsArray.append(value_button)
                value_button.grid(row=r, column=col, rowspan=1, columnspan=1)
                i = r
                day += 1
        value_button = ttk.Button(add_value_window, text=f"{value}", width=23,command=lambda c=day: click_date_button(c))
        value += 1
        value_button.grid(row=i + 1, column=0, rowspan=1, columnspan=1)
        buttonsArray.append(value_button)
    elif month_value in ["April", "June", "September", "November"]:
        if int(date) > 30:
            date = str(30)
        for r in range(3, 6):
            for col in range(10):
                value_button = ttk.Button(add_value_window, text=f"{value}", width=23, command=lambda c=day: click_date_button(c))
                value += 1
                buttonsArray.append(value_button)
                value_button.grid(row=r, column=col, rowspan=1, columnspan=1)
                day += 1
    else:
        if int(date) > 28:
            date = str(28)
        for r in range(3, 5):
            for col in range(10):
                value_button = ttk.Button(add_value_window, text=f"{value}", width=23, command=lambda c=day: click_date_button(c))
                value += 1
                buttonsArray.append(value_button)
                value_button.grid(row=r, column=col, rowspan=1, columnspan=1)
                day += 1
        for r in range(5,6):
            for col in range(8):
                value_button = ttk.Button(add_value_window, text=f"{value}", width=23, command=lambda c=day: click_date_button(c))
                value += 1
                buttonsArray.append(value_button)
                value_button.grid(row=r, column=col, rowspan=1, columnspan=1)
                day += 1
    current_date.config(text="Selected date: " + date + " " + month_value)




def ClickAddValue():
    global add_value_window
    add_value_window = Toplevel()
    add_value_window.grab_set()
    add_value_window.title("Input date")
    add_value_window.geometry("300x300")
    add_value_window.resizable(False, False)
    day = 1
    for c in range(16):
        add_value_window.columnconfigure(index=c, weight=1)
    for r in range(16):
        add_value_window.rowconfigure(index=r, weight=1)
    label = Label(add_value_window, text="Choose month")
    label.grid(column=3, row=0, rowspan=1, columnspan=4)
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    months_var = StringVar(value=months[0])
    select_month = ttk.Combobox(add_value_window, textvariable=months_var, values=months, state="readonly",
                                justify=CENTER,
                                height=5, width=33)
    select_month.bind("<<ComboboxSelected>>", lambda e: add_value_window.focus())
    select_month.grid(column=3, row=1, rowspan=1, columnspan=4)
    value = 1
    i = 0
    for r in range(3, 6):
        for col in range(10):
            value_button = ttk.Button(add_value_window, text=f"{value}", width=23, command=lambda c=day: click_date_button(c))
            value += 1
            buttonsArray.append(value_button)
            value_button.grid(row=r, column=col, rowspan=1, columnspan=1)
            i = r
            day += 1
    value_button = ttk.Button(add_value_window, text=f"{value}", width=23, command=lambda c=day: click_date_button(c))
    value_button.grid(row=i+1, column=0, rowspan=1, columnspan=1)
    number = date
    buttonsArray.append(value_button)
    select_month.bind("<<ComboboxSelected>>", check)
    confirm_button = ttk.Button(add_value_window, text="Ok", width=33, command=lambda: add_value_window.destroy())
    confirm_button.grid(row=10, column=4, rowspan=1, columnspan=2)
    global current_date
    current_date = Label(add_value_window, text="Selected date: " + number + " " + month_value)
    current_date.grid(column=2, row=7, rowspan=1, columnspan=6)
    add_value_window.mainloop()
    return current_date


# рамки, сейчас они просто в оперативке
graphFrame = Frame(main_window, background='#FFFFFF')
valuesFrame = Frame(main_window, background='#DAFDBA')


def AddValue():
    ClickAddValue()
    value = current_date
    valueLabel = Label(valuesFrame, text=value)
    graphValues.append(Entry(valuesFrame))

    valueLabel.grid(row=0, column=6, sticky="w", padx=10, pady=10)
    graphValues[len(graphValues)].grid(row=1, column=len(graphValues), sticky="e", padx=10, pady=10)


# фиксируем их на плоскость с помощью упаковщиков
# graphFrame.grid(row=0, column=0, columnspan=2, sticky="nsew")
valuesFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")

RenderBottom()
RenderGraph()
# Button(valuesFrame, "+", AddValue).grid(column=37, row=40)
=======
RenderBottom()
RenderGraph()
>>>>>>> b96a6692629f3c66174ed9969e49f31c1fa3451e

main_window.mainloop()
