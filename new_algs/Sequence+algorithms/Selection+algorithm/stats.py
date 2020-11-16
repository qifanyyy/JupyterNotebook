import numpy as np
import pandas as pd
import yaml

from cause.helper import Algorithm_Names
from cause.helper import Stochastic_Algorithm_Names
from cause.plotter import Plotter


class RawStats():

    def __init__(self, name, df, algos):
        self.__name = name
        self.__df = df
        self.__algos = algos

    @property
    def df(self):
        return self.__df

    @property
    def name(self):
        return self.__name

    @property
    def data(self):
        return self.__df.values

    @property
    def columns(self):
        return self.__df.columns

    @property
    def algos(self):
        return self.__algos

    def get_welfares(self):
        welfares = self.df.pivot(
            index='instance', columns='algorithm', values='welfare')
        # reorders columns
        return welfares[self.algos]

    def get_times(self):
        times = self.df.pivot(
            index='instance', columns='algorithm', values='time')
        return times[self.algos]

    def save(self, filename):
        pass

    @staticmethod
    def load(filename):
        pass


class RawSampleStats():

    def __init__(self, name, df, algos):
        self.__name = name
        self.__df = df
        self.__algos = algos
        self.__ratios = df.ratio.unique()

    @property
    def df(self):
        return self.__df

    @property
    def name(self):
        return self.__name

    @property
    def data(self):
        return self.__df.values

    @property
    def columns(self):
        return self.__df.columns

    @property
    def algos(self):
        return self.__algos

    @property
    def ratios(self):
        return self.__ratios

    def get_welfares(self, ratio):
        welfares = self.df[self.df.ratio == ratio].pivot(
            index='instance', columns='algorithm', values='welfare')
        # reorders columns
        return welfares[self.algos]

    def get_times(self, ratio):
        times = self.df[self.df.ratio == ratio].pivot(
            index='instance', columns='algorithm', values='time')
        return times[self.algos]


class RawStatsOptimal(RawStats):

    def __init__(self, name, df):
        super().__init__(name, df, [x.name for x in Algorithm_Names])

    def get_welfares_feasible(self):
        welfares = self.get_welfares()
        # get infeasible instances and drop rows
        index_infeasible = welfares.index[welfares.CPLEX == 0]
        return welfares.drop(index_infeasible)

    def get_times_feasible(self):
        welfares = self.get_welfares()
        times = self.get_times()
        # get infeasible instances and drop rows
        index_infeasible = welfares.index[welfares.CPLEX == 0]
        return times.drop(index_infeasible)

    def plot(self, outfolder="/tmp"):
        outfile_welfare = "%s/welfare_%s" % (outfolder, self.name)
        outfile_time = "%s/time_%s" % (outfolder, self.name)

        welfares = self.get_welfares_feasible()
        times = self.get_times_feasible()

        # normalize welfare and time by values of optimal algorithm (cplex)
        welfares = welfares.div(welfares.CPLEX, axis=0).multiply(100., axis=0)
        times = times.div(times.CPLEX, axis=0).multiply(100., axis=0)

        Plotter.boxplot_average_case(
            welfares.values, self.algos, outfile_welfare,
            ylabel="% of optimal welfare (CPLEX)")
        Plotter.boxplot_average_case(
            times.values, self.algos, outfile_time,
            top=100000, bottom=0.01, ylog=True,
            ylabel="% of time of optimal algorithm (CPLEX)")


class RawStatsRandom(RawStats):

    def __init__(self, name, df):
        super().__init__(
            name, df, [x.name for x in Stochastic_Algorithm_Names])

    def get_welfares(self):
        return self.df[['instance', 'algorithm', 'welfare']]

    def get_times(self):
        return self.df[['instance', 'algorithm', 'time']]

    def __get_normalized_welfares(self):
        welfares = self.get_welfares()
        # normalize welfare by average value on each instance
        welfares_means = pd.DataFrame(
            welfares.groupby(['instance', 'algorithm'])
                    .welfare.mean().reset_index(name='mean_welfare'))
        welfares = welfares.merge(welfares_means)
        welfares.eval(
            'welfare = (welfare / mean_welfare - 1.) * 100.', inplace=True)
        welfares = welfares.dropna()
        return welfares

    def plot(self, outfolder="/tmp"):
        outfile = "%s/random_%s" % (outfolder, self.name)
        welfares = self.__get_normalized_welfares()
        data = []
        for algo in self.algos:
            data.append(welfares[welfares.algorithm == algo].welfare.values)
            print("[%s] min = %.2f, max = %.2f" % (algo,
                welfares[welfares.algorithm == algo].welfare.min(),
                welfares[welfares.algorithm == algo].welfare.max()))
        Plotter.boxplot_random(data, self.algos, outfile)


class ProcessedStats():

    def __init__(self, name, algos, welfares, times, costw, costt):
        self.__name = name
        self.__algos = algos
        self.__welfares = welfares
        self.__times = times
        self.__costw = costw
        self.__costt = costt

    @property
    def name(self):
        return self.__name

    @property
    def welfares(self):
        return self.__welfares

    @property
    def times(self):
        return self.__times

    @property
    def costw(self):
        return self.__costw

    @property
    def costt(self):
        return self.__costt

    @property
    def algos(self):
        return self.__algos

    @staticmethod
    def load(filename):
        with open(filename, "r") as f:
            dobj = yaml.load(f, Loader=yaml.BaseLoader)
        return ProcessedStats.from_dict(dobj)

    def save(self, prefix):
        info = self.to_dict(prefix)
        with open("%s_pstats.yaml" % prefix, "w") as f:
            yaml.dump(info, f)
        self.welfares.to_csv(info["welfares"], float_format='%g')
        self.times.to_csv(info["times"], float_format='%g')
        self.costw.to_csv(info["costw"], float_format='%g')
        self.costt.to_csv(info["costt"], float_format='%g')

    @staticmethod
    def from_dict(dobj):
        welfares = pd.read_csv(dobj["welfares"], index_col='instance')
        times = pd.read_csv(dobj["times"], index_col='instance')
        costw = pd.read_csv(dobj["costw"], index_col='instance')
        costt = pd.read_csv(dobj["costt"], index_col='instance')
        return ProcessedStats(dobj["name"], dobj["algos"],
                              welfares, times, costw, costt)

    def to_dict(self, prefix):
        return {
            "name": self.name,
            "algos": self.algos,
            "welfares": "%s.welfares" % prefix,
            "times": "%s.times" % prefix,
            "costw": "%s.costw" % prefix,
            "costt": "%s.costt" % prefix
        }

    def filter(self, algos):
        return ProcessedStats(self.name + "_filtered",
                              algos,
                              self.welfares[algos].copy(),
                              self.times[algos].copy(),
                              self.costw[algos].copy(),
                              self.costt[algos].copy())


class ProcessedSampleStats():

    def __init__(self, name, algos, ratio, costw, costt,
                 t_ovhd, costw_extra, costt_extra):
        self.__name = name
        self.__algos = algos
        self.__ratio = ratio
        self.__costw = costw
        self.__costt = costt
        self.__t_ovhd = t_ovhd
        self.__costw_extra = costw_extra
        self.__costt_extra = costt_extra

    @property
    def name(self):
        return self.__name

    @property
    def algos(self):
        return self.__algos

    @property
    def ratio(self):
        return self.__ratio

    @property
    def costw(self):
        return self.__costw

    @property
    def costt(self):
        return self.__costt

    @property
    def t_ovhd(self):
        return self.__t_ovhd

    @property
    def costw_extra(self):
        return self.__costw_extra

    @property
    def costt_extra(self):
        return self.__costt_extra

    @staticmethod
    def load(filename):
        with open(filename, "r") as f:
            dobj = yaml.load(f, Loader=yaml.BaseLoader)
        return ProcessedSampleStats.from_dict(dobj)

    def save(self, prefix):
        info = self.to_dict(prefix)
        with open("%s_psample_stats_%.2f.yaml" % (prefix, self.ratio), "w") as f:
            yaml.dump(info, f)
        self.costw.to_csv(info["costw"], float_format='%g')
        self.costt.to_csv(info["costt"], float_format='%g')
        self.t_ovhd.to_csv(info["t_ovhd"], float_format='%g')
        self.costw_extra.to_csv(info["costw_extra"], float_format='%g')
        self.costt_extra.to_csv(info["costt_extra"], float_format='%g')

    @staticmethod
    def from_dict(dobj):
        costw = pd.read_csv(dobj["costw"], index_col='instance')
        costt = pd.read_csv(dobj["costt"], index_col='instance')
        t_ovhd = pd.read_csv(dobj["t_ovhd"], index_col='instance')
        costw_extra = pd.read_csv(dobj["costw_extra"], index_col='instance')
        costt_extra = pd.read_csv(dobj["costt_extra"], index_col='instance')
        return ProcessedSampleStats(dobj["name"], dobj["algos"], 
                                    float(dobj["ratio"]),
                                    costw, costt, t_ovhd, costw_extra, costt_extra)

    def to_dict(self, prefix):
        return {
            "name": self.name,
            "algos": self.algos,
            "ratio": float(self.ratio),
            "costw": "%s.costw.%.2f" % (prefix, self.ratio),
            "costt": "%s.costt.%.2f" % (prefix, self.ratio),
            "t_ovhd": "%s.t_ovhd.%.2f" % (prefix, self.ratio),
            "costw_extra": "%s.costw_extra.%.2f" % (prefix, self.ratio),
            "costt_extra": "%s.costt_extra.%.2f" % (prefix, self.ratio)
        }


class LambdaStats():

    def __init__(self, weight, costs, winners):
        self.__weight = weight
        self.__costs = costs
        self.__winners = winners

    @property
    def weight(self):
        return self.__weight

    @property
    def costs(self):
        return self.__costs

    @property
    def winners(self):
        return self.__winners

    def get_breakdown(self, algos):
        elements, counts = np.unique(self.winners.winner, return_counts=True)

        # create column for weight and add to matrix
        column = [counts[np.where(elements == algo)[0]]
                  for algo in algos]
        column = [0 if column[i].size == 0 else column[i][0]
                  for i in range(0, len(column))]
        column = np.asarray(column)
        return column

    @staticmethod
    def load(filename, weight):
        costs = pd.read_csv("%s.costs" % filename, index_col='instance')
        winners = pd.read_csv("%s.winners" % filename, index_col='instance')
        return LambdaStats(weight, costs, winners)

    def save(self, filename):
        self.costs.to_csv("%s.costs" % filename, float_format='%g')
        self.winners.to_csv("%s.winners" % filename, float_format='%g')

    def filter(self, algos):
        new_costs = self.costs[algos]
        new_winners = new_costs.idxmin(axis=1).to_frame().rename(columns={0: 'winner'})
        return LambdaStats(self.weight, new_costs, new_winners)


class LambdaSampleStats():

    def __init__(self, weight, winners, winners_extra):
        self.__weight = weight
        self.__winners = winners
        self.__winners_extra = winners_extra

    @property
    def weight(self):
        return self.__weight

    @property
    def winners(self):
        return self.__winners

    @property
    def winners_extra(self):
        return self.__winners_extra
    
    @staticmethod
    def load(filename, weight):
        winners = pd.read_csv("%s.winners" % filename, index_col='instance')
        winners_extra = pd.read_csv("%s.winners_extra" % filename,
                                    index_col='instance')
        return LambdaSampleStats(weight, winners, winners_extra)

    def save(self, filename):
        self.winners.to_csv("%s.winners" % filename, float_format='%g')
        self.winners_extra.to_csv("%s.winners_extra" % filename, float_format='%g')


class ProcessedDataset():

    def __init__(self, pstats, weights, lstats):
        self.__pstats = pstats
        self.__weights = weights
        self.__lstats = lstats

    @property
    def pstats(self):
        return self.__pstats

    @property
    def weights(self):
        return self.__weights

    @property
    def lstats(self):
        return self.__lstats

    @property
    def name(self):
        return self.__pstats.name

    @property
    def algos(self):
        return self.__pstats.algos

    @staticmethod
    def load(metafile):
        with open(metafile, "r") as f:
            dobj = yaml.load(f, Loader=yaml.BaseLoader)
        return ProcessedDataset.from_dict(dobj)

    @staticmethod
    def from_dict(dobj):
        pstats = ProcessedStats.load(dobj["pstats_file"])
        weights = np.array(dobj["weights"], dtype='float64')
        lstats_file_prefix = dobj["lstats_file_prefix"]
        lstats = {}
        for weight in weights:
            lstats[weight] = LambdaStats.load(
                "%s%.1f" % (lstats_file_prefix, weight), weight)
        return ProcessedDataset(pstats, weights, lstats)

    def filter(self, algos):
        # recompute lambda stats
        lstats = {}
        for weight in self.weights:
            lstats[weight] = self.lstats[weight].filter(algos)
        return ProcessedDataset(self.pstats.filter(algos),
                                self.weights,
                                lstats)

class ProcessedSamplesDataset():

    def __init__(self, ratios, weights, sstats, lstats):
        self.__ratios = ratios
        self.__weights = weights
        self.__sstats = sstats
        self.__lstats = lstats

    @property
    def ratios(self):
        return self.__ratios

    @property
    def weights(self):
        return self.__weights

    @property
    def sstats(self):
        return self.__sstats

    @property
    def lstats(self):
        return self.__lstats

    @staticmethod
    def load(metafile):
        with open(metafile, "r") as f:
            dobj = yaml.load(f, Loader=yaml.BaseLoader)
        return ProcessedSamplesDataset.from_dict(dobj)

    @staticmethod
    def from_dict(dobj):
        weights = np.array(dobj["weights"], dtype='float64')
        ratios = np.array(dobj["ratios"], dtype='float64')
        sstats_file_prefix = dobj["sstats_file_prefix"]
        lstats_file_prefix = dobj["lstats_file_prefix"]
        lstats = {}
        sstats = {}
        for ratio in ratios:
            sstats[ratio] = ProcessedSampleStats.load(
                "%s%.2f.yaml" % (sstats_file_prefix, ratio))
            lstats[ratio] = {}
            for weight in weights:
                lstats[ratio][weight] = LambdaSampleStats.load(
                    "%s%.2f_%.1f" % (lstats_file_prefix, ratio, weight),
                    weight)
        return ProcessedSamplesDataset(ratios, weights, sstats, lstats)