"""
@author: David Lei
@since: 28/08/2016
@modified: 

Resources:
http://interactivepython.org/runestone/static/pythonds/SortSearch/Hashing.html
http://www.bogotobogo.com/python/python_hash_tables_hashing_dictionary_associated_arrays.php
http://www.tutorialspoint.com/python/python_dictionary.htm

Implementation of a hashtable

Hashtables are the underlying data structure for:
- Sets
- Dictionaries
with optimizations for their specific uses

Hashtables are unordered associate arrays (map array index to key)

Time complexity:
                     best   worst
    - Search/lookup | O(1) | O(n) |
    - Insert        | O(1) | O(n) |
    - Delete        | O(1) | O(n) |

Space complexity: O(n)
"""

"""
    Notes on dealing with collision:
    1. Open addressing (or closed hashing)
    approach: use probing (searching) through alternate locations in the array (or probe the sequence) until either the
    target is found (update) or an empty slot is found (insert)

        - Learning probing:
            when collision, go to next available spot in the array or spot = current spot + i, where i is a pre set amount
            can easily lead to worst case O(n)
            interval between probes are constant i.e. i = 4, always step by 4

        - Quadratic probing:
            same as linear probing but the interval or i is increased linearly
            i.e. for the first collision i = 4, next time i = 8 etc giving a larger step

        - Double hashing:
            interval between probes is fixed for each record (if i go to index 0 twice, will lead to same
            interval. But it is computed by another hash function (aim to spread out entries)


      2. Separate chaining
        use a linked list at each index of our array, adding a collision is just appending to the end of the linked list

    Load factor = number of items / table size

    Ideal load factor:
   1/4 (0.25) < items/tbl_size < 3/4 (0.75)
   if load factor > max it should be (i.e. bound to 0.75) --> double size of table

   input --> hash fn  --> maps to hash table

   Good hash functions:
    - take into account whole key and the position of elements in the key
    - fast
    - minimize collisions
    - approximate random functions
    - in range of table size
    - uses big primes
    """
class HashTable:
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.size = 0
        self.keys = []                          # keys
        self.table = [[] for _ in range(self.capacity)]   # 1000 buckets in our table
        # in python [] is a linked list, so this will be separate chaining

    def _look_up(self, key):
        hashed_key = self.hash_function(key)    # brings us to index of linked list
        linked_list = self.table[hashed_key]
        if linked_list is None:                 # nothing in the linked list
            return False, linked_list
        else:                                   # traverse linked list
            for pair in linked_list:            # data stored as (key, data)
                if pair[0] == key:
                    return pair, linked_list    # return the data
            return False, linked_list

    def get(self, key):
        found_entry, linked_list = self._look_up(key)
        if found_entry:
            return found_entry[1]
        else:
            return False
    def re_size(self):
        print("\nResizing")
        print("Current size: " + str(self.size) + ", new capacity: " + str(self.capacity))

        items = self.get_items()    # everything in my current table is here
        self.size = 0
        self.capacity = self.capacity*2
        self.table = [[] for _ in range(self.capacity)]   # double size of table
        self.keys = []
        for pair in items:
            key = pair[0]
            data = pair[1]
            self.add(key, data)
        print("Re-sized")
        print("Current size: " + str(self.size) + ", new capacity: " + str(self.capacity))
        print(self.get_items())
        print()

    def set(self, key, data):
        """
        used to either:
                - add an item to our hashtable
                - update an item with same key to our hashtable
        :param key: key to look up with
        :param data: data to store
        :return:
        """
        found_entry, linked_list = self._look_up(key)
        if found_entry:                              # update current entry
            #found_entry = (found_entry[0], data)     # update tuple?
            found_entry[1] = data                    # can easily update the data stored here
                                                    # make sure you store entries as [] and not () and tuple won't allow assignment
        else:                                        # make new entry
            new_entry = [key, data]
            linked_list.append(new_entry)         # insert into head of linked list in O(1) time
            self.keys.append(key)                 # add key to keys for easy return
            self.size += 1                        # increase number of elements in our hashtable
            # Append (insertion to back) is O(1), while insertion (everywhere else) is O(n)
    def add(self, key, data):
        self.set(key, data)
        if self.size/self.capacity > 0.75:
            self.re_size()

    def delete(self, key):
        found_entry, linked_list = self._look_up(key)
        if found_entry:                         # found entry is a pair (key, data)
            linked_list.remove(found_entry)
            self.size -= 1
            self.keys.remove(key)
            # list.remove(object) is an O(n) operation
            # in hashtables, this hopefuley won't take too long as
            # values spread out, linkedlist isn't long ~ O(1)
        else:
            raise KeyError(key)
        
    def hash_function(self, key):   # hash fn from FIT1008
        value = 0
        a = 31415   # a big prime
        b = 27183   # another big prime
        for i in range(len(key)):
            value = (ord(key[i]) + a * value) % self.capacity   # makes sure in range of table size
            a = a*b % self.capacity
        return value
    def keys(self):
        return self.keys

    def get_items(self):
        return [(key, self.get(key)) for key in self.keys ]
if __name__ == "__main__":
    mytable = HashTable(3)
    mytable.add('a', 'Apple')
    mytable.add('aa', 'Angry Apple')
    mytable.add('b', 'Bee')
    print(mytable.get('a'))
    print(mytable.get_items())
    mytable.add('b', 'Beefly')
    print(mytable.get_items())
    mytable.delete('a')
    print(mytable.get_items())

