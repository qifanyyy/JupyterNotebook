import sys
import logging

import numpy as np

from aslib_scenario.aslib_scenario import ASlibScenario

__author__ = "Marius Lindauer, Jan N. van Rijn"
__license__ = "BSD"


# this is modified version of the validation script from AutoFolio

class Stats(object):

    def __init__(self, runtime_cutoff: int,
                 maximize: bool):
        """ Constructor

            Arguments
            ---------
            runtime_cutoff: int
                maximal running time
            maximize: bool
                whether objective has to be maxmized (true)
                or minimized (false)
        """
        self.par1 = 0.0
        self.par10 = 0.0
        self.timeouts = 0
        self.solved = 0
        self.unsolvable = 0
        self.presolved_feats = 0

        self.oracle_par10 = 0.0
        self.sbs_par10 = 0.0

        self.runtime_cutoff = runtime_cutoff
        self.maximize = maximize
        self.worse_than_sbs = 0  # int counter

        self.logger = logging.getLogger("Stats")

    def get_time_outs(self, remove_unsolvable: bool) -> int:
        if remove_unsolvable and self.runtime_cutoff:
            return self.timeouts - self.unsolvable
        else:
            return self.timeouts

    def get_n_samples(self, remove_unsolvable: bool) -> int:
        if self.runtime_cutoff:
            return self.get_time_outs(remove_unsolvable) + self.solved
        else:
            return self.solved

    def get_par10(self, remove_unsolvable: bool) -> float:
        if remove_unsolvable and self.runtime_cutoff:
            return self.par10 - (self.unsolvable * self.runtime_cutoff * 10)
        else:
            return self.par10

    def get_par10_oracle(self, remove_unsolvable: bool) -> float:
        if remove_unsolvable:
            return self.oracle_par10 - (self.unsolvable * self.runtime_cutoff * 10)
        else:
            return self.oracle_par10

    def get_par10_sbs(self, remove_unsolvable: bool) -> float:
        if remove_unsolvable:
            return self.sbs_par10 - (self.unsolvable * self.runtime_cutoff * 10)
        else:
            return self.sbs_par10

    def get_par1(self, remove_unsolvable: bool) -> float:
        if remove_unsolvable and self.runtime_cutoff:
            return self.par1 - (self.unsolvable * self.runtime_cutoff)
        else:
            return self.par1

    def get_score(self, remove_unsolvable: bool) -> float:
        if self.runtime_cutoff:
            # runtime scenario
            return self.par10 / self.get_n_samples(remove_unsolvable)
        else:
            # quality scenario
            return self.par1 / self.get_n_samples(remove_unsolvable)

    def get_score_oracle(self, remove_unsolvable: bool) -> float:
        return self.oracle_par10 / self.get_n_samples(remove_unsolvable)

    def get_score_sbs(self, remove_unsolvable: bool) -> float:
        return self.sbs_par10 / self.get_n_samples(remove_unsolvable)

    def get_closed_gap(self, remove_unsolvable: bool) -> float:
        system_score = self.get_score(remove_unsolvable)
        sbs = self.get_score_sbs(remove_unsolvable)
        oracle = self.get_score_oracle(remove_unsolvable)

        if self.maximize:
            return (system_score - sbs) / (oracle - sbs)
        else:
            return (sbs - system_score) / (sbs - oracle)

    def get_gap_remaining(self, remove_unsolvable: bool) -> float:
        system_score = self.get_score(remove_unsolvable)
        sbs = self.get_score_sbs(remove_unsolvable)
        oracle = self.get_score_oracle(remove_unsolvable)

        if self.maximize:
            return (oracle - system_score) / (oracle - sbs)
        else:
            return (system_score - oracle) / (sbs - oracle)

    def show(self, remove_unsolvable: bool = True):
        """
            shows statistics

            Arguments
            --------
            remove_unsolvable : bool
                remove unsolvable from stats

            Returns
            -------
            par10: int
                penalized average runtime
        """

        if remove_unsolvable and self.runtime_cutoff:
            rm_string = "removed"
            self.logger.debug("Statistics before removing unsolvable instances")
            self.logger.debug("PAR1: %.4f" % self.get_par1(False))
            self.logger.debug("PAR10: %.4f" % self.get_par10(False))
            self.logger.debug("Timeouts: %d / %d" % (self.get_time_outs(False), self.get_n_samples(False)))
        else:
            rm_string = "not removed"

        if self.runtime_cutoff:
            self.logger.info("PAR1: %.4f" % self.get_par1(remove_unsolvable))
            self.logger.info("PAR10: %.4f" % self.get_par10(remove_unsolvable))
            self.logger.info("Timeouts: %d / %d" % (self.get_time_outs(remove_unsolvable),
                                                    self.get_n_samples(remove_unsolvable)))
            self.logger.info("Presolved during feature computation: %d / %d" % (self.presolved_feats,
                                                                                self.get_n_samples(remove_unsolvable)))
            self.logger.info("Solved: %d / %d" % (self.solved, self.get_n_samples(remove_unsolvable)))
            self.logger.info("Unsolvable (%s): %d / %d" %
                             (rm_string, self.unsolvable, self.get_n_samples(remove_unsolvable) + self.unsolvable))
        else:
            self.logger.info("Number of instances: %d" % self.get_n_samples(remove_unsolvable))
            self.logger.info("Average Solution Quality: %.4f" % (self.get_par1(remove_unsolvable) / self.get_n_samples(remove_unsolvable)))

        self.logger.info(">>>>>>>>>>>>>>>>>>>>>")
        self.logger.info("System: %.4f" % (self.get_score(remove_unsolvable)))
        self.logger.info("Oracle: %.4f" % (self.get_score_oracle(remove_unsolvable)))
        self.logger.info("SBS: %.4f" % (self.get_score_sbs(remove_unsolvable)))

        self.logger.info("Gap closed: %.4f" % self.get_closed_gap(remove_unsolvable))
        self.logger.info("Gap remaining: %.4f" % self.get_gap_remaining(remove_unsolvable))


class Validator(object):

    def __init__(self):
        """ Constructor """
        self.logger = logging.getLogger("Validation")

    def validate_runtime(self, schedules: dict, test_scenario: ASlibScenario,
                         train_scenario: ASlibScenario):
        """
            validate selected schedules on test instances for runtime

            Arguments
            ---------
            schedules: dict {instance name -> tuples [algo, bugdet]}
                algorithm schedules per instance
            test_scenario: ASlibScenario
                ASlib scenario with test instances
            train_scenario: ASlibScenario
                ASlib scenario with test instances -- required for SBS
        """
        if test_scenario.performance_type[0] != "runtime":
            raise ValueError("Cannot validate non-runtime scenario with runtime validation method")

        stat = Stats(runtime_cutoff=test_scenario.algorithm_cutoff_time,
                     maximize=test_scenario.maximize[0])

        feature_times = False
        if test_scenario.feature_cost_data is not None and test_scenario.performance_type[0] == "runtime":
            feature_times = True

        ok_status = test_scenario.runstatus_data == "ok"
        unsolvable = ok_status.sum(axis=1) == 0
        stat.unsolvable += unsolvable.sum()

        # ensure that we got predictions for all test instances
        if set(test_scenario.instances).difference(schedules.keys()):
            self.logger.error(
                "Missing predictions for %s" % (set(test_scenario.instances).difference(schedules.keys())))
            sys.exit(1)

        stat.oracle_par10 = test_scenario.performance_data.min(axis=1).sum()
        sbs = train_scenario.performance_data.sum(axis=0).argmin()
        stat.sbs_par10 = test_scenario.performance_data.sum(axis=0)[sbs]

        for inst, schedule in schedules.items():
            self.logger.debug("Validate: %s on %s" % (schedule, inst))

            used_time = 0
            feature_steps_used = []
            for entry in schedule:
                if isinstance(entry, str):
                    if entry in test_scenario.algorithms:
                        algo = entry
                        budget = np.inf
                        time = test_scenario.performance_data[algo][inst]
                        self.logger.debug("Alloted time %f of %s vs true time %f" % (budget, algo, time))
                        used_time += min(time, budget)
                        solved = (time <= budget) and test_scenario.runstatus_data[algo][inst] == "ok"
                    elif entry in test_scenario.feature_steps:
                        feature_steps_used.append(entry)
                        if test_scenario.feature_group_dict[entry].get("requires") is not None:
                            missing_f_groups = list(
                                set(test_scenario.feature_group_dict[entry]["requires"]).difference(feature_steps_used))
                            if missing_f_groups:
                                self.logger.error("Required feature steps (%s) are missing for computing %s." % (
                                missing_f_groups, entry))
                        if feature_times:
                            ftime = test_scenario.feature_cost_data[entry][inst]
                            self.logger.debug("Used Feature time: %f" % (ftime))
                            used_time += ftime
                        solved = (test_scenario.feature_runstatus_data[entry][inst] == "presolved")
                    else:
                        self.logger.error("Schedule entry %s for %s not found in data" % (entry, inst))
                elif isinstance(entry, list):  # algorithm
                    algo, budget = entry
                    time = test_scenario.performance_data[algo][inst]
                    self.logger.debug("Alloted time %f of %s vs true time %f" % (budget, algo, time))
                    used_time += min(time, budget)
                    solved = (time <= budget) and test_scenario.runstatus_data[algo][inst] == "ok"
                self.logger.debug("Used time (so far): %f" % (used_time))

                if solved and used_time <= test_scenario.algorithm_cutoff_time:
                    stat.solved += 1
                    stat.par1 += used_time
                    self.logger.info("Solved after %f" % (used_time))
                    break
                elif used_time >= test_scenario.algorithm_cutoff_time:
                    stat.timeouts += 1
                    stat.par1 += test_scenario.algorithm_cutoff_time
                    self.logger.debug("Timeout after %f (< %f)" % (test_scenario.algorithm_cutoff_time, used_time))
                    break

            if not solved and used_time < test_scenario.algorithm_cutoff_time:
                self.logger.warn(
                    "Schedule ended without using all time: %f" % (test_scenario.algorithm_cutoff_time - used_time))
                self.logger.warn("Counting as timeout")
                stat.timeouts += 1
                stat.par1 += test_scenario.algorithm_cutoff_time

        stat.par10 = stat.par1 + 9 * \
                     test_scenario.algorithm_cutoff_time * stat.timeouts

        stat.show()

        return stat

    def validate_quality(self, schedules: dict, test_scenario: ASlibScenario,
                         train_scenario: ASlibScenario):
        """
            validate selected schedules on test instances for solution quality

            Arguments
            ---------
            schedules: dict {instance name -> tuples [algo, bugdet]}
                algorithm schedules per instance
            test_scenario: ASlibScenario
                ASlib scenario with test instances
            train_scenario: ASlibScenario
                ASlib scenario with test instances -- required for SBS
        """
        if test_scenario.performance_type[0] != "solution_quality":
            raise ValueError("Cannot validate non-solution_quality scenario with solution_quality validation method")

        self.logger.debug("FYI: Feature costs and algorithm runstatus is ignored")

        if test_scenario.maximize[0]:
            test_scenario.performance_data *= -1
            train_scenario.performance_data *= -1
            self.logger.debug("Removing *-1 in performance data because of maximization")

        stat = Stats(runtime_cutoff=None, maximize=test_scenario.maximize[0])

        # ensure that we got predictions for all test instances
        if set(test_scenario.instances).difference(schedules.keys()):
            self.logger.error(
                "Missing predictions for %s" % (set(test_scenario.instances).difference(schedules.keys())))
            sys.exit(1)

        if test_scenario.maximize[0]:
            stat.oracle_par10 = test_scenario.performance_data.max(axis=1).sum()
            sbs = train_scenario.performance_data.sum(axis=0).argmax()
            stat.sbs_par10 = test_scenario.performance_data.sum(axis=0)[sbs]
        else:
            stat.oracle_par10 = test_scenario.performance_data.min(axis=1).sum()
            sbs = train_scenario.performance_data.sum(axis=0).argmin()
            stat.sbs_par10 = test_scenario.performance_data.sum(axis=0)[sbs]

        for inst, schedule in schedules.items():
            if len(schedule) == 0:
                raise ValueError('Found empty schedule for instance %s' % inst)
            for entry in schedule:
                if isinstance(entry, str):
                    if entry in test_scenario.algorithms:
                        selected_algo = entry
                        perf = test_scenario.performance_data[selected_algo][inst]
                        break
                    else:
                        self.logger.debug("Skip %s" % (entry))
                elif isinstance(entry, list):
                    entry = entry[0]  # ignore cutoff
                    if entry in test_scenario.algorithms:
                        selected_algo = entry
                        perf = test_scenario.performance_data[selected_algo][inst]
                        break
                    else:
                        self.logger.debug("Skip %s" % (entry))
                else:
                    raise ValueError('schedule entries should be of type str or list')

            self.logger.debug("Using %s on %s with performance %f" % (selected_algo, inst, perf))

            stat.par1 += perf
            stat.solved += 1
            if test_scenario.maximize[0]:
                if perf < test_scenario.performance_data[sbs][inst]:
                    stat.worse_than_sbs += 1
                    print(
                        "%s(%.3f) vs %s (%.3f)" % (selected_algo, perf, sbs, test_scenario.performance_data[sbs][inst]))
            else:
                if perf > test_scenario.performance_data[sbs][inst]:
                    stat.worse_than_sbs += 1
                    print(
                        "%s(%.3f) vs %s (%.3f)" % (selected_algo, perf, sbs, test_scenario.performance_data[sbs][inst]))

        stat.show(remove_unsolvable=False)

        return stat
