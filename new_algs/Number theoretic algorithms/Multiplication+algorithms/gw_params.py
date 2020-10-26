"""
A module for generating recover parameters for the GWSSS secret sharing scheme.
Based on the paper:
[GW15] - Venkatesan Guruswami and Mary Wootters. Repairing reed-solomon codes. CoRR, abs/1509.04764, 2015
"""

from gf import Zmod, Extension
from polynomial import Polynomial, LinearFactors
from matrix import Matrix
from utils import log, inner_product, powers
from utils import random
from config import Config
from itertools import imap
from math import ceil
import operator

class GWParams(object):
    """Generate parameters for [GW15] reconstruction for Shamir (n,t) scheme
    @gf - the gf we live in, over some subfield we want to recover in
    @pts - list of scheme's points
    @t - the maximum degree of a polynomial of the code
    """
    def __init__(self, gf, pts, t):
        assert all(map(lambda x : x in gf, pts)), "Points not in %r" % gf
        assert len(set(pts)) == len(pts), "Points must be unique!"
        assert isinstance(gf, Extension), "Field must be an extension of some other finite-field"
        self._gf = gf
        self._pts = [x for x in pts]
        self._t = t
    
    def _linear_independant(self, elements):
        """Check if elements are linearly independant over the subfield"""
        return self._degree(elements) == len(elements)
    
    def _degree(self, elements):
        """Return the dimension of the vector space spanned by @elements over the subfield"""
        vecs = map(self._gf.to_subfield_vec, elements)
        return Matrix.matrix(vecs).rank()
    
    def generate(self, pos, good_enough=None, tries_limit=None, subgroup=None, basis=None):
        """Generate the parameters by finding good polynomials and building the parameters
        according to Proposition 8 & Remark 5 of [GW15].
        @pos - the reconstruction pos
        @good_enough - amount of subfield elements sent which is good enough for us.
                       if unset - the information theoretic best is taken (which might be impossible) 
        @tries_limit - amount of polynomial sets to try. If unset - number of tries is unlimited
        @subgroup - amount of points to randomly checks before calculating the bandwidth of the scheme
        @basis - optional specific basis of gf over subfield to use
        """
        pts = [p for p in self._pts]
        if pos not in pts:
            pts.append(pos)
        n = len(pts)
        t = self._t
        ext = self._gf.get_extension()
        
        # Set good enough to the lower bound of information needed - at least t parties, at least one element (in the big field)
        if good_enough is None:
            good_enough = -1
        good_enough = max(good_enough, t, ext)
        
        if tries_limit is None:
            tries_limit = -1
        
        # Set subgroup size for testing bandwidth
        # Only if bandwidth on subgroup seems to be better than current bandwidth we continue
        if subgroup is None:
            subgroup_fraction, subgroup_min = Config.GW_PARAMS_SUBGROUP_SIZE
            subgroup = int(ceil(n / subgroup_fraction))
            subgroup = max(subgroup, subgroup_min)
        subgroup = min(n-1, subgroup)
        subgroup_factor = float(subgroup) / n
        
        # Choose our polynomials so their evaluation in @pos will be some predefined base
        # We don't care about this degree of freedom - as it only changes our polynomial by a multiplicative scalar factor
        if basis is not None:
            assert len(basis) == ext, "Invalid size of basis supplied"
            assert self._linear_independant(basis), "Invalid basis supplied"
        else:
            # Choose the monomial basis as default
            subf = self._gf.get_subfield()
            gf_x = self._gf([subf.zero(), subf.one()])
            basis = [x for x in powers(gf_x, ext)]
        
        pol_deg = n - t - 2
        best_bandwidth = (n * ext) + 1 # <- More than the worst case bandwidth
        best_subgroup_bandwidth = int(ceil(subgroup_factor * best_bandwidth))
        shuffled_pts = [p for p in pts]
        best_pols = None
        done = False
        try_i = 0
        try:
            while not done and try_i != tries_limit:
                try_i += 1
                
                # Choose a random polynomials with a sample of the points as roots,
                # while still making sure the evaluation in `pos` will yield the `basis`
                pols = []
                for b in basis:
                    roots = random.sample(pts, pol_deg + 1) # Over sample by 1 in case @pos gets in
                    try:
                        roots.remove(pos)
                    except ValueError:
                        roots.pop(-1) # Remove someone else (arbitrary)
                    pol = LinearFactors(self._gf, roots, constraint=(pos, b))
                    pols.append(pol)
                
                # Sum the degree of the vector spaces spanned by {p(pt) | p in pols} for each pt (except pos)
                # First start with `subgroup` random points and see if 
                random.shuffle(shuffled_pts)
                pts_iter = iter(shuffled_pts)
                bandwidth = 0
                for i in xrange(subgroup):
                    pt = pts_iter.next()
                    if pt == pos:
                        pt = pts_iter.next()
                    bandwidth += self._degree(pol(pt) for pol in pols)
                
                if bandwidth > best_subgroup_bandwidth:
                    continue
                #else:
                bandwidth += sum(self._degree(pol(pt) for pol in pols) for pt in pts_iter if pt != pos)
                
                if bandwidth < best_bandwidth:
                    best_pols = pols
                    best_bandwidth = bandwidth
                    best_subgroup_bandwidth = int(ceil(subgroup_factor * best_bandwidth))
                    log.info("Found scheme with %d bandwidth (%d%%)", best_bandwidth, int(ceil((100.0 * best_bandwidth) / (ext*n))))
                    if bandwidth <= good_enough:
                        done = True
                
        except KeyboardInterrupt:
            if best_pols is None:
                raise
            # Else - continue normally
        
        basis_elements = map(lambda pol : -pol(pos), best_pols) #Notice: Negation added for correct result (mistake in [GW15] ?)
        dual = self._dual_basis(basis_elements)
        mus, mus_basis = self._calc_mus(pos, pts, best_pols)
        
        return dual, mus, mus_basis, best_bandwidth
        
    def _calc_mus(self, pos, pts, pols):
        """Calculate the mu values and a spanning base to their vector space for each party.
        Returns a tuple with mus and mus_basis:
        mus - a list mapping for each polynomial i -> a list of (pid, mu) for each party & mu needed to construct Tr(z_i * f(a*))
        mus_basis - for each party - a base for the vector space spanned by {mu}. This base has the property that mu = sum( mu_coefs_i * base_i )
                    where mu_coefs is the vector of mu (over the subfield) when projected only to the indexes `coefs`
        """
        # Polynomials chosen, now calculate the needed parameters for the scheme        
        # Mu values
        const_factor = reduce(operator.mul, (pos - b for b in pts if b != pos))
        party_factor = lambda pt : reduce(operator.mul, (pt - b for b in pts if b != pt))
        mus = []
        mus_by_party = [[] for i in xrange(len(pts))]
        for pol in pols:
            mus_i = []
            for pid, pt in enumerate(pts):
                if pt == pos:
                    continue
                mu = pol(pt) * (const_factor / party_factor(pt))
                if mu:
                    mus_i.append((pid, mu))
                    mus_by_party[pid].append(mu)
            mus.append(mus_i)

        # Find a basis for each of the parties' mus + a transformation
        # from mu to coefficients in this basis
        mus_basis = []
        for pid, p_mus in enumerate(mus_by_party):
            if len(p_mus) == 0:
                mus_basis.append(([],[]))
                continue
            
            # Perform full Gauss-Jordan elimination & Remove leftover zero rows
            m = Matrix.from_list(map(self._gf.to_subfield_vec, p_mus))
            m.rref()
            leading_coefs = []
            cur_row = 0
            for j in xrange(m.ncols()): # Find the first zero row
                if m[cur_row][j]:
                    leading_coefs.append(j)
                    cur_row += 1
                    if cur_row == m.nrows():
                        break
            for i in xrange(cur_row, m.nrows()): # Delete zero rows
                m.delete_row(-1)
            
            cur_basis = map(lambda row : self._gf.from_subfield_vec(list(row)), m.rows())
            mus_basis.append((cur_basis, leading_coefs))
    
        return mus, mus_basis

    def _dual_basis(self, basis):
        """Calculate the dual basis of @basis over the subfield.
        The algorithm used to calculate the dual basis comes from
        pages 110-111 of [FFCSE1987].
        Let e = {e_0, e_1, ..., e_{n-1}} be a basis of GF{q^n} as a
        vector space over GF{q} and d = {d_0, d_1, ..., d_{n-1}} be the
        dual basis of e. Since e is a basis, we can rewrite any d_c, 0 <=
        c <= n-1, as d_c = beta_0 e_0 + beta_1 e_1 + ... + beta_{n-1}
        e_{n-1}, for some beta_0, beta_1, ..., beta_{n-1} in GF{p}.
        Using properties of the trace function, we can rewrite the n
        equations of the form Tr(e_i d_c) = delta_{i,c} and express the
        result as the matrix vector product: A [beta_0, beta_1, ...,
        beta_{n-1}] = i_c, where the i,j-th element of A is Tr(e_i e_j)
        and i_c is the i-th column of the n x n identity matrix. Since
        A is an invertible matrix, [beta_0, beta_1, ..., beta_{n-1}] =
        A^{-1} i_c, from which we can easily calculate d_c.
        [FFCSE1987] Robert J. McEliece. Finite Fields for
                   Computer Scientists and Engineers. Kluwer Academic
                   Publishers, 1987.
        """
        assert all(map(lambda x : x in self._gf, basis)), "Basis elements not in GF"
        assert isinstance(self._gf, Extension), "Cannot find dual in %r" % self._gf
        
        n = len(basis)
        assert len(basis) == self._gf.get_extension(), "Invalid number of vectors - expected %d, got %d" % (self._gf.get_extension(), n)
        assert self._linear_independant(basis), "Invalid basis supplied"
        
        mat = Matrix.from_list([[self._gf.trace(b_i * b_j) for b_j in basis] for b_i in basis])
        inv = mat.inv()
        
        dual = []
        for col in inv.cols():
            gf_col = imap(self._gf.extend, col)
            dual_i = inner_product(gf_col, basis)
            dual.append(dual_i)
        
        # Check that dual found
        assert Matrix.from_list([[self._gf.trace(b_i * d_j) for d_j in dual] for b_i in basis]) == Matrix.identity(n, self._gf.get_subfield().one()), "Error validating dual basis!"
        return dual
