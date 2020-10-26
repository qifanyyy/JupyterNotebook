"""
@author: David Lei
@since: 28/08/2016
@modified:


https://www.quora.com/How-is-set-implemented-internally-in-python

It is a hash table, implemented very similarly the Python dict with some optimizations
that take advantage of the fact that the values are always null (in a set, we only care about the keys).
Set operations do require iteration over at least one of the operand tables (both in the case of union).
Iteration isn't any cheaper than any other collection ( O(n) ), but membership testing is O(1) on average.

"""

# Building dict.
dummy_dict = {}
dummy_dict['a'] = 'Apple'
dummy_dict['b'] = 'Batman'
dummy_dict['c'] = 'Candy'
dummy_dict['e'] = 'Egg Yolk'
dummy_dict['f'] = 'Frogs'
dummy_dict['g'] = 'Gnome'

key_value_pairs = [('burger', 10), ('chips', 100), ('greens', 2)]
yum = dict(key_value_pairs)
print(yum.items())
print(yum['burger'])

# Iteration.
for key in dummy_dict:
    print(str("key: " + str(key) + ", value: " + str(dummy_dict[key])))
for key, value in dummy_dict.items():
    print("key: %s, value: %s" % (key, value))

# Getting stuff.
print(dummy_dict.get('a'))
print(dummy_dict['a'])

# Deleting stuff.
del dummy_dict['a']
dummy_dict.pop('b')    # dictionary.pop(key, default)
print(dummy_dict.items())

# Keys can be anything that it not mutable (integers, keys, tuples).

# Comprehension, mapping of n: n ** 2.
squared_even_numbers = {n: n ** 2 for n in range(2, 100, 2)}
print(squared_even_numbers.keys())
print(squared_even_numbers.values())