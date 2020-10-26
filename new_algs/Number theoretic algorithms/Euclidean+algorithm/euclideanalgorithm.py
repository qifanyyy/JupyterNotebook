
def main():

    """
    The Euclidean Algorithm finds the highest common factor
    of two numbers. Here we create lists of number pairs and
    run the algorithm on it, printing out the result and the numbers
    divided by the HCF.
    """

    print("----------------------")
    print("| codedrome.com      |")
    print("| Euclid's Algorithm |")
    print("----------------------\n")

    avalues = (55, 27, 3, 14, 500, 30)
    bvalues = (5, 45, 15, 49, 12, 18)

    for i in range(0, 6):

        hcf = EuclideanHCF(avalues[i], bvalues[i])

        print("HCF of {} and {} = {}".format(avalues[i], bvalues[i], hcf))
        print("{} / {} = {:.0f}".format(avalues[i], hcf, avalues[i] / hcf))
        print("{} / {} = {:.0f}\n".format(bvalues[i], hcf, bvalues[i] / hcf))


def EuclideanHCF(a, b):

    """
    A simple implementation of a simple algorithm.
    """

    while(b != 0):
        temp = b
        b = a % b
        a = temp

    return a


main()
