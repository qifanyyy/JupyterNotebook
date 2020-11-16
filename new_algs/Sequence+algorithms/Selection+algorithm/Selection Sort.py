class Solution(object):
  def solve(self, array):
    """
    input: int[] array
    return: int[]
    """
    # write your solution here
    if not array or len(array) == 0:
      return array
    for i in range(len(array) - 1):
      min_idx = i
      for j in range(i, len(array) - 1):
        if array[j + 1] < array[min_idx]:
          min_idx = j + 1
      array[i], array[min_idx] = array[min_idx], array[i]
    return array

array=[ ]
ans=Solution()
ex=ans.solve(array)
print(ex)
