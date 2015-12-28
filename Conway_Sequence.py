'''
THere's some other solutions, e.g. using itertools.groupby.
This is the coroutine version.
'''
import sys
from contextlib import closing


def consumer(func):
    def wrapper(*args, **kw):
        it = func(*args, **kw)
        next(it)
        return it
    return wrapper
    
@consumer
def encoder(result):
    letter = yield
    count = 1
    while True:
        try:
            l = yield
        except GeneratorExit:
            result.extend([count, letter])
            return
        else:
            if l == letter:
                count += 1
            else:
                result.extend([count, letter])
                letter = l
                count = 1
    
    
r = [int(raw_input())]
l = int(raw_input())

result = r
for i in xrange(1, l):
    input_ = result[:]
    result = []
    with closing(encoder(result)) as it:
        for c in input_:
            it.send(c)

print ' '.join(map(str, result))
