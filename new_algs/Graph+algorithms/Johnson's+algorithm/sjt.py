import cProfile

#sjt needs a sorted set
#we should just assume our list is sorted though...
def sjt(items, time=False):
  def innerSJT(items):
    perms = []
    #default direction of items in sjt
    dirItems = [["<-", i] for i in items]

    if len(items) == 0:
      return perms

    perms.append(outputPermutation(dirItems))

    while True:
      mobileIndex = largestMobileIndex(dirItems)

      if mobileIndex == -1: #Stop when no more mobile items exist
        break;

      mobileIndex += swapItemInDirection(mobileIndex, dirItems)

      perms.append(outputPermutation(dirItems))

      revItemDirectionLargerThen(mobileIndex, dirItems)

    return perms

  if time:
    #profile in context because of inner function
    return cProfile.runctx('innerSJT(items)', None, locals())
  else:
    return innerSJT(items)


def swapItemInDirection(i, items):
  if items[i][0] == "->":
    items[i], items[i+1] = items[i+1], items[i]
    return 1
  else:
    items[i], items[i-1] = items[i-1], items[i]
    return -1


def largestMobileIndex(items):
  largest = 0
  largestIndex = -1

  for i, _ in enumerate(items):
    if isMobile(i, items):
      if largest < items[i][1]:
        largest = items[i][1]
        largestIndex = i

  return largestIndex

# The Mobility of an item is defined as:
# if the first item, [0], direction is left, "<-" then it is NOT mobile
# if the last item, [n-1], direction is right, "->" then it is NOT mobile
# if the item our item is pointing to is bigger then our item then is NOT mobile
# otherwise it IS mobile 
def isMobile(i, items):
  if i == 0 and items[i][0] == "<-":
    return False

  if i == len(items)-1 and items[i][0] == "->":
    return False

  if items[i][0] == "<-":
    return items[i][1] > items[i-1][1]
  else:
    return items[i][1] > items[i+1][1]


def revItemDirectionLargerThen(i, items):
  for j, _ in enumerate(items):
    if items[j][1] > items[i][1]:
      if items[j][0] == "<-":
        items[j][0] = "->"
      else:
        items[j][0] = "<-"


def outputPermutation(items):
  permutation = []
  for item in items:
    permutation.append(item[1])

  return permutation
  