def complement(c):
    a = len(c)
    for i in range(a-1,-1,-1):
        if c[i] == '1':
            break
        i -= 1
    if i == -1:
        return '1' + c
    j = i - 1
    while j >= 0:
        c = list(c)

        if c[j] == '1':
            c[j] = '0'
        else:
            c[j] = '1'
        c = ''.join(c)
        j -= 1
    return c


def add(a, b):
    """Add two binary number"""
    sum = bin(int(a, 2) + int(b, 2))
    return sum


def rightshift(a, b, c):
    """Arithmetic right shift"""
    if a[0] == "1":
        return "1" + a + b
    else:
        return "0" + a + b


one = int(input("Please enter multiplicand: "))
two = int(input("Please enter multiplier: "))
if abs(two) > abs(one):  # assigning larger value to one
    temp = one
    one = two
    two = temp
mul1 = "0" + bin(abs(int(one)))[2:]
n = len(mul1)
if one < 0:
    mul1 = complement(mul1)
# converting number to binary
mul2 = bin(two)[2:]
if len(mul2) < n:
    mul2 = "0" * (n - len(mul2)) + mul2
elif len(mul2) >= n:
    mul2 = mul2[-n:]
if two < 0:
    mul2 = complement(mul2)
print("binary of multiplicand: " + mul1)
print("binary of multiplier: " + mul2)
mul1_len = len(mul1)
mul2_len = len(mul2)
q0 = "0"

size = n
a = "0" * n
q1 = mul2[-1]
i = n
print("n " + "A " + "Q " + "q0 " + "Action")
while i > 0:
    # considering the three cases
    q1 = mul2[-1]
    if (q0 == "0" and q1 == "0") or (q0 == "1" and q1 == "1"):
        inter = rightshift(a, mul2, q0)
        a = inter[:mul1_len]
        mul2 = inter[mul1_len:-1]
        q0 = inter[-1]
        print(str(i) + " " + a + " " + mul2 + " " + q0 + " Right shift")
        i = i - 1

    elif q0 == "0" and q1 == "1":
        a = add(a, complement(mul1))[2:]
        if len(a) < n:
            a = "0" * (n - len(a)) + a
        elif len(a) >= n:
            a = a[-n:]
        print(str(i) + " " + a + " " + mul2 + " " + q0 + " A = A - M")
        inter = rightshift(a, mul2, q0)
        a = inter[:mul1_len]
        mul2 = inter[mul1_len:-1]
        q0 = inter[-1]
        print(str(i) + " " + a + " " + mul2 + " " + q0 + " Right shift")
        i = i - 1

    elif q0 == "1" and q1 == "0":
        a = add(a, mul1)
        if len(a) < n:
            a = "0" * (n - len(a)) + a
        elif len(a) >= n:
            a = a[-n:]
        a = a[-n:]
        print(str(i) + " " + a + " " + mul2 + " " + q0 + " A = A + M")
        inter = rightshift(a, mul2, q0)
        a = inter[:mul1_len]
        mul2 = inter[mul1_len:-1]
        q0 = inter[-1]
        print(str(i) + " " + a + " " + mul2 + " " + q0 + " Right shift")
        i = i - 1
ans = a + mul2
# converting binary to integer
if ans[0] == "1":
    ans2 = complement(ans)
    final = "-" + str(int(ans2, 2))
else:
    final = str(int(ans, 2))
print()
print("Final ans: " + final)
