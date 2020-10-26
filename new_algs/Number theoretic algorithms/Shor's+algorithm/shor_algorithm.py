import math
import argparse


def shor_algorithm(n: int):
    for a in range(1, n):
        r = 0
        while r < n:
            if math.pow(a, r) % n == 1:
                result = [a, r]
                num1 = int(math.pow(result[0], result[1] // 2) - 1)
                num2 = int(math.pow(result[0], result[1] // 2) + 1)
                p = math.gcd(num1, n)
                q = math.gcd(num2, n)
                if p != n and q != n:
                    return [p, q]
            r = r + 2
    return []


def main():
    parser = argparse.ArgumentParser(description='Simulate Shor\'s algorithm for N.')
    parser.add_argument('n', type=int, help='The integer to factor')
    args = parser.parse_args()
    p, q = shor_algorithm(args.n)
    print("Factor P is: " + str(p) + " and " + "Factor Q is: " + str(q))


if __name__ == "__main__":
    main()
