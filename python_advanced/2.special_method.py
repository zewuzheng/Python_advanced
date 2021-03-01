from math import hypot


class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector(%r, %r)' % (self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __abs__(self):
        return hypot(self.x, self.y)


V1 = Vector(1, 2)
V2 = Vector(2, 3)
V3 = V1 + V2
print(V3)
print(abs(V3))

# %%
# self define dict class for special use
import collections


class strdict(collections.UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item


a = strdict()
a[2] = 2
print(a)
print('2' in a.keys())

# %%
from array import array
import math


class Vector2d():
    typecode = 'd'

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))


v1 = Vector2d(3, 4)
print(v1.x, v1.y)
x, y = v1
print(x, y)
print(v1)
v1_clone = eval(repr(v1))
print(v1 == v1_clone)
print(abs(v1))


# %%
# classmethod and staticmethod

class Demo():
    def __init__(self):
        self.num = 0

    @classmethod
    def klassmeth(*args):
        return args

    @staticmethod
    def statmeth(*args):
        return args


print(Demo.klassmeth('spam'))
print(Demo.statmeth('spam'))


# %%
# protedted attribute
class test():
    def __init__(self):
        self._x = 1

    @property
    def x(self):
        return self._x


a = test()
print(a.x)

# %%
# a vector class
from array import array
import reprlib
import math
import numbers
import functools
import operator
import itertools


class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode,
                                 components)  # read iterables as vector, _components is protected variable

    def __iter__(self):
        return iter(self._components)  # Vector object is iterable

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('[') + 1: -2]
        return 'Vector({})'.format(components)

    # def __str__(self):
    #     return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(self._components))

    def __eq__(self, other):
        return (len(self) == len(other) and all(a == b for a, b in zip(self, other)))

    def __hash__(self):
        hashes = (hash(x) for x in self)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = '{.__name__} indices must be integers'
            raise TypeError(msg.format(cls))

    shortcut_names = 'xyzt'

    def __getattr__(self, item):
        cls = type(self)
        if len(item) == 1:
            pos = cls.shortcut_names.find(item)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, item))

    def __setattr__(self, key, value):
        cls = type(self)
        if key in cls.shortcut_names:
            raise AttributeError('{.__name__!r} object cant set attribute'.format(cls))
        super().__setattr__(key, value)

a = Vector([3, 4, 5])
print(a.x)
print(a[0])
a.x = 10
print(a.x)


# %%
from array import array
import reprlib

a = array('d', [1, 2, 3, 4])
b = reprlib.repr(a)
print(a)
print(b)
