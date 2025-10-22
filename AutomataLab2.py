class MealyMachine:
    def __init__(self):
        self.state = 'A'

    def reset(self):
        self.state = 'A'

    def transition(self, input_char):
        if self.state == 'A':
            if input_char == '0':
                self.state = 'B'
                return 'b'
            elif input_char == '1':
                self.state = 'A'
                return 'b'
        elif self.state == 'B':
            if input_char == '0':
                self.state = 'B'
                return 'b'
            elif input_char == '1':
                self.state = 'A'
                return 'a'

    def process(self, input_string):
        output = ""
        for ch in input_string:
            output += self.transition(ch)
        return output


class MooreMachine:
    def __init__(self):
        self.state = 'A'

    def reset(self):
        self.state = 'A'

    def output(self):
        """Output depends on current state only"""
        if self.state == 'C':  # C means we’ve detected “01”
            return 'a'
        return 'b'

    def transition(self, input_char):
        if self.state == 'A':
            if input_char == '0':
                self.state = 'B'
            else:
                self.state = 'A'
        elif self.state == 'B':
            if input_char == '1':
                self.state = 'C'
            else:
                self.state = 'B'
        elif self.state == 'C':
            if input_char == '0':
                self.state = 'B'
            else:
                self.state = 'A'

    def process(self, input_string):
        output = self.output()  # output before first input
        for ch in input_string:
            self.transition(ch)
            output += self.output()
        return output


# TEST BOTH MACHINES
inputs = ["011001", "110011"]

mealy = MealyMachine()
moore = MooreMachine()

for input_str in inputs:
    mealy.reset()
    moore.reset()
    print(f"\nInput: {input_str}")
    print(f"Mealy Output: {mealy.process(input_str)}")
    print(f"Moore Output: {moore.process(input_str)}")
