import numpy as np
import numpy.linalg
import os
import numexpr as ne
from random import shuffle, randint
import matplotlib.pyplot as plt
import logging
from time import gmtime, strftime


from TPC_Config import *




class Pattern(object):

    def __init__(self, id, pattern):
        self.pattern = pattern
        self.x_pos = False
        self.y_pos = False
        self.x_nn = False
        self.y_nn = False
        self.id = id

    def get_pattern(self):
        return self.pattern

    def get_sim_score(self, pattern, score_type,pmt_selection, Weights):

        ## Implement Quantum Efficiencies if not MonteCarlo Derived

        if not max(pattern):
            score = False
        elif score_type == 'BinaryDifference':
            sim_pattern = np.logical_xor(self.pattern, pattern)
            score = (sim_pattern == True).sum()

        elif score_type == 'Manhattan_Distance':
            A = [i / max(self.pattern) for i in self.pattern]  ## Should I use Sum or Max for Normalizaiton
            B = [j / max(pattern) for j in pattern]
            score = np.sum(np.abs(np.array(A) - np.array(B)))

        elif score_type == 'RMS_Normed':
            A = [i / sum(self.pattern) for i in self.pattern]  ## Should I use Sum or Max for Normalizaiton
            B = [j / sum(pattern) for j in pattern]
            score = np.sum(np.square(np.multiply(.8*Weights+1,np.subtract(np.array(A), np.array(B)))))
        elif score_type == 'Pattern_Fitter':
            score = (self.get_gof_pattern_fitter(self.pattern,pattern,pmt_selection, 'chi2gamma')+
                     self.get_gof_pattern_fitter(pattern,self.pattern, pmt_selection, 'chi2gamma'))
        elif score_type == 'Correlate':
            score = int(np.correlate(self.pattern,pattern))
        #### I need to implement Profile Likelihood Function from XENON Code
        elif score_type == 'Ranked_RMS':
            score = self.ranked_rms(pattern, Weights)

        else:
            score = False

        return score

    def get_gof_pattern_fitter(self, pattern0, pattern, pmt_selection, statistic):

        areas_observed = np.array([item for i, item in enumerate(pattern) if i in pmt_selection])
        q = np.array([item for i, item in enumerate(pattern0) if i in pmt_selection])
        square_syst_errors = (0 * areas_observed) ** 2

        qsum = q.sum(axis=-1)[..., np.newaxis]  # noqa
        fractions_expected = ne.evaluate("q / qsum")  # noqa
        total_observed = areas_observed.sum()  # noqa
        ao = areas_observed  # noqa
        # square_syst_errors = square_syst_errors[pmt_selection]  # noqa

        # The actual goodness of fit computation is here...
        # Areas expected = fractions_expected * sum(areas_observed)
        if statistic == 'chi2gamma':
            result = ne.evaluate("(ao + where(ao > 1, 1, ao) - {ae})**2 /"
                                 "({ae} + square_syst_errors + 1)".format(ae='fractions_expected * total_observed'))
        elif statistic == 'chi2':
            result = ne.evaluate("(ao - {ae})**2 /"
                                 "({ae} + square_syst_errors)".format(ae='fractions_expected * total_observed'))
        elif statistic == 'likelihood_poisson':
            # Poisson likelihood chi-square (Baker and Cousins, 1984)
            # Clip areas to range [0.0001, +inf), because of log(0)
            areas_expected_clip = np.clip(fractions_expected * total_observed, 1e-10, float('inf'))
            areas_observed_clip = np.clip(areas_observed, 1e-10, float('inf'))
            result = ne.evaluate("-2*({ao} * log({ae}/{ao}) + {ao} - {ae})".format(ae='areas_expected_clip',
                                                                                   ao='areas_observed_clip'))
        else:
            raise ValueError('Pattern goodness of fit statistic %s not implemented!' % statistic)

        return np.sum(result, axis=-1)

    def ranked_rms(self, pattern,Weights):

        # pattern_self = [i/sum(self.pattern) for i in self.pattern]
        pattern_self = np.array(self.pattern)/sum(self.pattern)
        # pattern = [i/sum(pattern) for i in pattern]
        pattern = np.array(pattern)/sum(pattern)
        ind_1 = np.argsort(self.pattern)[-30:][::-1]
        ind_2 = np.argsort(pattern)[-30:][::-1]
        difference_array = [np.sqrt((PMT_X[ind_1[i]]-PMT_X[ind_2[i]])**2+(PMT_Y[ind_1[i]]-PMT_Y[ind_2[i]])**2)
                            * (pattern_self[ind_1[i]]*Weights[ind_1[i]] + pattern[ind_2[i]]*Weights[ind_2[i]])
                            for i in range(0, len(ind_1))]
        similarity = sum(difference_array)
        return similarity

    def mega_ranked_rms(self, pattern,Weights):

        # pattern_self = [i/sum(self.pattern) for i in self.pattern]
        pattern_self = np.array(self.pattern)/sum(self.pattern)
        # pattern = [i/sum(pattern) for i in pattern]
        pattern = np.array(pattern)/sum(pattern)
        ind_1 = np.argsort(self.pattern)[-30:][::-1]
        ind_2 = np.argsort(pattern)[-30:][::-1]
        difference_array = [np.sqrt((PMT_X[ind_1[i]]-PMT_X[ind_2[i]])**2+(PMT_Y[ind_1[i]]-PMT_Y[ind_2[i]])**2)
                            * (pattern_self[ind_1[i]]*Weights[ind_1[i]] + pattern[ind_2[i]]*Weights[ind_2[i]])
                            for i in range(0, len(ind_1))]
        similarity = sum(difference_array)
        return similarity



    def set_position(self, x, y):
        self.x_pos = x
        self.y_pos = y

    def set_nn_position(self, x, y):
        self.x_nn = x
        self.y_nn = y

    def get_position(self):
        return self.x_pos, self.y_pos

    def get_nn_position(self):
        return self.x_nn, self.y_nn


class TpcRep(object):

    def __init__(self,plot_path):
        self.edm = np.zeros(1)
        self.resolution = 5
        self.pattern_list = []
        self.distribution = np.array(1)
        self.empty = True
        self.score = 'Ranked_RMS' # 'Pattern_Fitter'  # 'Correlate', 'RMS_Normed' 'Manhattan_Distance'  # Other options. BinaryDifference...
        self.tpc_radius = 50
        self.polar_dist = np.array(1)
        self.polar_dist_flipped = np.array(1)
        self.polar_nn_dist = np.array(1)
        self.pmt_selection = active_pmts
        self.plot_path=plot_path
        logging.critical('Begining EDM Construction')
        logging.critical('Type of distance calculation: '+self.score)

    def give_events(self, events, number_of_events, weights):

        if self.empty:
            print('Starting with ' + str(len(events)) + ' number of events')
            logging.critical('Starting with ' + str(len(events)) + ' number of events')
            # number_of_events = 400
            event_start = randint(100, len(events)-number_of_events)
            unsorted_events = [x for i, x in enumerate(events) if max(x[0]) and event_start < i < (event_start+number_of_events)]
            self.edm = np.zeros((len(unsorted_events), len(unsorted_events)))
            self.edm[0, 0] = 0
            shuffle(unsorted_events)
            unsorted_events, unsorted_x, unsorted_y = zip(*unsorted_events)  # Unzip the pattern, x and y after shuffle
            unsorted_events = [x[0:127] for x in unsorted_events]#.tolist()
            self.pattern_list.append(Pattern(0, unsorted_events[0]))
            self.pattern_list[0].set_nn_position(unsorted_x[0], unsorted_y[0])

            events_list = unsorted_events
            events_x = unsorted_x
            events_y = unsorted_y

            print('Finished shuffling. ' + str(len(unsorted_events)) + ' Events are left.')
            quarter, half, three_quarter = False, False, False
            for i, item in enumerate(events_list[1:]):
                I = i+1
                # print(i)
                if max(item) > 0:
                    for j, item2 in enumerate(self.pattern_list[:I]):
                        self.edm[I, j] = item2.get_sim_score(item, self.score, active_pmts,weights)
                        self.edm[j, I] = self.edm[I, j]
                    self.pattern_list.append(Pattern(I, item))
                    self.pattern_list[I].set_nn_position(events_x[I], events_y[I])

                if I / len(events_list) > .5 and not quarter:
                    print('Finished a quarter of EDM')
                    quarter = True
                elif I / len(events_list) > .75 and not half:
                    print('Finished half of the EDM')
                    half = True
                elif I / len(events_list) > .987 and not three_quarter:
                    print('Finished Three Quarters of the EDM')
                    three_quarter = True

            self.empty = False

        else:
            #  do something with appending
            print('Please dont add events more than once at this point')

    def cut_worse_5_percent(self):
        mean_score = np.mean(self.edm)
        mean_score_array = np.mean(self.edm, axis=1)
        dev_score = np.std(mean_score_array)
        del_count = 0
        for i, score in enumerate(mean_score_array.tolist()):
            if  score > mean_score + 2*dev_score: #score < mean_score - 1.5*dev_score or
                del self.pattern_list[i - del_count]
                self.edm = np.delete(self.edm, i - del_count, 0)
                self.edm = np.delete(self.edm, i - del_count, 1)
                del_count += 1
        plt.figure()
        plt.plot(mean_score_array, '*')
        plt.show()
        plt.close()
        mean_score_array = np.mean(self.edm, axis=1)
        plt.figure()
        plt.plot(mean_score_array, '*')
        plt.show()
        plt.close()

        print(np.shape(self.edm))
        print('There are ' + str(len(self.pattern_list)) + ' events left after cuts')

    def get_distribution(self):
        return self.distribution

    def get_nn_distribution(self):
        X = [item.get_nn_position()[0] for item in self.pattern_list]
        Y = [item.get_nn_position()[1] for item in self.pattern_list]

        return np.column_stack((X, Y))

    def get_nn_lists(self):
        X = [item.get_nn_position()[0] for item in self.pattern_list]
        Y = [item.get_nn_position()[1] for item in self.pattern_list]

        return X, Y

    def get_patterns(self):
        return self.pattern_list

    def save_edm(self, time=strftime("%m_%d_%H:%M:%S", gmtime())):
        self.time = str(time)
        if not os.path.exists(self.plot_path + self.time + '/'):
            os.mkdir(self.plot_path + self.time + '/')
        np.save(self.plot_path + self.time + '/' + 'EDM', self.edm)
        return self.time
    def save_distributions(self):
        np.save(self.plot_path + self.time + '/' + 'NN', self.get_nn_distribution())
        np.save(self.plot_path + self.time + '/' + 'Pattern_List', self.get_patterns())





