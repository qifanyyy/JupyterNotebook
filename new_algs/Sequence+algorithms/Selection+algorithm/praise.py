import numpy as np
import csv
from sklearn.preprocessing import LabelEncoder

from cause.predictor import Predictor
from cause.predictor import Evaluator


class PRAISEPredictor(Predictor):
    def __init__(self, pstats, lstats, sstats, lstats_sample):
        super().__init__(lstats)
        self.__pstats = pstats
        self.__lstats = lstats
        self.__sstats = sstats
        self.__lstats_sample = lstats_sample

    @property
    def ratio(self):
        return self.sstats.ratio

    @property
    def name(self):
        return self.sstats.name

    @property
    def pstats(self):
        return self.__pstats

    @property
    def lstats(self):
        return self.__lstats

    @property
    def sstats(self):
        return self.__sstats

    @property
    def lstats_sample(self):
        return self.__lstats_sample

    def run(self, outfolder="/tmp"):
        #stats_file = "%s/%s_stats_%.1f_%.2f" % (
        #    outfolder, self.name, self.weight, self.ratio)

        stats_file = "%s/%s_stats" % (outfolder, self.name)

        index = self.lstats_sample.winners.index

        y_true = self.lstats.winners.loc[index].values
        y_pred = self.lstats_sample.winners.values
        y_pred_extra = self.lstats_sample.winners_extra.values
        costs = self.lstats.costs.loc[index]
        
        # encode class labels to numbers
        le = LabelEncoder().fit(self.lstats.costs.columns.values)
        y_true = le.transform(y_true)
        y_pred = le.transform(y_pred)
        y_pred_extra = le.transform(y_pred_extra)
        y_true = np.reshape(y_true, (y_true.shape[0], 1))
        y_pred = np.reshape(y_pred, (y_pred.shape[0], 1))
        y_pred_extra = np.reshape(y_pred_extra, (y_pred_extra.shape[0], 1))
        # reorder cost columns to be sorted in encoded order
        new_costs_columns = le.inverse_transform(np.sort(le.transform(costs.columns)))
        costs = costs[new_costs_columns].values

        # compute costs with overhead
        costt_ovhd = PRAISEPredictor.__compute_costt_ovhd(
            self.pstats.times.loc[index], self.sstats.t_ovhd)
        costs_ovhd = (
                (self.weight * self.pstats.costw.loc[index]) ** 2 +
                (
                    (1 - self.weight) *
                    (self.pstats.costt.loc[index].add(costt_ovhd['0'], axis='index'))
                ) ** 2
            ) ** 0.5
        costs_ovhd = costs_ovhd[new_costs_columns].values

        acc = Evaluator.accuracy(y_true, y_pred)
        mse = Evaluator.mre_ovhd(y_true, y_pred, costs, costs_ovhd)
        acc_extra = Evaluator.accuracy(y_true, y_pred_extra)
        mse_extra = Evaluator.mre_ovhd(y_true, y_pred_extra, costs, costs_ovhd)

        stats = ["PRAISE", self.weight, self.ratio, acc, mse]
        stats_extra = ["PRAISE_EXTRA", self.weight,
            self.ratio, acc_extra, mse_extra]

        with open(stats_file, "a") as f:
            csv.writer(f).writerow(stats)
            csv.writer(f).writerow(stats_extra)

        # random selection
        for _ in range(100):
            y_rand = np.random.choice(le.transform(le.classes_),
                                    y_true.shape[0])
            acc_rand = Evaluator.accuracy(y_true, y_rand)
            mre_rand = Evaluator.mre(y_true, y_rand, costs)
            stats_rand = ["RANDOM", self.weight, self.ratio,
                acc_rand, mre_rand]
            with open(stats_file, "a") as f:
                csv.writer(f).writerow(stats_rand)

        # best algo selection
        u, indices = np.unique(y_true, return_inverse=True)
        best_algo = u[np.argmax(np.bincount(indices))]
        y_best = np.full(y_true.shape[0], best_algo, dtype=int)
        acc_best = Evaluator.accuracy(y_true, y_best)
        mre_best = Evaluator.mre(y_true, y_best, costs)
        stats_best = ["BEST", self.weight, self.ratio,
            acc_best, mre_best]
        with open(stats_file, "a") as f:
            csv.writer(f).writerow(stats_best)


    @staticmethod
    def __compute_costt_ovhd(times, t_ovhd):
        tmin = times.min(axis=1)
        tmax = times.max(axis=1)
        costt_ovhd = t_ovhd.div(
            tmax - tmin, axis="index").fillna(0.)
        return costt_ovhd
