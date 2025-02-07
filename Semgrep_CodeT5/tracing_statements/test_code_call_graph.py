def foo():
    bar()
    baz(42, "hello")

def bar():
    pass

def baz(x, y):
    bar()
