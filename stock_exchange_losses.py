n = int(raw_input())
price = [int(i) for i in raw_input().split()]

max_loss = 0
highest_price = 0
for p in price:
    highest_price = p if p > highest_price else highest_price
    loss = p - highest_price
    if loss < max_loss:
        max_loss = loss

print max_loss
