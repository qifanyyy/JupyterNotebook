from time import time


def fix_predigits(pi_digits, curr_index=-1):
    if pi_digits[curr_index] + 1 == 10:
        pi_digits[curr_index] = 0
        fix_predigits(pi_digits, curr_index - 1)
    else:
        pi_digits[curr_index] += 1
        pi_digits.append(0)


def spigot_algorithm(digits):
    array_len = int(10 * digits / 3) + 1
    array = [2] * array_len
    carry = 0
    curr_sum = 0
    pi_digits = []

    for _ in range(digits):
        for j in reversed(range(array_len)):
            num = j
            denom = num * 2 + 1

            curr_sum = array[j] * 10 + carry  # multiply by 10 and sum
            array[j] = curr_sum % denom if j > 0 else curr_sum % 10  # remainder
            carry = int(curr_sum / denom) * num

        predigit = int(curr_sum / 10)
        if predigit > 9:
            fix_predigits(pi_digits)
        else:
            pi_digits.append(int(curr_sum / 10))

    return pi_digits


if __name__ == '__main__':
    DIGITS = 100

    t1 = time()
    pi_digits = spigot_algorithm(DIGITS)
    t2 = time()

    print(f'{pi_digits.pop(0)}.{"".join([str(d) for d in pi_digits])}')
    print(f'\nCalculated {DIGITS} π digits in {t2 - t1} seconds')
