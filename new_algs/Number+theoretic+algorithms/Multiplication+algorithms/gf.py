"""
A module for handling finite fields
"""

from serializer import *
from utils import log, random, factor, powers, inner_product
from polynomial import Polynomial
from itertools import izip

__all__ = ['Zmod', 'Extension', 'GF', 'FFE']

class FF(object):
    def __init__(self, p, m=1):
        """A GF(p^m) finite field interface"""
        self._p = p
        self._m = m
        self._zero = None
        self._one  = None
        self._g = None
    
    def get_p(self):
        return self._p
    
    def get_deg(self):
        return self._m
    
    def get_mod(self):
        """Field modulus - _get_mod must be implemented"""
        return self._get_mod()
    
    def zero(self):
        """Return field's zero - _calc_zero must be implemented"""
        if self._zero is None:
            self._zero = self._calc_zero()
        return self._zero
    
    def one(self):
        """Return field's one - _calc_one must be implemented"""
        if self._one is None:
            self._one = self._calc_one()
        return self._one
    
    def rand(self, nonzero=False):
        """Return a random field element (optionaly non-zero) - _rand must be implemented"""
        return self._rand(nonzero)
    
    def inv(self, element):
        assert element in self, "%r not in field %r" % (element, self)
        assert not element.is_zero(), "Cannot invert zero (%r) of %r" % (element, self)
        return self._inv(element.get_x())
    
    def __call__(self, x):
        """Return an element with the value x"""
        return FFE(x, self)
    
    def __contains__(self, x):
        return (self == x.get_field())
    
    def __len__(self):
        return self._p ** self._m
    
    def generator(self):
        """Find a generator for F"""
        if self._g is not None:
            return self._g
        
        sz = len(self) - 1
        if sz == 1:
            self._g = self.one()
            return self._g
        
        # Check g**((n-1)/p) for all factors p of n-1
        # g is a generator if and only if none of these powers are `one`
        one = self.one()
        loopends = [sz // f for f in factor(sz)]
        found = False
        while not found:
            g = self.rand(nonzero=True)
            res = g.multi_pows(loopends)
            if one not in res:
                found = True
        self._g = g
        return g
    
    def all_generators(self):
        """Return an iterator on all field's generators"""
        sz = len(self) - 1
        loopends = [sz // f for f in factor(sz)]
        one = self.one()
        for x in self:
            if one not in x.multi_pows(loopends):
                yield x
    
    def __iter__(self):
        """Iterate over all non-zero elements of the field starting from fields 'one'"""
        return powers(self.generator(), len(self) - 1)
    

class Zmod(FF):
    """A Galios field over a prime number"""
    def __init__(self, p):
        FF.__init__(self, p)
        assert p > 1 and factor(p) == [p], "%r must be a prime integer!" % p

    def _get_mod(self):
        return self._p
    
    def _rand(self, nonzero):
        """Return a random field element"""
        start = 0
        if nonzero:
            start = 1
        x = random.randint(start, self._p - 1)
        return self(x)
    
    def _calc_zero(self):
        """Return field's zero"""
        return self(0)
    
    def _calc_one(self):
        """Return field's one"""
        return self(1)
    
    def _inv(self, x):
        """Returns @x's inverse in the field"""
        gcd, s, t = _egcd(x, self._p)
        return self(s)
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self._p == other._p)
        
    def __repr__(self):
        return "Zp_" + str(self._p)
    
    _SERIALIZE_PREFIX = "Zp_"
    def __serialize__(self):
        return self._SERIALIZE_PREFIX + str(self._p)
    
    @classmethod
    def __unserialize__(cls, s):
        """Returns a new Zmod object out of a Zmod serialized by serialize"""
        pre = cls._SERIALIZE_PREFIX
        assert s.startswith(pre) and len(s) > len(pre) and s[len(pre):].isdigit(), "Invalid representation of Zmod %r" % s
        s_p = s[len(pre) : ]
        p = int(s_p)
        return cls(p)


class Extension(FF):
    """A Finite Field Extension p^t*m of GF(p^t) (extends Zmod or Extension objects).
    @poly - an optional Polynomial - irreducible polynomial defining the extension.
            If not supplied - a sparse irreducible polynomial is randomly chosen.
    """
    def __init__(self, gf, m, poly=None):
        assert m > 1, "Extension must have m > 1"
        
        if isinstance(gf, int):
            gf = GF(gf)
        self._gf = gf
        self._ext = m
        FF.__init__(self, gf.get_p(), gf.get_deg() * self._ext)
        
        if poly is None:
            poly = Polynomial.irreducible_poly(self._gf, self._ext)
        self._poly = poly
        self._trace_f = None
    
    def _get_mod(self):
        return self._poly
    
    def get_subfield(self):
        return self._gf
    
    def get_extension(self):
        return self._ext
    
    def project(self, element):
        """Project @element to our subfield. @element must be in the field"""
        assert element in self, "%r not in field %r" % (element, self)
        pol = element.get_x()
        assert pol.deg() == 0, "Cannot project non-constant %r" % pol
        x = pol[0]
        return x
    
    def extend(self, element):
        """Opposite of project - returns a representation of @element in the extended field"""
        assert element in self._gf, "%r not in field %r" % (element, self._gf)
        pol = Polynomial(self._gf, [element])
        return self(pol)
    
    def to_subfield_vec(self, element):
        """Return a vector (list) of subfield elements which is
        the vector representation of @element over the subfiled
        """
        assert element in self, "%r not in field %r" % (element, self._gf)
        zero = self._gf.zero()
        pol = element.get_x()
        coefs = [x for x in pol]
        coefs.extend([zero] * (self._ext - len(coefs)))
        return coefs
    
    def from_subfield_vec(self, vec):
        """Opposite of to_subfield_vec - converts a vector of subfield
        elements to a field element
        """
        assert all(map(lambda x : x in self._gf, vec)), "Vector has elements not in subfield %r" % self._gf
        assert len(vec) == self._ext, "Wrong vector length %d, expected %d" % (len(vec), self._ext)
        return self(vec)
    
    def _rand(self, nonzero):
        """Return a random field element"""
        pol = Polynomial.rand(self._gf, self._ext - 1)
        while nonzero and pol.is_zero():
            pol = Polynomial.rand(self._gf, self._ext - 1)
        return self(pol)
    
    def _calc_zero(self):
        """Return field's zero"""
        return self(Polynomial(self._gf, []))
    
    def _calc_one(self):
        """Return field's one"""
        return self(Polynomial(self._gf, [self._gf.one()]))
    
    def _inv(self, x):
        """Returns @x's inverse in the field"""
        inverse = x.invert(self._poly)
        return self(inverse)
    
    def __eq__(self, other):
        assert isinstance(other, Extension), "%r not an Extension" % other
        return (self._gf == other._gf and self._m == other._m and self._poly == other._poly)
    
    def __call__(self, x):
        """Return an element with the value x"""
        if isinstance(x, (list, tuple)):
            x = Polynomial(self._gf, x)
        return FF.__call__(self, x)
        
    def __repr__(self):
        return "GF_%s^%s (ext %r)" % (self._p, self._m, self._gf)
    
    def __serialize__(self):
        poly_s = serialize(self._poly)
        gf_s = serialize(self._gf)
        return (gf_s, self._ext, poly_s)
    
    @classmethod
    def __unserialize__(cls, serialized):
        """Returns a new Extension object out of a Extension serialized by serialize"""
        gf_s, m, poly_s = serialized
        poly = unserialize(poly_s)
        gf = unserialize(gf_s)
        return cls(gf, m, poly)
    
    def trace(self, element, param=None):
        """Return the trace transformation applied on @element.
        The result is an element in the subfield.
        If optional @param is supplied, element is first multiplied by @param.
        """
        # Calculate once the trace of the standard basis
        # then use the result for calculating the trace of arbitrary elements
        if self._trace_f is None:
            self._calc_trace_base()
        assert element in self, "%r not in field %r" % (element, self)
        if param is not None:
            assert param in self, "Invalid scalar parameter for trace %r" % param
            element *= param
        
        return inner_product(self.to_subfield_vec(element), self._trace_f)
    
    def _calc_trace_base(self):
        """Calculate the subfield-linear trace transformation base for fast calculation"""
        self._trace_f = []
        q = len(self._gf)
        x_1 = self([self._gf.zero(), self._gf.one()]) #Go over `f(x) = x` powers (f(x)=1, f(x)=x, f(x)=x**2, ...)
        for base_i in powers(x_1, self._ext):
            cur = base_i
            tr = base_i
            for i in xrange(1, self._ext):
                cur = (cur ** q)
                tr += cur
            res = self.project(tr)
            self._trace_f.append(res)

# Recommended GF constructor
def GF(q, n=1):
    factors = factor(q)
    assert len(factors) == 1 and q > 1, "Cannot create GF with non prime power %d" % q
    p = factors[0]
    if q == p:
        if n == 1:
            return Zmod(p)
        else:
            return Extension(p, n)
    else:
        log = 1
        while q > p:
            q = q // p
            log += 1
        f = Extension(p, log)
        if n == 1:
            return f
        else:
            return Extension(f, n)


class FFE(object):
    """An element of a finite field.
    Supports all the basic arithmetic operations"""
    
    def __init__(self, x, p):
        """@x - integer, @p - a Zmod/Extension or a prime number (int)"""
        if isinstance(p, int):
            self._field = Zmod(p)
            self._mod = p
        else:
            self._field = p
            self._mod = self._field.get_mod()
        self._x = x % self._mod

    def get_x(self):
        return self._x
    
    def get_field(self):
        """Returns the elements field"""
        return self._field
        
    def inv(self):
        """Returns a FFE of the element's inverse"""
        return self._field.inv(self)
    
    def is_zero(self):
        return not self.__nonzero__()
        
    def __add__(self, other):
        assert self._field == other._field
        return FFE(self._x + other._x, self._field)

    def __sub__(self, other):
        assert self._field == other._field
        return FFE(self._x - other._x, self._field)

    def __mul__(self, other):
        if isinstance(other, FFE):
            assert self._field == other._field
            return FFE(self._x * other._x, self._field)
        else:
            return other.__rmul__(self)
    
    def __pow__(self, power):
        y = abs(power)
        if y == 1:
            new_ffe = self
        elif y == 0:
            new_ffe = self._field.one()
        else:
            new_ffe = FFE(pow(self._x, y, self._mod), self._field)
        
        if power < 0:
            new_ffe = new_ffe.inv()
        return new_ffe
    
    def multi_pows(self, powers):
        """calculate [self**i for i in powers] in parallel efficiently"""
        powers = list(powers)
        ys = map(abs, powers)
        max_val = max(ys)
        cur = self
        exp = 1
        res = [self._field.one()] * len(ys)
        while exp <= max_val:
            for i,v in enumerate(ys):
                if v & exp:
                    res[i] *= cur
            exp <<= 1
            if exp <= max_val:
                cur *= cur
        
        for i, power in enumerate(powers):
            if power < 0:
                res[i] = res[i].inv()
        return res

    def __div__(self, other):
        assert self._field == other._field
        return self * other.inv()
    
    def __neg__(self):
        return FFE(-self._x, self._field)
    
    def __pos__(self):
        return FFE(+self._x, self._field)

    def __eq__(self, other):
        if other is None:
            return False
        assert self._field == other._field
        return self._x == other._x

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        return self != self._field.zero()
    
    def __deepcopy__(self, memo):
        return self.__class__(self._x, self._field)

    def __repr__(self):
        return "%s%%%s"%(str(self._x), str(self._mod))
    
    def __hash__(self):
        return hash("%r@%r" % (self, self._field))
    
    def __serialize__(self):
        return serialize(self._x), serialize(self._field)
    
    @classmethod
    def __unserialize__(cls, serialized):
        """Returns a new FFE object out of a FFE serialized by serialize """
        x_s, field_s = serialized
        x, field = unserialize(x_s), unserialize(field_s)
        return cls(x, field)


def _egcd(a, b):
    """Extended Euclidean algorithm.
    Returns a tuple (gcd, s, t) such that:
    gcd(a,b) = s*a + t*b
    """
    if a == 0:
        return (b, 0, 1)
    else:
        div, mod = divmod(b, a)
        g, x, y = _egcd(mod, a)
        x, y = (y - x*div, x)
        return (g, x, y)

