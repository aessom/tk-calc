from enum import Enum

BUTTON_OFFSET = {
    "x": 0,
    "y": 2
}

GRID_LABELS = [
    ["C", "CE", "^", ""],
    [7, 8, 9, "÷"],
    [4, 5, 6, "×"],
    [1, 2, 3, "-"],
    [0, ".", "=", "+"]
]

CLEAR_BUTTONS = {
    "CE": "CLEAR_ENTRY",
    "C": "CLEAR"
}

OPERATORS = {
    "+": "ADD",
    "-": "SUBTRACT",
    "×": "MULTIPLY",
    "÷": "DIVIDE",
    "^": "EXPONENTIATE",
}

class State(Enum):
    FIRST_NUMBER = 1
    OPERATOR = 2
    SECOND_NUMBER = 3
    RESULT = 4

