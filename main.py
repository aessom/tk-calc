from tkinter import *
from tkinter import ttk
from functools import partial
from constants import *

current_state = State.FIRST_NUMBER
first_number = 0
operator = ""
second_number = 0
result = 0


def button_press(button):
    global current_state
    print(current_state)
    if isinstance(button, int):
        number_press(button)
    if button in OPERATORS:
        operator_press(button)


def number_press(num):
    global current_state
    match current_state:
        case State.FIRST_NUMBER:
            append_first_number(num)
        case State.OPERATOR:
            current_state = State.SECOND_NUMBER
            append_second_number(num)
        case State.SECOND_NUMBER:
            append_second_number(num)
        case State.RESULT:
            reset()
            append_first_number(num)


def operator_press(op):
    global first_number, second_number
    global operator, current_state
    match current_state:
        case State.FIRST_NUMBER:
            current_state = State.OPERATOR
            operator = op
        case State.OPERATOR:
            operator = op
        case State.SECOND_NUMBER:
            # TODO: perform calculation
            #       set result to first number
            #       set operator to op
            #       clear second number
            #       set state to operator
            pass
        case State.RESULT:
            # TODO: same as above
            pass
    update_current_line()


def append_first_number(num):
    global first_number
    if first_number == 0:
        first_number = num
    else:
        first_number = int(str(first_number) + str(num))
    update_current_line()


def append_second_number(num):
    global second_number
    if second_number == 0:
        second_number = num
    else:
        second_number = int(str(second_number) + str(num))
    update_current_line()


def update_current_line():
    global first_number, second_number
    global current_state, current_line
    match current_state:
        case State.FIRST_NUMBER:
            current_line.set(str(first_number))
        case State.OPERATOR:
            current_line.set(str(first_number))
        case State.SECOND_NUMBER:
            current_line.set(str(second_number))
        case State.RESULT:
            current_line.set(str(first_number))


def reset():
    global first_number, operator, second_number
    global current_state, result
    first_number = 0
    operator = ""
    second_number = 0
    current_state = State.FIRST_NUMBER
    result = 0



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

for row in range(len(GRID_LABELS)):
    for column in range(len(GRID_LABELS[row])):
        button = ttk.Button(frame,
                            text=str(GRID_LABELS[row][column]),
                            command=partial(button_press, GRID_LABELS[row][column])
                            ).grid(column=column, row=row + 2)

window.mainloop()