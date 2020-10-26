#!usr/bin/env python
from cffi import FFI
import os
import numba as nb

ffi = FFI()


ffi.cdef("""
#define KSW_XBYTE  0x10000
#define KSW_XSTOP  0x20000
#define KSW_XSUBO  0x40000
#define KSW_XSTART 0x80000

struct _kswq_t;
typedef struct _kswq_t kswq_t;

typedef struct {
        int score; // best score
        int te, qe; // target end and query end
        int score2, te2; // second best score and ending position on the target
        int tb, qb; // target start and query start
} kswr_t;

        kswr_t ksw_align(int qlen, uint8_t *query, int tlen, uint8_t *target, int m, const int8_t *mat, int gapo, int gape, int xtra, kswq_t **qry);
        kswr_t py_sw(int qlen, uint8_t *query, int tlen, uint8_t *target, int m, const int8_t *mat, int gapo, int gape, int xtra);

        int ksw_extend(int qlen, const uint8_t *query, int tlen, const uint8_t *target, int m, const int8_t *mat, int gapo, int gape, int w, int h0, int *_qle, int *_tle);
        int ksw_global(int qlen, const uint8_t *query, int tlen, const uint8_t *target, int m, const int8_t *mat, int gapo, int gape, int w, int *_n_cigar, uint32_t **_cigar);
        kswq_t *ksw_qinit(int size, int qlen, const uint8_t *query, int m, const int8_t *mat);

""")




py_sw = ''' 
kswr_t py_sw(int qlen, uint8_t *query, int tlen, uint8_t *target, int m, const int8_t *mat, int gapo, int gape, int xtra)
{
    kswq_t *q[2] = {0, 0};
    kswr_t r;
    r = ksw_align(qlen, query, tlen, target, m, mat, gapo, gape, xtra, q);
    free(q[0]); free(q[1]);
    return r;
};
'''


src = []
f =  open('./klib/ksw.c')
for i in f:
    if i.startswith('/*******************************************'):
        break
    else:
        src.append(i)

f.close()

src = ''.join(src)
src += '\n' + py_sw

#print src



_C = ffi.verify(src, extra_compile_args=['-I' + './klib/'])

x = ffi.new('kswq_t *q[2]')


A = ffi.new('const int8_t mat[25]')

A[0:25] = [1, -1, -1, -1, 0,
           -1, 1, -1, -1, 0,
           -1, -1, 1, -1, 0,
           -1, -1, -1, 1, 0,
           0, 0, 0, 0, 0]

#s = 'A'*512
s = chr(0) * 512
n = len(s)

z = _C.ksw_align(n, s, n, s, 5, A, 2, 1, 0x10000, x)

#z = _C.ksw_align2(n, s, n, s, 5, 2, 1, 0x10000)

z = _C.py_sw(n, s, n, s, 5, A, 2, 1, 0x80000)
print z.score, z.qb, z.qe



@nb.jit(nopython=True)
def hello(n, s, A):
    #return c_sin(x)
    z = _C.py_sw(n, s, n, s, 5, A, 2, 1, 0x80000)


hello(n, s, A)

