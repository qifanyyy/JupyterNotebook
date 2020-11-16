string1 = "ABCDEFGH"
string2 = "ABCUUUSD"

dict1 = {}
dict2 = {}

r_value = 1
counter = 0

# for i in range(len(string1)):
# 	dict1[i] = string1[i]
# print(dict1)

list1out = []
for i in range(len(string1) - r_value):
	list1= []
	for n in range(i, i+r_value):
		list1.append(string1[n])
		stringwhole = "".join(list1)
		
	list1out.append(stringwhole)
print(list1out)


list2out = []
for i in range(len(string2) - r_value):
	list2= []
	for n in range(i, i+r_value):
		list2.append(string2[n])
		stringwhole = "".join(list2)
		
	list2out.append(stringwhole)
print(list2out)

for i in list1out:
	if i in list2out:
		print("The match is found and its " + i)
		break
	else:
		print("No matches found!")
		break