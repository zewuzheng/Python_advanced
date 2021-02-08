## 1.list comprehension and generator expression

x = 'abc'
dummy = [ord(x) for x in x]
print(x)
print(dummy)

# %%
s = [1, 2, 3, 4, 5, 6, 7]
dummy = [x for x in s if x > 5]
print(dummy)

# %%
# nametupe

from collections import namedtuple

Card = namedtuple('CARD', ['rank', 'suit'])
a = Card(2, 'diamonds')
print(a)

# %%
# slice
s = 'bicycle'
print(s[::3])
print(s[::-1])
print(s[::-2])

a = slice(0, 2)
print(s[a])

# %%
# + and *
l = [1, 2, 3]
print(l * 5)
a = 'adfdsf'
b = 'dvcvcvc'
print(a + b)

wierd_board = [['_'] * 3] * 3
print(wierd_board)
wierd_board[1][2] = 'o'
print(wierd_board)  # the use of list duplicate in this way will refer to the same object

# the right way is to use list comprehension
wierd_board1 = [['_'] * 3 for i in range(3)]
wierd_board1[1][2] = 'o'
print(wierd_board1)

# %%
# list sort
a = [1, 2, 10, 3, 4, 5]
print(sorted(a))  ## crate a new copy of a, rather than changing a
print(a)
print(a.sort())  ## sort a itself, return None to idicate that changes made on a
print(a)

# %%
# collections.deque()

from collections import deque

dq = deque(range(10), maxlen=10)
dq.rotate(3)
print(dq)
dq.popleft()
print(dq)
dq.append(200)
print(dq)

# %%
# dict comprehension
import collections

a = [('a', 1), ('b', 2)]
d = {ap: num for ap, num in a}
print(d.items())  ## items is a list of tuple with key, value pair

## get value from keys that missing from dict
c = d.get('g', 0)
print(c)
d.update({'g': 1})
print(d)
d.update({'f': 2})
d['f'] += 3
d['o'] = 10
# d['l'] += 2
d.update({'l': [2]})
print(d.setdefault('l', []).append(1))
print(d)
dd = collections.defaultdict(list)
dd['a'] = 1
dd['b'].append('c')
print(dd)



