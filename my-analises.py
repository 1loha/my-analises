import datetime
import os
from tkinter import *
from tkinter import ttk

from SQLData import SQLDataBase
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import *

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

# Глобальные переменные
graphValues = []
valuesNumber = 1

buttonsArray = []
date = "1"
month_value = "January"


# дизайн нижней части окна
def RenderBottom():
    today = datetime.datetime.today()
    for i in range(5):
        valueLabel = Label(valuesFrame, text=(today + datetime.timedelta(days=i)).strftime("%d %B"))
        graphValues.append(Entry(valuesFrame))

        valueLabel.grid(row=0, column=i, sticky="w", padx=10, pady=10)
        graphValues[i].grid(row=1, column=i, sticky="e", padx=10, pady=10)

    # Button(valuesFrame, text="Render Graph", command=RenderGraph).grid()


# визуализация графика
def RenderGraph():
    value_y = np.array([15, 19, 13, 11, 14, 8, 6])
    value_x = np.array([1, 2, 3, 4, 5, 6, 7])
    # for i in range(0, len(value)):
    #     sum_time = (1 + 7) * len(days) / 2
    #     sr_x = sum_time / 7
    #     sr_xx = sr_x ** 2
    #
    #     sum_y = sum(value)
    #     sr_y = sum_y / len(value)
    #
    #     for j in range(0, len(value)):
    #         sum_xx += value[j] ** 2
    #         sum_xy += value[j] * j+1
    #
    #     b = (sum_xy - len(value) * sr_x * sr_y) / (sum_xx - len(value) * sr_xx)
    #     a = sr_y - b * sr_x
    #
    #     res = a + b * (i + 1)
    #     trend_line.append(res)

    figure = Figure(figsize=(15, 1), dpi=130, facecolor="#45C4B0")
    ax = figure.add_subplot(1, 1, 1)
    ax.grid()

    # $(t)
    ax.plot(value_x, value_y, label='cost', color="#45C4B0", marker=".", linestyle="-")

    # trend line
    z = np.polyfit(value_x, value_y, 1)
    p = np.poly1d(z)
    ax.plot(value_x, p(value_x), label='trend line', color="y", linestyle=":")


    ax.legend(loc = 'lower center')

    #
    # количество отметок на осях
    # plot.yaxis.set_major_locator(LinearLocator(5))
    # plot.set_yscale('symlog', linthresh=10)
    canv = FigureCanvasTkAgg(figure, main_window)
    canv.get_tk_widget().grid(row=0, column=0, sticky='nsew')






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
graphFrame.grid(row=0, column=0, columnspan=2, sticky="nsew")
valuesFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")

RenderBottom()
RenderGraph()
Button(valuesFrame, text="+", command=AddValue).grid(column=37, row=40)

main_window.mainloop()
