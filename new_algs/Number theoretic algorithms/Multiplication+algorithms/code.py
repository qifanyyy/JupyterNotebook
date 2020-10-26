#Booth Multiplication Algorithm
#The project statement is - "Implement the Booth's algorithm for multiplying binary numbers"
#Author: Abhimanyu Gupta
#Purpose: Booth Implementation Project for CSE112-Computer Organization at IIIT Delhi
#Reference: https://en.wikipedia.org/wiki/Booth%27s_multiplication_algorithm

import math

def getBinNumLength(num1,num2):#num1,num2 are int 
	if num1<0:
		num1*=-1
	if num2<0:
		num2*=-1
	
	maxNum=num1 if num1>num2 else num2
	
	if maxNum==0:
		return 1
	else:
		return int(math.log2(maxNum))+1

def get2sComplement(binNum):#binNum is string of binary number
	size=len(binNum)
	
	tempBin=""
	for i in range(size):
		tempBin+="1" if binNum[i]=="0" else "0"
	
	negBinNum=binaryAdd(tempBin,"1")
	
	return negBinNum

def toBinary(num,size):#num, size are int
	flag=False
	if num<0:
		num*=-1
		flag=True
	
	binNum=""
	for i in range(size-1,-1,-1):
		k=num>>i
		if k & 1:
			binNum+="1"
		else:
			binNum+="0"
	
	if flag:
		binNum=get2sComplement(binNum)
	
	return binNum

def binaryAdd(binNum1,binNum2):#binNum1,binNum2 are strings of binary number
	if len(binNum1)!=len(binNum2):
		maxBinNumLength=len(binNum1) if len(binNum1)>len(binNum2) else len(binNum2)
		for i in range(maxBinNumLength):
			if len(binNum1)<maxBinNumLength:
				binNum1="0"+binNum1
			elif len(binNum2)<maxBinNumLength:
				binNum2="0"+binNum2
			else:
				break
	
	length=len(binNum1)
	sumBinNum=""
	carry="0"
	for i in range(length-1,-1,-1):
		bit1=binNum1[i]
		bit2=binNum2[i]
		if bit1=="1" or bit2=="1":
			count=0
			if bit1=="1":
				count+=1
			if bit2=="1":
				count+=1
			if carry=="1":
				count+=1
			if count==1:
				sumBinNum="1"+sumBinNum
				carry="0"
			elif count==2:
				sumBinNum="0"+sumBinNum
				carry="1"
			else:
				sumBinNum="1"+sumBinNum
				carry="1"
		else:
			sumBinNum=carry+sumBinNum
			carry="0"
	
	return sumBinNum

def boothMultiply(num1,num2):#num1,num2 are int
	if num2<0:
		if num1>0 or abs(num2)>abs(num1):
			num1,num2=num2,num1

	maxBinSize=getBinNumLength(num1,num2)+1
	
	num1_bin=toBinary(num1,maxBinSize)
	num2_bin=toBinary(num2,maxBinSize)
	negativeNum1_bin=toBinary(num1*-1,maxBinSize)

	A=toBinary(num1,maxBinSize)+"0"*maxBinSize+"0"
	S=negativeNum1_bin+"0"*maxBinSize+"0"
	P="0"*maxBinSize+num2_bin+"0"

	for i in range(maxBinSize):
		comp=P[len(P)-2:]
		if comp=="00" or comp=="11":
			P=P[0]+P[:len(P)-1]
		elif comp=="01":
			P=binaryAdd(P,A)
			P=P[0]+P[:len(P)-1]
		elif comp=="10":
			P=binaryAdd(P,S)
			P=P[0]+P[:len(P)-1]

	productBin=P[:len(P)-1]
	if productBin[0]=="0":
		return int(productBin,2)
	else:
		productBin=get2sComplement(productBin)
		return -1*int(productBin,2)
		
if __name__=="__main__":
	num1=int(input())
	num2=int(input())

	print(num1,num2)

	prod_bin=boothMultiply(num1,num2)

	print(prod_bin)