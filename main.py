from tkinter import *
from tkinter import ttk
from functools import partial

GRID_LABELS = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3],
]

def number_press(num):
    if current_line.get():
        current_line.set(current_line.get() + str(num))
    else:
        current_line.set(str(num))

window = Tk()
window.title("Calculator")

frame = ttk.Frame(window)
frame.grid(column=0, row=0, sticky=NSEW)

complete_line = StringVar()
current_line = StringVar()

ttk.Label(frame, textvariable=complete_line).grid(row=0, columnspan=3, sticky=E)
complete_line.set("0")

ttk.Label(frame, textvariable=current_line).grid(row=1, columnspan=3, sticky=E)
current_line.set("-")

for row in range(3):
    for column in range(3):
        button = ttk.Button(frame,
                            text=str(GRID_LABELS[row][column]),
                            command=partial(number_press, GRID_LABELS[row][column])
                            ).grid(column=column, row=row + 2)

window.mainloop()