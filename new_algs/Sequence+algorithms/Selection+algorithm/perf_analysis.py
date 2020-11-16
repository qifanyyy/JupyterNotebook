import logging
import os

import numpy as np

from scipy.stats import spearmanr
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.special import comb

from pandas import DataFrame

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import tight_layout, figure, subplot, savefig, show, setp

import pandas as pd
import mpld3

from plottingscripts.plotting.scatter import plot_scatter_plot

from aslib_scenario.aslib_scenario import ASlibScenario

from asapy.utils.util_funcs import get_cdf_x_y

__author__ = "Marius Lindauer"
__copyright__ = "Copyright 2016, ML4AAD"
__license__ = "MIT"
__email__ = "lindauer@cs.uni-freiburg.de"


class PerformanceAnalysis(object):

    def __init__(self,
                 output_dn: str,
                 scenario: ASlibScenario):
        '''
        Constructor

        Arguments
        ---------
        output_dn:str
            output directory name
        '''
        self.logger = logging.getLogger("Performance Analysis")
        self.scenario = scenario
        self.output_dn = os.path.join(output_dn, "performance_plots")
        if not os.path.isdir(self.output_dn):
            os.mkdir(self.output_dn)

    def reduce_algos(self, max_algos: int):
        '''
            use a greedy forward search wrt VBS performance
            to shrink the set of algorithms to max_algos
            
            Arguments
            ---------
            max_algos: int
                maximal number of algorithms to be selected
                
            Returns
            -------
            typing.List[(str,float)] 
                list of tuples (algorithm, performance)
            
        '''
        performance_data = self.scenario.performance_data

        if self.scenario.maximize[0]:
            performance_data *= -1

        bsa = performance_data.mean(axis=0).idxmin()
        bsa_score = performance_data.mean(axis=0).min()
        selected_algos = [[bsa,bsa_score]]
        remaining_algos = set(self.scenario.algorithms)
        remaining_algos.remove(bsa)
        for i in range(1, max_algos):
            sels = [a[0] for a in selected_algos]
            best_algo = [
                None, self.__get_vbs(performance_data=performance_data[sels])]
            for algo in remaining_algos:
                sels_ = sels[:]
                sels_.append(algo)
                vbs = self.__get_vbs(
                    performance_data=performance_data[sels_])
                if vbs < best_algo[1]:
                    best_algo = [algo, vbs]
            if best_algo[0] is None:
                break
            selected_algos.append(best_algo)
            remaining_algos.remove(best_algo[0])
            self.logger.debug(best_algo)

        self.logger.warning("Because of algorithm filtering, we lost %f of VBS estimate." % (
            best_algo[1] - self.__get_vbs(performance_data=performance_data)))

        if self.scenario.maximize[0]:
            performance_data *= -1

        return selected_algos
    
    def get_greedy_portfolio_constr(self):
        '''
            using greedy forward selection wrt to VBS optimization,
            iteratively build portfolio
        '''
        
        algo_scores = self.reduce_algos(max_algos=len(self.scenario.algorithms))
        algos = ["Adding %s" %(a[0]) for a in algo_scores]
        if self.scenario.maximize[0]:
            scores = ["%.2f" %(a[1]*-1) for a in algo_scores]
        else:
            scores = ["%.2f" %(a[1]) for a in algo_scores]
        
        df = DataFrame(data=scores, index=algos, columns=["VBS score"])
        
        return df.to_html()

    def get_baselines(self):
        '''
            get baselines: best single algorithm and VBS

            Returns
            -------
            str
                html table with entries for bsa and vbs
        '''
        performance_data = self.scenario.performance_data
        table_data = []

        if self.scenario.maximize[0]:
            maxis = performance_data.max(axis=1)
            vbs_score = np.mean(performance_data.max(axis=1))
            algo_perfs = performance_data.mean(axis=0)
            best_indx = algo_perfs.idxmax()
            bsa = algo_perfs[best_indx]
        else:
            vbs_score = np.mean(performance_data.min(axis=1))
            algo_perfs = performance_data.mean(axis=0)
            best_indx = algo_perfs.idxmin()
            bsa = algo_perfs[best_indx]
        unsolvable = int(np.sum(np.sum(self.scenario.runstatus_data.values == "ok", axis=1) == 0))
        
        table_data.append(["Virtual Best Algorithm", vbs_score])
        table_data.append(["Best Single Algorithm (%s)" % (best_indx), bsa])
        table_data.append(["Instances not solved by any algorithm", unsolvable])

        if self.scenario.performance_type[0] == "runtime":
            n_inst = len(self.scenario.instances)
            vbs_clean = (vbs_score*n_inst - 10*self.scenario.algorithm_cutoff_time*unsolvable) / (n_inst - unsolvable)
            bsa_clean = (bsa*n_inst - 10*self.scenario.algorithm_cutoff_time*unsolvable) / (n_inst - unsolvable)
            table_data.append(["VBS (w/o unsolved instances)", vbs_clean])
            table_data.append(["Best Single Algorithm (w/o unsolved instances)", bsa_clean])

        df = pd.DataFrame(data=list(map(lambda x: x[1], table_data)), index=list(
            map(lambda x: x[0], table_data)), columns=[""])

        return df.to_html(header=False)

    def scatter_plots(self, plot_log_perf: bool=False):
        '''
            generate scatter plots of all pairs of algorithms in the performance data of the scenario
            and save them in the output directory

            Arguments
            ---------
            plot_log_perf: bool
                plot perf on log scale

            Returns
            -------
            list of all generated file names of plots
        '''
        matplotlib.pyplot.close()
        self.logger.info("Plotting scatter plots........")

        plots = []
        self.algorithms = self.scenario.algorithms
        n_algos = len(self.scenario.algorithms)

        if self.scenario.performance_type[0] == "runtime":
            max_val = self.scenario.algorithm_cutoff_time
        else:
            max_val = self.scenario.performance_data.max().max()

        for i in range(n_algos):
            for j in range(i + 1, n_algos):
                algo_1 = self.scenario.algorithms[i]
                algo_2 = self.scenario.algorithms[j]
                y_i = self.scenario.performance_data[algo_1].values
                y_j = self.scenario.performance_data[algo_2].values

                matplotlib.pyplot.close()

                if self.scenario.performance_type[0] == "runtime":
                    fig = plot_scatter_plot(x_data=y_i, y_data=y_j, max_val=max_val,
                                            labels=[algo_1, algo_2],
                                            metric=self.scenario.performance_type[0])
                else:
                    fig = figure(1, dpi=100)
                    ax1 = subplot(aspect='equal')
                    ax1.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
                    ax1.scatter(y_i, y_j, marker='x', c='black')
                    ax1.set_xlabel(algo_1, fontsize=20)
                    ax1.set_ylabel(algo_2, fontsize=20)
                    if plot_log_perf:
                        ax1.set_xscale("log")
                        ax1.set_yscale("log")
                    fig.tight_layout()
                    
                out_name = os.path.join(self.output_dn,
                                        "scatter_%s_%s.png" % (algo_1.replace("/", "_"), algo_2.replace("/", "_")))
                fig.savefig(out_name)
                plots.append((algo_1, algo_2, out_name))

        return plots

    def correlation_plot(self):
        '''
            generate correlation plot using spearman correlation coefficient and ward clustering

            Returns
            -------
            file name of saved plot
        '''
        matplotlib.pyplot.close()
        self.logger.info("Plotting correlation plots........")

        perf_data = self.scenario.performance_data.values
        algos = list(self.scenario.performance_data.columns)

        n_algos = len(algos)

        data = np.zeros((n_algos, n_algos)) + 1  # similarity
        for i in range(n_algos):
            for j in range(i + 1, n_algos):
                y_i = np.array(perf_data[:, i],dtype=np.float64)
                y_j = np.array(perf_data[:, j],dtype=np.float64)
                if np.sum(perf_data[:, i]) == 0:
                    y_i += np.random.rand(y_i.shape[0])*0.00001
                if np.sum(perf_data[:, j]) == 0:
                    y_j += np.random.rand(y_j.shape[0])*0.00001
                rho, p = spearmanr(y_i, y_j)
                data[i, j] = rho
                data[j, i] = rho

        link = linkage(data * -1, 'ward')  # input is distance -> * -1

        # plot clustering
        fig, ax = plt.subplots()
        dendrogram(link, labels=algos, orientation='right')
        out_plot = os.path.join(self.output_dn, "algo_clustering.png")
        plt.savefig(out_plot, format="png")
        matplotlib.pyplot.close()

        sorted_algos = [[a] for a in algos]
        for l in link:
            new_cluster = sorted_algos[int(l[0])][:]
            new_cluster.extend(sorted_algos[int(l[1])][:])
            sorted_algos.append(new_cluster)

        sorted_algos = sorted_algos[-1]

        # resort data
        indx_list = []
        for a in algos:
            indx_list.append(sorted_algos.index(a))
        indx_list = np.argsort(indx_list)
        data = data[indx_list, :]
        data = data[:, indx_list]

        fig, ax = plt.subplots()
        heatmap = ax.pcolor(data, cmap=plt.cm.Blues)

        # put the major ticks at the middle of each cell
        ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
        ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)

        plt.xlim(0, data.shape[0])
        plt.ylim(0, data.shape[0])

        # want a more natural, table-like display
        ax.invert_yaxis()
        ax.xaxis.tick_top()

        ax.set_xticklabels(sorted_algos, minor=False)
        ax.set_yticklabels(sorted_algos, minor=False)
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=90, fontsize=12, ha="left")
        labels = ax.get_yticklabels()
        plt.setp(labels, rotation=0, fontsize=12)

        fig.colorbar(heatmap)

        plt.tight_layout()

        out_plot = os.path.join(self.output_dn, "correlation_plot.png")
        plt.savefig(out_plot, format="png")

        return out_plot

    def get_contribution_values(self):
        '''
            contribution value computation

            Returns
            ------
            pandas.DataFrame() with columns being "Average Performance", "Marginal Performance", "Shapley Values" and indexes being the algorithms
        '''

        self.logger.info("Get contribution scores........")

        algorithms = self.scenario.algorithms
        instances = self.scenario.instances
        scenario = self.scenario
        n_insts = len(scenario.instances)

        performance_data = scenario.performance_data

        if self.scenario.maximize[0] == True:
            # Assume minimization
            performance_data = performance_data * -1

        max_perf = performance_data.max().max()

        is_time_scenario = self.scenario.performance_type[0] == "runtime"

        def metric(algo, inst):
            if is_time_scenario:
                perf = scenario.algorithm_cutoff_time - \
                    min(scenario.algorithm_cutoff_time,
                        performance_data[algo][inst])
                return perf
            else:
                return max_perf - performance_data[algo][inst]

        shapleys = self._get_VBS_Shap(instances, algorithms, metric)
        #shapleys = dict((k,v/n_insts) for k,v in shapleys.items())

        if self.scenario.maximize[0] == True:
            performance_data = performance_data * -1

        if self.scenario.maximize[0] == True:
            # marginal contribution code assumes: smaller is better
            self.scenario.performance_data = self.scenario.performance_data * - \
                1

        marginales = self._get_marginal_contribution()
        if self.scenario.maximize[0] == True:
            self.scenario.performance_data = self.scenario.performance_data * - \
                1

        averages = self._get_average_perf()

        #=======================================================================
        # sorted_avg = sorted(averages.items(), key=lambda x: x[1], reverse=True)
        # for algo, avg in sorted_avg:
        #     print("%s,%.3f,%.3f,%.3f" %(algo, avg, marginales[algo], shapleys[algo]))
        #=======================================================================
        
        out_fns = []
        for name, data_ in zip(["averages","marginales", "shapleys"], [averages, marginales, shapleys]):
            matplotlib.pyplot.close()
            fig = plt.figure()
            plt.axis('equal')
            ax = fig.gca()

            colormap = plt.cm.gist_ncar
            colors = [colormap(i) for i in np.linspace(
                0, 0.9, len(self.scenario.algorithms))]

            data_list = [data_[algo] for algo in algorithms]

            # automatically detect precision for legend
            mean_v = np.abs(np.mean(data_list))
            prec = 2
            while True:
                if round(mean_v, prec) > 0:
                    prec += 1
                    break
                prec += 1
            print_str = "%s (%.{}f)".format(prec)

            # rescale to fix pie plot issues
            sum_v = sum(data_.values())
            data_list = [v / sum_v for v in data_list]

            labels = [print_str % (algo, data_[algo]) for algo in algorithms]
            patches, texts = plt.pie(data_list, colors=colors)
            plt.legend(
                patches, labels, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

            plt.tight_layout()

            out_fn = os.path.join(
                self.output_dn, "contribution_%s_pie_plot.png" % (name))

            plt.savefig(out_fn, facecolor='w', edgecolor='w',
                        orientation='portrait', papertype=None, format=None,
                        transparent=False, pad_inches=0.02, bbox_inches='tight')

            out_fns.append(out_fn)

        return out_fns

    def _get_average_perf(self):
        '''
            compute average performance of algorithms
        '''
        averages = {}
        for algorithm in self.scenario.algorithms:
            averages[algorithm] = self.scenario.performance_data[
                algorithm].mean()
        return averages

    def _get_marginal_contribution(self):
        '''
            compute marginal contribution of each algorithm
        '''
        marginales = {}
        all_vbs = self.__get_vbs(self.scenario.performance_data)
        self.logger.info("VBS: %f" % (all_vbs))
        for algorithm in self.scenario.algorithms:
            remaining_algos = list(
                set(self.scenario.algorithms).difference([algorithm]))
            perf_data = self.scenario.performance_data[remaining_algos]
            rem_vbs = self.__get_vbs(perf_data)
            marginales[algorithm] = rem_vbs - all_vbs

        return marginales

    def __get_vbs(self, performance_data):
        return np.mean(performance_data.min(axis=1))

    def _get_VBS_Shap(self, instances, algorithms, metric):
        '''
            instances - the instances to solve.
            algorithms - the set of available algorithms.
            metric - the performance metric from (algorithm,instance) to real number. Higher is better.

            Returns a dictionary from algorithms to their Shapley value, where the coalitional function is
            $$ v(S) = \frac{1}{|X|} \sum_{x\in X} \max_{s\in S} metric(s,x),$$
            where X is the set of instances. This is the "average VBS game" with respect to the given instances,
            algorithms and metric.

            __author__ = "Alexandre Frechett et al"
            slight modification by me
        '''
        n = len(algorithms)
        m = len(instances)

        shapleys = {}

        # For each instance
        for instance in instances:
            instance_algorithms = sorted(
                algorithms, key=lambda a: metric(a, instance))

            # For each algorithm, from worst to best.
            for i in range(len(instance_algorithms)):
                ialgorithm = instance_algorithms[i]

                #print >> sys.stderr, 'Processing the rule corresponding to %d-th algorithm "%s" being the best in the coalition.' % (i,ialgorithm)

                # The MC-rule is that you must have the algorithm and none of
                # the better ones.
                '''
                If x is the instance and s_1^x,...,s_n^x are sorted from worst, then the rule's pattern is:
                $$ p_i^x = s_i^x \wedge \bigwedge_{j=i+1}^n \overline{s}_j^x $$
                and its weight is 
                $$ w_i^x = metric(s_i^x,x).$$
                '''
                pos = 1
                neg = n - i - 1

                metricvalue = metric(ialgorithm, instance)
                # normalised as fraction of instances
                value = 1 / float(m) * metricvalue
                #value = metricvalue
                #print >> sys.stderr, 'Value of this rule : 1/%d * %.4f = %.4f' % (m,metricvalue,value)

                # Calculate the rule Shapley values, and add them to the global
                # Shapley values.

                # Shapley value for positive literals in the rule.
                pos_shap = value / \
                    float(pos * comb(pos + neg, neg, exact=True))
                # Shapley value for negative literals in the rule.
                if neg > 0:
                    neg_shap = -value / \
                        float(neg * comb(pos + neg, pos, exact=True))
                else:
                    neg_shap = None

                # Update the Shapley value for the literals appearing in the
                # rule.
                for j in range(i, len(instance_algorithms)):
                    jalgorithm = instance_algorithms[j]

                    if jalgorithm not in shapleys:
                        shapleys[jalgorithm] = 0

                    if j == i:
                        shapleys[jalgorithm] += pos_shap
                    else:
                        shapleys[jalgorithm] += neg_shap

        return shapleys

    def get_cdf_plots(self, plot_log_perf: bool=False):
        '''
            plot the cummulative distribution function of each algorithm

            Arguments
            ---------
            plot_log_perf: bool
                plot perf on log scale

            Returns
            -------
            file name of saved plot
        '''
        matplotlib.pyplot.close()
        self.logger.info("Plotting CDF plots........")

        from cycler import cycler

        gs = matplotlib.gridspec.GridSpec(1, 1)

        fig = plt.figure()
        ax1 = plt.subplot(gs[0:1, :])

        colormap = plt.cm.gist_ncar
        fig.gca().set_prop_cycle(cycler('color', [
            colormap(i) for i in np.linspace(0, 0.9, len(self.scenario.algorithms))]))

        if self.scenario.performance_type[0] == "runtime":
            max_val = self.scenario.algorithm_cutoff_time
            min_val = max(0.0005, self.scenario.performance_data.min().min())
        else:
            max_val = self.scenario.performance_data.max().max()
            min_val = self.scenario.performance_data.min().min()
            
        if plot_log_perf: 
            min_val = max(0.0005, min_val)

        for algorithm in self.scenario.algorithms:
            x, y = get_cdf_x_y(
                self.scenario.performance_data[str(algorithm)], max_val)
            x = np.array(x)
            y = np.array(y)
            x[x < min_val] = min_val
            ax1.step(x, y, label=algorithm)

        ax1.grid(
            True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
        ax1.set_xlabel(self.scenario.performance_measure[0])
        ax1.set_ylabel("P(x<X)")
        ax1.set_xlim([min_val, max_val])
        if self.scenario.performance_type[0] == "runtime" or plot_log_perf:
            ax1.set_xscale('log')

        #ax1.legend(loc='lower right')
        ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        out_fn = os.path.join(self.output_dn, "cdf_plot.png")

        plt.savefig(out_fn, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format=None,
                    transparent=False, pad_inches=0.02, bbox_inches='tight')

        return out_fn

    def get_violin_plots(self, plot_log_perf: bool=False):
        '''
            compute violin plots (fancy box plots) for each algorithm
            
            Arguments
            ---------
            plot_log_perf: bool
                plot perf on log scale
        '''
        matplotlib.pyplot.close()
        self.logger.info("Plotting vilion plots........")

        cutoff = self.scenario.algorithm_cutoff_time
        fig, ax = plt.subplots(nrows=1, ncols=1)
        all_data = self.scenario.performance_data.values
        if self.scenario.performance_type[0] == "runtime":
            all_data[all_data > cutoff] = cutoff

        if self.scenario.performance_type[0] == "runtime" or plot_log_perf:
            all_data = np.log10(all_data)
            y_label = "log(%s)" % (self.scenario.performance_type[0])
        else:
            y_label = "%s" % (self.scenario.performance_type[0])
        n_points = all_data.shape[0]
        all_data = [all_data[:, i] for i in range(all_data.shape[1])]
        ax.violinplot(
            all_data, showmeans=False, showmedians=True, points=n_points)

        ax.yaxis.grid(True)
        ax.set_ylabel(y_label)

        plt.setp(ax, xticks=[y + 1 for y in range(len(all_data))],
                 xticklabels=self.scenario.performance_data.columns.values)

        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=12, ha="right")

        plt.tight_layout()

        out_fn = os.path.join(self.output_dn, "violin_plot.png")
        plt.savefig(out_fn)

        return out_fn

    def get_box_plots(self, plot_log_perf: bool=False):
        '''
            compute violin plots (fancy box plots) for each algorithm
            
            Arguments
            ---------
            plot_log_perf: bool
                plot perf on log scale
        '''
        matplotlib.pyplot.close()
        self.logger.info("Plotting box plots........")

        cutoff = self.scenario.algorithm_cutoff_time
        fig, ax = plt.subplots(nrows=1, ncols=1)
        all_data = self.scenario.performance_data.values
        if self.scenario.performance_type[0] == "runtime":
            all_data[all_data > cutoff] = cutoff

        n_points = all_data.shape[0]
        all_data = [all_data[:, i] for i in range(all_data.shape[1])]

        ax.boxplot(all_data)

        ax.yaxis.grid(True)
        y_label = "%s" % (self.scenario.performance_type[0])
        ax.set_ylabel(y_label)

        if self.scenario.performance_type[0] == "runtime" or plot_log_perf:
            ax.set_yscale('log')

        plt.setp(ax, xticks=[y + 1 for y in range(len(all_data))],
                 xticklabels=self.scenario.performance_data.columns.values)

        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=12, ha="right")

        try:
            plt.tight_layout()
        except ValueError:
            pass

        out_fn = os.path.join(self.output_dn, "box_plot.png")
        plt.savefig(out_fn)

        return out_fn

    def get_bar_status_plot(self):
        '''
            get status distribution as stacked bar plot
        '''
        matplotlib.pyplot.close()
        self.logger.info("Plotting bar plots........")
        runstatus_data = self.scenario.runstatus_data

        width = 0.5
        stati = ["ok", "timeout", "memout", "not_applicable", "crash", "other"]

        count_stats = np.array(
            [runstatus_data[runstatus_data == status].count().values for status in stati])
        count_stats = count_stats / len(self.scenario.instances)

        colormap = plt.cm.gist_ncar
        cc = [colormap(i) for i in np.linspace(0, 0.9, len(stati))]

        bottom = np.zeros((len(self.scenario.algorithms)))
        ind = np.arange(len(self.scenario.algorithms)) + 0.5
        plots = []
        for id, status in enumerate(stati):
            plots.append(
                plt.bar(ind, count_stats[id, :], width, color=cc[id], bottom=bottom))
            bottom += count_stats[id, :]

        plt.ylabel('Frequency of runstatus')
        plt.xticks(
            ind + width / 2., list(runstatus_data.columns), rotation=45, ha="right")
        lgd = plt.legend(list(map(lambda x: x[0], plots)), stati, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                         ncol=3, mode="expand", borderaxespad=0.)

        try:
            plt.tight_layout()
        except ValueError:
            pass
        out_fn = os.path.join(self.output_dn, "status_bar_plot.png")
        plt.savefig(out_fn, bbox_extra_artists=(lgd,), bbox_inches='tight')

        return out_fn

    def get_cd_diagram(self):
        '''
            computes critical distance plots with the orange package
        '''
        import Orange

        # orange allows unfortunately only 20 algorithms for cd diagrams
        MAX_ALGOS = 20

        if self.scenario.maximize[0] == True:
            # marginal contribution code assumes: smaller is better
            self.scenario.performance_data = self.scenario.performance_data * - \
                1

        matplotlib.pyplot.close()
        self.logger.info("Plotting critical distance plots........")
        # labels of each technique
        names = list(self.scenario.performance_data.columns)
        if len(names) > MAX_ALGOS:
            # sort algorithms by their average ranks
            names = list(self.scenario.performance_data.rank(
                axis=1).mean(axis=0).sort_values().index)
            names = names[:MAX_ALGOS]
            performance_data = self.scenario.performance_data[names]
        else:
            performance_data = self.scenario.performance_data

        avranks = performance_data.rank(axis=1).mean(
            axis=0).values  # average ranking of each technique
        number_of_datasets = len(self.scenario.instances)  # number of datasets

        cd = Orange.evaluation.compute_CD(
            avranks, number_of_datasets, alpha="0.05", test='nemenyi')
        out_fn = os.path.join(self.output_dn, "cd_diagram.png")
        Orange.evaluation.graph_ranks(
            avranks, names, cd=cd, width=12, textspace=2)
        plt.savefig(out_fn)

        if self.scenario.maximize[0] == True:
            # marginal contribution code assumes: smaller is better
            self.scenario.performance_data = self.scenario.performance_data * - \
                1

        return out_fn

    def get_footprints(self, eps=0.05):
        '''
            computes the algorithm footprint in feature space,
            i.e. all instances that can be solved within eps% of the VBS performance

            Arguments
            ---------
            eps: float
                eps% threshold to VBS performance
        '''

        self.logger.info("Plotting footprints........")

        self.scenario.feature_data = self.scenario.feature_data.fillna(
            self.scenario.feature_data.mean())

        # feature data
        features = self.scenario.feature_data.values

        # scale features
        ss = StandardScaler()
        features = ss.fit_transform(features)

        # feature reduction: pca
        # TODO: use feature selection first to use only important features
        pca = PCA(n_components=2)
        features = pca.fit_transform(features)
        features = pd.DataFrame(
            data=features, index=self.scenario.feature_data.index)

        performance_data = self.scenario.performance_data

        if self.scenario.maximize[0] == False:
            vbs_perf = performance_data.min(axis=1)
        else:
            vbs_perf = performance_data.max(axis=1)

        algorithms = self.scenario.algorithms

        out_fns = []
        for algo in algorithms:
            out_fn = os.path.join(
                self.output_dn, "footprint_%s" % (algo.replace("/", "_")))

            algo_perf = performance_data[algo]
            if self.scenario.maximize[0] == False:
                vbs_perfs = vbs_perf * (1 + eps)
                footprint = (algo_perf <= vbs_perfs) & (
                    self.scenario.runstatus_data[algo] == "ok")
            else:
                vbs_perfs = vbs_perf * (1 - eps)
                footprint = (algo_perf >= vbs_perfs) & (
                    self.scenario.runstatus_data[algo] == "ok")

            matplotlib.pyplot.close()
            fig = plt.figure()

            non_insts = footprint[footprint == False].index.tolist()
            feature_not = features.loc[non_insts]
            scatter = plt.scatter(
                feature_not[0], feature_not[1], c="black", linewidths=0, alpha=0.5, s=60)

            tooltip = mpld3.plugins.PointHTMLTooltip(scatter, non_insts,
                                                     voffset=10, hoffset=10)
            mpld3.plugins.connect(fig, tooltip)

            ok_insts = footprint[footprint == True].index.tolist()
            features_ok = features.loc[ok_insts]
            scatter = plt.scatter(
                features_ok[0], features_ok[1], c="red", linewidths=0, alpha=0.5, s=60)

            tooltip = mpld3.plugins.PointHTMLTooltip(scatter, ok_insts,
                                                     voffset=10, hoffset=10)
            mpld3.plugins.connect(fig, tooltip)

            #mpld3.save_html(fig, out_fn + ".html")
            plt.tight_layout()
            plt.savefig(out_fn + ".png", format="png")

            out_fns.append([algo, out_fn + ".html", out_fn + ".png"])

        return out_fns

    def instance_hardness(self, eps=0.05):
        '''
            plot instances in 2d PCA feature space 
            and color them according to number of algorithms that are at most eps% away from oralce score
        '''
        matplotlib.pyplot.close()
        self.logger.info("Plotting Instance hardness........")

        self.scenario.feature_data = self.scenario.feature_data.fillna(
            self.scenario.feature_data.mean())

        # feature data
        features = self.scenario.feature_data.values
        insts = self.scenario.feature_data.index.tolist()

        # scale features
        ss = StandardScaler()
        features = ss.fit_transform(features)

        # feature reduction: pca
        # TODO: use feature selection first to use only important features
        pca = PCA(n_components=2)
        features = pca.fit_transform(features)
        features = pd.DataFrame(
            data=features, index=self.scenario.feature_data.index)

        performance_data = self.scenario.performance_data

        if self.scenario.maximize[0] == False:
            vbs_perf = performance_data.min(axis=1)
        else:
            vbs_perf = performance_data.max(axis=1)

        algorithms = self.scenario.algorithms

        hardness_insts = pd.DataFrame(data=np.zeros((len(insts))), index=insts)

        for algo in algorithms:
            out_fn = os.path.join(self.output_dn, "footprint_%s.html" % (algo))

            algo_perf = performance_data[algo]
            if self.scenario.maximize[0] == False:
                vbs_perfs = vbs_perf * (1 + eps)
                footprint = (algo_perf <= vbs_perfs) & (
                    self.scenario.runstatus_data[algo] == "ok")
            else:
                vbs_perfs = vbs_perf * (1 - eps)
                footprint = (algo_perf >= vbs_perfs) & (
                    self.scenario.runstatus_data[algo] == "ok")

            hardness_insts.loc[footprint[footprint].index.tolist()] += 1

        fig = plt.figure()

        x = []
        y = []
        c = []
        insts_all = []
        for i in range(len(algorithms) + 1):
            insts = hardness_insts[
                (hardness_insts == float(i)).values].index.tolist()
            f = features.loc[insts]
            x.extend(f[0])
            y.extend(f[1])
            c.extend([i] * len(insts))
            insts_all.extend(insts)

        scatter = plt.scatter(x, y, c=c, vmin=1, vmax=len(
            algorithms), edgecolors="black", cmap=plt.cm.jet, linewidths=0, alpha=0.5, s=40)

        out_fn = os.path.join(self.output_dn, "instance_hardness")

        tooltip = mpld3.plugins.PointHTMLTooltip(scatter, insts_all,
                                                 voffset=10, hoffset=10)
        mpld3.plugins.connect(fig, tooltip)

        # mpld3 does not support legends
        #mpld3.save_html(fig, out_fn + ".html")

        plt.colorbar(scatter)
        plt.savefig(out_fn+".png", bbox_inches='tight')
            
        return out_fn+".html", out_fn+".png" 
