#Booths Algorithm

from convert import *
from boothfunctions import *

def prod(num1,num2):
	bNum1=convertToBinary(num1)
	bNum2=convertToBinary(num2)

	revbNum1=convertToBinary(-num1)		

	result=[0]*8
	result.extend(bNum2)
	result.append(0)

	bNum1=bNum1+[0]*9
	revbNum1=revbNum1+[0]*9			

	for i in range(8):
		if result[-2] == 1 and result[-1] == 0:
			result=add(result, revbNum1)
		elif result[-2] == 0 and result[-1] ==1:
			result=add(result,bNum1)
		result=RightShift(result)

	result=result[:-1]
	return convertToDecimal(result)