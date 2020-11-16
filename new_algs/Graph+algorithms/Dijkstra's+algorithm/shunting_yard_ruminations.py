from enum import Enum

# http://wcipeg.com/wiki/Shunting_yard_algorithm#Functions


class Associativity(Enum):
    LEFT = 0
    RIGHT = 1

opPriority = {}
opPriority["^"] = 200
opPriority["*"] = 100
opPriority["/"] = 100
opPriority["+"] = 50
opPriority["-"] = 50

opAssociativity = {}
opAssociativity["^"] = Associativity.RIGHT
opAssociativity["*"] = Associativity.LEFT
opAssociativity["/"] = Associativity.LEFT
opAssociativity["+"] = Associativity.LEFT
opAssociativity["-"] = Associativity.LEFT


class TokenType(Enum):
    OP = 0
    LP = 1
    RP = 2
    NUM = 3
    FUN = 4
    UMINUS = 5

# [4, 5)    
# s[4:5] => "3"
s0 = "1+2*3"
# output(postfix): 1 2 3 * +
# op stack: 
s1 = "10.2*2+3"
s2 = "1*2^3+4"
s3 = "sin(10+16*cos(3))"
s4 = "4-3-2"
# output(postfix): 4 3 - 2 -
# op stack: 
s5 = "4^3^2"
# output(postfix): 4 3 2 ^ ^
# op stack: 

s6 = "1*(2+3)"

s7 = "1*2+3"

s8 = "1*(2+3)*(2+2*2)"

s9 = "-3"
s10= "2-3"
s11= "-2-3"
s12= "(1-2)-1"
s13= "-(25)"
s14= "-(-25)"
s15="-(10*2)"

# postfix: 1 2 - 3 +
# uminus: 1 2 - 3 + 

# 10/(-1)*(-2)
# postfix: 10 -(1 -2 *)  /
# op stack: / u- * u-  


# tokens:
# 1, 10.2
# * + - / ^
# ( )
# sin, cos, tan, cot, atan, acot, asin, acos, sec, csc, sinh, cosh

def printlnList(l, end="\n"):
    for t in l:
        print(t, end=end)
    print()

def peek(l):
    return l[len(l)-1]

def to_token_stream(s):
    i = 0
    ts = []
    while i != len(s):
        if s[i] in "+-*/^":
            ts.append((TokenType.OP, s[i]))
            i += 1
            continue 
        if s[i] == '(':
            ts.append((TokenType.LP, None))
            i += 1
            continue 
        if s[i] == ')':
            ts.append((TokenType.RP, None))
            i += 1
            continue
        # [i, j)
        if s[i].isalpha():
            j = i + 1
            while s[j].isalpha() and j != len(s):
                j += 1
            fnname = s[i:j]
            ts.append((TokenType.FUN, fnname))
            i = j
            continue

        if s[i].isdigit() or s[i] == '.':
            j = i + 1
            #print("i = {0}".format(i))
            #print(j)
            # short-circuit evaluation False and XXX => False
            while j != len(s) and (s[j].isdigit() or s[j] == '.'):
                j += 1
            val = (float)(s[i:j])
            ts.append((TokenType.NUM, val))
            i = j
            continue
        print("error!")
        return None


    for i in range(len(ts) - 1):
        if ts[i][0] == TokenType.OP and ts[i][1] == '-':
            if i == 0:
                ts[i] = (TokenType.UMINUS, None)
            elif ts[i-1][0] in [TokenType.OP, TokenType.LP,
                                TokenType.UMINUS]:
                ts[i] = (TokenType.UMINUS, None)                
        
    return ts

def needToPop(lt, rt):
    if not (lt[0] in [TokenType.OP, TokenType.LP, TokenType.UMINUS]):
        raise RuntimeError("not an operator on top of the stack")


    if lt[0] == TokenType.UMINUS:
        return True
    
    if lt[0] == TokenType.LP:
        return False

    # op on top of the stack
    leftOp = lt[1]
    rightOp = rt[1]
            
    if opPriority[leftOp] > opPriority[rightOp]:
        return True

    if opPriority[rightOp] > opPriority[leftOp]:
        return False

    # leftOp == rightOp

    if opAssociativity[leftOp] == Associativity.LEFT:
        return True
    else:
        return False

    raise RuntimeError("couldn't understand associativity")


def to_postfix(ts):
    print("to_postfix started")
    postfix = []
    opStack = []
    for t in ts:        
        print("token: {0}".format(t))
        print("opStack:", end = "")
        printlnList(opStack)
        tokenType = t[0]
        #print(tokenType)

        if tokenType == TokenType.FUN:
            opStack.append(t)
            continue


        if tokenType == TokenType.UMINUS:
            opStack.append(t)
            continue

        
        if tokenType == TokenType.RP:
            while peek(opStack)[0] != TokenType.LP:
                postfix.append(opStack.pop())
            opStack.pop()
            if peek(opStack)[0] == TokenType.FUN:
                postfix.append(opStack.pop())                
            continue

        
        if tokenType == TokenType.LP:
            opStack.append(t)
            continue
        if tokenType == TokenType.NUM:
            postfix.append(t)
            continue
        if tokenType == TokenType.OP:
            # empty stack
            if not opStack:
                opStack.append(t)
                continue

            # non-empty stack

            # pop into postfix
            # all ops that should be done before ours


            while opStack and needToPop(peek(opStack), t):
                postfix.append(opStack.pop())

                print("popped, opStack:", end = "")
                printlnList(opStack)
            
            opStack.append(t)
            continue
                
        
    while opStack:
        tok = opStack.pop()
        postfix.append(tok)
        
    return postfix
    


# output(postfix) 1 2 3 ^ *
# op stack +

def test(s):
    t3 = to_token_stream(s)
    print("token stream")
    printlnList(t3)
    p = to_postfix(t3)

    printlnList(p)    
    print(s)


test(s3)
