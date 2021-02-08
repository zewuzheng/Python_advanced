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
        if isinstance(other, Vector):
            return len(self) == len(other) and all(a == b for a, b in zip(self, other))
        else:
            raise NotImplemented

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

    def __neg__(self):
        return Vector(-x for x in self)

    def __pos__(
            self):  # the realization of this example is due to __init__ of Vector is iterable, and Vector itself is iterable
        return Vector(self)

    def __add__(self, other):
        # if len(self) == len(other):
        return Vector(x + y for x, y in zip(self, other))
        # raise NotImplementedError('Unequal length vector operation not implemented')

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if isinstance(other, numbers.Real):
            return Vector(x * other for x in self)
        else:
            raise NotImplemented

    def __rmul__(self, other):
        return self * other

    def __matmul__(self, other):
        try:
            return Vector(x*y for x,y in zip(self,other))
        except TypeError:
            raise NotImplemented

    def __rmatmul__(self, other):
        return self @ other


a = Vector([3, 4, 5])
print(-a)

c = Vector([3, 4, 5])
d = Vector([1, 2, 3])
print(c + d)
e = Vector([1, 2, 3, 4])
print(c + e)
print((0, 0, 0) + c)
print(a * 10)

#%%
# @ is a dot product operator
import numpy as np
a = np.array([1,3,4])
b = np.array([2,3,4])
print(a@b)
c = [1,3,4]
d = (3,4)
c.extend(d)
print(c)
c += d
print(c)