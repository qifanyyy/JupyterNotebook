import sys

class Hanoi:
	def __init__(self, N, verbose = False):
		if (N > 0):
			self.number = N
		else:
			raise ValueError("Wrong number of disks!")

		self.peg = [list(reversed(range(self.number + 1))), [], []]
		self.peg[0].remove(0)
		self.display()
		self.showEachMove = verbose
		self.numberOfMoves = 0
		self.recursionDepth = 0

	
	def display(self):
		for i in range(3):
			print ("{0}: {1}".format(i, self.peg[i]))
		print ()
	

	def move(self, source, target):
		if source:
			disk = source.pop()
			if (len(target) > 0):
				if (disk > target[len(target) - 1]):
					sys.exit("Wrong move on smaller disk!")
			
			target.append(disk)
			self.numberOfMoves += 1
			if self.showEachMove:
				self.display()
		else:
			print ("Wrong move!")


	def solve(self):
		self.solveLevel(self.number, self.peg[0], self.peg[1], self.peg[2])
		if (self.showEachMove == False):
			self.display()
		print ("The number of moves was", self.numberOfMoves)
		print ("The recursion depth was", self.recursionDepth)


	def solveLevel(self, N, source, helper, target):
		self.recursionDepth += 1
		if (N > 0):
			self.solveLevel(N - 1, source, target, helper)  # move tower of size N-1 to helper
			self.move(source, target)  # move disk from source peg to target peg
			self.solveLevel(N - 1, helper, source, target)


if (len(sys.argv) < 2):
	sys.exit("The program needs the number of disks as an argument")

showEachMove = False

if (sys.argv[1] == '-v'):
	showEachMove = True
	numberPosition = 2
elif ((len(sys.argv) > 2) and (sys.argv[2] == '-v')):
	showEachMove = True
	numberPosition = 1
else:
	numberPosition = 1

#print (numberPosition)
#print (sys.argv[numberPosition])

try:
	number = int(sys.argv[numberPosition])
except:
	sys.exit("The program needs the number of disks as an argument")

hanoi = Hanoi(number, showEachMove)
hanoi.solve()