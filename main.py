from tkinter import *
from tkinter import ttk
from functools import partial
from constants import *
from calc import calculate


class Calculator:
    def __init__(self):
        self.current_state = State.FIRST_NUMBER
        self.first_number = None
        self.operator = None
        self.second_number = None
        self.result = None
    
    def append_first_number(self, num):
        if self.first_number is None:
            self.first_number = num
        else:
            self.first_number = int(str(self.first_number) + str(num))
    
    def append_second_number(self, num):
        if self.second_number is None:
            self.second_number = num
        else:
            self.second_number = int(str(self.second_number) + str(num))

    def number_press(self, num):
        match self.current_state:
            case State.FIRST_NUMBER:
                self.append_first_number(num)
            case State.OPERATOR:
                self.advance_state()
                self.append_second_number(num)
            case State.SECOND_NUMBER:
                self.append_second_number(num)
            case State.RESULT:
                self.advance_state()
                self.reset()
                self.append_first_number(num)
        self.update_lines()

    def operator_press(self, op):
        match self.current_state:
            case State.FIRST_NUMBER:
                self.advance_state()
                self.operator = op
                if self.first_number is None:
                    self.first_number = 0
            case State.OPERATOR:
                self.operator = op
            case State.SECOND_NUMBER:
                self.result = calculate(self.first_number, self.operator, self.second_number)
                self.roll_over(op)
            case State.RESULT:
                self.roll_over(op)
        self.update_lines()

    def roll_over(self, op):
        self.first_number = self.result
        self.operator = op
        self.second_number = None
        self.current_state = State.OPERATOR

    def advance_state(self):
        match self.current_state:
            case State.FIRST_NUMBER:
                self.current_state = State.OPERATOR
            case State.OPERATOR:
                self.current_state = State.SECOND_NUMBER
            case State.SECOND_NUMBER:
                self.current_state = State.RESULT
            case State.RESULT:
                self.current_state = State.FIRST_NUMBER
        print(self.current_state)

    def update_lines(self):
        match self.current_state:
            case State.FIRST_NUMBER:
                update_tk_window("", str(self.first_number))
            case State.OPERATOR:
                update_tk_window(str(self.first_number) + self.operator, str(self.first_number))
            case State.SECOND_NUMBER:
                update_tk_window(str(self.first_number) + self.operator, str(self.second_number))
            case State.RESULT:
                update_tk_window(str(self.first_number) + self.operator + str(self.second_number) + "=", self.result)

    def cat_line(self):
        line = ""
        if self.first_number is not None:
            line += str(self.first_number)
        if self.operator is not None:
            line += str(self.operator)
        if self.second_number is not None:
            line += str(self.second_number)
        return line

    def reset(self):
        self.first_number = None
        self.operator = None
        self.second_number = None
        self.result = None


def button_press(button):
    if isinstance(button, int):
        calc.number_press(button)
    if button in OPERATORS:
        calc.operator_press(button)

def update_tk_window(top_line, bottom_line):
    complete_line.set(top_line)
    current_line.set(bottom_line)


calc = Calculator()

window = Tk()
window.title("Calculator")

frame = ttk.Frame(window)
frame.grid(column=0, row=0, sticky=NSEW)

complete_line = StringVar()
ttk.Label(frame, textvariable=complete_line).grid(row=0, columnspan=3, sticky=E)
complete_line.set("")

current_line = StringVar()
ttk.Label(frame, textvariable=current_line).grid(row=1, columnspan=3, sticky=E)
current_line.set("")

for row in range(len(GRID_LABELS)):
    for column in range(len(GRID_LABELS[row])):
        button = ttk.Button(frame,
                            text=str(GRID_LABELS[row][column]),
                            command=partial(button_press, GRID_LABELS[row][column])
                            ).grid(column=column + BUTTON_OFFSET["x"], row=row + BUTTON_OFFSET["y"])

window.mainloop()