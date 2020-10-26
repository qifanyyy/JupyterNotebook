# Compute the extended euclidean algorithm, returns the GCD and the Bezout Coefficients
def ext_euclid(a, b):
    a, b = abs(a), abs(b)
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def main():
    print("---- Extended Euclidean Algorithm ----\n")

    # Get user input
    while True:
        try:
            a = int(input("Insert the first integer: "))
            b = int(input("Insert the second integer: "))
            break
        except ValueError:
            print("\nYou must enter two integer.\n")

    # Execute the extended euclidean algorithm and print the results
    gcd, x, y = ext_euclid(a, b)
    print("\nGreatest Common Divisor (GCD):", gcd)
    print("Bezout Coefficients (x, y):", "(", x, ",", y, ")")


if __name__ == '__main__':
    main()
