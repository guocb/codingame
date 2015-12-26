import sys
import math

class Water(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        Lake().add_water(self)
        
    def join(self, rhs):
        self.lake.join(rhs.lake)
        
    def __repr__(self):
        return 'W(%s %s)' % (self.x, self.y)
            
LAKES = []
class Lake(object):
    def __init__(self):
        self.waters = set([])
        self._waterset = None
        self.area = 0
        global LAKES
        LAKES.append(self)
        
    def __repr__(self):
        return str(self.waters)
        
    @property
    def waterset(self):
        if not self._waterset:
            self._waterset = set([(w.x, w.y) for w in self.waters])
        return self._waterset
    
    def join(self, rhs):
        if self is rhs:
            return
        self.waters |= rhs.waters
        for w in rhs.waters:
            w.lake = self
        rhs.waters = set([])
        rhs.area = 0
        self.area = len(self.waters)
        
    def add_water(self, *waters):
        for w in waters:
            self.waters.add(w)
            w.lake = self
        self.area = len(self.waters)
            
    def in_lake(self, x, y):
        return (x, y) in self.waterset
            
l = int(raw_input())
h = int(raw_input())
xwater = None
ywater = [None for _ in xrange(l)]
for y in xrange(h):
    for x, c in zip(xrange(l), raw_input()):
        print >>sys.stderr, c,
        if c == 'O':
            water = Water(x, y)
            if xwater:
                xwater.join(water)
            if ywater[x]:
                ywater[x].join(water)
            xwater = ywater[x] = water
        else:
            xwater = None
            ywater[x] = None
    print >>sys.stderr,''
    xwater = None
    
LAKES = [l for l in LAKES if l.waters]
for l in LAKES:
    print >>sys.stderr, l

n = int(raw_input())
for i in xrange(n):
    x, y = [int(j) for j in raw_input().split()]
    found = False
    for lake in LAKES:
        if lake.in_lake(x, y):
            print lake.area
            found = True
            break
    if not found:
        print 0
    

