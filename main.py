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
        top = frame.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        frame.rowconfigure([0, 1], weight=1)

        complete_line_label = ttk.Label(frame, textvariable=self.complete_line)
        current_line_label = ttk.Label(frame, textvariable=self.current_line)

        complete_line_label.grid(row=0, column=0, columnspan=4, sticky=E)
        current_line_label.grid(row=1, column=0, columnspan=4, sticky=E)

        complete_line_label.config(font=("TkTextFont", COMPLETE_LINE_FONT_SIZE))
        current_line_label.config(font=("TkTextFont", CURRENT_LINE_FONT_SIZE))

        for row in range(len(GRID_LABELS)):
            for column in range(len(GRID_LABELS[row])):
                button = ttk.Button(frame,
                                    text=str(GRID_LABELS[row][column]),
                                    command=partial(self.button_press, GRID_LABELS[row][column])
                                    )
                button.grid(column=column + BUTTON_OFFSET["x"], row=row + BUTTON_OFFSET["y"], sticky=NSEW)
                frame.rowconfigure(row + BUTTON_OFFSET["y"], weight=1)
                frame.columnconfigure(column + BUTTON_OFFSET["x"], weight=1)

    def resize_labels(self, root):
        label_font = font.nametofont("TkTextFont")
        label_font.config(size=int(root.width/10))
        self.complete_line_label.config(font=label_font)
        self.current_line_label.config(font=label_font)

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