"""
A module for Polynomial - represents a polynomial over a finite field
"""

from utils import copy, factor, powers
from serializer import *
import operator
from itertools import izip, izip_longest, repeat

__all__ = ['Polynomial', 'LinearFactors']

def _oper(f):
    groups = lambda coefs, zero : izip_longest(*coefs, fillvalue=zero)
    wrap = lambda cls, zero, *coefs : cls._strip_zeros_coefs(zero, [f(*x) for x in groups(coefs, zero)])
    return wrap


class Polynomial(object):
    """A polynomial with coefficients from any type supporting arithmetic operations"""
    
    def __init__(self, field, coefficients=None):
        """Create a new Polynomial with the given coefficients in the field @field.
        @coefficients - optional argument may be a list or iterator
                        of the coefficients - free factor at [0], etc'.
        """
        self._field = field
        self._zero = field.zero()
        self._one = field.one()
        if coefficients is None:
            coefficients = []
        self._coef = [x for x in coefficients]
        self._strip_zeros()
        self._is_irreducible = None
    
    def _strip_zeros(self):
        """Remove trailing zeros"""
        self._coef = self._strip_zeros_coefs(self._zero, self._coef)
    
    @classmethod
    def _strip_zeros_coefs(cls, zero, coef):
        """Remove trailing zeros"""
        n = len(coef)
        for c in reversed(coef):
            if c != zero:
                break
            n -= 1
        if n == 0:
            return [zero]
        else:
            return coef[:n]
    
    def _new(self, coefficients=None):
        """Convenience for generating a new Polynomial in the same field"""
        return self.__class__(self._field, coefficients)
    
    def is_zero(self):
        """Check if the constant zero polynomial"""
        return self._is_zero_coefs(self._zero, self._coef)
    
    @classmethod
    def _is_zero_coefs(cls, zero, coef):
        return len(coef) == 1 and coef[0] == zero
    
    def deg(self):
        """Return the polynomial's degree"""
        return self._deg_coefs(self._coef)
    
    @classmethod
    def _deg_coefs(cls, coef):
        return len(coef) - 1
    
    def __iter__(self):
        """Iterate over polynomial coefficients from least significant to top coefficient"""
        return iter(self._coef)
    
    def __len__(self):
        """Return the 'dimension' of the polynomial (f(x)=0 is 0, else degree-1)"""
        if self.is_zero():
            return 0
        else:
            return len(self._coef)
    
    def __getitem__(self, pos):
        """Get coefficient @pos (returns zero for pos > degree)"""
        if pos > self.deg():
            return self._zero
        return self._coef[pos]
    
    def __call__(self, pos):
        """Evaluate the polynomial at given @pos"""
        return self._eval(pos)
    
    
    # Define all basic per-coefficient operations
    
    _add_coefs = classmethod( _oper(operator.add) )
    def __add__(self, other):
        res = self._add_coefs(self._zero, self._coef, other._coef)
        return self._new(res)
    
    _sub_coefs = classmethod( _oper(operator.sub) )
    def __sub__(self, other):
        res = self._sub_coefs(self._zero, self._coef, other._coef)
        return self._new(res)
    
    _neg_coefs = classmethod( _oper(operator.neg) )
    def __neg__(self):
        res = self._neg_coefs(self._zero, self._coef)
        return self._new(res)
    
    _pos_coefs = classmethod( _oper(operator.pos) )
    def __pos__(self):
        res = self._pos_coefs(self._zero, self._coef)
        return self._new(res)
    
    
    @classmethod
    def _scalar_mult_coefs(cls, zero, coef, scalar):
        """Multiplies the coefficients by the given scalar"""
        return cls._monomial_mult_coefs(zero, coef, scalar, 0)
    
    @classmethod
    def _monomial_mult_coefs(cls, zero, coef, scalar, deg):
        """Multiplies the coefficients by (scalar * x^deg)"""
        if scalar == zero:
            return [zero]
        return ([zero] * deg) + [scalar * x for x in coef]
    
    def __mul__(self, other):
        return self._mul_mod(other)
    
    def _mul_mod(self, other, mod=None):
        """Multiply self with the given polynomial.
        If optional argument @mod given, operations done modulo the given polynomial.
        """
        if mod is not None:
            mod = mod._coef
        res = self._mul_coefs(self._zero, self._coef, other._coef, mod)
        return self._new(res)
    
    @classmethod
    def _mul_coefs(cls, zero, a, b, mod=None):
        """Naive multiplication"""
        if cls._is_zero_coefs(zero, a) or cls._is_zero_coefs(zero, b):
            return [zero]
        res = [zero] * (len(a) + len(b) - 1)
        for i,v1 in enumerate(a):
            for j,v2 in enumerate(b):
                res[i+j] += (v1 * v2)
        
        res = cls._strip_zeros_coefs(zero, res)
        if mod is not None:
            _, res = cls._divmod_coefs(zero, res, mod)
        return res
    
    def __divmod__(self, other):
        div, mod = self._divmod_coefs(self._zero, self._coef, other._coef)
        return self._new(div), self._new(mod)
    
    @classmethod
    def _divmod_coefs(cls, zero, dividend, divisor):
        #Handle special end cases
        divisor_deg = cls._deg_coefs(divisor)
        if cls._deg_coefs(dividend) < divisor_deg or cls._is_zero_coefs(zero, dividend):
            return [zero], dividend
        
        # Constant polynomial divisor
        divisor_top_inv = divisor[-1]**(-1)
        if divisor_deg == 0:
            quotient = cls._scalar_mult_coefs(zero, dividend, divisor_top_inv)
            return quotient, [zero]
        
        quotient, remainder = [zero], dividend
        while cls._deg_coefs(remainder) >= divisor_deg and cls._is_zero_coefs(zero, remainder) == False:
            cur_exp = cls._deg_coefs(remainder) - divisor_deg
            coef = remainder[-1] * divisor_top_inv

            deg_diff = cur_exp - cls._deg_coefs(quotient)
            if deg_diff > 0:
                quotient.extend(repeat(zero, deg_diff))
            quotient[cur_exp] += coef
            
            # chunk = (coef * x**cur_exp) * divisor
            chunk = cls._monomial_mult_coefs(zero, divisor, coef, cur_exp)
            remainder = cls._sub_coefs(zero, remainder, chunk)
            remainder = cls._strip_zeros_coefs(zero, remainder)

        return quotient, remainder
    
    def __mod__(self, other):
        _, mod = self.__divmod__(other)
        return mod
    
    def __pow__(self, y, mod=None):
        if mod is not None:
            mod = mod._coef
        pol = self._pow_coefs(self._field, self._coef, y, mod)
        return self._new(pol)
    
    @classmethod
    def _pow_coefs(cls, F, coef, y, mod=None):
        assert y >= 0, "Invalid power for polynomial"
        zero, one = F.zero(), F.one()
        if cls._is_zero_coefs(zero, coef):
            return [zero]
        
        res = [one]
        while y > 0:
            if y & 1:
                res = cls._mul_coefs(zero, res, coef, mod)
            y >>= 1
            if y > 0:
                coef = cls._mul_coefs(zero, coef, coef, mod)
        return res
    
    def __eq__(self, other):
        assert isinstance(other, Polynomial), "Non polynomial for __eq__ %r" % other
        return self._field == other._field and self._coef == other._coef
    
    def __neq__(self, other):
        assert isinstance(other, Polynomial), "Non polynomial for __neq__ %r" % other
        return self._field != other._field or self._coef != other._coef
    
    def invert(self, other):
        """Find INV such that `(self * INV) mod other` is the GCD(self, other)"""
        gcd, s, t = self._egcd_coefs(self._zero, self._coef, other._coef)
        return self._new(s)
    
    @classmethod
    def _egcd_coefs(cls, zero, a, b):
        """Extended Euclidean algorithm on coef lists.
        Returns a tuple (gcd, s, t) such that:
        gcd(a,b) = s*a + t*b
        where multiplication and is polynomial multiplication.
        @zero - the zero of the field
        """
        if cls._is_zero_coefs(zero, a):
            if cls._is_zero_coefs(zero, b):
                return ([zero], [zero], [zero])
            else:
                # Canonize leading factor for monic result
                inverse = b[-1] ** (-1)
                b = cls._scalar_mult_coefs(zero, b, inverse)
                return (b, [zero], [inverse])
        else:
            div, mod = cls._divmod_coefs(zero, b, a)
            g, x, y = cls._egcd_coefs(zero, mod, a)
            xdiv = cls._mul_coefs(zero, x, div)
            newx = cls._sub_coefs(zero, y, xdiv)
            return (g, newx, x)
    
    @classmethod
    def _gcd_coefs(cls, zero, a, b):
        """Calculate GCD on coef lists.
        @zero - the zero of the field
        """
        while cls._is_zero_coefs(zero, b) == False:
            _, mod = cls._divmod_coefs(zero, a, b)
            b, a = mod, b
        # Canonize leading factor for monic result
        if cls._is_zero_coefs(zero, a) == False:
            inverse = a[-1] ** (-1)
            a = cls._scalar_mult_coefs(zero, a, inverse)
        return a
    
    def evaluate(self, pos):
        """Evaluate the polynomial at given @pos.
        If pos is an iterable, a list of evaluations is returned.
        """
        if isinstance(pos, (list, tuple)):
            return map(self._eval, pos)
        return self._eval(pos)
    
    def _eval(self, pos):
        """Evaluate at a single position @pos"""
        return self._eval_coefs(self._coef, pos)
    
    @classmethod
    def _eval_coefs(cls, coef, pos):
        monomials = ((c * p_i) for c, p_i in izip(coef, powers(pos)))
        return reduce(operator.add, monomials)
    
    @classmethod
    def rand(cls, field, degree, coefficients=None, constraint=None, exact_degree=False):
        """Create a new random Polynomial of degree @degree over @field.
        @field - field where coefficientscome from. Has to implement methods zero(), rand(nonzero)
        @coefficients - an iterable containing values for certain coefficients.
                       None is treated as no constraint on the coefficient.
                       In case the list is shorter than degree it is extended with None-s.
        @constraint - a (x,y) point that must be on the polynomial, or None if no constraint.
        @exact_degree - force top coefficient to be non-zero?
        Returns a new Polynomial
        """
        # Number of coefficients needed
        assert degree >= 0, "Invalid degree %d" % degree
        n_coef = degree + 1
        
        if coefficients is None:
            coefficients = []
        zero = field.zero()
        
        # Extend coefficient constraints if needed
        assert len(coefficients) <= n_coef, "Too many coefficient constraints (%d) given for degree %d" % (len(coefficients), degree)
        if len(coefficients) < n_coef:
            coefficients.extend([None] * (n_coef - len(coefficients)))
        
        # Set top coefficient to non-zero according to exact_degree
        if exact_degree is True and coefficients[-1] is None:
            coefficients[-1] = field.rand(nonzero=True)
        
        # Choose random coefficients & Build the polynomial
        coef = []
        for c in coefficients:
            if c is None:
                c = field.rand()
            coef.append(c)
        poly = cls(field, coef)
        
        # Handle the (x,y) constraint if given
        if constraint is not None:
            x,y = constraint
            
            # Special free factor constraint
            if x == zero:
                assert coefficients[0] is None, "Not enough degrees of freedom for zero-constraint"
                poly._coef[0] = y
            else:
                # Choose one of our freedom degrees
                pos = None
                for i,v in enumerate(coefficients):
                    if v is None:
                        pos = i
                        break
                assert pos is not None, "Not enough degrees of freedom for constraints"
                
                # Change the position so f(x)=y for the constraint
                poly._coef[pos] = zero
                cur_y = poly.evaluate(x)
                diff_y = y - cur_y
                new_coef = diff_y / (x**pos)
                poly._coef[pos] = new_coef
        
        return poly
    
    def is_irreducible(self):
        """Return True iff the polynomial is irreducible"""
        if self._is_irreducible is None:
            self._is_irreducible = self._is_irreducible_coefs(self._field, self._coef)
        return self._is_irreducible
    
    @classmethod
    def _is_irreducible_coefs(cls, F, coef):
        """Rabin irreducibility test"""
        zero, one = F.zero(), F.one()
        if cls._is_zero_coefs(zero, coef):
            return False
        
        # Make polynomial monic
        if coef[-1] != one:
            inverse = coef[-1] ** (-1)
            coef = cls._scalar_mult_coefs(zero, coef, inverse)
        modulo = lambda pol : cls._divmod_coefs(zero, pol, coef)[1]
        
        deg = cls._deg_coefs(coef)
        deg_factors = factor(deg)
        pows = [deg // f for f in reversed(deg_factors)]
        pows.append(deg) # Calculate `x^(q^deg)` as well
        
        # Calc (x^q mod f) and then its powers, make irreducibility tests on the fly
        q = len(F)
        cur_val =  modulo([zero]*q + [one])
        cur_exp = 1
        minus_x = [zero, -one]
        for d in pows:
            # Calc next power
            exp = d - cur_exp
            cur_val = cls._pow_coefs(F, cur_val, int(q**exp), coef)
            cur_exp = d
            pol = cls._add_coefs(zero, cur_val, minus_x) # x^(q^d) - x
            
            # Do test for current power (except for last power)
            if d < deg:
                gcd = cls._gcd_coefs(zero, pol, coef)
                if gcd != [one]:
                    return False
        
        # Final test on `x^(q^deg) - x`
        if cls._is_zero_coefs(zero, modulo(pol)):
            return True
        # else:
        return False
    
    @classmethod
    def irreducible_poly(cls, F, d):
        """Generate a Polynomial of degree exactly @d irreducible over @F"""
        gen = F.generator()
        zero, one = F.zero(), F.one()
        minus_one = -one
        coef = ([zero] * d) + [one]
        
        # Exhaustively go over polynomials until an irreducible is found
        while True:
            for i in xrange(len(coef) - 1):
                if coef[i] == zero:
                    coef[i] = one
                    break
                # else
                coef[i] *= gen
                if coef[i] == one:
                    coef[i] = zero if (i != 0) else one
                else:
                    break
            if cls._is_irreducible_coefs(F, coef):
                return Polynomial(F, coef)
    
    def __repr__(self):
        """String representation of object"""
        monomials = []
        for i,c in enumerate(self._coef):
            if i == 0:
                monomials.append("%r" % c)
            elif c != self._zero:
                monomials.append("%r*X^%d" % (c, i))
        
        poly = " + ".join(monomials)
        return "Polynomial(%s)" % poly
    
    def __serialize__(self):
        return self._field, self._coef
    
    @classmethod
    def __unserialize__(cls, serialized):
        """Creates a new Polynomial object by unserializing given @serialized string"""
        field, coef = serialized
        return cls(field, coef)

class LinearFactors(object):
    """A polynomial defined by its roots and some optional additional (x,y) point for y != 0.
    Supports only a limited number of operations - but may be converted to Polynomial.
    """
    def __init__(self, field, roots, constraint=None):
        """If @constraint=(x,y) is given, the leading coefficient is
        fixed so P(x)=y, else leading coefficient is `one`
        """
        self._roots = [x for x in roots]
        self._len = len(self._roots)
        self._one = field.one()
        self._zero = field.zero()
        self._gf = field
        self._factor = self._one
        
        if constraint is not None:
            x,y = constraint
            cur_y = self._eval(x)
            self._factor = (cur_y ** (-1)) * y
            assert y, "Constraint %r can't be another root!" % constraint

    def evaluate(self, pos):
        """Evaluate a single or a list of positions"""
        if isinstance(pos, (list, tuple)):
            return map(self._eval, pos)
        return self._eval(pos)
    
    def __call__(self, pos):
        return self._eval(pos)
        
    def _eval(self, pos):
        if pos in self._roots:
            return self._zero
        return reduce(operator.mul, (pos - x for x in self._roots), self._factor)
    
    def to_polynomial(self):
        """Return a equivalent Polynomial"""
        factors = (Polynomial(self._gf, [-x, self._one]) for x in self._roots)
        lc = Polynomial(self._gf, [self._factor])
        return reduce(operator.mul, factors, lc)
        
