'''																BOOTH’S ALGORITHM
Name: Shubham Lohan 
Roll No: 2019275
Computer Organization
Group 01

'''

check=False		#true if any  one of the no is negative
max_no=0		#takes absolute max no in Integer
max_bit=0		#takes max bits used by that max no
space=""		#to make a fix seperation of length of maxbit
def main():
	global max_no,check
	multiplicand_dec = input("Enter your 1st Number: ")
	multiplier_dec = input("Enter your 2nd Number: ")
	if((int(multiplicand_dec)<0 and int(multiplier_dec)>0 )or int(multiplicand_dec)>0 and int(multiplier_dec)<0):
		check=True
	if (int(multiplicand_dec)==0 or int(multiplier_dec)==0 ):
		print("Result : 0")
	else:
		max_no=max(abs(int(multiplicand_dec)),abs(int(multiplier_dec)))
		multiplicand_bin = covert_Dec_to_binary(multiplicand_dec)
		multiplier_bin = covert_Dec_to_binary(multiplier_dec)
		booths_multiplication(multiplicand_bin, multiplier_bin)
def booths_multiplication(mcand, plier):
	global max_bit,check,space				
	# print("multipcand: " + mcand + " multiplier: " + plier)								
	acc="0"*max_bit   			#storing acc default value (000..)
	product=acc+plier+"0"		#product contains first accum. of length maxbit then multipier and last bit of Q(intially 0) 		
	# print("Steps\t"+"Accumulator"+space+"Q"+space+"\tQ-1")		
	for i in range(1,max_bit+1):			#loop runs of max bit 
		print(product_value(i, product))		#print  value of Acc and Q and Q-1	
		operation = product[len(product)-2:]
		product = perform_operation(product,mcand,operation)
		
	product = ASR(product)
	if (check):				#true -> any one of multipler or multiplicand is neqative(not both)
		print("Binary result: "+product[1:])
		temp=result(product[1:])	#two's complement the resulted product because of negative value  		
		print("Binary result(absolute): " + temp)
		print("Decimal result: -" + str(int(result(product),2)))

	else:
		print("Binary result: "+str(product[1:]))			#required binary result 
		print("Decimal result: "+str(int(product,2)))		#required decimal result
	return
def result(product):				#to make -ve result to +ve result in binary
	tempstr=product[::-1]
	u=tempstr.find("1")
	t=len(tempstr)-u-1
	temp=''
	if  t==-1:
		temp=flipped(product)
		return temp
	else:
		temp=flipped(product[:t])
		return temp+product[t:]

def flipped(temp):
	tempstr=""
	for i in temp:
		if i=="0":
			tempstr+="1"
		else:
			tempstr+="0"
	return tempstr
		
def perform_operation(product,mcand,operation):		#perform operation by comparing value of Q and Q-1 
    if operation == "00" or operation=="11":		# if it is 00 or 11 then no operation only Arithmatic Shift Operation
        product = ASR(product)	
        # print("No operation")
        return product
    elif operation == "01":				#if it is 01 then Addition(A=A+M) is performed and then ASR
        temp = binAdd(product[:max_bit],mcand)
        product = temp + product[max_bit:]
        product = ASR(product)
        return product
    elif operation == "10":				#if it is 10 then Subtraction(A=A-M) is performed and then ASR
        ##Product = Product - mcand
        temp= subtraction(product[:max_bit],mcand)
        product=temp+product[max_bit:]
        product = ASR(product)
        # print("A=A-M")
        return product

def subtraction(product,mcand):			#binary subtraction between product and multiplicand
	carry = 0
	answer = ""
	for i in range(len(product)-1,-1,-1):
		if (mcand[i] == "1" and product[i] == "0"):
			if (carry == 1):
				answer = "0" + answer
			else:
				answer = "1" + answer
				carry = 1
		elif (mcand[i] == "1" and product[i] == "1"):
			if (carry == 1):
				answer = "1" + answer
				carry = 1

			else:
				answer = "0" + answer
		elif (mcand[i] == "0" and product[i] == "1"):
			if (carry == 1):
				answer = "0" + answer
				carry = 0
			else:
				answer = "1" + answer

		elif (mcand[i] == "0" and product[i] == "0"):
			if (carry == 1):
				answer = "1" + answer
			else:
				answer = "0" + answer
	return answer

def ASR(product):				#Arithmatic shift right
    product = product[0]+product[:len(product)-1]
    return product


##Adds the two binary strings
def binAdd(accumulator, Q):
    product = ""
    carry = 0
    for i in range(len(accumulator) - 1, -1, -1):
        if carry == 0:
            if accumulator[i] == "1" and Q[i] == "1": #case 1 and 1
                product = "0" + product
                carry = 1
            elif accumulator[i] == "0" and Q[i] == "0":	#case 0 and 0
                product = "0" + product
            else:
                product = "1" + product          #case 0 or 1
        elif carry == 1:
            if accumulator[i] == "1" and Q[i] == "1": #case 1 and 1
                product = "1" + product
                carry = 1
            elif accumulator[i] == "0" and Q[i] == "0":		#case 0 and 0
                product = "1" + product
                carry = 0
            else:								#case 0 or 1
                product = "0" + product
                carry = 1
    return product

def product_value(iteration, product):
	global max_bit,space
	line =str(iteration)+space+ product[:max_bit] +space + product[max_bit:2*max_bit] +space+ product[2*max_bit]
	return line

def covert_Dec_to_binary(dec):
	global max_no,max_bit
	max_no_bin="{0:b}".format(max_no)
	max_bit=int(len(max_no_bin))+1
	spacer()
	if int(dec)<0: 
		bin = twos_complement(dec)
	else:
		bin = "{0:b}".format(int(dec))
		for i in range(max_bit-len(bin)):
			bin = "0" + bin

	return bin


def twos_complement(dec):
	temp= abs(int(dec) + 1)
	temp_bin = "{0:b}".format(temp)
	number=flipped(temp_bin)
	for i in range(max_bit-len(number)):
		number = "1" + number
	return number
def spacer():
	global space
	space=" "*max_bit
	return space
main()
