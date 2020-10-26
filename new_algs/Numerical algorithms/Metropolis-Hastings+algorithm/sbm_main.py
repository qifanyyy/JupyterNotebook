import numpy as np
import sbm
import pickle
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument(
    '--seed', '-seed',
    type=int, default=19931028,
    help="random seeds for numpy. Default: 19931028."
)

parser.add_argument(
    '--size',
    type=lambda s: list(map(int, s.split(","))), default="250,250",
    help="group size of each class. Default: 250,250 for two classes."
)

parser.add_argument(
    '--prob_p', '-p',
    type=float, default=None,
    help="connection prob within communities. Default: 0.48."
)

parser.add_argument(
    '--prob_q', '-q',
    type=float, default=None,
    help="connection prob between communities. Default: 0.32."
)

parser.add_argument(
    '--niter',
    type=int, default=10,
    help="niter * n. Default: 10."
)

parser.add_argument(
    '--vsteps',
    type=int, default=100,
    help="steps showing result."
)

parser.add_argument(
    "--trial", "-t",
    type=str, default="1",
    help="which experiment you're running now. Default: 1."
)

parser.add_argument(
    '--beta1', '-b1',
    type=float, default=1.0,
    help="Beta 1. Kappa in paper. Default: 1.0."
)

parser.add_argument(
    '--beta2', '-b2',
    type=float, default=1.0,
    help="Beta 2. Kappa in paper. Default: 1.0."
)

parser.add_argument(
    '--xi',
    type=float, default=1.0,
    help="temperature parameter xi. Default: 1.0."
)

parser.add_argument(
    '--repeat',
    type=int, default=1,
    help="Repeat experiment under same dataset for ? times. Default: 1."
)

parser.add_argument(
    '--Pstar',
    type=lambda s: list(map(float, s.split(","))), default=None,
    help="Connectivity matrix defined by user. \
    Default is None (homogenous matrix w/ input p,q). Default: None."
)

parser.add_argument(
    '--alginitR',
    type=lambda s: list(map(int, s.split(","))), default=None,
    help="True matrix R (diagonal). Default is none, \
    meaning same class size. (row by row)"
)

parser.add_argument(
    '--knowp',
    type=bool, default=False,
    help="Whether know P. Default is no."
)

parser.add_argument(
    '--show',
    type=bool, default=False,
    help="Show R during sampling."
)

parser.add_argument(
    '--note',
    type=str, default=""
)


def main(args):

    K = len(args.size)
    if args.prob_q is None or args.prob_q is None:
        Pstar = pickle.load(open("Pstar_unbalanced.pkl", "rb"))
        assert len(Pstar) == K
        args.numclass = K
        name_extra = ""
    else:
        p = args.prob_p
        q = args.prob_q
        Pstar = q * np.ones([K, K]) + np.diag((p - q) * np.ones(K))
        name_extra = "p" + str(p) + "q" + str(q)

    if args.alginitR is None:
        alginitR = np.diag(args.size)
        c = np.repeat(np.arange(K), args.size)
    else:
        assert len(args.alginitR) == K ** 2
        alginitR = np.array(args.alginitR).reshape((K, K))
        c = np.repeat(np.arange(K), np.sum(alginitR, axis=0))

    n = len(c)
    # print("=" * 10 + " Print out your input " + "=" * 10)
    # for arg in vars(args):
    #     print(arg, getattr(args, arg))

    # print("=" * 30)

    np.random.seed(args.seed)

    niter = args.niter * n

    attmpt = sbm.sbm(alginitR, Pstar, e0=None, niter=niter,
                     knowp=False, show=args.show, xi=args.xi)

    dirmake = args.note + "/K" + str(K) + "n" + str(n) +\
              "xi" + str(args.xi) + name_extra +\
              "_exp" + args.trial + "/"
    if not os.path.exists(dirmake):
        os.makedirs(dirmake)

    for repeat_mark in range(args.repeat):
        if args.alginitR is None:
            e0 = np.zeros((n,)).astype(int)
            ind = np.random.permutation(n)
            halfn = int(n / 2)  # half wrong
            e0[ind[:halfn]] = c[ind[:halfn]]
            e0[ind[halfn:]] = np.random.randint(K, size=halfn)
            alginitR = sbm.Rdiff(e0, c)
        else:
            e0 = np.concatenate(list(
                map(lambda x: np.repeat(np.arange(K), x), alginitR.T)))

        logPostList = []
        misList = []
        # labelList = []
        count = 1
        RList = []
        initR = alginitR

        while np.sum(initR - np.diag(np.diag(initR))) > 0 and count < 5:
            initR = sbm.Rdiff(e0, c)
            print("initial mistake is {}".format(
                np.sum(initR - np.diag(np.diag(initR)))))

            res = attmpt.MHsampler(
                e0=e0, niter=niter,
                knowp=args.knowp, vsteps=args.vsteps)
            e0 = res.label
            logPostList.append(res.logPost)
            misList.append(res.n_mis)
            RList.append(res.finalR)
            count = count + 1
        finalR = sbm.Rdiff(e0, attmpt.c)
        mist = np.sum(finalR - np.diag(np.diag(finalR)))

        with open(dirmake + "input_repeat" + str(repeat_mark) + ".pkl", "wb") as out:
            pickle.dump(
                [attmpt.K, attmpt.n, attmpt.niter, Pstar, alginitR], out)

        # save_figs
        with open(dirmake + "output_repeat" + str(repeat_mark) + ".pkl", "wb") as out:
            pickle.dump(
                [logPostList, mist, RList, attmpt.postattrue], out)


if __name__ == "__main__":

    args = parser.parse_args()
    main(args)
    # tf.app.run(main)
