from itertools import count

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(raw_input())
horses = []
for i in xrange(n):
    pi = int(raw_input())
    horses.append(pi)

horses.sort()
iter1 = iter(horses)
iter2 = iter(horses[1:])
min_diff = -1
for h1, h2, idx in zip(iter1, iter2, count()):
    diff = h1 - h2 if h1 > h2 else h2 - h1
    min_diff = diff if diff < min_diff or min_diff < 0 else min_diff

print min_diff
