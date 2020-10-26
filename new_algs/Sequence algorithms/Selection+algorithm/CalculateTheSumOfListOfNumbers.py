def listSum(numList):
    result = 0
    for i in numList:
        result = result + i
    return result


if __name__ == "__main__":
    print("The sum of [1, 2, 3, 4, 5] is:")
    print(listSum([1, 2, 3, 4, 5]))