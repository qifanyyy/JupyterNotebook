def main():
    print("Booth's Algorithm for multiplication")

    print("Input Multiplicand M: ", end="")
    m = int(input())
    if m < 0:
        m = TwoComp(("{0:0%db}" % 8).format(m))   # Calculate the two's complement number of m
    else:
        m = ("{0:0%db}" % 8).format(m)   # Convert to bits and assign directly
    print(m)
    print("Input Multiplier Q: ", end="")
    q = int(input())
    if q < 0:
        q = TwoComp( ("{0:0%db}" % 8).format(q) )
    else:
        q = ("{0:0%db}" % 8).format(q)
    print(q)


    a='00000000'
    q0=list('0')
    q= list(a+q)
    for k in range (8) : # the code will run 8 times acc to Booth's algorithm

        if (q[-1]+q0[0]) == '00' :
            q0[0] = q[-1]
            q= list(RightShift("".join(q)))


        elif (q[-1]+q0[0]) == '01':
            q = (list(add("".join(q[:8]), m))[-8:] + q[8:])
            q0[0] = q[-1]
            q = list(RightShift("".join(q)))


        elif (q[-1]+q0[0]) == '10':
            q = (list(add("".join(q[:8]), TwoComp(m)))[-8:] + q[8:])
            q0[0] = q[-1]
            q = list(RightShift("".join(q)))


        elif (q[-1]+q0[0]) == '11':
            q0[0] = q[-1]
            q = list(RightShift("".join(q)))

    print()
    print('RESULT')

    if(q[0]=='1') :
        result=TwoComp("".join(q[1:]))
        print(result)
        result=str(int(result,2))
        print("-" + result)

    else :
        result =("".join(q[1:]))
        print(int(result,2))
        print(result)


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


def RightShift(a) : #function to carry out right shift
    a=list(a)
    for i in range (len(a)-1,0,-1) :
        a[i]=a[i-1]
    return "".join(a)

main()

