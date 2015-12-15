import sys

class LoopException(Exception):
    pass

class ExitException(Exception):
    pass

class Bender(object):
    map_ = {
        'S': (0, 1),
        'E': (1, 0),
        'N': (0, -1),
        'W': (-1, 0)
    }
    def __init__(self, x, y, dir_='S'):
        self.x, self.y = x, y
        self._dir = dir_
        self.turnning_map = ['S', 'E', 'N', 'W']
        self.path = []
        self.dir_path = []
        self.next_turn = 'S'
        self.breaker = False
        self.inverted = False

    def set_beer(self):
        self.breaker = not self.breaker

    @property
    def pos(self):
        return self.x, self.y
    @property
    def heading(self):
        dx, dy = self.map_[self._dir]
        return self.x + dx, self.y + dy

    def move_on(self):
        self.next_turn = self.turnning_map[0]
        if (self.x, self.y, self._dir, self.breaker) in self.path:
            raise LoopException()

        self.path.append((self.x, self.y, self._dir, self.breaker))
        self.dir_path.append(self._dir)
        self.x, self.y = self.heading

    def inverse(self):
        self.turnning_map.reverse()
        self.inverted = not self.inverted

    def turns(self, new_dir=None):
        if new_dir:
            self._dir = new_dir
            return
        self._dir = self.next_turn
        idx = self.turnning_map.index(self._dir)
        idx = idx + 1 if idx < 3 else 0
        self.next_turn = self.turnning_map[idx]

    def on_obstacle(self, ob):
        if self.breaker:
            # replace the obj
            global game_map
            game_map[ob.y][ob.x] = Space(ob.x, ob.y)
            self.path = []
            print >> sys.stderr, 'break a obstacle at', ob.x, ob.y
            self.move_on()
        else:
            self.turns()

class Element(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

class Space(Element):
    def on_bender(self, ben):
        ben.move_on()

class Origin(Space):
	def __init__(self, x, y):
		Space.__init__(self, x, y)
		global ben
		ben = Bender(x, y)

class Wall(Element):
    def on_bender(self, ben):
        ben.turns()

class Obstacle(Element):
    def on_bender(self, ben):
        ben.on_obstacle(self)

class Turn(Element):
    def __init__(self, x, y):
        Element.__init__(self, x, y)
        self._dir = None
    def on_bender(self, ben):
        ben.move_on()
        ben.turns(self._dir)

class TurnN(Turn):
    def __init__(self, x, y):
        Turn.__init__(self, x, y)
        self._dir = 'N'
class TurnS(Turn):
    def __init__(self, x, y):
        Turn.__init__(self, x, y)
        self._dir = 'S'
class TurnW(Turn):
    def __init__(self, x, y):
        Turn.__init__(self, x, y)
        self._dir = 'W'
class TurnE(Turn):
    def __init__(self, x, y):
        Turn.__init__(self, x, y)
        self._dir = 'E'

class Tomb(Element):
    def on_bender(self, ben):
        ben.move_on()
        raise ExitException()

class Inverter(Element):
    def on_bender(self, ben):
        ben.move_on()
        ben.inverse()

class Beer(Element):
    def on_bender(self, ben):
        ben.set_beer()
        ben.move_on()

PEER = None
class Teleport(Element):
    def __init__(self, x, y):
        Element.__init__(self, x, y)
        global PEER
        self.peer = PEER
        if PEER:
            PEER.peer = self
        else:
            PEER = self

    def on_bender(self, ben):
        ben.move_on()
        ben.x, ben.y = self.peer.x, self.peer.y

FACTORY = {
    '#': Wall,
    'X': Obstacle,
    ' ': Space,
    '@': Origin,
    'I': Inverter,
    'T': Teleport,
    '$': Tomb,
    'N': TurnN,
    'S': TurnS,
    'W': TurnW,
    'E': TurnE,
    'B': Beer,
}
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

l, c = [int(i) for i in raw_input().split()]
game_map = []
ben = None
for y in xrange(l):
    row = []
    for ch, x in zip(raw_input(), xrange(c)):
        row.append(FACTORY[ch](x, y))
    game_map.append(row)


result_map = {'S': 'SOUTH', 'N': 'NORTH', 'E': 'EAST', 'W': 'WEST'}
try:
    while True:
        x, y = ben.heading
        game_map[y][x].on_bender(ben)

except ExitException:
    print '\n'.join([result_map[d] for d in ben.dir_path])

except LoopException:
    print >> sys.stderr, ''.join(ben.dir_path)
    print 'LOOP'
