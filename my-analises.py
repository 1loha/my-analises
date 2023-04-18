import datetime
from tkinter import *

# Инициализация окна
window = Tk()

window.title('Cash App')
window.geometry('800x500')
window.minsize(800, 500)

# window.maxsize(1200, 750)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(1, weight=1)

# Настройки
graphWidth = 800 #window.winfo_width()
graphHeight = 180 #window.winfo_height()
graphLineWidth = 2

# Глобальные переменные
graphValues = []
valuesNumber = 5


# дизайн нижней части окна
def RenderBottom():
    today = datetime.datetime.today()
    firstDay = today.day
    #firstDay = datetime.datetime()
    for i in range(5):
        dateLabel = Label(tableFrame, text=(today + datetime.timedelta(days=i)).strftime("%d %B"))
        graphValues.append(Entry(tableFrame))

        dateLabel.grid(row=0, column=i, sticky="w", padx=10, pady=10)
        graphValues[i].grid(row=1, column=i, sticky="e", padx=10, pady=10)

    Button(tableFrame, text="Render Graph", command=RenderGraph).grid()


# визуализация графика
def RenderGraph():
    canv = Canvas(graphFrame, width=800, height=250, bg="#ADFF2F")
    canv.place(relx=0, rely=0, anchor="nw")

    pad_x = 20
    pad_y = 20

    # ось абсцисс
    canv.create_line(pad_x, graphHeight, graphWidth, graphHeight, width=graphLineWidth, arrow=LAST)
    # ось ординат
    canv.create_line(pad_x, graphHeight, pad_x, 0, width=graphLineWidth, arrow=LAST)
    # аля данные с таблицы
    value = [1, 5, 2, 3, 4, 4, 8, 2]

    ordinate = graphHeight
    ordinate_step = ordinate // len(value)
    abscissa = graphWidth
    abscissa_step = abscissa // len(value)

    # отметки растянутые на ось y
    for i in range(graphHeight, pad_y, -ordinate_step):
        startLine1 = pad_x - 5
        startLine2 = pad_x + 5
        end1, end2 = ordinate, ordinate
        canv.create_line(startLine1, end1 - i, startLine2, end2 - i, width=1)

    # отметки растянутые на ось x
    # пока с косяком
    for i in range(pad_x, graphWidth, abscissa_step):
        startLine01, startLine02 = pad_x*2, pad_x*2
        end01 = graphHeight + 5
        end02 = graphHeight - 5
        canv.create_line(startLine01 + i, end01, startLine02 + i, end02, width=1)


    # Просчет графика
    # for i in range(valuesNumber-1):
    #     firstValue = graphValues[i].get()
    #     secondValue = graphValues[i+1].get()
    #
    #     if(firstValue != '' and secondValue!=''):
    #         canv.create_text(graphWidth / valuesNumber * i, graphHeight / 2 + 20, text="13 April", fill="#45C4B0",
    #                          font=("Helvectica", "10"))
    #         canv.create_line(graphWidth / valuesNumber * i, graphHeight/2-int(firstValue), graphWidth / valuesNumber * (i+1),  graphHeight/2-int(secondValue),
    #                      width=graphLineWidth)

# рамки, сейчас они просто в оперативке
#notesFrame = Frame(window, background='#45C4B0')
graphFrame = Frame(window, background='#ADFF2F')
tableFrame = Frame(window, background='#1AFFD2')

# фиксируем их на плоскость с помощью упаковщиков
# pack()-установка по пикселям
# grid()-установка на таблице
# place()-установка по координатам
#notesFrame.grid(row=0, column=0, sticky="nsew")
graphFrame.grid(columnspan=2, sticky="nsew")
tableFrame.grid(columnspan=2, sticky="nsew")

RenderBottom()
RenderGraph()

window.mainloop()
