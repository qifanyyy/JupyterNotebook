import numpy as np
import pandas as pd
import glob
import yaml
import math
import scipy.stats.stats as st
from scipy.optimize import curve_fit

from cause.helper import *

from cause.stats import RawStats
from cause.stats import RawStatsOptimal
from cause.stats import RawStatsRandom
from cause.stats import ProcessedStats
from cause.stats import LambdaStats
from cause.stats import ProcessedDataset
from cause.stats import RawSampleStats
from cause.stats import ProcessedSampleStats
from cause.stats import LambdaSampleStats

from cause.features import Features

from cause.plotter import Plotter

from cage.auctionset import AuctionSet

class RawStatsLoader():

    __schema = {'instance': np.object_,
                'algorithm': np.object_,
                'time': np.float64,
                'welfare': np.float64,
                'ngoods': np.int64,
                'nwin': np.int64,
                'util_mean': np.float64,
                'util_stddev': np.float64,
                'price_mean': np.float64}

    __columns = ['instance', 'algorithm',
                'time', 'welfare',
                'ngoods', 'nwin', 'util_mean',
                'util_stddev', 'price_mean']

    def __init__(self, infolder, name):
        self.__infolder = infolder
        self.__name = name

    @property
    def infolder(self):
        return self.__infolder

    @property
    def schema(self):
        return self.__schema

    @property
    def columns(self):
        return self.__columns

    @property
    def name(self):
        return self.__name

    def load(self):
        allstats = self.__load()
        # average over multiple runs when needed
        allstats = allstats.groupby(
            ['instance', 'algorithm']).mean().reset_index()
        # filter out non heuristic algos
        allstats = allstats[allstats.algorithm.isin(
                [x.name for x in Heuristic_Algorithm_Names])]
        return RawStats(self.name, allstats, [x.name for x in Heuristic_Algorithm_Names])

    def load_optimal(self):
        optstats = self.__load()
        # average over multiple runs when needed
        optstats = optstats.groupby(
            ['instance', 'algorithm']).mean().reset_index()
        # filter instances that don't have results for all algos
        optstats = optstats.groupby('instance').filter(
            lambda x: set(x.algorithm.unique()) ==
                      set([x.name for x in Algorithm_Names])
        ).reset_index()
        return RawStatsOptimal(self.name, optstats)

    def load_random(self):
        randstats = self.__load()
        # filter out non-stochastic algos
        randstats = randstats[randstats.algorithm.isin(
                [x.name for x in Stochastic_Algorithm_Names])]
        return RawStatsRandom(self.name, randstats)

    def __load(self):
        allstats = pd.DataFrame()
        for stats_file in sorted(glob.glob(self.infolder + "/*")):
            stats = pd.read_csv(stats_file, header=None,
                                names=self.columns, dtype=self.schema)
            # use schema.keys() instead of self.columns for python>=3.6
            allstats = allstats.append(stats, ignore_index=True)
        return allstats


class RawSampleStatsLoader():

    __schema = {'ratio': np.float64,
                'instance': np.object_,
                'algorithm': np.object_,
                'time': np.float64,
                'welfare': np.float64,
                'ngoods': np.int64,
                'nwin': np.int64,
                'util_mean': np.float64,
                'util_stddev': np.float64,
                'price_mean': np.float64}

    __columns = ['ratio', 'instance', 'algorithm',
                'time', 'welfare',
                'ngoods', 'nwin', 'util_mean',
                'util_stddev', 'price_mean']

    def __init__(self, infolder, name):
        self.__infolder = infolder
        self.__name = name

    @property
    def infolder(self):
        return self.__infolder

    @property
    def schema(self):
        return self.__schema

    @property
    def columns(self):
        return self.__columns

    @property
    def name(self):
        return self.__name

    def load(self):
        allstats = self.__load()
        # average over multiple runs when needed
        allstats = allstats.groupby(
            ['ratio', 'instance', 'algorithm']).mean().reset_index()
        return RawSampleStats(self.name, allstats,
                              [x.name for x in Heuristic_Algorithm_Names])

    def __load(self):
        allstats = pd.DataFrame()
        for stats_file in sorted(glob.glob(self.infolder + "/*")):
            stats = pd.read_csv(stats_file, header=None,
                                names=self.columns, dtype=self.schema)
            # use schema.keys() instead of self.columns for python>=3.6
            allstats = allstats.append(stats, ignore_index=True)
        return allstats


class StatsPreprocessor():

    @staticmethod
    def process(rawstats):
        if isinstance(rawstats.df, RawStatsOptimal):
            pstats = pd.DataFrame(
                rawstats.df.groupby('instance')
                .apply(StatsPreprocessor.__compute_costs_optimal))
        else:
            pstats = pd.DataFrame(
                rawstats.df.groupby('instance')
                .apply(StatsPreprocessor.__compute_costs))

        costt = pstats.pivot(
            index='instance', columns='algorithm', values='costt')
        costw = pstats.pivot(
            index='instance', columns='algorithm', values='costw')

        return ProcessedStats(rawstats.name,
                              rawstats.algos,
                              rawstats.get_welfares(),
                              rawstats.get_times(),
                              costw[rawstats.algos],
                              costt[rawstats.algos])  # reorder columns by algo

    @staticmethod
    def __compute_costs(data):
        wmin = data.welfare.min()
        wmax = data.welfare.max()
        tmin = data.time.min()
        tmax = data.time.max()
        if wmax - wmin == 0:
            data.eval('costw = 0', inplace=True)
        else:
            data.eval(
                'costw = (@wmax - welfare) / (@wmax - @wmin)', inplace=True)
        if tmax - tmin == 0:
            data.eval('costt = 0', inplace=True)
        else:
            data.eval('costt = (time - @tmin) / (@tmax - @tmin)', inplace=True)
        return data

    @staticmethod
    def __compute_costs_optimal(data):
        wcplex = data[data.algorithm == "CPLEX"].welfare.values[0]
        tcplex = data[data.algorithm == "CPLEX"].time.values[0]

        if wcplex == 0:
            data.eval('costw = 0', inplace=True)
        else:
            data.eval('costw = 1. - welfare / @wcplex', inplace=True)

        data.eval('costt = time / @tcplex', inplace=True)
        return data


class SampleStatsPreprocessor():

    @staticmethod
    def process(rawsamplestats, ratio):
        welfares = rawsamplestats.get_welfares(ratio)
        times = rawsamplestats.get_times(ratio)

        wmin = welfares.min(axis=1)
        wmax = welfares.max(axis=1)
        costw = (-welfares).add(wmax, axis='index').div(
            wmax - wmin, axis='index').fillna(0.)

        tmin = times.min(axis=1)
        tmax = times.max(axis=1)
        costt = times.sub(tmin, axis='index').div(
            tmax - tmin, axis='index').fillna(0.)

        t_ovhd = pd.DataFrame(times.sum(axis=1))
        #t_ovhd = pd.DataFrame(times.max(axis=1))

        # compute stretched welfare
        data = rawsamplestats.df[rawsamplestats.df.ratio == ratio][[
            "ratio", "instance", "algorithm", "welfare", "time"]].copy()
        data['welfare_extra'] = data.apply(stretch_welfare, axis=1)
        #data.eval("welfare_extra = welfare / ratio", inplace=True)

        # compute stretched time
        data['time_extra'] = data.apply(stretch_time, axis=1)

        # get extrapolated welfares and times as matrix
        # rows=instances, columns=algorithms
        welfares_extra = data.pivot(
            index='instance', columns='algorithm', values='welfare_extra')
        times_extra = data.pivot(
            index='instance', columns='algorithm', values='time_extra')
        # reorder columns
        welfares_extra = welfares_extra[rawsamplestats.algos]
        times_extra = times_extra[rawsamplestats.algos]

        # compute predicted costs:
        # costs with predicted (extrapolated) values
        wmin_extra = welfares_extra.min(axis=1)
        wmax_extra = welfares_extra.max(axis=1)
        costw_extra = (-welfares_extra).add(wmax_extra, axis='index').div(
            wmax_extra - wmin_extra, axis='index').fillna(0.)

        tmin_extra = times_extra.min(axis=1)
        tmax_extra = times_extra.max(axis=1)
        costt_extra = times_extra.sub(tmin_extra, axis='index').div(
            tmax_extra - tmin_extra, axis='index').fillna(0.)

        # create and return processed sample stats
        return ProcessedSampleStats(rawsamplestats.name,
                                    rawsamplestats.algos,
                                    ratio,
                                    costw,
                                    costt,
                                    t_ovhd,
                                    costw_extra,
                                    costt_extra)        

    @staticmethod
    def process_old(rawsamplestats, ratio):
        psstats = pd.DataFrame(
            rawsamplestats.df[rawsamplestats.df.ratio == ratio]
            .groupby('instance')
            .apply(SampleStatsPreprocessor.__compute_costs_and_extra))

        costt = psstats.pivot(
            index='instance', columns='algorithm', values='costt')
        costw = psstats.pivot(
            index='instance', columns='algorithm', values='costw')
        t_ovhd = psstats.pivot(
            index='instance', columns='algorithm', values='t_ovhd')
        costt_extra = psstats.pivot(
            index='instance', columns='algorithm', values='costt_extra')
        costw_extra = psstats.pivot(
            index='instance', columns='algorithm', values='costw_extra')

        return ProcessedSampleStats(rawsamplestats.name,
                                    rawsamplestats.algos,
                                    ratio,
                                    costw[rawsamplestats.algos],
                                    costt[rawsamplestats.algos],
                                    t_ovhd[rawsamplestats.algos],
                                    costw_extra[rawsamplestats.algos],
                                    costt_extra[rawsamplestats.algos])

    @staticmethod
    def __compute_costs_and_extra(data):
        # first, just compute cost of instance
        wmin = data.welfare.min()
        wmax = data.welfare.max()
        tmin = data.time.min()
        tmax = data.time.max()
        if wmax - wmin == 0:
            data.eval('costw = 0', inplace=True)
        else:
            data.eval(
                'costw = (@wmax - welfare) / (@wmax - @wmin)', inplace=True)
        if tmax - tmin == 0:
            data.eval('costt = 0', inplace=True)
        else:
            data.eval('costt = (time - @tmin) / (@tmax - @tmin)', inplace=True)
        
        # compute time overhead
        t_ovhd = data.time.sum()
        data.eval('t_ovhd = @t_ovhd', inplace=True)

        # compute stretched welfare
        data['welfare_extra'] = data.apply(stretch_welfare, axis=1)
        # compute stretched time
        data['time_extra'] = data.apply(stretch_time, axis=1)
        # compute predicted costs: costw_extra, costt_extra
        wmin_extra = data.welfare_extra.min()
        wmax_extra = data.welfare_extra.max()
        tmin_extra = data.time_extra.min()
        tmax_extra = data.time_extra.max()
        if wmax - wmin == 0:
            data.eval('costw_extra = 0', inplace=True)
        else:
            data.eval(
                'costw_extra = (@wmax_extra - welfare_extra) / (@wmax_extra - @wmin_extra)',
                inplace=True)
        if tmax - tmin == 0:
            data.eval('costt_extra = 0', inplace=True)
        else:
            data.eval(
                'costt_extra = (time_extra - @tmin_extra) / (@tmax_extra - @tmin_extra)',
                inplace=True)
        
        return data


class LambdaStatsPreprocessor():

    def __init__(self, pstats):
        self.__pstats = pstats

    @property
    def pstats(self):
        return self.__pstats

    def process(self, weight):
        costs = ((weight * self.pstats.costw) ** 2 +
                ((1 - weight) * self.pstats.costt) ** 2) ** 0.5
        winners = costs.idxmin(axis=1).to_frame().rename(columns={0: 'winner'})
        return LambdaStats(weight, costs, winners)


class LambdaSampleStatsPreprocessor():

    def __init__(self, sstats):
        self.__sstats = sstats

    @property
    def sstats(self):
        return self.__sstats

    def process(self, weight):
        costs = ((weight * self.sstats.costw) ** 2 +
                ((1 - weight) * self.sstats.costt) ** 2) ** 0.5
        winners = costs.idxmin(axis=1).to_frame().rename(columns={0: 'winner'})
        costs_extra = ((weight * self.sstats.costw_extra) ** 2 +
                      ((1 - weight) * self.sstats.costt_extra) ** 2) ** 0.5
        winners_extra = costs_extra.idxmin(axis=1)\
                                   .to_frame()\
                                   .rename(columns={0: 'winner_extra'})
        return LambdaSampleStats(weight, winners, winners_extra)

class DatasetCreator():

    @staticmethod
    def create(weights, infolder, outfolder, name):
        # filenames
        prefix = "%s/%s" % (outfolder, name)
        pstats_file = "%s_pstats.yaml" % prefix
        lstats_file_prefix = "%s_lstats_" % prefix
        metafile = "%s.yaml" % prefix

        # load raw stats
        # process and save raw stats
        pstats = StatsPreprocessor.process(
            RawStatsLoader(infolder, name).load())
        pstats.save(prefix)

        # process and save lambda stats per weight
        ls_preproc = LambdaStatsPreprocessor(pstats)
        for weight in weights:
            lstats = ls_preproc.process(weight)
            lstats.save("%s%.1f" % (lstats_file_prefix, weight))

        # save dataset metafile
        dobj = {
            "pstats_file": pstats_file,
            "weights": weights.tolist(),
            "lstats_file_prefix": lstats_file_prefix
        }

        with open(metafile, "w") as f:
            yaml.dump(dobj, f)


class SamplesDatasetCreator():

    @staticmethod
    def create(weights, infolder, outfolder, name):
        # filenames
        prefix = "%s/%s" % (outfolder, name)
        sstats_file_prefix = "%s_psample_stats_" % prefix
        lstats_file_prefix = "%s_lstats_" % prefix
        metafile = "%s_samples.yaml" % prefix

        # load raw stats
        rawsamplestats = RawSampleStatsLoader(infolder, name).load()
        ratios = rawsamplestats.ratios

        # process and save raw stats
        for ratio in ratios:
            sstats = SampleStatsPreprocessor.process(
                rawsamplestats, ratio)
            sstats.save(prefix)
            lssp = LambdaSampleStatsPreprocessor(sstats)
            for weight in weights:
                lstats = lssp.process(weight)
                lstats.save(
                    "%s%.2f_%.1f" % (lstats_file_prefix, ratio, weight))

         # save dataset metafile
        dobj = {
            "weights": weights.tolist(),
            "ratios": ratios.tolist(),
            "sstats_file_prefix": sstats_file_prefix,
            "lstats_file_prefix": lstats_file_prefix
        }

        with open(metafile, "w") as f:
            yaml.dump(dobj, f)


class FeatureExtractor():

    @staticmethod
    def extract(infolder, name, outfolder,
                in_parallel=False, num_threads=2, task_queue_file=None):
        info = {
            "infolder": infolder,
            "name": name,
            "features": "%s/%s.features" % (outfolder, name)
        }
        with open("%s/%s_features.yaml" % (outfolder, name), "w") as f:
            yaml.dump(info, f)

        # write header to file
        header = pd.DataFrame(columns = ["instance", *[x.name for x in Feature_Names]])
        header.set_index('instance').to_csv(info["features"])

        if not in_parallel:
            # append features of each instance to file
            for instance_file in sorted(glob.glob(infolder + "/*")):
                FeatureExtractor.extract_from_instance(instance_file, info["features"])
        else:
            import threading, queue
            # create task queue
            my_queue = queue.Queue()
            if task_queue_file:
                with open(task_queue_file, "r") as f:
                    for instance_file in f.read().splitlines():
                        my_queue.put(instance_file)
            else:
                for instance_file in sorted(glob.glob(infolder + "/*")):
                    my_queue.put(instance_file)
            # create threads and start processing
            for tid in range(num_threads):
                aThread = threading.Thread(target=FeatureExtractor.__do_work,
                                           args=(my_queue, info["features"], tid))
                # daemon lets the program end once the tasks are done
                aThread.daemon = True
                aThread.start()

            print("Starting")
            # wait until all tasks are done
            my_queue.join()
            print("Done")

    # a function to handle 1 task
    @staticmethod
    def __do_work(my_queue, output_file, thread_id):
        # write to different output files
        features_file = output_file + "." + str(thread_id)
        while not my_queue.empty():
            instance_file = my_queue.get()
            FeatureExtractor.extract_from_instance(instance_file, features_file)
            my_queue.task_done()

    @staticmethod
    def extract_from_instance(instance_file, features_file):
        aset = AuctionSet.load(instance_file)

        # shorthand variables:
        b = aset.bid_set.values
        r = aset.bid_set.quantities
        a = aset.ask_set.values
        s = aset.ask_set.quantities

        ### stats for average bid prices
        nobs, b_minmax, b_mean, b_var, b_skew, b_kurt = st.describe(b/np.sum(r, axis=1), ddof=0)
        ### stats for average ask prices
        nobs, a_minmax, a_mean, a_var, a_skew, a_kurt = st.describe(a/np.sum(s, axis=1), ddof=0)
        ### stats for bid bundle size
        nobs, r_minmax, r_mean, r_var, r_skew, r_kurt = st.describe(np.sum(r, axis=1), ddof=0)
        ### stats for ask bundle size
        nobs, s_minmax, s_mean, s_var, s_skew, s_kurt = st.describe(np.sum(s, axis=1), ddof=0)
        ####### heterogeneity -> resource type axis (stats inside a bundle)
        # stats for resource quantities demanded for each resource type: sum, mean, min, max per res type, then describe
        nobs, rt_sum_minmax, rt_sum_mean, rt_sum_var, rt_sum_skew, rt_sum_kurt = st.describe(np.sum(r, axis=0), ddof=0)
        nobs, rt_mean_minmax, rt_mean_mean, rt_mean_var, rt_mean_skew, rt_mean_kurt = st.describe(np.mean(r, axis=0), ddof=0)
        nobs, rt_min_minmax, rt_min_mean, rt_min_var, rt_min_skew, rt_min_kurt = st.describe(np.min(r, axis=0), ddof=0)
        nobs, rt_max_minmax, rt_max_mean, rt_max_var, rt_max_skew, rt_max_kurt = st.describe(np.max(r, axis=0), ddof=0)
        # stats for resource quantities offered for each resource type
        nobs, st_sum_minmax, st_sum_mean, st_sum_var, st_sum_skew, st_sum_kurt = st.describe(np.sum(s, axis=0), ddof=0)
        nobs, st_mean_minmax, st_mean_mean, st_mean_var, st_mean_skew, st_mean_kurt = st.describe(np.mean(s, axis=0), ddof=0)
        nobs, st_min_minmax, st_min_mean, st_min_var, st_min_skew, st_min_kurt = st.describe(np.min(s, axis=0), ddof=0)
        nobs, st_max_minmax, st_max_mean, st_max_var, st_max_skew, st_max_kurt = st.describe(np.max(s, axis=0), ddof=0)
        # stats for demand/supply ratio by resource types: total, mean
        nobs, qratio_sum_minmax, qratio_sum_mean, qratio_sum_var, qratio_sum_skew, qratio_sum_kurt = st.describe(np.sum(r, axis=0)/np.sum(s, axis=0), ddof=0)
        nobs, qratio_mean_minmax, qratio_mean_mean, qratio_mean_var, qratio_mean_skew, qratio_mean_kurt = st.describe(np.mean(r, axis=0)/np.mean(s, axis=0), ddof=0)
        # stats for surplus quantity by resource types
        nobs, qsurplus_sum_minmax, qsurplus_sum_mean, qsurplus_sum_var, qsurplus_sum_skew, qsurplus_sum_kurt = st.describe(np.sum(s, axis=0) - np.sum(r, axis=0), ddof=0)
        # quantity spread by resource type (max requested quantity of resource k - min offered quantity of resource k)
        nobs, qspread_minmax, qspread_mean, qspread_var, qspread_skew, qspread_kurt = st.describe(np.max(r, axis=0) - np.min(s, axis=0), ddof=0)
        # mid price
        bid_max = (b / r.sum(axis=1)).max()
        ask_min = (a / s.sum(axis=1)).min()
        mid_price = (bid_max + ask_min) / 2
        # bid-ask spread
        ba_spread = bid_max - ask_min
        # total demand quantity
        r_total = r.sum()
        # total supply quantity
        s_total = s.sum()
        # total demand value
        b_total = b.sum()
        # total supply value
        a_total = a.sum()
        # surplus value per surplus unit
        surplus_value_per_surplus_unit = 0 if r_total == s_total else (b_total - a_total) / (r_total - s_total)
        ### append features
        features = np.array([
                ## instance name to be used as index
                  instance_file
                ### group 1: instance - price related
                , b_mean                 # average_bid_price_mean
                , math.sqrt(b_var)       # average_bid_price_stddev
                , b_skew                 # average_bid_price_skewness
                , b_kurt                 # average_bid_price_kurtosis
                , a_mean                 # average_ask_price_mean
                , math.sqrt(a_var)       # average_ask_price_stddev
                , a_skew                 # average_ask_price_skewness
                , a_kurt                 # average_ask_price_kurtosis
                , bid_max                # average_bid_price_max
                , ask_min                # average_ask_price_min
                , mid_price              # mid_price
                , ba_spread              # bid_ask_spread
                , ba_spread / mid_price  # bid_ask_spread_over_mid_price
                ### group 2: instance - quantity related
                , r_mean                 # bid_bundle_size_mean
                , math.sqrt(r_var)       # bid_bundle_size_stddev
                , r_skew                 # bid_bundle_size_skewness
                , r_kurt                 # bid_bundle_size_kurtosis
                , s_mean                 # ask_bundle_size_mean
                , math.sqrt(s_var)       # ask_bundle_size_stddev
                , s_skew                 # ask_bundle_size_skewness
                , s_kurt                 # ask_bundle_size_kurtosis
                ### group 3: instance - quantity per resource related (measure of heterogeneity)
                # --> demand side
                , rt_sum_mean            # total_demand_per_resource_mean
                , math.sqrt(rt_sum_var)  # total_demand_per_resource_stddev
                , rt_sum_skew            # total_demand_per_resource_skewness
                , rt_sum_kurt            # total_demand_per_resource_kurtosis
                , rt_mean_mean           # average_demand_per_resource_mean
                , math.sqrt(rt_mean_var) # average_demand_per_resource_stddev
                , rt_mean_skew           # average_demand_per_resource_skewness
                , rt_mean_kurt           # average_demand_per_resource_kurtosis
                , rt_min_mean            # minimum_demand_per_resource_mean
                , math.sqrt(rt_min_var)  # minimum_demand_per_resource_stddev
                , rt_min_skew            # minimum_demand_per_resource_skewness
                , rt_min_kurt            # minimum_demand_per_resource_kurtosis
                , rt_max_mean            # maximum_demand_per_resource_mean
                , math.sqrt(rt_max_var)  # maximum_demand_per_resource_stddev
                , rt_max_skew            # maximum_demand_per_resource_skewness
                , rt_max_kurt            # maximum_demand_per_resource_kurtosis
                # --> supply side
                , st_sum_mean            # total_supply_per_resource_mean
                , math.sqrt(st_sum_var)  # total_supply_per_resource_stddev
                , st_sum_skew            # total_supply_per_resource_skewness
                , st_sum_kurt            # total_supply_per_resource_kurtosis
                , st_mean_mean           # average_supply_per_resource_mean
                , math.sqrt(st_mean_var) # average_supply_per_resource_stddev
                , st_mean_skew           # average_supply_per_resource_skewness
                , st_mean_kurt           # average_supply_per_resource_kurtosis
                , st_min_mean            # minimum_supply_per_resource_mean
                , math.sqrt(st_min_var)  # minimum_supply_per_resource_stddev
                , st_min_skew            # minimum_supply_per_resource_skewness
                , st_min_kurt            # minimum_supply_per_resource_kurtosis
                , st_max_mean            # maximum_supply_per_resource_mean
                , math.sqrt(st_max_var)  # maximum_supply_per_resource_stddev
                , st_max_skew            # maximum_supply_per_resource_skewness
                , st_max_kurt            # maximum_supply_per_resource_kurtosis
                ### group 4: instance - demand-supply balance related
                , surplus_value_per_surplus_unit      # surplus_value_per_surplus_unit
                , b_total / a_total                   # demand_supply_ratio_value
                , r_total / s_total                   # demand_supply_ratio_quantity
                , qratio_sum_mean                     # demand_supply_ratio_total_quantity_per_resource_mean
                , math.sqrt(qratio_sum_var)           # demand_supply_ratio_total_quantity_per_resource_stddev
                , qratio_sum_skew                     # demand_supply_ratio_total_quantity_per_resource_skewness
                , qratio_sum_kurt                     # demand_supply_ratio_total_quantity_per_resource_kurtosis
                , qratio_mean_mean                    # demand_supply_ratio_mean_quantity_per_resource_mean
                , math.sqrt(qratio_mean_var)          # demand_supply_ratio_mean_quantity_per_resource_stddev
                , qratio_mean_skew                    # demand_supply_ratio_mean_quantity_per_resource_skewness
                , qratio_mean_kurt                    # demand_supply_ratio_mean_quantity_per_resource_kurtosis
                , s_total - r_total                   # surplus_quantity
                , qsurplus_sum_mean                   # surplus_total_quantity_per_resource_mean
                , math.sqrt(qsurplus_sum_var)         # surplus_total_quantity_per_resource_stddev
                , qsurplus_sum_skew                   # surplus_total_quantity_per_resource_skewness
                , qsurplus_sum_kurt                   # surplus_total_quantity_per_resource_kurtosis
                , qspread_mean                        # quantity_spread_per_resource_mean
                , math.sqrt(qspread_var)              # quantity_spread_per_resource_stddev
                , qspread_skew                        # quantity_spread_per_resource_skewness
                , qspread_kurt                        # quantity_spread_per_resource_kurtosis
                , b_mean / a_mean                     # ratio_average_price_bid_to_ask
                , r_mean / s_mean                     # ratio_bundle_size_bid_to_ask
            ])


        fpi = pd.DataFrame(features.reshape((1, features.shape[0])),
            columns = ["instance", *[x.name for x in Feature_Names]]).set_index('instance')

        with open(features_file, "a") as f:
            fpi.to_csv(f, header=False, float_format='%g')
            f.close()


class SampleStatsFit():

    @staticmethod
    def fit_welfare(raw_sample_stats, outfolder="/tmp"):
        sample_welfares = pd.DataFrame()
        for ratio in raw_sample_stats.ratios:
            sample_welfares = sample_welfares.append(
                raw_sample_stats.get_welfares(ratio).agg("mean"),
                ignore_index=True)
        sample_welfares = sample_welfares.set_index(raw_sample_stats.ratios)
        # save xdata, ydata to file
        sample_welfares.to_csv("%s/welfares_over_ratio" % outfolder,
                               sep='&', line_terminator='\\\\\n')
        # plot welfare over ratios
        Plotter.plot_data_over_ratios(sample_welfares, "welfare", outfolder)

        xdata = 10000 * sample_welfares.index
        for algo in sample_welfares.columns:
            print('==== %s ====' % algo)
            ydata = sample_welfares[algo]
            popt, pcov = curve_fit(func_poly1, xdata, ydata, bounds=(0, np.inf))
            print("welfare lin:", popt, np.sqrt(np.diag(pcov))*100./popt, "%")
            popt, pcov = curve_fit(func_sqrt, xdata, ydata, bounds=(0, np.inf))
            print("welfare sqrt:", popt, np.sqrt(np.diag(pcov))*100./popt, "%")
            popt, pcov = curve_fit(func_logn, xdata, ydata, bounds=(0, np.inf))
            print("welfare logn:", popt, np.sqrt(np.diag(pcov))*100./popt, "%")
            popt, pcov = curve_fit(func_poly2, xdata, ydata, bounds=(0, np.inf))
            print("welfare n2:", popt, np.sqrt(np.diag(pcov))*100./popt, "%")
            popt, pcov = curve_fit(func_npow, xdata, ydata, bounds=(0, np.inf))
            print("welfare a*n^b:", popt, np.sqrt(np.diag(pcov))*100./popt, "%")

    @staticmethod
    def fit_time(raw_sample_stats, outfolder="/tmp"):
        sample_times = pd.DataFrame()
        for ratio in raw_sample_stats.ratios:
            sample_times = sample_times.append(
                raw_sample_stats.get_times(ratio).agg("mean"),
                ignore_index=True)
        sample_times = sample_times.set_index(raw_sample_stats.ratios)
        # save xdata, ydata to file
        sample_times.to_csv("%s/times_over_ratio" % outfolder,
                            sep='&', line_terminator='\\\\\n')
        # plot welfare over ratios
        Plotter.plot_data_over_ratios(sample_times, "time", outfolder)

        xdata = 10000 * sample_times.index
        for algo in sample_times.columns:
            print('==== %s ====' % algo)
            ydata = sample_times[algo]
            popt, pcov = curve_fit(func_nlogn, xdata, ydata, bounds=(0, np.inf))
            print("time nlogn:",  popt, np.sqrt(np.diag(pcov))*100./popt, "%")
            popt, pcov = curve_fit(func_poly2, xdata, ydata, bounds=(0, np.inf))
            print("time n2:",  popt, np.sqrt(np.diag(pcov))*100./popt, "%")
            popt, pcov = curve_fit(func_poly3, xdata, ydata, bounds=(0, np.inf))
            print("time n3:",  popt, np.sqrt(np.diag(pcov))*100./popt, "%")
            popt, pcov = curve_fit(func_poly321, xdata, ydata, bounds=(0, np.inf))
            print("time n321:",  popt, np.sqrt(np.diag(pcov))*100./popt, "%")
            popt, pcov = curve_fit(func_n3logn, xdata, ydata, bounds=(0, np.inf))
            print("time n3logn:",  popt, np.sqrt(np.diag(pcov))*100./popt, "%")
            popt, pcov = curve_fit(func_n2logn, xdata, ydata, bounds=(0, np.inf))
            print("time n2logn:",  popt, np.sqrt(np.diag(pcov))*100./popt, "%")
            popt, pcov = curve_fit(func_nlogn_n, xdata, ydata, bounds=(0, np.inf))
            print("time nlogn+n:",  popt, np.sqrt(np.diag(pcov))*100./popt, "%")

