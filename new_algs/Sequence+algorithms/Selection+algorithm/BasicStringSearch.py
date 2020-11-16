'''
    Brute Force String Search

    Repeated shift T one place along S and then compare the characters of T with those of S.
    Do this until a match of T in S is found, or the end of S is reached

    :param string   T   The pattern to search for in S
    :param string   S   The string to search for the pattern in

    :return integer
'''
def search(T, S):
    sI = 0
    while sI + len(T) <= len(S):
        tI = 0
        while tI < len(T) and T[tI] == S[sI + tI]:
            tI = tI + 1
        if tI == len(T):
            return sI
        sI = sI + 1
    return -1
