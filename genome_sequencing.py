import sys
from itertools import permutations

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(raw_input())
subseq = []
for i in xrange(n):
    subseq.append(raw_input())

def merge(str1, str2):
    len1, len2 = len(str1), len(str2)
    if len1 >= len2:
        # str1 longer thna str2
        for i in range(len2, 0, -1):
            if str1[-i:] == str2[:i]:
                return str1 + str2[i:]
        return str1 + str2
    else:
        for i in range(len2 - len1, -1, -1):
            if str1 == str2[i: i + len1]:
                return str2
        return merge(str1, str2[:len1]) + str2[len1:]


min_v = 0
for x in permutations(subseq):
    it = iter(x)
    str1 = it.next()
    for str2 in it:
        str1 = merge(str1, str2)
    min_v = len(str1) if len(str1) < min_v or min_v == 0 else min_v

print min_v
