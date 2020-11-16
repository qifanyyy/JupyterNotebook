class Solution(object):
    def rainbowSort(self, array):
        """
    input: int[] array
    return: int[]
    """
        if not array:
            return
        lst = []
        sumMinusOne, sumZero, sumOne = self.count(array)
        for i in range(sumMinusOne):
            lst.append(-1)
        for i in range(sumZero):
            lst.append(0)
        for i in range(sumOne):
            lst.append(1)
        return lst

    def count(self, array):
        sumZero, sumOne, sumMinusOne = 0, 0, 0
        for i in range(len(array)):
            if array[i] == -1:
                sumMinusOne += 1
            elif array[i] == 0:
                sumZero += 1
            else:
                sumOne += 1
        return sumMinusOne, sumZero, sumOne


array = [0, 0, -1]
a = Solution()
b = a.rainbowSort(array)