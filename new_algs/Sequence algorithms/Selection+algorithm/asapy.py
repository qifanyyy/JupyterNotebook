import logging
import sys
import os
import json
from collections import namedtuple, OrderedDict

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from plottingscripts.plotting.scatter import plot_scatter_plot

from aslib_scenario.aslib_scenario import ASlibScenario

from asapy.perf_analysis.perf_analysis import PerformanceAnalysis
from asapy.feature_analysis.feature_analysis import FeatureAnalysis
from asapy.out_builder.html_builder import HTMLBuilder

__author__ = "Marius Lindauer"
__copyright__ = "Copyright 2016, ML4AAD"
__license__ = "MIT"
__email__ = "lindauer@cs.uni-freiburg.de"


class ASAPy(object):

    def __init__(self,
                 output_dn: str=".",
                 plot_log_perf: bool=False):
        '''
        Constructor

        Arguments
        ---------
        output_dn:str
            output directory name
        '''
        self.logger = logging.getLogger("ASAPy")

        self.scenario = None
        self.output_dn = output_dn
        self.plot_log_perf = plot_log_perf

        if not os.path.isdir(self.output_dn):
            os.mkdir(self.output_dn)

    def read_scenario_ASlib(self, scenario_dn: str):
        '''
        Read scenario from ASlib format

        Arguments
        ---------
        scenario_dn: str
            Scenario directory name 
        '''

        self.scenario = ASlibScenario()
        self.scenario.read_scenario(dn=scenario_dn)

    def read_scenario_CSV(self, csv_data: namedtuple):
        '''
        Read scenario from ASlib format

        Arguments
        ---------
        csv_data: namedtuple
            namedtuple with the following fields: "perf_csv", "feat_csv", "obj", "cutoff", "maximize", "cv_csv" 
            "cv_csv" can be None
        '''
        self.scenario = ASlibScenario()
        self.scenario.read_from_csv(perf_fn=csv_data.perf_csv,
                                    feat_fn=csv_data.feat_csv,
                                    objective=csv_data.obj,
                                    runtime_cutoff=csv_data.cutoff,
                                    maximize=csv_data.maximize,
                                    cv_fn=csv_data.cv_csv)

    def get_default_config(self):
        '''
            get default configuration which enables all plots

            Returns
            -------
            dict
        '''
        config = {"Performance Analysis": {"Status bar plot": True,
                                           "Box plot": True,
                                           "Violin plot": True,
                                           "CDF plot": True,
                                           "Scatter plots": True,
                                           "Correlation plot": True,
                                           "Contribution of algorithms": True,
                                           "Critical Distance Diagram": True,
                                           "Footprints": True,
                                           "Instance Hardness": True,
                                           "Baselines": True
                                           },
                  "Feature Analysis": {"Status Bar Plot": True,
                                       "Violin and box plots": True,
                                       "Correlation plot": True,
                                       "Feature importance": True,
                                       "Clustering": True,
                                       "CDF plot on feature costs": True
                                       }
                  }

        return config

    def print_config(self):
        '''
            generate template for config file
        '''
        print(json.dumps(self.get_default_config(), indent=2))

    def load_config(self, fn: str):
        '''
            load config from file

            Arguments
            ---------
            fn: str
                file name with config in json format

            Returns
            -------
            config: dict
        '''
        with open(fn) as fp:
            config = json.load(fp)

        return config

    def main(self, config: dict, max_algos: int=20,
             only_fold:int=None):
        '''
            main method

            Arguments
            ---------
            config: dict
                configuration that enables or disables plots
            max_algos: int
                maximum number of algos to consider; 
                if more are available, we take the n best algorithm on average performance
            only_fold: int
                use only the given <only_fold> cv-fold data for analyze
        '''
        
        if only_fold:
            self.logger.info("Using only test data from %d cv-split" %(only_fold))
            _, self.scenario = self.scenario.get_split(only_fold)

        n_prev_algos = None
        if self.scenario is None:
            raise ValueError(
                "Please first read in Scenario data; use scenario input or csv input")

        if self.scenario.performance_type[0] == "solution_quality" and self.scenario.maximize[0]:
            # revoke inverting the performance as done in the scenario reader
            self.scenario.performance_data *= -1
            self.logger.info("Revoke * -1 on performance data")

        if len(self.scenario.algorithms) > max_algos:
            n_prev_algos = len(self.scenario.algorithms)
            self.logger.warning(
                "We reduce the algorithms to the greedy selected VBS-improving algorithms (at most %d)" % (max_algos))
            pa = PerformanceAnalysis(output_dn=self.output_dn,
                                     scenario=self.scenario)

            algos_score = pa.reduce_algos(max_algos=max_algos)
            best_algos = [a[0] for a in algos_score] 
            self.scenario.algorithms = best_algos
            self.scenario.performance_data = self.scenario.performance_data[
                best_algos]
            self.scenario.runstatus_data = self.scenario.runstatus_data[
                best_algos]

        data = OrderedDict()

        # meta data
        meta_data_df = self.get_meta_data()
        data["Meta Data"] = {
            "table": meta_data_df.to_html(header=False)
        }

        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # performance analysis
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if config.get("Performance Analysis"):
            pa = PerformanceAnalysis(output_dn=self.output_dn,
                                     scenario=self.scenario)
            data["Performance Analysis"] = OrderedDict()
            if n_prev_algos is not None:
                data["Performance Analysis"][
                    "tooltip"] = "To provide a clear overview, we reduced the number of algorithms (%d) to the greedily selected most VBS-improving %d algorithms." % (n_prev_algos, len(self.scenario.algorithms))

            if config["Performance Analysis"].get("Baselines"):
                baseline_table = pa.get_baselines()
                data["Performance Analysis"]["Baselines"] = {"tooltip": "Baslines: Best Single Algorithm (i.e., best algorithm on average across instances), Virtual Best Solver (aka Oracle, i.e., average across best performance per instance; theoretical best algorithm selector)",
                                                             "table": baseline_table}

            if config["Performance Analysis"].get("Status bar plot"):
                status_plot = pa.get_bar_status_plot()
                data["Performance Analysis"]["Status bar plot"] = {"tooltip": "Stacked bar plots for runstatus of each algorithm",
                                                                   "figure": status_plot}

            # get box plot
            if config["Performance Analysis"].get("Box plot"):
                box_plot = pa.get_box_plots(plot_log_perf=self.plot_log_perf)
                data["Performance Analysis"]["Box plot"] = {"tooltip": "Box plots to show the performance distribution of each algorithm",
                                                            "figure": box_plot}

            # get violin plot
            if config["Performance Analysis"].get("Violin plot"):
                violion_plot = pa.get_violin_plots(
                    plot_log_perf=self.plot_log_perf)
                data["Performance Analysis"]["Violin plot"] = {"tooltip": "Violin plots to show the probablity density of each algorithm's performance. Also showing the median (middle line) and min/max value.",
                                                               "figure": violion_plot}

            # get cdf plot
            if config["Performance Analysis"].get("CDF plot"):
                cdf_plot = pa.get_cdf_plots(plot_log_perf=self.plot_log_perf)
                data["Performance Analysis"]["CDF plot"] = {"tooltip": "Cumulative Distribution function (CDF) plots. At each point x (e.g., running time cutoff), how many of the instances (in percentage) can be solved. Better algorithms have a higher curve for minimization problems.",
                                                            "figure": cdf_plot}

            # get cd diagram
            if config["Performance Analysis"].get("Critical Distance Diagram"):
                cd_plot = pa.get_cd_diagram()
                data["Performance Analysis"]["Critical Distance Diagram"] = {"tooltip": "Critical Distance (CD) diagram based on a Nemenyi two tailed test using average rankings. CD (top left) shows the critical distance. Distances larger than CD corresponds to a statistical significant difference in the ranking. We show only the best 20 ranked algorithms.",
                                                                             "figure": cd_plot}

            # generate scatter plots
            if config["Performance Analysis"].get("Scatter plots"):
                scatter_plots = pa.scatter_plots(
                    plot_log_perf=self.plot_log_perf)
                data["Performance Analysis"]["Scatter plots"] = OrderedDict({
                    "tooltip": "Scatter plot to compare the performance of two algorithms on all instances -- each dot represents one instance."})
                scatter_plots = sorted(
                    scatter_plots, key=lambda x: x[0] + x[1])
                for plot_tuple in scatter_plots:
                    key = "%s vs %s" % (plot_tuple[0], plot_tuple[1])
                    data["Performance Analysis"]["Scatter plots"][
                        key] = {"figure": plot_tuple[2]}

            # generate correlation plot
            if config["Performance Analysis"].get("Correlation plot"):
                correlation_plot = pa.correlation_plot()
                data["Performance Analysis"]["Correlation plot"] = {"tooltip": "Correlation based on Spearman Correlation Coefficient between all algorithms and clustered with Wards hierarchical clustering approach. Darker fields corresponds to a larger correlation between the algorithms. See [Xu et al SAT 2012]",
                                                                    "figure": correlation_plot}

            # get contribution values
            if config["Performance Analysis"].get("Contribution of algorithms"):
                avg_fn, marg_fn, shap_fn = pa.get_contribution_values()
                data["Performance Analysis"]["Contribution of algorithms"] = OrderedDict({
                    "tooltip": "Contribution of each algorithm"})

                data["Performance Analysis"]["Contribution of algorithms"][
                    "Average Performance"] = {"figure": avg_fn}
                data["Performance Analysis"]["Contribution of algorithms"]["Marginal Contribution"] = {"figure": marg_fn,
                                                                                                       "tooltip": "Marginal contribution to the virtual best solver (VBS, aka oracle) (i.e., how much decreases the VBS performance by removing the algorithm; higher value correspond to more importance). See [Xu et al SAT 2012]"}
                data["Performance Analysis"]["Contribution of algorithms"]["Shapley Values"] = {"figure": shap_fn,
                                                                                                "tooltip": "Shapley values (i.e., marginal contribution across all possible subsets of portfolios; again higher values corresponds to more importance; see [Frechette et al AAAI'16]. For running time scenarios, the metric is cutoff - running time; for non-running time, the metric is (worst performance across all instances and algorithms)- performance."}
                portfolio_table = pa.get_greedy_portfolio_constr()
                data["Performance Analysis"]["Contribution of algorithms"]["Portfolio Construction"] = {
                    "tooltip": "Starting with the Single Best Solver, iteratively add algorithms to the portfolio by optimizing VBS",
                    "table" : portfolio_table
                }

            # generate footprint plots
            if config["Performance Analysis"].get("Footprints"):
                footprints_plots = pa.get_footprints()
                data["Performance Analysis"]["Footprints"] = OrderedDict({
                    "tooltip": "Footprints of algorithms (instances red marked if the algorithm is at most 5% away from oracle performance) in 2-d PCA feature space. Inspired by [Smith-Miles et al. Computers & OR 2014]"})
                footprints_plots = sorted(footprints_plots, key=lambda x: x[0])
                for plot_tuple in footprints_plots:
                    key = "%s" % (plot_tuple[0])
                    data["Performance Analysis"]["Footprints"][
                        key] = {"html": plot_tuple[1], "figure": plot_tuple[2]}

            # generate instance hardness plot
            if config["Performance Analysis"].get("Instance Hardness"):
                hardness_plot = pa.instance_hardness()
                data["Performance Analysis"]["Instance Hardness"] = {"tooltip": "Projecting instances into 2d PCA feature space; the color encodes the number of algorithms that perform within 5% of the oracle performance.",
                                                                     "figure": hardness_plot[1],
                                                                     "html": hardness_plot[0]}

        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # feature analysis
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if config.get("Feature Analysis"):
            data["Feature Analysis"] = OrderedDict()
            fa = FeatureAnalysis(output_dn=self.output_dn,
                                 scenario=self.scenario)

            if config["Feature Analysis"].get("Status Bar Plot"):
                status_plot = fa.get_bar_status_plot()
                data["Feature Analysis"]["Status Bar Plot"] = {"tooltip": "Stacked bar plots for runstatus of each feature groupe",
                                                               "figure": status_plot}

            # box and violin plots
            if config["Feature Analysis"].get("Violin and box plots"):
                name_plots = fa.get_box_violin_plots()
                data["Feature Analysis"]["Violin and box plots"] = OrderedDict({
                    "tooltip": "Violin and Box plots to show the distribution of each instance feature. We removed NaN from the data."})
                for plot_tuple in name_plots:
                    key = "%s" % (plot_tuple[0])
                    data["Feature Analysis"]["Violin and box plots"][
                        key] = {"figure": plot_tuple[1]}

            # correlation plot
            if config["Feature Analysis"].get("Correlation plot"):
                correlation_plot = fa.correlation_plot()
                data["Feature Analysis"]["Correlation plot"] = {"tooltip": "Correlation based on Pearson product-moment correlation coefficients between all features and clustered with Wards hierarchical clustering approach. Darker fields corresponds to a larger correlation between the features.",
                                                                "figure": correlation_plot}

            # feature importance
            if config["Feature Analysis"].get("Feature importance"):
                importance_plot = fa.feature_importance()
                data["Feature Analysis"]["Feature importance"] = {"tooltip": "Using the approach of SATZilla'11, we train a cost-sensitive random forest for each pair of algorithms and average the feature importance (using gini as splitting criterion) across all forests. We show the median, 25th and 75th percentiles across all random forests of the 15 most important features.",
                                                                  "figure": importance_plot}

            # cluster instances in feature space
            if config["Feature Analysis"].get("Clustering"):
                cluster_plot = fa.cluster_instances()
                data["Feature Analysis"]["Clustering"] = {"tooltip": "Clustering instances in 2d; the color encodes the cluster assigned to each cluster. Similar to ISAC, we use a k-means to cluster the instances in the feature space. As pre-processing, we use standard scaling and a PCA to 2 dimensions. To guess the number of clusters, we use the silhouette score on the range of 2 to 12 in the number of clusters",
                                                          "figure": cluster_plot}

            # get cdf plot
            if self.scenario.feature_cost_data is not None and config["Feature Analysis"].get("CDF plot on feature costs"):
                cdf_plot = fa.get_feature_cost_cdf_plot()
                data["Feature Analysis"]["CDF plot on feature costs"] = {"tooltip": "Cumulative Distribution function (CDF) plots. At each point x (e.g., running time cutoff), for how many of the instances (in percentage) have we computed the instance features. Faster feature computation steps have a higher curve. Missing values are imputed with the maximal value (or running time cutoff).",
                                                                         "figure": cdf_plot}

        self.create_html(data=data)

    def create_html(self, data: OrderedDict):
        '''
        create html report
        '''

        html_builder = HTMLBuilder(output_dn=self.output_dn,
                                   scenario_name=self.scenario.scenario)
        html_builder.generate_html(data)

    def get_meta_data(self):
        '''
            read meta data from self.scenario and generate a pandas.Dataframe with it
        '''
        data = []

        data.append(
            ("Number of instances", len(self.scenario.instances)))
        data.append(
            ("Number of algorithms", len(self.scenario.algorithms)))

        data.append(
            ("Performance measure", self.scenario.performance_measure[0]))
        data.append(("Performance type", self.scenario.performance_type[0]))
        data.append(("Maximize?", str(self.scenario.maximize[0])))
        if self.scenario.algorithm_cutoff_time:
            data.append(
                ("Running time cutoff (algorithm)", str(self.scenario.algorithm_cutoff_time)))
        if self.scenario.algorithm_cutoff_memory:
            data.append(
                ("Memory cutoff (algorithm)", str(self.scenario.algorithm_cutoff_memory)))
        if self.scenario.features_cutoff_time:
            data.append(
                ("Running time cutoff (features)", str(self.scenario.features_cutoff_time)))
        if self.scenario.features_cutoff_memory:
            data.append(
                ("Memory cutoff (Features)", str(self.scenario.features_cutoff_memory)))
        data.append(
            ("# Deterministic features", len(self.scenario.features_deterministic)))
        data.append(
            ("# Stochastic features", len(self.scenario.features_stochastic)))
        data.append(("# Feature groups", len(self.scenario.feature_steps)))
        data.append(
            ("# Deterministic algorithms", len(self.scenario.algortihms_deterministics)))
        data.append(
            ("# Stochastic algorithms", len(self.scenario.algorithms_stochastic)))
        if self.scenario.feature_cost_data is not None:
            data.append(("Feature costs provided?", "True"))
        else:
            data.append(("Feature costs provided?", "False"))

        meta_data = pd.DataFrame(data=list(map(lambda x: x[1], data)), index=list(
            map(lambda x: x[0], data)), columns=[""])

        return meta_data
