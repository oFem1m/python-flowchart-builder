def complex_function(x, y, z):
    if x > 0:
        for i in range(x):
            print(f"Iteration {i}")
            if i % 2 == 0:
                print("Even iteration")
                if y > 5:
                    while y > 0:
                        print(f"y = {y}")
                        y -= 1
                elif y < 5:
                    for j in range(y):
                        print(f"Inner iteration {j}")
                        if j == 3:
                            break
                else:
                    print("y is exactly 5")
            else:
                print("Odd iteration")
                if z > 10:
                    while z > 0:
                        print(f"z = {z}")
                        z -= 2
                elif z < 10:
                    for k in range(z):
                        print(f"Inner iteration {k}")
                        if k == 5:
                            continue
                else:
                    print("z is exactly 10")
    elif x < 0:
        for i in range(abs(x)):
            print(f"Negative iteration {i}")
            if i % 3 == 0:
                print("Divisible by 3")
                if y > 10:
                    while y > 0:
                        print(f"y = {y}")
                        y -= 2
                elif y < 10:
                    for j in range(y):
                        print(f"Inner iteration {j}")
                        if j == 7:
                            break
                else:
                    print("y is exactly 10")
            else:
                print("Not divisible by 3")
                if z > 20:
                    while z > 0:
                        print(f"z = {z}")
                        z -= 3
                elif z < 20:
                    for k in range(z):
                        print(f"Inner iteration {k}")
                        if k == 10:
                            continue
                else:
                    print("z is exactly 20")
    else:
        print("x is zero")
        if y > 0:
            for i in range(y):
                print(f"Positive y iteration {i}")
                if i % 4 == 0:
                    print("Divisible by 4")
                    if z > 30:
                        while z > 0:
                            print(f"z = {z}")
                            z -= 4
                    elif z < 30:
                        for j in range(z):
                            print(f"Inner iteration {j}")
                            if j == 15:
                                break
                    else:
                        print("z is exactly 30")
                else:
                    print("Not divisible by 4")
                    if z > 40:
                        while z > 0:
                            print(f"z = {z}")
                            z -= 5
                    elif z < 40:
                        for k in range(z):
                            print(f"Inner iteration {k}")
                            if k == 20:
                                continue
                    else:
                        print("z is exactly 40")
        else:
            print("y is non-positive")
            if z > 0:
                for i in range(z):
                    print(f"Positive z iteration {i}")
                    if i % 5 == 0:
                        print("Divisible by 5")
                        if y < -5:
                            while y < 0:
                                print(f"y = {y}")
                                y += 1
                        elif y > -5:
                            for j in range(abs(y)):
                                print(f"Inner iteration {j}")
                                if j == 2:
                                    break
                        else:
                            print("y is exactly -5")
                    else:
                        print("Not divisible by 5")
                        if y < -10:
                            while y < 0:
                                print(f"y = {y}")
                                y += 2
                        elif y > -10:
                            for k in range(abs(y)):
                                print(f"Inner iteration {k}")
                                if k == 5:
                                    continue
                        else:
                            print("y is exactly -10")
            else:
                print("z is non-positive")
