class Calculator:
    def __init__(self, factor=1):
        self.factor = factor

    def add(self, a, b):
        if a < 0 and b < 0:
            return (a + b) * self.factor
        elif a > b:
            return (a + b + self.factor)
        else:
            return a + b

    def scale_list(self, lst):
        scaled_list = []
        for item in lst:
            if item > 0:
                scaled_list.append(item * self.factor)
            else:
                scaled_list.append(0)
        return scaled_list

def sum_even_numbers(lst):
    total = 0
    for num in lst:
        if num % 2 == 0:
            total += num
    return total

def factorial(n):
    result = 1
    counter = n
    while counter > 0:
        result *= counter
        counter -= 1
    return result

class NumberManager:
    def __init__(self, numbers):
        self.numbers = numbers  

    def filter_greater_than(self, threshold):
        return [num for num in self.numbers if num > threshold]

    def find_maximum(self):
        max_val = self.numbers[0]
        for num in self.numbers:
            if num > max_val:
                max_val = num
        return max_val

