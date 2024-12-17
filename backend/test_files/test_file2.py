def test_file2(xs):
    for x in xs:
        a = -1
        if x % 2 == 0:
            print("четное", a)
            if x % 4 == 0:
                print("кратно 4", a)
                break
    else:
        print("Все нечетные")
    return 0