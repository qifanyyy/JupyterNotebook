def Selection_Sort(nums):
    for i in range(10):
        minpos = i
        for j in range(i,11):
            if nums[j] < nums[minpos]:
                minpos = j
        temp = nums[i]
        nums[i] = nums[minpos]
        nums[minpos] = temp
        print(nums)

nums = [5,3,7,2,4,1,11,8,10,9,6]
Selection_Sort(nums)
print(nums)