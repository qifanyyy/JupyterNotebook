import time
from typing import Callable, Union
import matplotlib.pyplot as plt
import pandas as pd
from selection_algorithms.sorting_reduction import quick_sort_reduction
from utils.inputs import InputList, InputListIndex
from scipy.signal import lfilter


class AlgoAnalysisList:
    def __init__(self, algo: Callable):
        """
        For a given problem in algorithmic that takes a standardized input (for instance: a list)
        this class will give information of the running time of the algorithm. It will also
        give an approximate of the complexity of the algorithm
        Parameters
        ----------
        algo: The algorithm as a function
        """
        self.algo = algo
        self.algo_name = algo.__name__

    def __repr__(self):
        return f'AlgoAnalysis(name={self.algo_name})'

    def calculate_time_single_list(self, input_l: list) -> float:
        """
        Calculate the computation time of an algo on a specific list
        Parameters
        ----------
        input_l (list): Input list of the algorithm

        Returns
        -------
        float: computation time in ms
        """
        start_time = time.time()
        _ = self.algo(input_l)
        end_time = time.time()

        return end_time - start_time

    def calculate_time_multiple_lists(self,
                                      range_length: int,
                                      harmonization: bool = False,
                                      f_harmonization: Union[int, list] = 10,
                                      worst_case: bool = True,
                                      **kwargs) -> \
            Union[pd.Series, pd.DataFrame]:
        """
        Generate random input lists of variate length within the range size
        and perform the time computation
        Parameters
        ----------
        range_length: range of length of the input lists to test: from 1 to range_length
        harmonization: reduce noise of the curve
        f_harmonization: harmonization factor, an integer or a list the bigger n the smoother the curve will be
        worst_case: in the context of list sorting, all the input lists will be ones of worse case (reversed)
        kwargs: the other arguments of the input lists

        Returns
        -------
        List[float]
        """
        res_time_l = [self.calculate_time_single_list(input_l=InputList(l_length=l_length,
                                                                        worst_case=worst_case,
                                                                        **kwargs))
                      for l_length in range(1, range_length + 1)]
        dict_res_time = {'raw': res_time_l}

        if harmonization:
            if type(f_harmonization) == int:
                f_harmonization = [f_harmonization]
            # It is a list
            for n in f_harmonization:
                b = [1.0 / n] * n
                a = 1
                res_time_filtered = lfilter(b, a, res_time_l)
                dict_res_time[f'harmonization (n={n})'] = res_time_filtered

        res_time = pd.DataFrame(dict_res_time)
        res_time.index += 1
        return res_time


class AlgoAnalysisListIndex:
    def __init__(self, algo: Callable):
        """
        For a given problem in algorithmic that takes a standardized input a list and an index of this list
        this class will give information of the running time of the algorithm. It will also
        give an approximate of the complexity of the algorithm
        Parameters
        ----------
        algo: The algorithm as a function
        """
        self.algo = algo
        self.algo_name = algo.__name__

    def calculate_time_single_list(self, *args) -> float:
        """
        Calculate the computation time of an algo on a specific list
        Parameters
        ----------
        *args: Input arguments of the list index algorithm (i.e. a list first and then an index of this list

        Returns
        -------
        float: computation time in ms
        """
        start_time = time.time()
        _ = self.algo(*args)
        end_time = time.time()

        return end_time - start_time

    def calculate_time_multiple_lists(self,
                                      range_length: int,
                                      harmonization: bool = False,
                                      f_harmonization: Union[int, list] = 10,
                                      worst_case: bool = True,
                                      **kwargs) -> \
            Union[pd.Series, pd.DataFrame]:
        """
        Generate random input lists of variate length within the range size
        and perform the time computation
        Parameters
        ----------
        range_length: range of length of the input lists to test: from 1 to range_length
        harmonization: reduce noise of the curve
        f_harmonization: harmonization factor, an integer or a list the bigger n the smoother the curve will be
        worst_case: in the context of list sorting, all the input lists will be ones of worse case (reversed)
        kwargs: the other arguments of the input lists

        Returns
        -------
        List[float]
        """
        res_time_l = [self.calculate_time_single_list(*InputListIndex(l_length=l_length,
                                                                      worst_case=worst_case, **kwargs))
                      for l_length in range(1, range_length + 1)]
        dict_res_time = {'raw': res_time_l}

        if harmonization:
            if type(f_harmonization) == int:
                f_harmonization = [f_harmonization]
            # It is a list
            for n in f_harmonization:
                b = [1.0 / n] * n
                a = 1
                res_time_filtered = lfilter(b, a, res_time_l)
                dict_res_time[f'harmonization (n={n})'] = res_time_filtered

        res_time = pd.DataFrame(dict_res_time)
        res_time.index += 1
        return res_time


if __name__ == '__main__':
    algo_test = AlgoAnalysisListIndex(quick_sort_reduction)
    df = algo_test.calculate_time_multiple_lists(range_length=1000, harmonization=True, f_harmonization=[2, 20, 200])
    print(df)
    df.plot()
    plt.show()
