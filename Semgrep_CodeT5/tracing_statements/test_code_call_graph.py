def f1():
    f2()
    f3(42, "hello")

def f2():
    f3(42, "hello")

def f3(x, y):
    f4()

def f4():
    pass

f1()