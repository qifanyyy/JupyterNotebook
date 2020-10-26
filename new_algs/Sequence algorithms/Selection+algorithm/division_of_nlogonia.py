
flag = int(input().strip())
while flag != 0:
	queries = flag
	div_x, div_y = [int(x) for x in input().split()]
	for j in range(queries):
		pt_x, pt_y = [int(x) for x in input().split()]
		if pt_x == div_x or pt_y == div_y: # On boarder.
			print("divisa")
		elif pt_x < div_x and pt_y > div_y: # NorthWestern.
			print("NO")
		elif pt_x > div_x and pt_y > div_y: # NorthEastern.
			print("NE")
		elif pt_x < div_x and pt_y < div_y: # SouthWestern.
			print("SO")
		elif pt_x > div_x and pt_y < div_y: # SouthEastern.
			print("SE")
		else:
			raise KeyError
	# Read next test case.
	flag = int(input().strip())
	if flag == 0:
		break
