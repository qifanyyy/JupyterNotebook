"""
Defines a general Transformation defined by a matrix.
Two types of Transformations are implemented, for BGW & DIK multiplication sub-prtocols:

Truncinator transforms evaluations of a polynomial F(X)= a_n*X^n + ... + a_0
to evaluations of some truncated polynomial (m < n) f(X)= a_m *X^m + ... + a_0
For any (unknown) polynomial.

Resmapler transforms evaluations of a polynomial F(a_1), F(a_2), ...
to the evaluations F(b_1), F(b_2), ...
for given [a_i], [b_i], for any (unknown) polynomial.
"""

from matrix import Matrix, VanderMatrix
from serializer import *

__all__ = ['Truncinator', 'Resampler']

class Transformation(object):
    """A generic transformation calculated by a matrix.
    Supports applying the transformation, lazy initialization and object serialization.
    Implementations of a specific Transformation need to implement _calc_transformation.
    """
    def __init__(self, field, lazy=False):
        self._field = field
        self._matrix = None
        if not lazy:
            self._matrix = self._calc_transformation()
    
    def apply(self, vec):
        """Apply the transformation of @vec"""
        assert all(map(lambda x : x in self._field, vec)), "Not all values are in the field"
        
        # Lazy initialization?
        if self._matrix is None:
            self._calc_transformation()
        assert len(vec) == self._matrix.ncols(), "Invalid input length, received %d expected %d" % (len(vec), self._matrix.ncols())
        
        # Perform transformation
        transformed = self._matrix * Matrix.matrix([vec]).t()
        
        typ = type(vec)
        if isinstance(transformed, typ) is False:
            transformed = typ(transformed)
        return transformed
    
    def __call__(self, vec):
        return self.apply(vec)
    
    def __serialize__(self):
        """Return a printable encoding of the Transformation (including its internal data & transformation)"""
        return serialize(self._field), serialize(self._matrix)
    
    @classmethod
    def __unserialize__(cls, serialized):
        """Creates a new Transformation object by unserializing given @serialized string"""
        F_s, mat_s = serialized
        F, mat = unserialize(F_s), unserialize(mat_s)
        self = cls(F, lazy=True)
        self._matrix = mat
        return self
    

class Truncinator(Transformation):
    """Truncates polynomial samples.
    A truncinator object is defined by a vector @xs of sample positions,
    degree @n of the source polynomial & degree @m of a destination polynomial (m < n).
    An input <F(xs_1), ..., F(xs_k)> is transformed to <f(xs_1), ..., f(xs_k)>
    where f is F truncated to degree m.
    All calculations are done over the Zmod @field.
    The transformation itself is (V * P * V^-1) where V is the Vandermonde for [xs_i]
    and P is a projection matrix from projecting n to m.
    """
    def __init__(self, xs, n, m, field, lazy=False):
        """
        @xs - vector of sample positions (x-axis values)
        @n - degree of source polynomial
        @m - degree of dest polynomial
        @field - a Zmod in which evaluation is done in
        @lazy - do lazy initialization of the transformation?
                This initialization may take a lot of time and resources.
        """
        assert n > m, "n (%d) must be bigger than m (%d) for truncation" % (n, m)
        assert len(xs) >= n, "At least n evaluation points must be supplied (xs)"
        assert len(xs) == len(set(xs)), "All evaluation points must be unique (xs)"
        assert all(map(lambda x : x in field, xs)), "Not all evaluation point are in the field"
        self._n = n
        self._m = m
        self._xs = xs
        Transformation.__init__(self, field, lazy=lazy)
    
    def _calc_transformation(self):
        """Calculate the matrix for the transformation"""
        # Generate the vandermonde matrix & calculate its inverse (heavy part)
        one = self._field.one()
        zero = self._field.zero()
        
        # Create the Vandermonde matrix, create the projection matrix
        # and calculate the multiplication of the two with the inverse
        vander = VanderMatrix(self._xs)
        proj = Matrix.diag([one]*self._m + [zero]*(len(self._xs) - self._m))
        transformation = vander * proj * vander.inv()
        return transformation

    def reduce(self, vec):
        """Reduce the vector @vec <F(xs_1), ..., F(xs_k)>
        from the poly of degree n to the truncated poly of degree m
        """
        return self.apply(vec)
    
    def __serialize__(self):
        """Return a printable encoding of the Truncinator (including its internal data & transformation)"""
        F_s = serialize(self._field)
        mat_s = serialize(self._matrix)
        xs = [serialize(x) for x in self._xs]
        return F_s, mat_s, xs, self._n, self._m
    
    @classmethod
    def __unserialize__(cls, serialized):
        """Creates a new Truncinator object by unserializing given @serialized data"""
        F_s, mat_s, xs_s, n, m = serialized
        F, mat = unserialize(F_s), unserialize(mat_s)
        xs = [unserialize(x) for x in xs_s]
        self = cls(xs, n, m, F, lazy=True)
        self._matrix = mat
        return self

class Resampler(Transformation):
    """Calculate new samples from given polynomial samples at different positions.
    A Resampler object is defined by a vector @srcs of source sample positions,
    a vector @dsts of destination sample positions.
    An input <F(srcs_1), ..., F(srcs_n)> is transformed to <F(dsts_1), ..., f(dsts_m)>
    All calculations are done over the Zmod @field.
    The transformation itself is (V_d * V_s^-1) where V_s, V_d are the
    Vandermonde matrices for [src_i], [dst_i] respectively.
    This transformation is hyper-invertible if all evaluation points srcs & dsts are different.
    """
    def __init__(self, srcs, dsts, field, lazy=False):
        """
        @srcs - vector of src sample positions (x-axis values)
        @dsts - vector of dst sample positions (x-axis values)
        @field - a Zmod in which evaluation is done in
        @lazy - do lazy initialization of the transformation?
                This initialization may take a lot of time and resources.
        """
        assert all(map(lambda x : x in field, srcs)), "Not all src evaluation point are in the field"
        assert all(map(lambda x : x in field, dsts)), "Not all dst evaluation point are in the field"
        assert len(srcs + dsts) == len(set(srcs + dsts)), "All evaluation points should be unique"
        self._as = srcs
        self._bs = dsts
        Transformation.__init__(self, field, lazy=lazy)
    
    def _calc_transformation(self):
        """Calculate the matrix for the transformation"""
        sampler = VanderMatrix(self._bs, ncols=len(self._as))
        interpolator = VanderMatrix(self._as).inv()
        transformation = sampler * interpolator
        return transformation
    
    def src_len(self):
        """Returns the number of samples needed as input"""
        return len(self._as)
    
    def dst_len(self):
        """Returns the number of samples returned by the transformation"""
        return len(self._bs)
    
    def apply(self, vec, n_results=None):
        """Resample the given samples of @vec.
        @n_results - If set, return the first n_results only
        """
        res = Transformation.apply(self, vec)
        if n_results is None:
            return res
            
        assert n_results is None or 0 <= len(res) <= n_results, "Transformation returned less results than requested!"
        return res[:n_results]
    
    def __serialize__(self):
        """Return a printable encoding of the Truncinator (including its internal data & transformation)"""
        F_s = serialize(self._field)
        mat_s = serialize(self._matrix)
        srcs = [serialize(x) for x in self._as]
        dsts = [serialize(x) for x in self._bs]
        return F_s, mat_s, srcs, dsts
    
    @classmethod
    def __unserialize__(cls, serialized):
        """Creates a new Truncinator object by unserializing given @serialized data"""
        F_s, mat_s, srcs_s, dsts_s = serialized
        F, mat = unserialize(F_s), unserialize(mat_s)
        srcs = [unserialize(x) for x in srcs_s]
        dsts = [unserialize(x) for x in dsts_s]
        self = cls(srcs, dsts, F, lazy=True)
        self._matrix = mat
        return self
