import numpy as np
import pandas as pd

from sklearn.ensemble import ExtraTreesClassifier

from cause.plotter import Plotter
from cause.predictor import ClassificationSet


class Breakdown():

    def __init__(self, data, weights, algos, name):
        self.__data = data
        self.__weights = weights
        self.__algos = algos
        self.__name = name
        # todo validate input:
        # data is an np.array with dims (num algos, num weights)

    @property
    def data(self):
        return self.__data

    @property
    def weights(self):
        return self.__weights

    @property
    def algos(self):
        return self.__algos

    @property
    def name(self):
        return self.__name

    def save_to_latex(self, outfolder="/tmp", weight=1.):
        outfile = "%s/breakdown_%s" % (outfolder, self.name)
        index = np.where(self.weights==weight)[0][0]  # location for lambda=weight
        breakdown_perc = self.data[:,index] * 100. / self.data[:,index].sum()
        # write latex table to file
        with open(outfile, "w") as f:
            for algo in range(self.data.shape[0]):
                f.write("&\t%s\t&\t%.2f\\%%\t\t\n" % (
                    self.data[algo, index], breakdown_perc[algo]))

    def plot(self, outfolder="/tmp"):
        Plotter.plot_breakdown(self, outfolder)


class Postprocessor():

    def __init__(self, dataset):
        self.__dataset = dataset

    @property
    def dataset(self):
        return self.__dataset

    def breakdown(self):
        breakdown = np.empty(shape=(0,0))
        for weight in self.dataset.weights:
            column = self.dataset.lstats[weight].get_breakdown(self.dataset.algos)
            if breakdown.shape[0] == 0:
                breakdown = column
            else:
                breakdown = np.vstack([breakdown, column])
        breakdown = np.transpose(breakdown)

        return Breakdown(breakdown, self.dataset.weights,
                         self.dataset.algos, self.dataset.name)


class FeatsPostprocessor(Postprocessor):

    def __init__(self, dataset, features):
        super().__init__(dataset)
        self.__features = features

    @property
    def features(self):
        return self.__features

    def save_feature_importances_by_weight(self, outfolder, weight):
        lstats = self.dataset.lstats[weight]
        clsset = ClassificationSet.sanitize_and_init(
            self.features.features, lstats.winners, lstats.costs)
        clf = ExtraTreesClassifier()
        clf = clf.fit(clsset.X, clsset.y.ravel())
        importances = pd.DataFrame(data=clf.feature_importances_.reshape(
                                       (1, len(clf.feature_importances_))
                                    ),
                                   columns=self.features.features.columns)
        # sort feature names by average importance
        sorted_feature_names = [name for _,name in 
                                sorted(zip(importances.mean(axis=0), self.features.features.columns))
                                ][::-1]
        importances = importances[sorted_feature_names]
        feats = pd.DataFrame(columns=["order", "value", "name"])
        feats["order"] = np.arange(len(self.features.features.columns))[::-1]
        feats["value"] = np.transpose(importances.values)
        feats["name"] = sorted_feature_names
        feats.to_csv("%s/feats_%.1f" % (outfolder, weight),
                     sep="&", index=False, line_terminator="\\\\\n")


    def save_feature_importances(self, outfolder):
        # compute feature importances for each weight
        importances = np.empty(shape=(0,0))
        for weight in self.dataset.weights:
            lstats = self.dataset.lstats[weight]
            clsset = ClassificationSet.sanitize_and_init(
                self.features.features, lstats.winners, lstats.costs)
            clf = ExtraTreesClassifier()
            clf = clf.fit(clsset.X, clsset.y)
            if importances.shape[0] == 0:
                importances = clf.feature_importances_
            else:
                importances = np.vstack([importances, clf.feature_importances_])
        # sort feature names by average importance
        sorted_feature_names = [name for _,name in 
                                sorted(zip(importances.mean(axis=0), self.features.features.columns))
                                ][::-1]
        importances = pd.DataFrame(data=importances, columns=self.features.features.columns)
        importances = importances[sorted_feature_names]
        feats = pd.DataFrame(columns=["order", "value", "name", "error"])#, \
                        #dtype={"order": np.int64, "value": np.float_, "name":np.object_, "error": np.float_})
        feats["order"] = np.arange(len(self.features.features.columns))[::-1]
        feats["value"] = importances.mean(axis=0).values
        feats["error"] = importances.std(axis=0).values
        feats["name"] = sorted_feature_names
        feats.to_csv("%s/feats" % outfolder,
                     sep="&", index=False, line_terminator="\\\\\n")
        
        Plotter.plot_feature_importances(importances, outfolder, 30)


class MALAISEPostprocessor():

    def __init__(self, stats_file):
        schema = {
            "classifier": np.object_,
            "weight": np.float_,
            "algorithm": np.object_,
            "acc_train": np.float_,
            "acc_test": np.float_,
            "mre_train": np.float_,
            "mre_test": np.float_
        }
        columns = ["classifier", "weight", "algorithm",
                   "acc_train", "acc_test", "mre_train", "mre_test"]
        stats = pd.read_csv(stats_file, header=None, names=columns, dtype=schema)
        # average random classifier runs
        self.__stats = stats.groupby(["weight", "classifier", "algorithm"]).mean().reset_index()

    @property
    def stats(self):
        return self.__stats

    def save(self, outfolder):
        acc_file = "%s/accuracy_data" % outfolder
        rmre_file = "%s/rmre_data" % outfolder
        # save accuracy to file for pgfplots
        acc = self.stats[self.stats.classifier == "MALAISE"][[
            "weight", "acc_train", "acc_test"]]
        acc.acc_train *= 100
        acc.acc_test *= 100
        np.savetxt(acc_file, acc,
                   fmt="%.1f\t&\t%.8f\t&\t%.8f",
                   newline="\t\\\\\n")
        # compute rmre
        mre_best = self.stats[self.stats.classifier == "BEST"][[
            "weight", "algorithm", "mre_train", "mre_test"]].set_index("weight")
        mre_ml = self.stats[self.stats.classifier == "MALAISE"][[
            "weight", "mre_train", "mre_test"]].set_index("weight")
        mre_rand = self.stats[self.stats.classifier == "RANDOM"][[
            "weight", "mre_train", "mre_test"]].set_index("weight")
        rmre = mre_best[["algorithm"]]
        rmre.loc[:,"rmre_train_rand"] = mre_ml.mre_train / mre_rand.mre_train 
        rmre.loc[:,"rmre_train_best"] = mre_ml.mre_train / mre_best.mre_train
        rmre.loc[:,"rmre_test_rand"] = mre_ml.mre_test / mre_rand.mre_test
        rmre.loc[:,"rmre_test_best"] = mre_ml.mre_test / mre_best.mre_test
        # save rmre to file for pgfplots
        np.savetxt(rmre_file, rmre.reset_index(),
                   fmt="%.1f\t&\t%s\t&\t%.8f\t&\t%.8f\t&\t%.8f\t&\t%.8f",
                   newline="\t\\\\\n")
        #rmre.to_csv(rmre_file, sep="&", header=False, float_format="%.5f",
        #            index=True, line_terminator="\\\\\n")


class PRAISEPostprocessor():

    def __init__(self, stats_file):
        schema = {
            "predictor": np.object_,
            "weight": np.float_,
            "ratio": np.float_,
            "acc": np.float_,
            "mse": np.float_,
        }
        columns = ["predictor", "weight", "ratio", "acc", "mse"]
        stats = pd.read_csv(stats_file, header=None, names=columns, dtype=schema)
        # average random classifier runs
        self.__stats = stats.groupby([
            "predictor", "weight", "ratio"]).mean().reset_index()

    @property
    def stats(self):
        return self.__stats

    @staticmethod
    def __filter_rmse_min_ratio(rmse, outfolder):
        rmse_best = pd.DataFrame(index=rmse.weight.unique(),
            columns=["min_ratio", "min_ratio_extra",
                     "acc", "rmse_rand", "rmse_best",
                     "acc_extra", "rmse_extra_rand", "rmse_extra_rand"])
        for weight in rmse.weight.unique():
            rmse_per_weight = rmse[rmse.weight == weight]
            min_ratio, min_ratio_extra = PRAISEPostprocessor.___rmse_over_ratio(
                rmse_per_weight, weight, outfolder)
            rmse_best.loc[weight] = [
                min_ratio, min_ratio_extra,
                rmse_per_weight[
                    rmse_per_weight.ratio == min_ratio].acc.values[0],
                rmse_per_weight[
                    rmse_per_weight.ratio == min_ratio].rmse_rand.values[0],
                rmse_per_weight[
                    rmse_per_weight.ratio == min_ratio].rmse_best.values[0],
                rmse_per_weight[
                    rmse_per_weight.ratio == min_ratio_extra].acc_extra.values[0],
                rmse_per_weight[
                    rmse_per_weight.ratio == min_ratio_extra].rmse_extra_rand.values[0],
                rmse_per_weight[
                    rmse_per_weight.ratio == min_ratio_extra].rmse_extra_best.values[0]
            ]
        return rmse_best

    @staticmethod
    def ___rmse_over_ratio(rmse, weight, outfolder):
        stats = rmse[["ratio", "rmse_best"]]
        filename = "%s/praise_rmse_over_ratio_%.1f" % (outfolder, weight)
        np.savetxt(filename, stats,
                   fmt="%.2f\t&\t%.8f",
                   newline="\t\\\\\n")
        data = stats.set_index("ratio")
        min_ratio = data.idxmin()
        Plotter.plot_data_over_ratios(
            data, "rmse_%.1f" % weight, outfolder, ylog=True)
    
        stats_extra = rmse[["ratio", "rmse_extra_best"]]
        filename_extra = "%s/praise_extra_rmse_over_ratio_%.1f" % (outfolder, weight)
        np.savetxt(filename_extra, stats_extra,
                   fmt="%.2f\t&\t%.8f",
                   newline="\t\\\\\n")
        data_extra = stats_extra.set_index("ratio")
        min_ratio_extra = data_extra.idxmin()
        Plotter.plot_data_over_ratios(
            data_extra, "rmse_extra_%.1f" % weight, outfolder, ylog=True)

        return min_ratio.values[0], min_ratio_extra.values[0]
        

    def save(self, outfolder="/tmp"):
        rmse_file = "%s/rmse_acc_data_praise" % outfolder

        # get accuracy
        acc = self.stats[self.stats.predictor == "PRAISE"][[
            "weight", "ratio", "acc"]].set_index(["weight", "ratio"])
        acc_extra = self.stats[self.stats.predictor == "PRAISE_EXTRA"][[
            "weight", "ratio", "acc"]].set_index(["weight", "ratio"])
        acc.acc *= 100.
        acc_extra.acc *= 100.

        # compute rmse
        mse_best = self.stats[self.stats.predictor == "BEST"][[
            "weight", "ratio", "mse"]].set_index(["weight", "ratio"])
        mse_praise = self.stats[self.stats.predictor == "PRAISE"][[
            "weight", "ratio", "mse"]].set_index(["weight", "ratio"])
        mse_praise_extra = self.stats[self.stats.predictor == "PRAISE_EXTRA"][[
            "weight", "ratio", "mse"]].set_index(["weight", "ratio"])
        mse_rand = self.stats[self.stats.predictor == "RANDOM"][[
            "weight", "ratio", "mse"]].set_index(["weight", "ratio"])

        # create df with all stats for each (weight, ratio) pair
        rmse = acc
        rmse.loc[:,"rmse_rand"] = mse_praise.mse / mse_rand.mse 
        rmse.loc[:,"rmse_best"] = mse_praise.mse / mse_best.mse
        ### with extrapolation
        rmse.loc[:,"acc_extra"] = acc_extra.acc
        rmse.loc[:,"rmse_extra_rand"] = mse_praise_extra.mse / mse_rand.mse 
        rmse.loc[:,"rmse_extra_best"] = mse_praise_extra.mse / mse_best.mse

        # filter by min ratio per weight
        rmse_best = PRAISEPostprocessor.__filter_rmse_min_ratio(
            rmse.reset_index(), outfolder)
        # save rmse to file for pgfplots
        np.savetxt(rmse_file, rmse_best.reset_index(),
                   fmt="%.1f\t&\t%.2f\t&\t%.2f\t&\t%.8f\t&\t%.8f\t&\t%.8f\t&\t%.8f\t&\t%.8f\t&\t%.8f",
                   newline="\t\\\\\n")
