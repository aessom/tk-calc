from tkinter import *
from tkinter import ttk
from functools import partial
from constants import *
import calculator

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.calculator = None

        self.complete_line = StringVar()
        self.current_line = StringVar()
        self.complete_line.set("")
        self.current_line.set("")

        self.calculator = calculator.Calculator(self.complete_line, self.current_line)
        self.build_gui()

    def build_gui(self):
        frame = ttk.Frame(self.root)
        frame.grid(column=0, row=0, sticky=NSEW)

        complete_line_label = ttk.Label(frame, textvariable=self.complete_line)
        current_line_label = ttk.Label(frame, textvariable=self.current_line)

        complete_line_label.grid(row=0, column=0, columnspan=3, sticky=E)
        current_line_label.grid(row=1, column=0, columnspan=3, sticky=E)

        for row in range(len(GRID_LABELS)):
            for column in range(len(GRID_LABELS[row])):
                button = ttk.Button(frame,
                                    text=str(GRID_LABELS[row][column]),
                                    command=partial(self.button_press, GRID_LABELS[row][column])
                                    ).grid(column=column + BUTTON_OFFSET["x"], row=row + BUTTON_OFFSET["y"])  

    def button_press(self, button):
        if isinstance(button, int):
            self.calculator.number_press(button)
        if button in OPERATORS:
            self.calculator.operator_press(button)
        if button == "=":
            self.calculator.result_press()
        if button in CLEAR_BUTTONS:
            self.calculator.clear_press(button)

if __name__ == "__main__":
    root = Tk()
    calculator_gui = CalculatorGUI(root)
    root.mainloop()