#
import abc

class Tombola(abc.ABC):

    @abc.abstractmethod
    def load(self, iterable):
        """
        Load an iterable to object
        """

    @abc.abstractmethod
    def pick(self):
        """
        pick an item and delete it from Tombola, and return it
        if null, then raise LookupError
        """

    def inspect(self):
        item = []
        while True:
            try:
                item.append(self.pick())
            except LookupError:
                break
        self.load(item)
        return tuple(sorted(item))

    def loaded(self):
        return bool(self.inspect())


class BingoCage(Tombola):
    def __init__(self, items):
        self._randommizer = random.SystemRandom()
        self._items = []
        self.load(items)

    def load(self, items):
        self._items.extend(items)
        self._randommizer.shuffle(self._items)

    def pick(self):
        try:
            self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        return self.pick()


# %%
# always dont subclass default type like list and dict..

import collections


class Doubledict(dict):
    def __setitem__(self, key, value):
        super(Doubledict, self).__setitem__(key, value * 2)


a = Doubledict(foo=2)
print(a)
a.update({'bol': [3]})
print(a)


class Coubledict(collections.UserDict):
    def __setitem__(self, key, value):
        super(Coubledict, self).__setitem__(key, value * 2)


c = Coubledict(foo=2)
print(c)
c.update({'bol': [3]})
print(c)

# above conflict only exist when you subclass default type that is written in C language
