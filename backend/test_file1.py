def power(x, n):
    res = 1
    i = 0
    while i < n:
        res *= x
        i += 1
    return res
