import random

r = random.random

def random_sample(lst, m):
    n = len(lst)
    tmp = lst[:]
    for i in range(n, n-m, -1):
        j = int(r() * i)
        tmp[i-1], tmp[j-1] = tmp[j-1], tmp[i-1]

    return tmp[:-m]

l = list(range(10))
print(random_sample(l, 5))