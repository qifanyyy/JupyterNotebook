9##########################################
#                                        #
# Added by mmasdeu                       #
# Authors: Xevi Guitart and Marc Masdeu  #
#                                        #
##########################################

from sage.matrix.constructor import Matrix
from sage.rings.all import RealField
from sage.structure.sage_object import SageObject
from sage.misc.all import union
from sage.functions.all import (floor,ceil)
from sage.rings.all import IntegerRing
from sage.rings.all import RationalField
from collections import deque
from collections import namedtuple
from sage.plot.plot import plot
from sage.plot.plot import polygon
from sage.plot.plot import point
from itertools import count, izip
from two_stage_euclidean import *

###################################################################
#                                                                 #
#                                                                 #
# Calculate the continued fraction expansion in a real quadratic  #
#                                                                 #
# Main Reference:                                                 #
# G.E.Cooke, "A weakening of the euclidean property               #
#            for integral domains and applications                #
#             to algebraic number theory I"                       #
#                                                                 #
# We implement an algorithm that automates the method of proof    #
# laid out in the above paper. Other than computing continued     #
# fractions, we obtain certificates of the fact that a real       #
# quadratic field of class number one is two-stage Euclidean.     #
# This a theorem conditional on some GRH.                         #
#                                                                 #
# Authors: Xevi Guitart and Marc Masdeu                           #
#                                                                 #
#                                                                 #
###################################################################


def quadratic_continued_fraction(F, xx, Nbound = 50, Tbound = 5, optimize_for_length = False, max_iters = 500):
    r"""
    Returns a list of elements in the ring
    of integers of F representing a continued fraction expansion
    for x.

    When first called, the function does enough precomputation to
    show that the field is E_2 (in the sense of Cooke), and stores
    the data needed to efficiently compute continued
    fractions. Subsequent calls for other elements of the same
    number field are very fast. The optional arguments are
    parameters passed to the algorithm. If working with large
    discriminants (larger than 1000), then Nbound should be
    increased to 100. For discriminants up to 8000, the function
    will return when Nbound is at least 200. We do not have
    examples of number fields for which Tbound has to be changed
    from the default.

    INPUT::
    - an element x of a real quadratic number field F of
      class number one.

    EXAMPLES::

        sage: from twostage.quadratic_continued_fraction import *
        sage: K.<a> = QuadraticField(53)
        sage: x = 18/5*a + 2/5
        sage: v = quadratic_continued_fraction(K, x)
        sage: y = v[0] + 1/(v[1] + 1/(v[2] + 1/v[3]))
        sage: x == y
        True

        sage: x = 9/5 * a + 3/10
        sage: v = quadratic_continued_fraction(K, x)
        sage: len(v)
        4

    """
    global __continued_fraction_cache
    if not F.degree() == 2 or F.class_number() != 1 or not F.is_totally_real():
        raise ValueError, "The argument must belong to a real quadratic field of class number one."
    xx = F(xx)
    try:
        our_cache = __continued_fraction_cache
    except NameError:
        __continued_fraction_cache=dict()
    try:
        P = __continued_fraction_cache[F]
    except KeyError:
        P = QuadraticContinuedFraction(F,Nbound,Tbound)
        P.solve()
        __continued_fraction_cache[F] = P

    if not optimize_for_length:
        v = []
        knm1 = xx
        kn = 1
        while True:
            div = min(P.evaluate_number(knm1/kn),key=lambda div:abs((kn-(knm1-kn*div[0])*div[1]).norm()))
            if div[1] == 1:
                div = [div[0] + 1]
                r = knm1 - kn * div[0]
                div.append(r)
                an = div[0]
                knp1 = div[1]
            else:
                r = kn - (knm1 - kn * div[0]) * div[1]
                div.append(r)
                an = div[0]
                knp1 = knm1 - kn * an
                v.append(an)
                if knp1 == 0:
                    break
                knm1 = kn
                kn = knp1
                an = div[1]
                knp1 = div[2]

            v.append(an)
            if knp1 == 0:
                break
            knm1 = kn
            kn = knp1
        return v

    opt_v = []
    opt_len = 10**10
    # Below we try to find a short continued fraction
    for iters in range(max_iters):
        v = []
        knm1 = xx
        kn = 1
        while True:
            div = P.evaluate_number(knm1/kn,all_vector=False)
            if div[1] == 1:
                div = [div[0]+1]
                r = knm1-kn*div[0]
                div.append(r)
                an = div[0]
                knp1 = div[1]
            else:
                r = kn - (knm1-kn*div[0])*div[1]
                div.append(r)
                an = div[0]
                knp1 = knm1-kn*an
                v.append(an)
                if knp1 == 0:
                    break
                knm1 = kn
                kn = knp1
                an = div[1]
                knp1 = div[2]
            v.append(an)
            if knp1 == 0:
                break
            knm1 = kn
            kn = knp1
        if len(v) <= opt_len:
            opt_v.append(v)
            opt_len = len(v)
    return opt_v

def all_quadratic_continued_fractions_up_to_length(F, xx,max_length=4,Nbound=50,Tbound=5,optimize_for_length=False, get_img_part = None, threshold = None):
    global __continued_fraction_cache
    xx = F(xx)
    if not F.degree() == 2 or F.class_number() != 1 or not F.is_totally_real():
        raise ValueError, "The argument must belong to a real quadratic field of class number one."
    try:
        our_cache=__continued_fraction_cache
    except NameError:
        __continued_fraction_cache = dict()
    try:
        P=__continued_fraction_cache[F]
    except KeyError:
        P=QuadraticContinuedFraction(F,Nbo3und,Tbound)
        P.solve()
        __continued_fraction_cache[F] = P

    # Given kn,knm1, return all the possible coefficients of the continued fraction,
    # and their next quotients, as a vector.
    def get_ans(P,knm1,kn,only_length_one=False):
        assert knm1 != 0 and kn != 0
        res = []
        knm10 = knm1
        kn0 = kn
        for div in P.evaluate_number(knm10 / kn0):
            knm1 = knm10
            kn = kn0
            v = []
            if div[1] == 1:
                div = [ div[0] + 1 ]
                r = knm1 - kn * div[0]
                div.append(r)
                an = div[0]
                knp1 = div[1]
            else:
                r = kn - (knm1 - kn * div[0]) * div[1]
                div.append(r)
                an = div[0]
                knp1 = knm1 - kn * an
                v.append(an)
                if knp1 == 0:
                    if an != 1 and an != -1:
                        res.append((v,kn,knp1,True))
                    continue
                kn = knp1
                an = div[1]
                knp1 = div[2]

            v.append(an)
            if not only_length_one and len(v) == 2:
                res.append((v, kn, knp1, knp1 == 0))
        return res

    V = [([],xx,1,False)]
    outV = []
    work_to_do = True
    while work_to_do:
        work_to_do = False
        newV = []
        print "(%s)"%len(V),
        sys.stdout.flush()
        for ans, knm1, kn, done in V:
            if not done and get_img_part(ans) > threshold:
                if len(ans) < max_length-1:
                    new_ans_vec = get_ans(P,knm1,kn)
                    if len(new_ans_vec) > 0:
                        work_to_do = True
                        newV.extend([(ans+na[0],na[1],na[2],na[3]) for na in new_ans_vec])
                elif len(ans) < max_length:
                    new_ans_vec = get_ans(P,knm1,kn,only_length_one = True)
                    if len(new_ans_vec)>0:
                        work_to_do = True
                        newV.extend([(ans+na[0],na[1],na[2],na[3]) for na in new_ans_vec])
            else:
                outV.append((ans,knm1,kn,done))
        V = newV
    return [vv[0] for vv in outV]
