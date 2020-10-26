import itertools

S = [ 'a', 'ab', 'ba' ]

for i in range(len(S)+1):
  for c in itertools.combinations(S, i):
    cc = ''.join(c)
    if len(cc) <= 6:
      print (c)

stuff = ['A', 'B', 'C']
print("COMBS 1: ")
combs_len1 = list(itertools.combinations(stuff, 1))
print(combs_len1)
print("COMBS 2: ")

combs_len2 = list(itertools.combinations(stuff, 2))
print(combs_len2)
print("COMBS 3: ")

combs_len3 = list(itertools.combinations(stuff, 3))
print(combs_len3)
print("PERMS: ")

perms = list(itertools.permutations(stuff))
print(perms)
print("PERMS 1: ")

perms_len1 = list(itertools.permutations(stuff, 1))
print(perms_len1)
print("PERMS 2: ")

perms_len2 = list(itertools.permutations(stuff, 2))
print(perms_len2)
print("PERMS 3: ")

perms_len3 = list(itertools.permutations(stuff, 3))
print(perms_len3)
