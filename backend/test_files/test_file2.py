def test_file2(xs):
    for x in xs:
        a = 1
        if x % 2 == 0:
            print("четное", a)
            if x % 4 == 0:
                print("кратно 4", a)
                break
            elif x % 3 == 0:
                print("Кратно 3")
                break
            else:
                x = 0
            x += 2
    else:
        print(123)
    print(321)
    return 0
