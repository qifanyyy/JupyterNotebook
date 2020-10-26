def Karatsuba_multiplication(x, y):
    global odd_count
    if x < 10 and y < 10:
        return x * y
    else:
        if x < 10 and y > 9:
            a = 1
            b = x
            c = int(y / 10 ** (int(len(str(y)) / 2)))
            d = int(y % 10 ** (int(len(str(y)) / 2)))
        elif y < 10 and x > 9:
            a = 1
            b = y
            c = int(x / 10 ** (int(len(str(x)) / 2)))
            d = int(x % 10 ** (int(len(str(x)) / 2)))
        else:
            a = int(x / 10 ** (int(len(str(x)) / 2)))
            b = int(x % 10 ** (int(len(str(x)) / 2)))
            c = int(y / 10 ** (int(len(str(y)) / 2)))
            d = int(y % 10 ** (int(len(str(y)) / 2)))
        if x > y:
            z = (10 ** (int(len(str(x))))) * (Karatsuba_multiplication(a, c)) + (10 ** (int(len(str(x)) / 2))) * (
                    Karatsuba_multiplication(a, d) + Karatsuba_multiplication(b, c)) + Karatsuba_multiplication(b,
                                                                                                                d)

            return z
        else:
            z = (10 ** (int(len(str(y))))) * (Karatsuba_multiplication(a, c)) + (10 ** (int(len(str(y)) / 2))) * (
                    Karatsuba_multiplication(a, d) + Karatsuba_multiplication(b, c)) + Karatsuba_multiplication(b,
                                                                                                                d)

            return z


def input_a():
    global odd_count
    global a
    try:
        a = int(input(" First number : "))
        if len(str(a)) % 2 == 1:
            a = a * 10
            odd_count = 1
    except:
        print("Sorry, we only accept integers. Please provide a number")
        input_a()


def input_b():
    global odd_count
    global b
    try:
        b = int(input(" Second number : "))
        if len(str(b)) % 2 == 1:
            b = b * 10
            odd_count = odd_count + 1
    except:
        print("Sorry, we only accept integers. Please provide a number")
        input_b()


if __name__ == "__main__":
    global a, b, odd_count
    input_a()
    input_b()
    print("\nAnswer : ", Karatsuba_multiplication(a, b) / (10 ** odd_count))
