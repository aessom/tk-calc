from enum import Enum

GRID_LABELS = [
    ["C", "CE", "^", ""],
    [7, 8, 9, "÷"],
    [4, 5, 6, "×"],
    [1, 2, 3, "-"],
    [0, ".", "=", "+"]
]

OPERATORS = ["+", "-", "×", "÷", "^"]

class State(Enum):
    FIRST_NUMBER = 1
    OPERATOR = 2
    SECOND_NUMBER = 3
    RESULT = 4

