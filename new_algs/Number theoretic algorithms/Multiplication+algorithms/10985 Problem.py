#-------------------------------------------------------------------------------
# Name:        10958 problem
# Purpose:     Determine if you can create an equation using addition,
#              multiplication, exponents, and concatenation with the digits
#              in ascending order to create the number 10958
#
# Author:      schess0412
#
# Created:     19/04/2017
# Copyright:   (c) schess0412 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#Set base string as example equation
base_string = "-1+2+3+4+5+6+7+8+9-";
change_string = base_string;

def stringCheck(type, change_string):
    if type in change_string:
        while type in change_string:
            base_pos = change_string.find(type);

            #establish variables to check the previous position for an operation and repeat
            check_pos = 1;
            pre_string = "";
            pstr = 0;
            while 1==1:
                if change_string[base_pos-check_pos] == "+" or change_string[base_pos-check_pos] == "*" or change_string[base_pos-check_pos] == "^" or change_string[base_pos-check_pos] == "|" or change_string[base_pos-check_pos] == "-":
                    break;
                pre_string = change_string[base_pos-check_pos]+pre_string;
                check_pos += 1;
                pstr += 1;

            #establish variables to check the next position for an operation and repeat
            check_pos = 1;
            after_string = "";
            astr = 1;
            while 1==1:
                if change_string[base_pos+check_pos] == "+" or change_string[base_pos+check_pos] == "*" or change_string[base_pos+check_pos] == "^" or change_string[base_pos+check_pos] == "|" or change_string[base_pos+check_pos] == "-":
                    break;
                after_string = after_string+change_string[base_pos+check_pos];
                check_pos += 1;
                astr += 1;

            #establish variables to combine the two strings together and insert them back into the base string
            if type == "+": result = int(after_string) + int(pre_string);
            elif type == "*": result = int(after_string) * int(pre_string);
            elif type == "^": result = int(after_string) ** int(pre_string);
            else: result = after_string + pre_string;

            change_string = change_string[0:base_pos-pstr] + str(result) + change_string[base_pos+astr:];
    return change_string;

while 1==1:
    #set the adjustible string to the base string
    change_string = base_string;

    #PEMDAS the equation
    change_string = stringCheck("|", change_string);
    change_string = stringCheck("^", change_string);
    change_string = stringCheck("*", change_string);
    change_string = stringCheck("+", change_string);

    #check if the result is 10985
    if change_string == "-10985-": break;

    #display the equation and its result
    print(base_string + " = " + change_string);

    #adjust base equation
    pos_check = 2;
    while 1==1:
        if base_string[pos_check] == "|":
            base_string = base_string[0:pos_check] + "+" + base_string[pos_check+1:];
            pos_check += 2;
        elif base_string[pos_check] == "^":
            base_string = base_string[0:pos_check] + "|" + base_string[pos_check+1:];
            break;
        elif base_string[pos_check] == "*":
            base_string = base_string[0:pos_check] + "^" + base_string[pos_check+1:];
            break;
        elif base_string[pos_check] == "+":
            base_string = base_string[0:pos_check] + "*" + base_string[pos_check+1:];
            break;
        else:
            print("Error");
            print(base_string[pos_check]);
            exit();

#print(pre_string + after_string);
#print(result);
print(base_string + " = " + change_string);

exit();
