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
            # First Number > First Number
            case State.FIRST_NUMBER:
                self.append_first_number(num)
            # Operator > Second Number
            case State.OPERATOR:
                self.advance_state()
                self.append_second_number(num)
            # Second Number > Second Number
            case State.SECOND_NUMBER:
                self.append_second_number(num)
            # Result > (Reset) > First Number
            case State.RESULT:
                self.reset()
                self.append_first_number(num)
        self.update_lines()

    def operator_press(self, op):
        match self.current_state:
            # First Number > Operator
            case State.FIRST_NUMBER:
                self.advance_state()
                self.operator = op
                if self.first_number is None:
                    self.first_number = 0
            # Operator > Operator
            case State.OPERATOR:
                self.operator = op
            # Second Number > Result > First Number > Operator
            case State.SECOND_NUMBER:
                self.result = calculate(self.first_number, self.operator, self.second_number)
                self.roll_over(op)
            # Result > First Number > Operator
            case State.RESULT:
                self.roll_over(op)
        self.update_lines()
    
    def result_press(self):
        match self.current_state:
            # First Number = Result
            case State.FIRST_NUMBER:
                self.result = self.first_number
            # First Number + First Number = Result
            case State.OPERATOR:
                self.second_number = self.first_number
                self.result = calculate(self.first_number, self.operator, self.second_number)
            # First Number + Second Number = Result
            case State.SECOND_NUMBER:
                self.result = calculate(self.first_number, self.operator, self.second_number)
            # Result + Second Number = Result
            case State.RESULT:
                self.first_number = calculate(self.first_number, self.operator, self.second_number)
                self.result = calculate(self.first_number, self.operator, self.second_number)
        self.current_state = State.RESULT
        print(self.current_state)
        self.update_lines()

    def roll_over(self, op):
        # If an operator is pressed after both numbers are entered,
        # get the result and roll it over to a new calculation
        self.first_number = self.result
        self.operator = op
        self.second_number = None
        self.current_state = State.OPERATOR
        print(self.current_state)

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
                update_tk_window(None, str(self.first_number))
            case State.OPERATOR:
                update_tk_window(self.cat_line(), str(self.first_number))
            case State.SECOND_NUMBER:
                update_tk_window(None, str(self.second_number))
            case State.RESULT:
                update_tk_window(self.cat_line(), self.result)

    def cat_line(self):
        line = ""
        if self.first_number is not None:
            line += str(self.first_number)
        if self.operator is not None:
            line += str(self.operator)
        if self.second_number is not None:
            line += str(self.second_number)
        if self.current_state == State.RESULT:
            line += "="
        return line

    def reset(self):
        # Reset to initialized values
        self.current_state = State.FIRST_NUMBER
        self.first_number = None
        self.operator = None
        self.second_number = None
        self.result = None
        update_tk_window("", "")


def button_press(button):
    if isinstance(button, int):
        calc.number_press(button)
    if button in OPERATORS:
        calc.operator_press(button)
    if button == "=":
        calc.result_press()

def update_tk_window(top_line, bottom_line):
    if top_line is not None:
        complete_line.set(top_line)
    if bottom_line is not None:
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