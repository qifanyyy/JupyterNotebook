from sympy.ntheory.continued_fraction import *
from sympy.ntheory import n_order
import numpy as np
import math
import sys
import os
import argparse
import csv


def better_a(m):
    ord_lis = []
    idx_lis = []
    for a in range(2, m):
        if math.gcd(a, m) == 1:
            ord_lis.append(n_order(a, m))
            idx_lis.append(a)
    return idx_lis[ord_lis.index(min(ord_lis))]


def args_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', '-t', metavar='seq/nor')
    method = parser.add_mutually_exclusive_group()
    method.add_argument('--individual', '--indiv', '-i',
                        type=int, nargs=4, metavar=('res', 'len', 'N', 'a'))
    method.add_argument('--file', '-f', type=int, nargs=2, metavar=('N', 'a'))

    parser.add_argument('--log', '-l', action='store_true')
    return parser.parse_args()


def run_CF(args):

    if args.individual:
        res = args.individual[0]
        bitlen = args.individual[1]
        N = args.individual[2]
        a = args.individual[3]
        cf_ind(res, bitlen, N, a)
    if args.file:
        if args.file[1] == 0:
            for i in range(2, args.file[0]):
                if math.gcd(i, args.file[0]) == 1:
                    args.file[1] = i
                    cf_file(args)
        else:
            cf_file(args)


def checkFactor(r, N, a):
    if r % 2 == 0:
        exponential = math.pow(a, r/2)
        plus = int(exponential+1)
        minus = int(exponential-1)
        maxiter_2 = 15
        p_factor = math.gcd(plus, N)
        q_factor = math.gcd(minus, N)
        p_tri_flag = False
        q_tri_flag = False
        if p_factor == 1 or p_factor == N:
            p_tri_flag = True
        if q_factor == 1 or q_factor == N:
            q_tri_flag = True
        if p_tri_flag and q_tri_flag:
            print(f'trivial factors: {p_factor}, {q_factor}')
            return False
        if not p_tri_flag:
            if math.gcd(p_factor, N) != 1:
                print('Factors: {0}, {1}'.format(p_factor, N//p_factor))
                return True
        if not q_tri_flag:
            if math.gcd(q_factor, N) != 1:
                print('Factors: {0}, {1}'.format(q_factor, N//q_factor))
                return True
        '''
        if (p_factor==1 or p_factor==N) and (q_factor==1 or q_factor==N):
            print(f'trivial factors: {p_factor}, {q_factor}')
            return False                  
        '''

        print('Factors: {0}, {1}'.format(p_factor, q_factor))
        return True
    else:
        print("The estimated r is odd, try other cases!\n")


def cf_file(args):

    if not args.type:
        raise Exception("-f must with -t")
    if args.type == 'seq':
        path = './sequential/result/'
    elif args.type == 'nor':
        path = './normal/result/'
    else:
        raise Exception("Wrong given type!")
    fileargs = args.file
    N = fileargs[0]
    a = fileargs[1]
    filename = str(N)+"_"+str(a)+'.csv'
    filename = path+filename
    if args.log:
        logpath = path+str(N)+"_"+str(a)+'.log'
        sys.stdout = open(logpath, 'w')
    print(filename)
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    succ = []
    for i in range(len(data)):
        res = data[i][0]
        print('+'*35)
        print(f"res: {res}")
        if cf_ind(res, len(res), N, a):
            succ.append(res)
    if len(succ) != 0:
        print('*'*35)
        print(f"Success res: {succ}")
        print('*'*35)


def cf_ind(res, bitlen, N, a):
    appro_deg = 5
    if len(res) > bitlen:
        res = res.replace(" ", "")
    if not isinstance(res, str):
        res = int(str(res), 2)
    else:
        res = int(res, 2)
    denomi = 2**bitlen
    frac = Rational(res, denomi)
    threshold = 1/(2*denomi)
    print("="*35)
    print("CF algorithm rule:")
    print("(1) appro.denominator < N")
    print("(2) abs(appro-frac) < threshold")
    print("="*35)

    print(f"Analyzing fraction: {frac}")
    print(f"N = {N}, a={a}")
    it = continued_fraction_convergents(continued_fraction_iterator(frac))
    # next(it)
    for n in range(appro_deg):
        print('-'*35)
        try:
            app = next(it)
            print(f'{n}th appro: {app}')
            dif = app-frac
            print(f'abs_diff: {abs(dif)}')

            pos_r = app.denominator()
            print(f'possible_order: {pos_r}')
            if pos_r % 2 == 1 or pos_r == 0:
                print("The possible order is odd or 0")
                continue
            if pos_r > N:
                print("Violate rule (1)")
                continue
            if abs(dif) > threshold:
                print("Violate rule (2)")
                continue
            if checkFactor(pos_r, N, a):
                return True
        except Exception as e:
            print(e)
            break
    return False


if __name__ == '__main__':
    res = int('10000000', 2)
    denomi = 2**8
    frac = Rational(3, 7)

    # CF(res,denomi,15,4)
    # cf3(frac,15,4)
    cf_ind(res, 8, 15, 4)
