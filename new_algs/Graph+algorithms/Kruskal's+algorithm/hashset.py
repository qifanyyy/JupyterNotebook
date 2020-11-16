class HashSet:
    class __Placeholder:
        def __init__(self):
            pass

        def __eq__(self, other):
            return False

    def __add(item, items):
        idx = hash(item) % len(items)
        loc = -1

        while items[idx] != None:
            if items[idx] == item:
                # item already in set
                return False

            if loc < 0 and type(items[idx]) == HashSet.__Placeholder:
                loc = idx

            idx = (idx + 1) % len(items)

        if loc < 0:
            loc = idx

        items[loc] = item

        return True

    def __remove(item, items):
        idx = hash(item) % len(items)

        while items[idx] != None:
            if items[idx] == item:
                nextIdx = (idx + 1) % len(items)
                if items[nextIdx] == None:
                    items[idx] = None
                else:
                    items[idx] = HashSet.__Placeholder()
                return True

            idx = (idx + 1) % len(items)

        return False

    def __rehash(oldList, newList):
        for x in oldList:
            if x != None and type(x) != HashSet.__Placeholder:
                HashSet.__add(x, newList)

        return newList

    def __init__(self, contents=[]):
        self.items = [None] * 10
        self.numItems = 0

        for item in contents:
            self.add(item)

    def __str__(self):
        return str(self.__repr__())

    def __repr__(self):
        cleanItems = []
        for item in self.items:
            if item != None and type(item) != HashSet.__Placeholder:
                cleanItems.append(item)
        return str(cleanItems)

    def __iter__(self):
        for i in range(len(self.items)):
            if self.items[i] != None and type(self.items[i]) != HashSet.__Placeholder:
                yield self.items[i]

                # Following are the mutator set methods

    def add(self, item):
        if HashSet.__add(item, self.items):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= 0.75:
                self.items = HashSet.__rehash(self.items, [None] * 2 * len(self.items))

    def remove(self, item):
        if HashSet.__remove(item, self.items):
            self.numItems -= 1
            load = max(self.numItems, 10) / len(self.items)
            if load <= 0.25:
                self.items = HashSet.__rehash(self.items, [None] * int(len(self.items) / 2))
        else:
            raise KeyError("Item not in HashSet")

    def discard(self, item):
        if HashSet.__remove(item, self.items):
            self.numItems -= 1
            load = max(self.numItems, 10) / len(self.items)
            if load <= 0.25:
                self.items = HashSet.__rehash(self.items, [None] * int(len(self.items) / 2))

    def update(self, other):
        for item in other:
            self.items.add(item)

    def intersection_update(self, other):
        for item in self.items:
            if item != None and type(item) != HashSet.__Placeholder and item not in other:
                self.discard(item)

    def difference_update(self, other):
        for item in other:
            self.discard(item)

    # Following are the accessor methods for the HashSet
    def __len__(self):
        numItems = 0
        for item in self.items:
            if item != None and type(item) != HashSet.__Placeholder:
                numItems += 1
        return numItems

    def __contains__(self, item):
        idx = hash(item) % len(self.items)
        while self.items[idx] != None and self.items[idx] != HashSet.__Placeholder:
            if self.items[idx] == item:
                return True

            idx = (idx + 1) % len(self.items)

        return False

    def intersection(self, other):
        intersectionSet = HashSet()
        for item in self:
            if item in other and item != None and type(item) != HashSet.__Placeholder and item in other:
                intersectionSet.add(item)
        return intersectionSet

    # return elements in self that are not in other
    def difference(self, other):
        diffSet = HashSet()
        for item in self.items:
            if item != None and item not in other:
                diffSet.add(item)
        return diffSet

    def __eq__(self, other):
        if self.__len__() != len(other):
            return False
        numSame = 0
        for item in self.items:
            if type(item) != HashSet.__Placeholder:
                if item in other:
                    numSame += 1
        if self.__len__() == numSame:
            return True
        return False