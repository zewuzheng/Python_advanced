# else that is not used in if
# %%
for i in range(10):
    print(f'i in {i}')
else:
    print('exit for')

j = 0
while j < 10:
    print(f'j in {j}')
    j += 1
else:
    print('exit while')

try:
    print('in try')
except NotImplemented:
    print('exit try')


# %%
class LookingGlass:
    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'JABBERWOCKY'

    def reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please do not divide by Zero!')
            return True


with LookingGlass() as w:  # w is the variable that return by __enter__
    print('hello!')
    print(w)
print('hello')
print(w)

# %%
# contextmanager

import contextlib


@contextlib.contextmanager
def glassprint():
    import sys
    original_write = sys.stdout.write
    msg = ''

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    try:
        yield 'Happy'
    except ZeroDivisionError:
        msg = 'Please do not divide by Zero!'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)


# in contextlib.contextmanager, the phase before yield is viewed as __enter__ method,
# and phase after yield is viewed as __exit__ method.

with glassprint() as g:
    print('The line')
    print(g)

print('The line')
print(g)
