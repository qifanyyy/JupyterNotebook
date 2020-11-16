import math

product = 0
arr = []
arrLen1 =[]
arrLen1 =[]

countArr = []
x = 567
y = 12
x= max(x, y)
y = min(x, y)
length = 0
count = len(str(x)) * len(str(y))
countMinus = 0
first = 0

i = 1
while(i < y):
    yDigit = math.floor(y/i%10)
    product = x * yDigit * i
    arr.append(product)
    j = 1
    while (j < x):
        xDigit = math.floor(x / j % 10)
        if (xDigit * yDigit >= 10):
            count += 1
            if (len(str(j)) == len(str(x))):
                count-=1
                # print("-: "+str(1 / len(str(y))))
                # print("x: "+str(xDigit)+" y: "+str(yDigit))

        j *= 10
    i *= 10

# print('countMinus: '+str(countMinus))
# print("count: "+str(count))
i = 0
while(i < len(arr)):
    arr[i] = [int(d) for d in str(arr[i])]
    i+=1
# print(arr)

len1 = None
len2 = None
setFirstToOneLessThanMaxLen = False
i = 0
f = 0
while(i < len(arr)-1):
    if(len(arr[i]) > len(arr[i+1])):
        minLen1 = len(arr[i+1])
        maxLen1 = len(arr[i])
    elif(len(arr[i]) < len(arr[i+1])):
        minLen1 = len(arr[i])
        maxLen1 = len(arr[i+1])
    else:
        minLen1 = len(arr[i])
        maxLen1 = len(arr[i])
        setFirstToOneLessThanMaxLen = True
    len1 = maxLen1 - minLen1
    if (f == 0):
        if setFirstToOneLessThanMaxLen == True:
            first = maxLen1 - 1
        else:
            first = maxLen1 - len1 * 2
    #     print("first: " + str(first))
    # print("Max Len: "+str(maxLen1))
    # print("Min Len: "+str(minLen1))
    # print("len1: "+str(len1))
    # print("-----------------------------")
    if(i <= len(arr) - 3):
        if (len(arr[i+1]) > len(arr[i + 2])):
            minLen2 = len(arr[i + 2])
            maxLen2 = len(arr[i+1])
        elif (len(arr[i+1]) < len(arr[i + 2])):
            minLen2 = len(arr[i+1])
            maxLen2 = len(arr[i + 2])
        else:
            minLen2 = len(arr[i+1])
            maxLen2 = len(arr[i+1])
        len2 = maxLen2 - minLen2
        # print("Max Len2: " + str(maxLen2))
        # print("Min Len2: " + str(minLen2))
        # print("len2: " + str(len2))
    if(len1 != None) and (len2 != None):
        if (len1 == len2):
            countArr.append(first)
            # print("len1 == len2: "+str(len1))
            # print("len2 == len1: "+str(len2))
        elif (len1 < len2):
            first -= len2
            countArr.append(first)
            # print("len1 < len2: " + str(len1))
            # print("len2 < len1: " + str(len2))
        else:
            first += len2
            countArr.append(first)
            # print("len1 > len2: " + str(len1))
            # print("len2 > len1: " + str(len2))
    if(len2 == None):
        countArr.append(first)
    f+=1
    i+=1
# print("countArr: ")
# print(countArr)
# print("count: "+str(count))
# print(arr)

for i in range(0, len(arr)-1):
    while(len(arr[i])!=len(arr[len(arr)-1])):
        arr[i].insert(0,0)
# print("arr:")
# print(arr)

result = [sum(e) for e in zip(*arr)]
# print("result: ")
# print(result)

i = len(result)-1
while(i >= 1):
    if (result[i]>=10):
        addNum = math.floor(result[i]/10%10)
        #print("result i:"+str(result[i])+" addNum: "+str(addNum))
        result[i-1]+=addNum
    i-=1

for ind in range(0, len(result)):
    if result[ind] >= 10:
        count+=1
# print(result)

# print(result)
if result[0] >=10:
    count-=1
count += sum(countArr)
print("Number of Steps: "+str(count))



# for (var i = 0; i < arr.length; i++) {
# for (var j = 0; j < arr[i].length; j++) {
# if ((i <= arr.length - 2)) {
# arr[i+1][j] += arr[i][j]
# if (arr[i][j] >= 10) {count++;}
# }
# }
# }
# console.log(arr2)
#
# count += countArr.reduce((a, b) => a + b, 0);
# console.log('count: '+count)
# console.log("countArr: ");
# console.log(countArr);
