def convert_to_binary(number,length = 8):
    adder = "0"*length
    summer = ""
    while(number > 0):
        summer = summer + str(int(number%2))
        number = int(number/2)
    summer = (((adder + summer[::-1])[::-1])[:length])[::-1]
    return summer
def convert_to_integer(binary):
    binary = binary[::-1]
    summer = 0
    for i in range(len(binary)):
        summer = summer +(int(binary[i]))*(2**i)
    return summer
def binary_bit_flip(binary):
    binary = convert_to_binary(binary)
    empty = ""
    for i in range(len(binary)):
        character = binary[i]
        if(character == "1"):
            empty = empty + "0"
        else:
            empty = empty + "1"
    return empty
def add_binary(binary_a, binary_b):
    binary_a = convert_to_integer(binary_a)
    binary_b = convert_to_integer(binary_b)
    summ = binary_a + binary_b
    binary_of_sum = convert_to_binary(summ) 
    return binary_of_sum
def get_twos_complement(binary):
    ones_complement = binary_bit_flip(binary)
    summ = add_binary(ones_complement , convert_to_binary(1))
    return summ
def right_shift(binary):
    binary = convert_to_integer(binary)
    binary = binary >> 1
    return convert_to_binary(binary , 16)
def Booths_multiplication(binary_a,binary_b):
    starting_8_bits = "00000000"
    B = ""
    B_Complement = ""
    if(binary_a < 0):
        binary_a = abs(binary_a)
        B = get_twos_complement(binary_a)
        B_Complement = convert_to_binary(binary_a)
    else:
        B = convert_to_binary(binary_a)
        B_Complement = get_twos_complement(binary_a)
    ending_8_bits = ""
    if(binary_b < 0):
        binary_b = abs(binary_b)
        ending_8_bits = get_twos_complement(binary_b)
    else:
        ending_8_bits = convert_to_binary(binary_b)
    starting_8_bits_0th_val = '0'
    loop_count_variable = 8
    steps_done = 1
    while(loop_count_variable > 0):
        ending_8_bits_0th_val = ending_8_bits[len(ending_8_bits) - 1:]
        str_Leno = " STEP : " + str(steps_done) + " "
        print()
        print(" +"+("+"*len(str_Leno))+"+")
        print(" +"+str_Leno+"+")
        print(" +"+("+"*len(str_Leno))+"+")
        print()
        if (((ending_8_bits_0th_val + starting_8_bits_0th_val) == '00') or ((ending_8_bits_0th_val + starting_8_bits_0th_val) == '11')):
            print(" The operation done is RIGHT SHIFT")
            working_binary = starting_8_bits[0] + right_shift(starting_8_bits + ending_8_bits + starting_8_bits_0th_val)
            starting_8_bits = working_binary[:8]
            ending_8_bits = working_binary[8:2*8]
            starting_8_bits_0th_val = working_binary[len(working_binary)-1]
            print(" starting_8_bits = ", starting_8_bits, "ending_8_bits = ", ending_8_bits, "New starting_8_bits_0th_val = ",starting_8_bits_0th_val)
        elif ((ending_8_bits_0th_val + starting_8_bits_0th_val) == '01'):
            print(" The operation done is ADDITION and RIGHT SHIFT")
            starting_8_bits = add_binary(starting_8_bits, B)
            starting_8_bits = starting_8_bits[-8:]
            working_binary = starting_8_bits[0] + right_shift(starting_8_bits + ending_8_bits + starting_8_bits_0th_val)
            starting_8_bits = working_binary[:8]
            ending_8_bits = working_binary[8:2*8]
            starting_8_bits_0th_val = working_binary[len(working_binary)-1]
            print(" starting_8_bits = ", starting_8_bits, "ending_8_bits = ", ending_8_bits, "New starting_8_bits_0th_val = ",starting_8_bits_0th_val)
        elif ((ending_8_bits_0th_val + starting_8_bits_0th_val) == '10'):
            print(" The operation done is SUBTRACTION and RIGHT SHIFT")
            starting_8_bits = add_binary(starting_8_bits, B_Complement)
            starting_8_bits = starting_8_bits[-8:]
            working_binary = starting_8_bits[0] + right_shift(starting_8_bits + ending_8_bits + starting_8_bits_0th_val)
            starting_8_bits = working_binary[:8]
            ending_8_bits = working_binary[8:2*8]
            starting_8_bits_0th_val = working_binary[len(working_binary)-1]
            print(" starting_8_bits = ", starting_8_bits, "ending_8_bits = ", ending_8_bits, "New starting_8_bits_0th_val = ",starting_8_bits_0th_val)
        loop_count_variable = loop_count_variable - 1
        steps_done = steps_done + 1
    final_16_bit_code = starting_8_bits + ending_8_bits
    return final_16_bit_code
def result_giver(binary_a,integer_binary_a): 
    sign_bit = binary_a[0]
    result_binary = ""
    if(sign_bit == "1"):
        ones_complement_result = binary_bit_flip(integer_binary_a)
        result_binary = add_binary(ones_complement_result , convert_to_binary(1))
        value = -1 * convert_to_integer(result_binary)
        return value
    if(sign_bit == "0"):
        value = convert_to_integer(binary_a)
        return value
def main():
    print(" Binary Multiplication using Booth's Algorithm\n Enter the number for the first variable (Integer)")
    a = int(input())
    print(" Enter the number for the second variable (Integer)")
    b = int(input())
    print(" The Result with calculation is as follows : ")
    value = Booths_multiplication(a,b)
    print("\n")
    print(" The Result in binary form is ", value)
    decimal_of_the_binary_Val = result_giver(value,convert_to_integer(value))
    print(" The result in decimal form is " , decimal_of_the_binary_Val)   
if __name__ == "__main__":
   main()