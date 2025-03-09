def f1():
    f2()
    f3()

def f2():
    f3()

def f3():
    f4()

def f4():
    pass
   
f1()