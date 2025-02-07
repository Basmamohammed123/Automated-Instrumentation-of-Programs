def add(a, b):
    result = 0

    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Both inputs must be numbers")

    if a < 0 and b < 0:
        result = a + b + abs(a - b)
    elif a > b:
        for i in range(int(b)):
            result += a + i
    else:
        counter = 0
        while counter < b:
            result += a + counter
            counter += 1