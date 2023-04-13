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
graphWidth = 300
graphHeight = 200
graphLineWidth = 2

# Глобальные переменные
graphValues = []
valuesNumber = 5


# дизайн нижней части окна
def RenderBottom():
    today = datetime.datetime.today()
    for i in range(5):
        valueLabel = Label(valuesFrame, text=(today + datetime.timedelta(days=i)).strftime("%d %B"))
        graphValues.append(Entry(valuesFrame))

        valueLabel.grid(row=0, column=i, sticky="w", padx=10, pady=10)
        graphValues[i].grid(row=1, column=i, sticky="e", padx=10, pady=10)

    Button(valuesFrame, text="Render Graph", command=RenderGraph).grid()


# визуализация графика
def RenderGraph():
    canv = Canvas(graphFrame, width=graphWidth, height=graphHeight, bg="white")
    canv.place(relx=.5, rely=.5, anchor="center")

    # Оси координат
    canv.create_line(graphWidth / 2, graphHeight, graphWidth / 2, 0, width=graphLineWidth, arrow=LAST)
    canv.create_line(0, graphHeight / 2, graphWidth, graphHeight / 2, width=graphLineWidth, arrow=LAST)


    # Просчет графика
    for i in range(valuesNumber-1):
        firstValue = graphValues[i].get()
        secondValue = graphValues[i+1].get()

        if(firstValue != '' and secondValue!=''):
            canv.create_text(graphWidth / valuesNumber * i, graphHeight / 2 + 20, text="13 April", fill="#45C4B0",
                             font=("Helvectica", "10"))
            canv.create_line(graphWidth / valuesNumber * i, graphHeight/2-int(firstValue), graphWidth / valuesNumber * (i+1),  graphHeight/2-int(secondValue),
                         width=graphLineWidth)

# рамки, сейчас они просто в оперативке
notesFrame = Frame(window, background='#45C4B0')
graphFrame = Frame(window, background='#9AEBA3')
valuesFrame = Frame(window, background='#DAFDBA')

# фиксируем их на плоскость с помощью упаковщиков
# pack()-установка по пикселям
# grid()-установка на таблице
# place()-установка по координатам
notesFrame.grid(row=0, column=0, sticky="nsew")
graphFrame.grid(row=0, column=1, sticky="nsew")
valuesFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")

RenderBottom()
RenderGraph()

window.mainloop()
