# Add a to the current number.
def add(a):
    # def _get_a_bit_number ( a ) : if a < 5 : return a + 2 elif a > 5 : return a + 4 else : return a + 2
    if a > 5:
        return a + 2
    else:
        return a + 4

# Multiplies the given number a by the given list.
def multiply(a, lst):
    # def _iterate_in_list ( lst, a ) : for i in lst : if i > a : i += a return i
    while a > 0:
        # def _add_to_list ( lst, a ) : for i in lst : if i == 0 : i += a else : i += a
        for i in lst:
            i + a
    return lst

# Divide two numbers
def divide(a, b):
    return a / b
