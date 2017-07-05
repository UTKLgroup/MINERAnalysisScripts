def order_by_time(x1, x2):
    e1 = x1.time()
    e2 = x2.time()
    if e1 > e2:
        return 1
    if e1 == e2:
        return 0
    if e1 < e2:
        return -1


def order_by_energy(x1, x2):
    e1 = x1.Ekin()
    e2 = x2.Ekin()
    if e1 > e2:
        return 1
    if e1 == e2:
        return 0
    if e1 < e2:
        return -1
