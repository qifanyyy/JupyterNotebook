import numpy as np
import copy


def updateK(e, K):
    newe = copy.deepcopy(e)
    n = len(newe)
    setfull = list(range(K))
    ind = np.random.randint(n)
    b = newe[ind]
    del setfull[newe[ind]]
    b_prime = np.random.choice(setfull)
    newe[ind] = b_prime
    return newe, ind, b, b_prime


def Rdiff(e, c):
    K = np.max(c) + 1
    Ze = Zform(e, K)
    Zc = Zform(c, K)
    R = np.matmul(np.transpose(Ze), Zc).astype(int)
    return R


def Zform(e, K):
    n = len(e)
    Ze = np.zeros((n, K))
    Ze[np.arange(n), e] = 1
    return Ze


class sbm:
    def __init__(self, R, Pstar, e0, niter, beta1=1, beta2=1,
                 xi=1, knowp=False, show=False):
        self.Pstar = Pstar
        self.beta1 = beta1
        self.beta2 = beta2
        self.xi = xi
        self.K = R.shape[0]
        self.n = np.sum(R)
        self.c = np.repeat(np.arange(self.K), np.sum(R, axis=0))
        self.A = self.genA()
        self.e0 = e0
        self.niter = niter
        self.postattrue = self.logpostpdf(self.c, knowp)
        self.show = show

    def updateZe(self, Ze, ind, b, b_prime):
        newZe = copy.deepcopy(Ze)
        newZe[ind, b] = Ze[ind, b] - 1
        newZe[ind, b_prime] = Ze[ind, b_prime] + 1
        return newZe

    def updateMat(self, matO, matN, ind, b, b_prime, Ze):
        A_ind = self.A[ind, ].reshape((-1, 1))
        tmp = (A_ind * Ze).sum(axis=0)  # dim: k
        new_matO = matO.copy()
        new_matO[b, :] = new_matO[b, :] - tmp
        new_matO[b_prime, :] = new_matO[b_prime, :] + tmp
        new_matO[:, b] = new_matO[:, b] - tmp
        new_matO[:, b_prime] = new_matO[:, b_prime] + tmp

        new_matN = matN.copy()
        nZe = Ze.sum(axis=0)
        new_matN[b, :] = new_matN[b, :] - nZe
        new_matN[b_prime, :] = new_matN[b_prime, :] + nZe
        new_matN[:, b] = new_matN[:, b] - nZe
        new_matN[:, b_prime] = new_matN[:, b_prime] + nZe
        new_matN[b, b] = new_matN[b, b] + 1 + 1
        # new_matN[b_prime, b_prime] = new_matN[b_prime, b_prime] + 1 - 1
        new_matN[b_prime, b] = new_matN[b_prime, b] - 1
        new_matN[b, b_prime] = new_matN[b, b_prime] - 1
        return new_matO, new_matN

    def loggam_apprx(self, x):
        tmp = (x + 1 / 2) * np.log(x) - x + 1 / 2 * np.log(2 * np.pi)
        return tmp

    def genA(self):
        Zc = Zform(self.c, self.K)
        Omega = np.matmul(np.matmul(Zc, self.Pstar), np.transpose(Zc))
        A = np.random.binomial(1, Omega)
        tmp = np.triu(A) - np.diag(np.diag(A))
        A = tmp + np.transpose(tmp)
        return A

    def logpostpdf(self, e, knowp=False):
        Ze = Zform(e, self.K)
        if knowp:
            [a, b] = self.Pstar[0, :2]
            ZZ = np.matmul(Ze, np.transpose(Ze))
            OS = np.sum(ZZ * self.A) / 2
            NS = (np.sum(ZZ) - self.n) / 2
            p = (np.log(a * self.n * (1 - b)) - np.log(b * self.n * (1 - a))) * OS - np.log((1 - b) / (1 - a)) * NS
            return p
        else:
            matO = np.matmul(np.matmul(np.transpose(Ze), self.A), Ze)
            matN = np.matmul(
                np.matmul(np.transpose(Ze), np.ones([self.n, self.n])), Ze
            ) - np.diag(np.sum(Ze, axis=0))
            matY = matN - matO
            p = np.sum(
                self.loggam_apprx(matO + self.beta1 - 1) +
                self.loggam_apprx(matY + self.beta2 - 1) -
                self.loggam_apprx(matN + self.beta1 + self.beta2 - 2)
            ) / 2
            return p

    def logpostpdf_fast(self, matO, matN):
        matY = matN - matO
        p = np.sum(
            self.loggam_apprx(matO + self.beta1 - 1) +
            self.loggam_apprx(matY + self.beta2 - 1) -
            self.loggam_apprx(matN + self.beta1 + self.beta2 - 2)
        ) / 2
        return p

    def MHsampler(self, e0=None, niter=None, knowp=False, vsteps=100):
        '''
        Args:
            e0: init
            niter: total # of iterations
            K: # of class
            beta1, beta2: hyper-param
            A: adjacency matrix
            xi: temperature
            c: true label assignment
        '''
        if e0 is None:
            e0 = self.e0
        if niter is None:
            niter = self.niter

        curr_e = copy.deepcopy(e0)
        curr_Ze = Zform(curr_e, self.K)
        curr_matO = np.matmul(
            np.matmul(np.transpose(curr_Ze), self.A), curr_Ze)
        curr_matN = np.matmul(
            np.matmul(
                np.transpose(curr_Ze), np.ones([self.n, self.n])), curr_Ze
        ) - np.diag(np.sum(curr_Ze, axis=0))

        logPost = []
        logPost.append(self.logpostpdf_fast(curr_matO, curr_matN))
        # logPost.append(self.logpostpdf(e0, knowp))
        n_mis = []

        for i in np.arange(1, niter):
            # newe = updateK(currente, self.K)
            new_e, ind, b, b_prime = updateK(curr_e, self.K)
            new_Ze = self.updateZe(curr_Ze, ind, b, b_prime)
            new_matO, new_matN = self.updateMat(
                curr_matO, curr_matN, ind, b, b_prime, curr_Ze)

            # logNew = self.logpostpdf(newe, knowp)
            logNew = self.logpostpdf_fast(new_matO, new_matN)
            logdiff = logNew - logPost[i - 1]
            tmp = np.random.uniform(0, 1)

            if tmp < np.exp(self.xi * logdiff):
                curr_e, curr_Ze = new_e, new_Ze
                curr_matO, curr_matN = new_matO, new_matN
                logPost.append(logNew)
            else:
                logPost.append(logPost[i - 1])

            # if i % vsteps == 0:
            #     R = Rdiff(currente, self.c)
            #     mist = np.sum(R - np.diag(np.diag(R)))
            #     print("iteration: {}, mistake: {}".format(i, mist))
            #     if self.show:
            #         print(R)
            #     n_mis.append(mist)

        class dummy:
            pass

        res = dummy()
        res.logPost = logPost
        res.label = curr_e
        res.n_mis = n_mis
        res.finalR = Rdiff(curr_e, self.c)

        return res
