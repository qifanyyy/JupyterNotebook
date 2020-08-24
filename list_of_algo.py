import re
list_of_algos=[]
'''
    create a list of algos, before:, no special char
'''
with open("list_of_algorithms.txt") as f:
    for lines in f.readlines():
        if lines[0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" :
            lines= lines[2:]
        if lines[:2] == "o ":
            lines= lines[2:]
        lines= lines.strip()
        for every_word in lines:
            if ":" in lines:
                lines= lines.split(':')[0]
        ##for each letter in the string if not number or character then replace it with blank space 
            
            if lines not in list_of_algos:
                if lines[0] not in "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, a	b	c	d	e	f	g	h	i	j	k	l	m	n	o	p	q	r	s	t	u	v	w	x	y	z" :
                    lines= lines[2:]
                    if "edit" in lines:
                        lines= lines[:-6]
                    list_of_algos.append(lines)
                else:
                    if "edit" in lines:
                        lines= lines[:-6]
                if ("algorithm" not in lines) and ("Algorithm" not in lines):
                    lines+= " algorithm"
                list_of_algos.append(lines)

for index in range(len(list_of_algos)):
    for every_word in list_of_algos[index]:
        if (every_word.isalnum() or every_word.isalpha()):
            if every_word.isascii() or every_word=="'" or every_word=="*":
                continue
            else:
                list_of_algos[index]=list_of_algos[index].replace(every_word,' ')
        else:
            if every_word!="'" and every_word!="*" and every_word!="-":
                list_of_algos[index]=list_of_algos[index].replace(every_word,' ')

print (len(list_of_algos))
with open("output_of_algos.txt", "w") as output:
    output.write(str(list_of_algos))