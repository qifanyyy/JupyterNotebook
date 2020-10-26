#Extended Euclidian algorithm
#Takes in two integers, finds greatest common divisor, and weights s and t
def ExtendedEuclidean(a,b):
    r0 = a;
    r1 = b;
    x0 = 1;
    x1 = 0;
    y0 = 0;
    y1 = 1;
    z = [r0,x0,y0];
    while r1>0:
        r = r0%r1;
        q = (r0-r)/r1;
        x = x0-q*x1;
        y = y0-q*y1;
        z = [r1,x1,y1];
        x0 = x1;
        y0 = y1;
        x1 = x;
        y1 = y;
        r0 = r1;
        r1 = r;
    print("\ngcd(", a, ",", b, ") =", r0, "\nWeight s: ", x0, "\nWeight t: ", y0);

a = int(input("Enter a: "));
b = int(input("Enter b: "));
ExtendedEuclidean(a,b);