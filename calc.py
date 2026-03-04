from constants import *

def calculate(num1, operator, num2):
    match OPERATORS[operator]:
        case "ADD":
            return num1 + num2
        case "SUBTRACT":
            return num1 - num2
        case "MULTIPLY":
            return num1 * num2
        case "DIVIDE":
            return num1 / num2
        case "EXPONENTIATE":
            return num1 ** num2