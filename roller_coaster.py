'''
Another simple solution:
import sys
from itertools import islice


L, C, N = [int(i) for i in raw_input().split()]
q = [int(x) for x in sys.stdin.readlines()]

all_people = sum(q)
if all_people <= L:
    print C * all_people
    sys.exit(0)
    
def next_game(data, limit):
    reg = {}
    idx = 0
    while True:
        if idx in reg:
            subtotal, idx = reg[idx]
            yield subtotal
            continue
        
        last_idx = idx
        subtotal = 0
        while subtotal + data[idx] <= limit:
            subtotal += data[idx]
            idx += 1
            idx = idx if idx < len(data) else 0
        reg[last_idx] = subtotal, idx
        yield subtotal
            
it = next_game(q, L)
print sum(islice(it, 0, C))
'''
import sys
from itertools import izip_longest, islice


def get_max_value_under(d, limit):
    ratio = 4
    data_num = 3
    data = [d]
    datalen =[len(d)]
    tmp = d
    for _ in range(data_num + 1):
        it = iter(tmp)
        tmp = [sum(x) for x in izip_longest(*[it] * ratio, fillvalue=0)]
        data.append(tmp)
        datalen.append(len(tmp))
        
    reg = {}
    data_idx = 0
    d = data[data_idx]
    idx = 0
    while True:
        total = 0
        if idx in reg:
            total, idx = reg[idx]
            yield total
            continue
        last_idx = idx
        while total + d[idx] <= limit:
            if idx % ratio or data_idx == data_num:
                total += d[idx]
                idx += 1
                idx = 0 if idx == datalen[data_idx] else idx
                
            else:
                data_idx += 1
                d = data[data_idx]
                idx /= ratio
                
        while data_idx > 0:
            data_idx -= 1
            d = data[data_idx]
            idx *= ratio
            
            while total + d[idx] <= limit:
                total += d[idx]
                idx += 1
                idx = 0 if idx == datalen[data_idx] else idx
        
        reg[last_idx] = (total, idx)
        yield total
        

L, C, N = [int(i) for i in raw_input().split()]
q = [int(x) for x in sys.stdin.readlines()]

all_people = sum(q)
if all_people <= L:
    print C * all_people
    sys.exit(0)

it = get_max_value_under(q, L)
print sum(islice(it, 0, C))
