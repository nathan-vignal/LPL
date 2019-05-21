a = [[1,2,3],[4,5,6]]
for b in a:
    for c in b:
        if c == 2:
            continue
        print(c)