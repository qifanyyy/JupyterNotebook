from utils import log, copy, inner_product
from operator import mul
from itertools import izip, imap
from gf import Zmod, Extension, FFE
from polynomial import Polynomial

class SecretSharingScheme(object):
    """Genereal secret sharing scheme template.
    represents a scheme for sharing between @n parties, with threshold @t, where secret and shares are of type supporting
    arithmetic operations, __deepcopy__, __repr__, __serialize__ & class method __unserialize__
    """
    def __init__(self, n, t):
        self._n = n
        self._t = t

    def share(self, secret, *args, **kwargs):
        """Share @secret. Returns n shares"""
        ret = self._share(secret, *args, **kwargs)
        assert len(ret) == self._n, "Invalid number of shares returned (Got %d expected %d)" % (len(ret), self._n)
        return ret
    
    def preprocess(self, share, *args, **kwargs):
        """Preprocessing on share before sending to reconstruction.
        Must be called on shares before reconstruction is made
        """
        return share
    
    def reconstruct(self, shares, *args, **kwargs):
        """Reconstruct the secret from given shares.
        If reconstruction is not possible None returned.
        """
        return self._recon(shares, *args, **kwargs)

class NullSSS(SecretSharingScheme):
    """The null secret sharing gives everybody the secret.
    It can be looked at as a Shamir-Secret sharing with t=0.
    """
    def __init__(self, n, t):
        SecretSharingScheme.__init__(self, n, t)
    
    def _share(self, secret):
        return [copy.deepcopy(secret) for i in xrange(self._n)]
    
    def _recon(self, shares):
        if isinstance(shares, dict):
            shares = shares.values()
        if not all(map(shares[0].__eq__, shares)):
            log.error("Inconsistent shares received in Null-scheme reconstruction")
            return None
        secret = copy.deepcopy(shares[0])
        return secret

class ShamirSSS(SecretSharingScheme):
    """Shamir Secret Sharing Scheme over a finite field.
    @field - the FF which we live in.
    @points - the n x-values by which shares will be evaluated and reconstructed
    @secret_pos - an element in @field indicating the x-value of the secret in the scheme.
    """
    def __init__(self, n, t, field, points, secret_pos=None):
        SecretSharingScheme.__init__(self, n, t)
        assert all(map(lambda p : p in field, points)), "Points not in scheme's field"
        assert len(points) == n, "Wrong number of points: Received %d, expected %d" % (len(points), n)
        assert secret_pos is None or secret_pos in field, "Secret's position not in scheme's field"
        assert secret_pos not in points, "Cannot create a secure scheme when position is one of the points"
        self._gf = field
        self._points = [x for x in points]
        if secret_pos is None:
            secret_pos = field.zero()
        self._default_pos = secret_pos
    
    def _share(self, secret, pos=None, pos_index=None):
        """Share @secret : generate a random polynomial F with F(@pos) = @secret,
        and return a list of F(x) for all scheme's points.
        @pos - position of the secret. When None - position is set to 0 (free factor)
        """
        # Set the constraints vector - the position of our secret
        pos = self._get_pos(pos, pos_index)
        assert pos is None or pos in self._gf, "Position not in scheme's field"
        assert secret in self._gf, "Secret not in scheme's field"
        
        # Generate a random polynomial with f(pos) = secret
        poly = Polynomial.rand(self._gf, self._t, constraint=(pos, secret))
        log.debug("Sharing %r with %r", secret, poly)
        
        # Create and return the shares - evaluate the polynomial at all points
        shares = poly.evaluate(self._points)
        return shares
    
    def _recon(self, shares, pos=None, pos_index=None):
        """Reconstruct a secret stored in @pos from the given shares.
        @shares may be a dictionary mapping party->share, containing more than t pairs.
                if @shares is a regular iterable, it has to have exactly n values and
                x values are taken from initialization.
        @pos - position of the secret. Assumed zero (free factor) if not supplied
        """
        assert len(shares) > self._t, "Not enough shares given: Received %d, expected at least %d" % (len(shares), self._t + 1)
        assert len(shares) <= self._n, "Too many shares received %d > %d" % (len(shares), self._n)
        if isinstance(shares, dict) is False:
            shares = dict(izip(self._points, shares))
        assert all(imap(lambda x : x in self._gf, shares.itervalues())), "Shares not in scheme's field"
        
        pos = self._get_pos(pos, pos_index)
        assert pos in self._gf, "Position not in scheme's field"
        
        xs, ys = zip(*shares.iteritems())
        
        # Perform Lagrange interpolation to get f(pos)
        f_x = self._gf.zero()
        xs_mul = reduce(mul, (pos - x for x in xs))
        for i in xrange(len(xs)):
            # Calculate cur lagrange polynomial
            denominator = pos - xs[i] # The part to be removed from xs_mul
            for j in xrange(len(xs)):
                if i == j:
                    continue
                denominator *= (xs[i] - xs[j])
            lagrange_i = xs_mul * denominator.inv()
            f_x += ys[i] * lagrange_i
        
        return f_x
    
    def _get_pos(self, pos, pos_index):
        """Determine the position for received arguments"""
        if pos is not None:
            assert pos_index is None, "Can't use both pos and pos_index"
            return pos
        elif pos_index is not None:
            return self._points[pos_index]
        else:
            return self._default_pos

class GWSSS(ShamirSSS):
    """Shamir Secret Sharing Scheme over a finite field with [GW15] low-bandwidth reconstruction.
    @params - a dictionary mapping pos -> ([v_i], [mu_ij]) for the reconstruction
              [v_i] - the dual basis of the position's basis z_i
              [mu_ij] - for each z_i: list of needed (pid,mu) pairs
    """
    def __init__(self, n, t, field, points, secret_pos=None, params=None):
        assert isinstance(field, Extension), "GW reconstruction only available over Extension fields"
        ShamirSSS.__init__(self, n, t, field, points, secret_pos)
        if params is None:
            params = {}
        self._params = params
    
    def preprocess(self, share, src, pos=None, pos_index=None):
        """Return the needed trace functionals of the share as a mu -> Tr(mu * share) map
        @src - the soruce party.
        @pos - the position to be recovered.
        @pos_index - The index to @points given as part of factory in initialization
        If both @pos and @pos_index are None, default pos is taken.
        """
        pos = self._get_pos(pos, pos_index)
        assert pos in self._gf, "Position not in scheme's field"
        assert share in self._gf, "%r not in field %r" % (share, self._gf)
        assert pos in self._params, "Reconstruction of position %r undefined" % pos
        
        # Return Tr(b_i * share) for all b_i in the basis of vector space
        # spanned by my needed mu values. These traces can be later used
        # to calculate Tr(mu * share) for all of these mu values
        _, _, mus_basis, _ = self._params[pos]
        basis, _ = mus_basis[src]
        res = [self._gf.trace(share, b) for b in basis]
        log.debug("GWSSS prep %d : %d", src, len(res))
        return res
    
    def _recon(self, traces, pos=None, pos_index=None):
        """Reconstruct the secret from position @pos using the given @traces.
        @traces - a data structure st. traces[p] = [Tr(b_i * f(p))] for all 
        vectors b_i in the defined [b_i] mu's basis (from the generated parameters).
        """
        pos = self._get_pos(pos, pos_index)
        assert pos in self._params, "Reconstruction of position %r undefined" % pos
        dual, mus, mus_basis, _ = self._params[pos]

        # Calculate mu's traces from the parameter basis:
        # Tr(mu * f(p)) = sum( t_i * Tr(b_i * f(p)) )
        # Where [t_i] is defined by mu = sum(t_i * b_i).
        # But basis b was chosen so [t_i] is made of values
        # of mu as viewed as a vector over the subfield.
        mu_traces = [dict() for _ in xrange(len(traces))]
        for m_i in mus:
            for pid, mu in m_i:
                basis, indices = mus_basis[pid]
                mu_subf = self._gf.to_subfield_vec(mu)
                coefs = (mu_subf[i] for i in indices)
                res = inner_product(traces[pid], coefs)
                mu_traces[pid][mu] = res
        
        # Calc and sum for all i: tr(z_i*f(pos)) * v_i , using:
        #    tr(z_i*f(pos)) = tr(mu_i_1*f(p_1)) + ... + tr(mu_i_n*f(p_n))
        subzero = self._gf.get_subfield().zero()
        res = self._gf.zero()
        for v_i, m_i in izip(dual, mus):
            tr_z_subfield = sum((mu_traces[pid][mu] for pid, mu in m_i), subzero)
            res += self._gf.extend(tr_z_subfield) * v_i
        return res
