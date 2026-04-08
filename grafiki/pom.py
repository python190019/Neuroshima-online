for i in range(5):
    s = "["
    for j in range(9):
        s += '"' + "None" + '"' + ', '
    s += "]"
    print(s[0:(len(s)-3)] + "]")