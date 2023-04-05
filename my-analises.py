from tkinter import *

window = Tk()
window.title('Cash App')
window.geometry('800x500')
window.minsize(800, 500)
window.maxsize(1200, 750)

# рамки, сейчас они просто в оперативке
frame_date = Frame(window, height=200, width=400, background='yellow')
frame_add = Frame(window, height=200, width=400, background='green')
frame_temp = Frame(window, height=300, width=800, background='red')

# фиксируем их на плоскость с помощью упаковщиков
# pack()-установка по пикселям
# grid()-установка на таблице
# place()-установка по координатам
frame_date.grid(row=0, column=0, sticky="ns")
frame_add.grid(row=0, column=1)
frame_temp.grid(row=1, column=0, columnspan=2, sticky="we")


# создаем лэйблы на родительском фрейме
# тут же можно настраивать шрифт
label_train_text = Label(frame_add, text="training time")
label_train_value = Label(frame_add, text="8:00")

label_walk_text = Label(frame_add, text="walking time")
label_walk_value = Label(frame_add, text="18:00")

label_shop_text = Label(frame_add, text="shopping")
label_shop_value = Label(frame_add, text="19:00")


# лэйблы располагаем таблично для удобства
label_shop_text.grid(row=0, column=0, sticky="w", padx=10, pady=10)
label_shop_value.grid(row=0, column=1, sticky="e", padx=10, pady=10)

label_walk_text.grid(row=1, column=0, sticky="w", padx=10, pady=10)
label_walk_value.grid(row=1, column=1, sticky="e", padx=10, pady=10)

label_train_text.grid(row=2, column=0, sticky="w", padx=10, pady=10)
label_train_value.grid(row=2, column=1, sticky="e", padx=10, pady=10)


# условно именуем остальные фреймы
# expand - центр фрейма, padx pady - отступы
label_frame_date = Label(frame_date, text="frame_date")
label_frame_date.pack(expand=True, padx=20, pady=20)

label_frame_temp = Label(frame_temp, text="frame_temp")
label_frame_temp.pack(expand=True, padx=20, pady=20)





window.mainloop()
