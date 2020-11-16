def processInput():
    listP = []
    clause = []
    file = open("k-sat-input.txt")
    file.readline()
    file.readline()
    x = file.readline()
    dict = list(x)
    dict.pop()
    dict = [int(i) for i in dict]

    for line in file:
        line = line.split(" ")
        line.pop()
        line = [int(i) for i in line]

        for e in line:
            y = dict[abs(e) - 1]

            if y == 1:
                y = True
            else:
                y = False

            if e < 0:
                clause.append(not y)
            else:
                clause.append(y)

        listP.append(clause)
        clause = []

    file.close()
    return listP


def getOr(clause):
    res = clause[0]
    for e in range(1, len(clause) - 1):
        res = res or clause[e]
    return res


def getAnd(clause):
    res = clause[0]
    for e in range(1, len(clause) - 1):
        res = res and clause[e]
    return res


def main():
    print("K-SAT")
    final = []
    list = processInput()
    for e in list:
        final.append(getOr(e))
    res = getAnd(final)
    print("The result of the input is:", res)


main()
