import sys


class CannotMerge(Exception):
    pass

class Loss(object):
    def __init__(self, from_, to=None):
        self._from = from_
        self.to = to if to else from_

    def merge(self, rhs):
        if self._from > rhs._from:
            if self.to > rhs.to:
                self.to = rhs.to

        elif self.to > rhs.to:
            self._from =rhs._from
            self.to = rhs.to
        else:
            raise CannotMerge()

    @property
    def delta(self):
        return self._from - self.to

    def __cmp__(self, rhs):
        return self.delta - rhs.delta
    def __repr__(self):
        return '<%s~%s>' % (self._from, self.to)


n = int(raw_input())
losses = map(Loss, map(int, raw_input().split()))
print >>sys.stderr, 'init value:', losses

while True:
    i_losses = iter(losses)
    lhs = i_losses.next()
    new_losses = []
    try:
        while True:
            rhs = i_losses.next()
            try:
                lhs.merge(rhs)
            except CannotMerge:
                new_losses.append(lhs)
                lhs = rhs
    except StopIteration:
        new_losses.append(lhs)
    if len(new_losses) == len(losses):
        break
    losses = new_losses
    print >>sys.stderr, losses


losses.sort(reverse=True)
print -losses[0].delta
