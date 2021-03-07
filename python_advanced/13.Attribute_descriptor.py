# the class that have methods __get__ __set__ __delete__ is descriptor
# %%
class quantity:
    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[
                self.storage_name] = value  ## why use dict, because setattr with get into a loop of setting attribute
        else:
            raise ValueError('value must be > 0')


class LineItem:
    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    def __repr__(self):
        return f'{self.__class__.__name__}({self.description}, weight = {self.weight}, price = {self.price})'


a = LineItem('Mango', 10, 9.9)
print(a)
a.weight = 20
print(a)
a.weight = -10

# %%
# The cultivation of this code is based on functionality

import abc


class AutoStorage:

    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.storage_name]

    def __set__(self, instance, value):
        instance.__dict__[self.storage_name] = value


class Validated(abc.ABC, AutoStorage):

    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """
        return validated value or raise ValueError
        """


class Quantity(Validated):

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):

    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value


class LineItem:
    description = NonBlank('description')
    weight = Quantity('weight')
    price = Quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    def __repr__(self):
        return f'{self.__class__.__name__}({self.description}, weight = {self.weight}, price = {self.price})'


a = LineItem('mango', 15, 5)
print(a)
print(a.__dict__)
print(Quantity.__dict__)


# %%
# cover descriptor and uncover descriptor

def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]


# the function cls_name get the type name of obj_or_cls

def display(obj):
    cls = type(obj)
    if cls is type:
        return '<class {}>'.format(obj.__name__)
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return '<{} object>'.format(cls_name(obj))


def print_args(name, *args):
    pseudo_args = ','.join(display(x) for x in args)
    print('-> {}.__{}__({})'.format(cls_name(args[0]), name, pseudo_args))


class Overriding:
    """override descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):
        print('-> Managed.spam({})'.format(display(self)))


# the class that have __set__ method is Overriding descriptor.
print(Managed.over)
# output is -> Overriding.__get__(<Overriding object>,None,<class Managed>)
# So actually, although descriptor is class attribute of Managed, but when no object created for Managed,
# then instance is None, and owner is Managed
# when setting attr, then descriptor will cover object attr.

# for OverridingNOGet, its descriptor will be overided by object attribute.

# for NonOverriding: it dont has __set__ method, so setting attribute will cover __get__ method__ of this class.

obj = Managed()
Managed.over = 1
Managed.over_no_get = 2
Managed.non_over = 3
print(obj.over, obj.over_no_get, obj.non_over)
obj.over = 5
obj.over_no_get = 6
obj.non_over = 7
print(obj.over, obj.over_no_get, obj.non_over)

######################################################################################
# getting attribute of class will get from __get__ method of that class
# but setting attribute of class will not get from __set__ method of that class
######################################################################################

# %%
# methods are descriptor
# Because methods all have __get__

obj = Managed()
print(obj.spam)  # <bound method Managed.spam of <__main__.Managed object at 0x7f91ddacf908>>
print(Managed.spam) # <function Managed.spam at 0x7f91ce92aa60>
obj.spam = 7
print(obj.spam) # 7
######################################################################################################################
# if set attribute obj.spam = 7, it will cover the method 'spam' in obj, because methods are Non-overriding descriptor
######################################################################################################################

#%%
# Investigation of methods in Class

import collections

class Text(collections.UserString):

    def __repr__(self):
        return f'Text({self})'

    def reverse(self):
        return self[::-1]

word = Text('forward')
print(word.data) # forward
print(word) # forward
print(word.reverse())
print(Text.reverse(Text('backward')))
print(type(Text.reverse), type(word.reverse)) # <class 'function'> <class 'method'>
print(Text.reverse.__get__(word)) # <bound method Text.reverse of Text(forward)>
print(Text.reverse.__get__(None, Text)) # <function Text.reverse at 0x7f91ce92a400>
print(word.reverse) # <bound method Text.reverse of Text(forward)>
print(word.reverse.__self__) # forward  word.reverse.__self__ = word
print(word.reverse.__func__ is Text.reverse) # True

# bounding methods will also have a mthod __call__, which utilize __func__ to get function in the class,
# and bound the function to __self__, which is the object created.

#%%
#################################################################################################
#################################################################################################
#                The usage of descriptor
#################################################################################################
#################################################################################################

# firstly, use property to keep clean coding.

# use descriptor to validate value of attributes. And you only need to have __set__ methods.

# use descriptor that only have __get__ method can realize high efficient cache.
# e.g. if we are doing time-consuming calculation, we can use Non-overriding descriptor first to get the result,
# and then set attribute of object to cover it.
# In this way, we dont need to do calculation anymore next time we use this value.

# non_special method can be override by attribute setting.
# But special method can't be override, because it is looked up in class, not in object.


