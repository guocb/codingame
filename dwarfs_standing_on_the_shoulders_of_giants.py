import sys


class Node(object):
    def __init__(self, num = 0):
        self.kids = []
        self.num = num
        self.is_root = True

    def add_kid(self, kid):
        self.kids.append(kid)
        kid.is_root = False

    def __repr__(self):
        return '<%s>' % self.num

    @property
    def longest_chain(self):
        if not self.kids:
            return 1
        ml = 1
        for k in self.kids:
            l = k.longest_chain
            ml = l if l > ml else ml
        return ml + 1


reg = {}

n = int(raw_input()) # the number of relationships of influence
for i in xrange(n):
     # x: a relationship of influence between two people (x influences y)
    x, y = [int(j) for j in raw_input().split()]
    x = reg.setdefault(x, Node(x))
    y = reg.setdefault(y, Node(y))
    x.add_kid(y)

ml = 0
for n in reg.values():
    if n.is_root:
        print n.longest_chain
        sys.exit(0)
