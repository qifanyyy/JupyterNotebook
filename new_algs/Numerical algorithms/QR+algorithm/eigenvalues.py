#Edward Harianto
import numpy as np

def isDiagonal(mat):
	for i in range(len(mat)):
		for j in range(len(mat)):
			if(i == j):
				continue
			else:
				if (abs(mat[i][j]) > 0.001):
					return False
	return True

def qrAlgorithm(mat):
	num = 0
	
	while(True):
		q,r = np.linalg.qr(mat)
		mat = np.dot(r,q)
		
		if(isDiagonal(mat)):
			break
		num+=1

	print('QR Factoriztion matrix')
	print(mat)
	print(str(num) + ' iterations')
	
	count = 1
	for i in range(len(mat)):
		for j in range(len(mat)):
			if (i == j):
				print("lambda " + str(count) + ": " + str(mat[i][j]))
				count+=1

 

def main():
	mat = [[2,0,2,0,2],[0,3,0,3,0],[2,0,2,0,2],[0,3,0,3,0],[2,0,2,0,2]]
	matrix = np.array(mat)
	
	qrAlgorithm(matrix)	



if __name__ == '__main__':
	main()