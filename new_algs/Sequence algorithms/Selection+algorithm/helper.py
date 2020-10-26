from enum import Enum
import numpy as np
from scipy.special import lambertw


class Algorithm_Names(Enum):
    GREEDY1 = 0
    GREEDY2 = 1
    GREEDY3 = 2
    GREEDY1S = 3
    HILL1 = 4
    HILL1S = 5
    HILL2 = 6
    HILL2S = 7
    SA = 8
    SAS = 9
    CASANOVA = 10
    CASANOVAS = 11
    CPLEX = 12
    RLPS = 13


class Heuristic_Algorithm_Names(Enum):
    GREEDY1 = 0
    GREEDY2 = 1
    GREEDY3 = 2
    GREEDY1S = 3
    HILL1 = 4
    HILL1S = 5
    HILL2 = 6
    HILL2S = 7
    SA = 8
    SAS = 9
    CASANOVA = 10
    CASANOVAS = 11


class Stochastic_Algorithm_Names(Enum):
    HILL2 = 6
    HILL2S = 7
    SA = 8
    SAS = 9
    CASANOVA = 10
    CASANOVAS = 11


class Feature_Names(Enum):
    ### group 1: instance - price related
    average_bid_price_mean                                     = 0
    average_bid_price_stddev                                   = 1
    average_bid_price_skewness                                 = 2
    average_bid_price_kurtosis                                 = 3
    average_ask_price_mean                                     = 4
    average_ask_price_stddev                                   = 5
    average_ask_price_skewness                                 = 6
    average_ask_price_kurtosis                                 = 7
    average_bid_price_max                                      = 8
    average_ask_price_min                                      = 9
    mid_price                                                  = 10
    bid_ask_spread                                             = 11
    bid_ask_spread_over_mid_price                              = 12
    ### group 2: instance - quantity related
    bid_bundle_size_mean                                       = 13
    bid_bundle_size_stddev                                     = 14
    bid_bundle_size_skewness                                   = 15
    bid_bundle_size_kurtosis                                   = 16
    ask_bundle_size_mean                                       = 17
    ask_bundle_size_stddev                                     = 18
    ask_bundle_size_skewness                                   = 19
    ask_bundle_size_kurtosis                                   = 20
    ### group 3: instance - quantity per resource related (measure of heterogeneity)
    total_demand_per_resource_mean                             = 21
    total_demand_per_resource_stddev                           = 22
    total_demand_per_resource_skewness                         = 23
    total_demand_per_resource_kurtosis                         = 24
    average_demand_per_resource_mean                           = 25
    average_demand_per_resource_stddev                         = 26
    average_demand_per_resource_skewness                       = 27
    average_demand_per_resource_kurtosis                       = 28
    minimum_demand_per_resource_mean                           = 29
    minimum_demand_per_resource_stddev                         = 30
    minimum_demand_per_resource_skewness                       = 31
    minimum_demand_per_resource_kurtosis                       = 32
    maximum_demand_per_resource_mean                           = 33
    maximum_demand_per_resource_stddev                         = 34
    maximum_demand_per_resource_skewness                       = 35
    maximum_demand_per_resource_kurtosis                       = 36
    # --> supply side
    total_supply_per_resource_mean                             = 37
    total_supply_per_resource_stddev                           = 38
    total_supply_per_resource_skewness                         = 39
    total_supply_per_resource_kurtosis                         = 40
    average_supply_per_resource_mean                           = 41
    average_supply_per_resource_stddev                         = 42
    average_supply_per_resource_skewness                       = 43
    average_supply_per_resource_kurtosis                       = 44
    minimum_supply_per_resource_mean                           = 45
    minimum_supply_per_resource_stddev                         = 46
    minimum_supply_per_resource_skewness                       = 47
    minimum_supply_per_resource_kurtosis                       = 48
    maximum_supply_per_resource_mean                           = 49
    maximum_supply_per_resource_stddev                         = 50
    maximum_supply_per_resource_skewness                       = 51
    maximum_supply_per_resource_kurtosis                       = 52
    ### group 4: instance - demand-supply balance related
    surplus_value_per_surplus_unit                             = 53
    demand_supply_ratio_value                                  = 54
    demand_supply_ratio_quantity                               = 55
    demand_supply_ratio_total_quantity_per_resource_mean       = 56
    demand_supply_ratio_total_quantity_per_resource_stddev     = 57
    demand_supply_ratio_total_quantity_per_resource_skewness   = 58
    demand_supply_ratio_total_quantity_per_resource_kurtosis   = 59
    demand_supply_ratio_mean_quantity_per_resource_mean        = 60
    demand_supply_ratio_mean_quantity_per_resource_stddev      = 61
    demand_supply_ratio_mean_quantity_per_resource_skewness    = 62
    demand_supply_ratio_mean_quantity_per_resource_kurtosis    = 63
    surplus_quantity                                           = 64
    surplus_total_quantity_per_resource_mean                   = 65
    surplus_total_quantity_per_resource_stddev                 = 66
    surplus_total_quantity_per_resource_skewness               = 67
    surplus_total_quantity_per_resource_kurtosis               = 68
    quantity_spread_per_resource_mean                          = 69
    quantity_spread_per_resource_stddev                        = 70
    quantity_spread_per_resource_skewness                      = 71
    quantity_spread_per_resource_kurtosis                      = 72
    ratio_average_price_bid_to_ask                             = 73
    ratio_bundle_size_bid_to_ask                               = 74
    ### group 4: instance - critical values related
    #critical_density_bids   = 75
    #critical_density_asks   = 76
    #critical_price_bids     = 77
    #critical_price_asks     = 78


### functions used for fitting welfare and time to some curves

def func_poly1(x, a):#, b):
    return a * x# + b

def func_poly2(x, a):#, b):
    return a * x * x# + b

def func_poly3(x, a):#, b):
    return a * x * x * x# + b

def func_poly321(x, a, b, c, d):
    return a * x * x * x + b * x * x + c * x + d

def func_sqrt(x, a):#, b):
    return a * np.sqrt(x)# + b

def func_nlogn(x, a):#, b):
    return a * x * np.log(x)# + b

def func_nlogn_n(x, a, b):
    return a * x * np.log(x) + b * x

def func_logn(x, a):#, b):
    return a * np.log(x)# + b

def func_n2logn(x, a):#, b):
    return a * x * x * np.log(x)# + b

def func_n3logn(x, a):#, b):
    return a * x * x * x * np.log(x)# + b

def func_npow(x, a, b):
    return a * (x ** b)


#### functions to extrapolate time and welfare

def o_n2(time, ratio):
    return time / (ratio ** 2)

def o_n3(time, ratio):
    return time / (ratio ** 3)

def o_nlogn(time, ratio):
    # if f(n)=nlogn=a measured => time on full instance is f(n/r)
    # n=f^-1(f(n))=f^-1(a) => f(n/r)=f(f^-1(a)/r)
    # f^-1(y) = y / lambertw(y)
    time_inv = time / lambertw(time).real
    return time_inv / ratio * np.log(time_inv / ratio)

def o_nlogn_n(time, ratio):
    # inverse of x log x + x: x / lambertw(e x)
    time_inv = time / lambertw(time * np.exp(1)).real
    return time_inv / ratio * np.log(time_inv / ratio) + time_inv / ratio

def o_n2logn(time, ratio):
    time_inv = (2 * time / lambertw(2 * time).real) ** (1./2)
    return (time_inv / ratio) ** 2 * np.log(time_inv / ratio)


def stretch_time(row):
    """extrapolates the time value of the full instance from the sample value

    :param row: one row from all stats for running the algorithms on all instances
    :returns: dataframe row where time column was stretched
    """
    if row.algorithm in ['GREEDY1', 'GREEDY2', 'GREEDY3', 'GREEDY1S', 'SA', 'SAS']:
       # extrapolate time value for algorithms with O(nlogn) time complexity
        new_time = o_nlogn(row.time, row.ratio)
    elif row.algorithm in ['HILL1', 'HILL1S']: #, 'HILL2', 'HILL2S']:
        # extrapolate time value for algorithms with O(n^2logn) time complexity
        new_time = o_n2logn(row.time, row.ratio)
    else:
        # CASANOVA, CASANOVAS, HILL2, HILL2S
        # extrapolate time value for algorithms with O(n^2) time complexity
        new_time = o_n2(row.time, row.ratio)
            
    return new_time

def stretch_welfare(row):
    """extrapolates the welfare value of the full instance from the sample value

    :param row: one row from all stats for running the algorithms on all instances
    :returns: dataframe row where welfare column was stretched
    """
    if row.algorithm in ['HILL1S']:
        new_welfare = row.welfare / (row.ratio ** 0.93)
    elif row.algorithm in ['GREEDY3']:
        new_welfare = row.welfare / (row.ratio ** 0.87)
    elif row.algorithm in ['GREEDY1', 'GREEDY2', 'HILL1']:
        new_welfare = row.welfare / (row.ratio ** 0.85)
    elif row.algorithm in ['SA', 'SAS']:
        new_welfare = row.welfare / (row.ratio ** 0.96)
    elif row.algorithm in ['GREEDY1S']:
        new_welfare = row.welfare / (row.ratio ** 0.97)
    elif row.algorithm in ['HILL2']:
        new_welfare = row.welfare / (row.ratio ** 1.03)
    elif row.algorithm in ['HILL2S']:
        new_welfare = row.welfare / (row.ratio ** 1.02)
    else:
        # extrapolate welfare value for algorithms with O(n) welfare complexity
        new_welfare = row.welfare / row.ratio
    return new_welfare
