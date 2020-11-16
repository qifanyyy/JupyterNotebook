def main():
    print("Restoring Division Method")

    sign=1

    print("Input Dividend Q: ", end="")
    q = int(input())
    if(q<0):
        sign=sign+1
    q = ("{0:0%db}" % 8).format(abs(q))   # Convert to bits and assign directly
    print(q)
    print("Input Divisor M: ", end="")
    m = int(input())
    if(m<0):
        sign=sign+1
    m = ("{0:0%db}" % 8).format(abs(m))
    print(m)
    if(m=='00000000'):
        print('Aborting. Divisor cannot be zero.')
    else:
        a='00000000'
        q= list(a+q)

        for k in range(8):  #the code will run 8 times acc to Restoring Division algorithm
            q=list(LeftShift("".join(q)))
            q=(list(add("".join(q[:8]), TwoComp(m)))[-8:]) + q[8:]
            if(q[0]=='1') :
                q=q+['0']
                q = (list(add("".join(q[:8]), (m)))[-8:]) + q[8:]
            else :
                q=q+['1']


        print()
        print('RESULT:')
        print('Quotient (Register Q)= ')

        result = "".join(q[-8:])
        print(result)
        result = int(result, 2)

        if(sign%2==0):
            print('Binary value of negative quotient:')
            b=TwoComp("".join(q[-8:]))
            print(b)
            result="-" + str(result)
            print(result)
        else :
            print(result)

        print('Remainder (Register A)= ')
        remainder="".join(q[:8])
        print(remainder)
        remainder=int(remainder,2)
        print(remainder)

        print()
        print('OUTPUT')
        print(str(result) + "R" + str(remainder))


def add(x, y):   # function to carry out binary addition and returns the result as a string
    maxlen = max(len(x), len(y))

    # Normalize lengths
    x = x.zfill(maxlen)
    y = y.zfill(maxlen)
    result = ''
    carry = 0
    for i in range(maxlen - 1, -1, -1): #reverse order range, decreasing by 1 in every iteration
        r = carry
        r += 1 if x[i] == '1' else 0
        r += 1 if y[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1
    if carry != 0: result = '1' + result
    result.zfill(maxlen)
    return result[-16:]


def TwoComp(n): # function that returns the 2s complement of the binary input, both input and output are strings
    li = list(n)
    for i in range(len(li)):
        li[i] = "0" if li[i] == "1" else "1"
    return add("".join(li), "1")


def LeftShift(a) : #function to carry out left shift
    a=list(a)
    return "".join(a[-(len(a)-1):])

main()
