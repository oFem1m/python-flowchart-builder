def sample_function(x):
    if x < 0:
        x += 5
    elif x == 0:
        return 0
    else:
        for i in range(5):
            print(i)
        x -= 5
    y = 6
    return x
