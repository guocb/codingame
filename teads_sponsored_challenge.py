import sys


class Node(object):
    def __init__(self, name):
        self.name = name
        self.neighbours = []

    def add_neighbour(self, rhs):
        self.neighbours.append(rhs)
        rhs.neighbours.append(self)

    @property
    def neighbour_count(self):
        return len(self.neighbours)

    def __repr__(self):
        return '(%s)' % self.name

nodes = {}
n = int(raw_input()) # the number of adjacency relations

for i in xrange(n):
     # xi: the ID of a person which is adjacent to yi
     # yi: the ID of a person which is adjacent to xi
    xi, yi = [int(j) for j in raw_input().split()]
    nx = nodes.setdefault(xi, Node(str(xi)))
    ny = nodes.setdefault(yi, Node(str(yi)))
    nx.add_neighbour(ny)

# find a root
ROOT = None
for n in nodes.values():
    if n.neighbour_count == 1:
        ROOT = n
        break

stack = []
# build a tree
tree = [ROOT]
max_len = 0
while True:
    tot = tree[-1]
    if tot.neighbour_count == 1:
        length = len(tree)
        if length == 1:
            tree.append(tot.neighbours[0])
            continue
        max_len = length if length > max_len else max_len
        if not stack:
            break
        n, pos = stack.pop()
        tree = tree[:pos]
        tree.append(n)
        print >>sys.stderr, tree
    elif tot.neighbour_count == 2:
        for n in tot.neighbours:
            if n is not tree[-2]:
                tree.append(n)
                break
    else:
        for n in tot.neighbours:
            if n is not tree[-2]:
                stack.append((n, len(tree)))
        n, _ = stack.pop()
        tree.append(n)

print max_len / 2
