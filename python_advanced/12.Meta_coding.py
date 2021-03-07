# %%
# hasattr

a = {'c': 1, 'd': 2}
print(a)
print(hasattr(a, 'items'))
print(hasattr(a, 'e'))

# %%
from urllib.request import urlopen
import warnings
import os
import json

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = '/home/zzheng17/reinforcement_learning/Python_advanced/python_advanced/data/osconfeed.json'

#
# def load():
#     if not os.path.exists(JSON):
#         msg = f'downloading {URL} to {JSON}'
#         warnings.warn(msg)
#         with urlopen(URL) as remote, open(JSON, 'wb') as local:
#             local.write(remote.read())

with open(JSON) as fp:
    raw_feed = json.load(fp)

from collections import abc


class FrozonJSON:
    """
    a read only api, for attr reading in JSON Object
    """

    def __init__(self, mapping):
        self._data = dict(mapping)

    def __getattr__(self, item):
        if hasattr(self._data, item):
            return getattr(self._data, item)
        else:
            try:
                return FrozonJSON.build(self._data[item])
            except KeyError:
                raise AttributeError

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


feed = FrozonJSON(raw_feed)
print(feed.Schedule.speakers[40].items())

# %%
# the true creator __new__ vs __init__
import json
import keyword

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = '/home/zzheng17/reinforcement_learning/Python_advanced/python_advanced/data/osconfeed.json'

with open(JSON) as fp:
    raw_feed = json.load(fp)

from collections import abc


class FrozonJSON:
    """
    a read only api, for attr reading in JSON Object
    """

    def __new__(cls, args):
        if isinstance(args, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(args, abc.MutableSequence):
            return [cls(item) for item in args]
        else:
            return args

    def __init__(self, mapping):
        self._data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self._data[key] = value

    def __getattr__(self, item):
        if hasattr(self._data, item):
            return getattr(self._data, item)
        else:
            try:
                return FrozonJSON(self._data[item])
            except KeyError:
                raise AttributeError


a = {'class': 1, 'c': 2, 'd': {'e': 3}}
a_f = FrozonJSON(a)
print(a_f.class_)
print(a_f.d)

# %%
# shelve module
import warnings
import json
import keyword

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = '/home/zzheng17/reinforcement_learning/Python_advanced/python_advanced/data/osconfeed.json'

with open(JSON) as fp:
    raw_feed = json.load(fp)


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


def load_db(db):
    raw_data = raw_feed
    warnings.warn('loading!.....')
    for collection, rec_list in raw_data['Schedule'].items():
        record_type = collection[:-1]
        for record in rec_list:
            key = f'{record_type}.{record["serial"]}'
            record['serial'] = key
            print(record)
            db[key] = Record(**record)


DB_NAME = '/home/zzheng17/reinforcement_learning/Python_advanced/python_advanced/data/schedule1_db'
CONFERNCE = 'conference.115'

import shelve

db = shelve.open(DB_NAME)
if CONFERNCE not in db:
    load_db(db)

speaker = db['speaker.3471']
print(type(speaker))
print(speaker.name, speaker.twitter)

db.close()


# %%
# self.__dict__ attr test

class Rec:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


a = Rec(c=1)
print(a.__dict__)
print(a.c)

# %%
# test for **record
record = {'serial': 1521, 'name': 'offsite'}


def rec(**kwargs):
    for key, value in kwargs.items():
        print(key, '=', value)


rec(**record)

# %%
#
import warnings
import inspect


# in previous version, Record can only have speaker and venue serial, but not linked to the record
class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            raise NotImplemented


class MissingDatabaseError(RuntimeError):
    """raise when db is needed but not loaded"""


class DbRecord(Record):
    _db = None  # this attr is connected to the class itself, but not class object

    @staticmethod
    def set_db(db):
        DbRecord._db = db

    @staticmethod
    def get_db():
        return DbRecord._db

    @classmethod  # the difference between classmethod and staticmethod is that it need the method from within the class
    def fetch(cls, ident):
        db = cls.get_db()
        try:
            return db[ident]
        except TypeError:
            if db is None:
                msg = "database not set; call '{}.set_db(my_db)'"
                raise MissingDatabaseError(msg.format(cls.__name__))
            else:
                raise

    def __repr__(self):
        if hasattr(self, 'serial'):
            cls_name = self.__class__.__name__
            return '<{} serial={!r}>'.format(cls_name, self.serial)
        else:
            return super().__repr__()


# print(DbRecord._db)
# a = DbRecord
# print(a._db)
# b = DbRecord
# b._db = 2
# print(a._db)
# print(b._db)
# DbRecord._db = 3
# print(b._db)
# print(a._db)
# c = DbRecord
# print(c._db)
#
# print(c.__class__)
# print(c.__name__)
# print(c.__dict__)

class Event(DbRecord):

    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)

    @property
    def speakers(self):
        if not hasattr(self, '_speaker_objs'):
            spkr_serials = self.__dict__['speakers']
            fetch = self.__class__.fetch
            self._speaker_objs = [fetch('speaker.{}'.format(key)) for key in spkr_serials]
        return self._speaker_objs

    def __repr__(self):
        if hasattr(self, 'name'):
            cls_name = self.__class__.__name__
            return '<{}{!r}>'.format(cls_name, self.name)
        else:
            return super().__repr__()


import json

JSON = '/home/zzheng17/reinforcement_learning/Python_advanced/python_advanced/data/osconfeed.json'

with open(JSON) as fp:
    raw_feed = json.load(fp)


def load_db(db):
    raw_data = raw_feed
    for collection, rec_list in raw_data['Schedule'].items():
        record_type = collection[:-1]
        cls_name = record_type.capitalize()  # each type as class name
        cls = globals().get(cls_name, DbRecord)  # if Event, get Event, else, get DbRecord
        if inspect.isclass(cls) and issubclass(cls, DbRecord):
            factory = cls
        else:
            factory = DbRecord
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = factory(**record)


DB_NAME = '/home/zzheng17/reinforcement_learning/Python_advanced/python_advanced/data/schedule2_db'
CONFERNCE = 'conference.115'

import shelve

db = shelve.open(DB_NAME)
if CONFERNCE not in db:
    load_db(db)

# %%
DbRecord.set_db(db)
event = DbRecord.fetch('event.33950')
print(event)
print(event.venue)
print(event.venue.name)


# %%
# LineItem : readable, writable property

# this is an only readable class
class LineItem:

    def __init__(self, description, weight, price):
        self._description = description
        self._weight = weight
        self._price = price

    @property
    def weight(self):
        return self._weight if self._weight > 0 else 0

    @property
    def price(self):
        return self._price if self._price > 0 else 0

    def subtotal(self):
        return self.weight * self.price


a = LineItem('apple', -2, 10)
print(a.subtotal())
a.weight = 10


# %%
class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if value > 0:
            self._weight = value
        else:
            raise ValueError('value must be > 0')

    def subtotal(self):
        return self.weight * self.price


a = LineItem('apple', -1, 10)
print(a.subtotal())
a.weight = 2
print(a.subtotal())


# %%
# learning of property: it is a class
# object attr will cover class attr

class Class:
    data = 'class data'

    @property
    def proc_data(self):
        return 'proc data'


obj = Class()
print(obj.data)
print(Class.data)
print(obj.__dict__)
obj.data = 'object data'
print(obj.data)
print(Class.data)
print(obj.__dict__)


# but for proc_data, although it is class data, but it cant be covered by object data
# obj.proc_data = 'proc_data'

# %%
class Class:
    data = 'class data'

    @property
    def proc_data(self):
        return 'proc data'


obj = Class()
print(obj.proc_data)
obj.__dict__['proc_data'] = 'foo'
print(vars(obj))
print(obj.proc_data)
Class.proc_data = 'baz'
print(obj.proc_data)


# the main purpose of above code is that, obj.attr will not find in object obj first, but
# find in obj.__class__, and only if class dont have property , then find in object obj.

# %%
# the doc of property
class Class:
    data = 'class data'

    @property
    def proc_data(self):
        """
        The property data attribute
        """
        return 'proc data'


# %%
# a property factory function
def quantity(storage_name):
    def qty_getter(instance):
        return instance.__dict__[
            storage_name]  # for property, only directly get value from obj.__dict__ will skip property

    def qty_setter(instance, value):
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)


class LineItem:
    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


nutmeg = LineItem('Moluccan nutmeg', 8, 13.5)
print(nutmeg.weight)
print(nutmeg.price)

#%%
# the difference between __class__, __dict__ and __slots__
class Test:
    def __init__(self):
        self.text = 'hello'

t = Test()
print(t.__class__)
print(t.__dict__)
print(t.__slots__)

