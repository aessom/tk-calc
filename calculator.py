from constants import *

class Calculator:
    def __init__(self, complete_line, current_line):
        self.current_state = State.FIRST_NUMBER
        self.first_number = None
        self.operator = None
        self.second_number = None
        self.result = None
        self.memory = None
        self.complete_line = complete_line
        self.current_line = current_line
    
    def append_first_number(self, num):
        if self.first_number is None:
            self.first_number = str(num)
        else:
            self.first_number = self.first_number + str(num)
    
    def append_second_number(self, num):
        if self.second_number is None:
            self.second_number = str(num)
        else:
            self.second_number = self.second_number + str(num)

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
                    self.first_number = "0"
            # Operator > Operator
            case State.OPERATOR:
                self.operator = op
            # Second Number > Result > First Number > Operator
            case State.SECOND_NUMBER:
                self.result = self.calculate()
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
                self.result = self.calculate()
            # First Number + Second Number = Result
            case State.SECOND_NUMBER:
                self.result = self.calculate()
            # Result + Second Number = Result
            case State.RESULT:
                self.first_number = self.calculate()
                self.result = self.calculate()
        self.current_state = State.RESULT
        print(self.current_state)
        self.update_lines()

    def clear_press(self, button):
        if button == "C":
            self.reset()
        if button == "CE":
            match self.current_state:
                # Reset
                case State.FIRST_NUMBER:
                    self.reset()
                # Remove operator and rewind state
                # And clear top line
                case State.OPERATOR:
                    self.operator = None
                    self.current_state = State.FIRST_NUMBER
                    self.update_lines(self.first_number)
                    self.update_tk_window("", None)
                # Delete second number and update bottom line
                case State.SECOND_NUMBER:
                    self.second_number = None
                    self.current_state = State.OPERATOR
                    self.update_lines("")
                # Delete everything
                case State.RESULT:
                    self.reset()

    def memory_press(self, button):
        if button == "MC":
            self.memory = None

        if button == "MR":
            if self.memory:
                match self.current_state:
                    # Replace first number
                    case State.FIRST_NUMBER:
                        self.first_number = self.memory
                    # Fill second number and update state
                    case State.OPERATOR:
                        self.second_number = self.memory
                        self.current_state = State.SECOND_NUMBER
                    # Replace second number
                    case State.SECOND_NUMBER:
                        self.second_number = self.memory
                    # Reset and fill first number
                    case State.RESULT:
                        self.reset()
                        self.first_number = self.memory
                self.update_lines()

        if button == "MS":
            match self.current_state:
                # Store first number
                case State.FIRST_NUMBER:
                    self.memory = self.first_number
                # Store first number
                case State.OPERATOR:
                    self.memory = self.first_number
                # Store second number
                case State.SECOND_NUMBER:
                    self.memory = self.second_number
                # Store result
                case State.RESULT:
                    self.memory = self.result

    def decimal_press(self):
        match self.current_state:
            # Append
            case State.FIRST_NUMBER:
                if "." not in self.first_number:
                    self.append_first_number(".")
            # Advance state and append to second number
            case State.OPERATOR:
                self.advance_state()
                self.append_second_number("0.")
            # Append
            case State.SECOND_NUMBER:
                if "." not in self.second_number:
                    self.append_second_number(".")
            # Reset and append to first number
            case State.RESULT:
                self.reset()
                self.append_first_number("0.")
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

    def update_lines(self, forced=False):
        if isinstance(forced, str):
            self.update_tk_window(self.cat_line(), forced)
        match self.current_state:
            case State.FIRST_NUMBER:
                self.update_tk_window(None, self.first_number)
            case State.OPERATOR:
                self.update_tk_window(self.cat_line(), self.first_number)
            case State.SECOND_NUMBER:
                self.update_tk_window(None, self.second_number)
            case State.RESULT:
                self.update_tk_window(self.cat_line(), self.result)

    def cat_line(self):
        line = ""
        if self.first_number is not None:
            line += self.first_number
        if self.operator is not None:
            line += self.operator
        if self.second_number is not None:
            line += self.second_number
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
        self.update_tk_window("", "")

    def update_tk_window(self, complete_line, current_line):
        if complete_line is not None:
            self.complete_line.set(complete_line)
        if current_line is not None:
            self.current_line.set(current_line)
    
    def calculate(self):
        first_number = float(self.first_number)
        second_number = float(self.second_number)
        result = float(0)
        match OPERATORS[self.operator]:
            case "ADD":
                result = first_number + second_number
            case "SUBTRACT":
                result = first_number - second_number
            case "MULTIPLY":
                result = first_number * second_number
            case "DIVIDE":
                result = first_number / second_number
            case "EXPONENTIATE":
                result = first_number ** second_number
        return str(self.normalize_float(result))
            
    def normalize_float(self, num):
        if int(num) == num:
            return int(num)
        return num
        