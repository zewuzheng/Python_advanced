# %%
def generators():
    print('generator begin')
    for j in range(10):
        print(f'yield {j}')
        yield j
    print('generator end')


g = generators()
print(g)
for j in g:
    print(j)

#%%
# co-process
# in co-process, use next to activate it, and the process always stop at the right of =
def co_process(a):
    print(f'a equals {a}')
    b = yield a
    print(f'b equals {b}')
    c = yield a + b
    print(f'c equals {c}')

co = co_process(10)
print('co-process begin')
d = next(co)
print(d)
e = co.send(20)
print(e)
co.send(99)

#%%
# co-process for calculating moving average

def move_avg():
    total = 0.0
    count = 0
    average = None
    while True:
        num = yield average
        total += num
        count += 1
        average = total / count

avg = move_avg()
next(avg)
print(avg.send(10))
print(avg.send(11))
print(avg.send(12))
print(avg.send(13))
avg.close()

#%%
# pre-activate co-process decorator
# we dont need next to activate co-process

def co_proc(func):
    def prime(*args, **kwargs):
        f = func(*args, **kwargs)
        next(f)
        return f
    return prime

@co_proc
def move_avg1():
    total = 0.0
    count = 0
    average = None
    while True:
        num = yield average
        total += num
        count += 1
        average = total / count

avg = move_avg1()
print(avg.send(10))
print(avg.send(11))
print(avg.send(12))
print(avg.send(13))

#%%
# co-process that simulate taxi process

from collections import namedtuple
Event = namedtuple('event','time proc action')
print(Event)

def taxi_process(ident, trips, start_time = 0):
    time = yield Event(start_time, ident, 'leave garage')
    for i in range(trips):
        time = yield Event(time, ident, 'pick up passenger')
        time = yield Event(time, ident, 'drop off passenger')

    yield Event(time, ident, 'going home')

taxi1 = taxi_process(0, 3)
print(next(taxi1))
print(taxi1.send(2))
print(taxi1.send(5))
print(taxi1.send(10))
print(taxi1.send(11))
print(taxi1.send(15))
print(taxi1.send(30))
print(next(taxi1))
taxi1.close()
