# %%
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(self.text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return 'Sentence(%s)' % self.text
        # return 'Sentence(%s)' % reprlib.repr(self.text)


s = Sentence('How are you? I am fine, thank you!')
print(s)
for word in s:
    print(word)
print(iter(s))

# %%
# iterable object and iterator

s = 'abc'
for char in s:
    print(char)

f = 'abc'
it = iter(f)  # get iterator from iterable object
while True:
    try:
        print(next(it))
    except StopIteration:
        del it
        break

f = 'abc'
while True:
    try:
        print(next(f))
    except StopIteration:
        break

## generator
# %%
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(self.text)

    def __repr__(self):
        return 'Sentence(%s)' % self.text
        # return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:
            yield word


s = Sentence('I am a hero')
for w in s:
    print(w)

it = iter(s)
while True:
    try:
        print(next(it))
    except StopIteration:
        break

# %%
# y version

import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % self.text
        # return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in RE_WORD.finditer(self.text):
            yield word.group()
        return


s = Sentence('I am a hero')
for w in s:
    print(w)

it = iter(s)
while True:
    try:
        print(next(it))
    except StopIteration:
        break

# %%
# generator expression
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % self.text
        # return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        return (match.group() for match in RE_WORD.finditer(self.text))


s = Sentence('I am a hero')
for w in s:
    print(w)

it = iter(s)
while True:
    try:
        print(next(it))
    except StopIteration:
        break

# %%
# special usage of iter
from random import randint


def dice():
    return randint(1, 6)


dicer = iter(dice, 1)
for i in dicer:
    print(i)

# dicer call dice iteratively, and yield every value return by dice, if return value equals 1, then stop iteration
