"""
@author: David Lei
@since: 7/11/2017

http://www.geeksforgeeks.org/count-possible-decodings-given-digit-sequence/
"""

maping = {
    "1": "A",
    "2": "B",
    "3": "C",
    "4": "D",
    "5": "E",
    "6": "F",
    "7": "G",
    "8": "H",
    "9": "I",
    "10": "J",
    "11": "K",
    "12": "L",
    "13": "M",
    "14": "N",
    "15": "O",
    "16": "P",
    "17": "Q",
    "18": "R",
    "19": "S",
    "20": "T",
    "21": "U",
    "22": "V",
    "23": "W",
    "24": "X",
    "25": "Y",
    "26": "Z"
}


def get_decodings(digits, i, decodings):
    if i < 0:
        return decodings
    new_decodings_single = []
    new_decodings_double = []
    if digits[i] != "0":
        if not decodings:
            new_decodings_single.append(maping[digits[i]])
            new_decodings_single = get_decodings(digits, i - 1, new_decodings_single)
        else:
            for code in decodings:
                new_code = maping[digits[i]] + code
                new_decodings_single.append(new_code)
            new_decodings_single = get_decodings(digits, i - 1, new_decodings_single)
    if i < 1:
        return new_decodings_single
    # Need to get next value.
    new_digit = digits[i - 1] + digits[i]
    if int(new_digit) > 27:
        return new_decodings_single
    if not decodings:
        new_decodings_double.append(maping[new_digit])
        new_decodings_double = get_decodings(digits, i - 2, new_decodings_double)
    else:
        for code in decodings:
            new_code = maping[new_digit] + code
            new_decodings_double.append(new_code)
        new_decodings_double = get_decodings(digits, i - 2, new_decodings_double)
    decodings = []
    decodings.extend(new_decodings_single + new_decodings_double)
    return decodings

digits = "1234"
print(get_decodings(digits, len(digits) - 1, []))
# YAY OMG THIS WORKS!