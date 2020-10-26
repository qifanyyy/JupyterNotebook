import numpy as np
import math
import datetime


def Rank(Q, t):
    x = 0
    for i in range(len(Q)):
        if Q[i] < t:
            x += 1
    return x


def getSample(S, s):
    sample = [0 for _ in range(s)]
    for i in range(s):
        sample[i] = S[int(np.random.rand() * len(S))]
    return sample


def lazySelect(k):
    n_3_4 = int(math.pow(math.sqrt(math.sqrt(n)), 3))
    x = (k * math.pow(math.sqrt(math.sqrt(n)), -1))
    l = int(max(0, (x - math.sqrt(n))))
    h = int(min(n_3_4, (x + math.sqrt(n))))
    start = datetime.datetime.now()
    while 1 == 1:
        R = getSample(data, n_3_4)
        quickSort(R, 0, int(n_3_4 - 1))
        L = R[l]
        H = R[h]
        Lp = Rank(data, L)
        # print(L)
        Hp = Rank(data, H)
        # print(H)
        P = []
        for i in range(n):
            if (data[i] >= L) & (data[i] <= H):
                    P.append(data[i])
        if (Lp <= k) & (k <= Hp) & (len(P) <= 4 * n_3_4 + 1):

            quickSort(P, 0, len(P) - 1)
            result = P[k - Lp]
            break
    end = datetime.datetime.now()
    print("lazyselect: " + str(result) + "   耗时：" + str(end - start) )


def quickSort(array, begin, end):
        if begin < end:
            i = begin + 1
            j = end
            while i < j:
                if array[i] > array[begin]:  # 如果比较的数组元素大于基准数，则交换位置。
                    t=array[i]
                    array[i]=array[j]
                    array[j]=t
                    j = j - 1
                else:
                    i += 1  # 将数组向后移一位，继续与基准数比较。
            if array[i] >= array[begin]:  # 这里必须要取等“>=”，否则数组元素由相同的值时，会出现错误！
                i = i - 1
            t = array[i]
            array[i] = array[begin]
            array[begin] = t
            quickSort(array, begin, i)
            quickSort(array, j, end)


def Sort():
    start = datetime.datetime.now()
    quickSort(data, 0, len(data) - 1)
    if n % 2 == 0:
        result = data[int(n/2)]
    else:
        result = (data[int((n+1)/2)] + data[int((n-1)/2)])/2
    end = datetime.datetime.now()
    print("排序结果：" + str(result) + "   耗时：" + str(end - start))


def exch (array, i, j):
    if i != j:
        array[i] ^= array[j]
        array[j] = array[i] ^ array[j]
        array[i] ^= array[j]


def select_middle(array, beg, end, n):
    if n == 1:
        return array[1]
    i = beg
    for j in range(i + 1, end):
        if array[j] <= array[beg]:
            i += 1
            exch(array, i, j)
    exch(array, beg, i)
    if i < n / 2:
        return select_middle(array, i + 1, end, n)
    elif i > n / 2:
        return select_middle(array, beg, i - 1, n)
    else:
        if n % 2 == 0:
            return array[i]
        else:
            m = array[0]
            for j in range(1, i - 1):
                if array[j] > m:
                    m = array[j]
            return (array[i] + m) / 2


def Sort_1():
    start = datetime.datetime.now()
    result = select_middle(data, 0, len(data) - 1, len(data))
    end = datetime.datetime.now()
    print("线性结果：" + str(result) + "耗时：" + (str(end - start)))


if __name__ == '__main__':
    n = 10000
    # data = np.random.rand(n)
    # data = np.random.normal(1, 3, n)
    data = np.random.zipf(3, n)
    # print(data)
   #  Sort()
    # Sort_1()
    lazySelect(int(n/2))





