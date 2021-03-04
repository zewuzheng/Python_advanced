# in python, variable is reference of object, but not the box that contains object
# all variables have their own id, object type and value
# %%
t1 = (1, 2, [3])
print(id(t1[-1]))
t1[-1].append(4)
print(id(t1[-1]))
t1[-1] = [3, 4, 5]
print(id(t1[-1]))

## for tuple, or unmutable object, we cannot change its id, once we have new assignment, its id will be changed
## but for mutable object like list, method like .append() do not change its id

# %%
# deepcopy and copy
# copying a list, the element in the list will have same reference
from copy import deepcopy

a = [3, [1, 2], (1, 2, 3)]
print(id(a[2]))
b = list(a)
print(id(b[2]))
a[1].append(3)
print(b)

c = deepcopy(a)
a[1].append(4)
print(c)

# %%
# unmutable object reference
a = (1, 2, 3)
print(id(a))
a += (4, 5)
print(a)
print(id(a))


# %%
# mutable object cannot be default parameter of function
# because default parameters are generated when function is initialized
# ex
class bus():
    def __init__(self, passenger=[]):
        self.passenger = passenger

    def pick(self, name):
        self.passenger.append(name)

    def drop(self, name):
        self.passenger.remove(name)


a = bus()
b = bus()
a.pick('zzw')
print(b.passenger)

# the right way
#%%
class bus():
    def __init__(self, passenger = None):
        if passenger is None:
            self.passenger = []
        else:
            self.passenger = list(passenger)

    def pick(self, name):
        self.passenger.append(name)

    def drop(self, name):
        self.passenger.remove(name)

#%%
a = 1
def count(a):
    b = a
    b +=1
    print(b)

count(a)
print(a)

c = [2]
def count1(c):
    d = c
    d.append(1)
    print(d)

count1(c)
print(c)

