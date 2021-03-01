# doc property of function

def my_func(a: list) -> None:
    """
    This is an example of function documentation
    """
    print("Hello World")


print(my_func.__doc__)

# function lambda
words = ['abffg', 'bcwew', 'cdsd', 'dvvvcz']
print(sorted(words, key=lambda word: word[::-1]))
print(words)


# %%
# self define callable type
class Cal():
    def __init__(self):
        self.num = 1

    def __call__(self):
        print(self.num)


a = Cal()
a()


# %%
# the parameter and return of functions will be reflected in __annotations__
# print(my_func.__annotations__)

def my_par(a: int, *b: [int], c=None, **d):
    if b:
        print("b detected,", [x for x in b])

    if c is not None:
        print("c detected", c)

    if d:
        print('d detected', d)


my_par(1)
my_par(1, 3, 4, 5)
my_par(1, 3, 4, 5, c=10)
my_par(1, 3, 4, 5, c=10, e=9, f=8)
print(my_par.__annotations__)
print(my_par.__defaults__)


# decorator
# actually, for decorator, the following are the same

# @decorator
# def target():
#     print('running target()')
#
# def target():
#     print('running target()')
#
# target = decorator(target)  decorator return a function target that may not be the same as original one

def deco(func):
    def inner():
        print('inner!')

    return inner


@deco
def target():
    print('target!')


target()
# decoration will be executed before py is ran, such as when importing the module

# %%
# param field
b = 6


def f3(a):
    # global b
    print(a)
    print(b)
    b = 10


f3(4)


# %%
class Average():
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total / len(self.series)


avg = Average()
print(avg(10))
print(avg(11))
print(avg(12))


# %%
# in function type
def Average():
    series = []  # series is free variable in this scheme

    def averager(new_valule):
        series.append(new_valule)
        total = sum(series)
        return total / len(series)

    return averager


a = Average()
print(a(10))
print(a(11))
print(a(12))


# %%
# in function type
def Average():
    count = 0  # count and total is unmutable object
    total = 0

    def averager(new_valule):
        nonlocal count, total  # use nonlocal to indicate that count and total reference
        count += 1  # this is equal to count= count + 1, so count is regard as local variable
        total += new_valule
        return total / count

    return averager


a = Average()
print(a(10))
print(a(11))
print(a(12))

# %%
# parameterized decorator
import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


def clock(fmt=DEFAULT_FMT):   # parameterized factory function
    def decorate(func):    # decorate function
        def clocked(*_args):    # function that being decorated
            t0 = time.time()
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ','.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result

        return clocked

    return decorate

@clock()
def snooze(seconds):
    time.sleep(seconds)

for i in range(3):
    snooze(.123)