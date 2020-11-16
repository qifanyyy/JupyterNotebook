import numpy as np 
import pandas as pd 

# Define our core functions
def not_out_score(not_out, matches_played):
    return round((not_out / matches_played) * 100.0, 2)

def h_n_f_score(hundreds, fifties, matches_played):
    '''
    Contains hundreds and fifties
    '''
    return round((((hundreds + fifties) / matches_played) * 100.0), 2)

def s_n_f_score(sixes, fours, balls_faced):
    '''
    Sixes and Fours Score
    '''
    return round((((sixes + fours) / balls_faced) * 100.0), 2)

def pure_average_score(total_runs, matches_played):
    return round((total_runs / matches_played), 2)

def potential_score(highest_score, total_runs, matches_played):
    if highest_score == total_runs and matches_played == 1:
        return 0
    else:
        return round((((total_runs - highest_score) / total_runs) * 100.0), 2)
    
def strike_rate_score(highest_score, total_runs, strike_rate):
    if highest_score == total_runs:
        if strike_rate > 100 and strike_rate <= 150:
            strike_rate -= 20
        elif strike_rate > 150 and strike_rate < 250:
            strike_rate -= 15 
    elif highest_score - total_runs > 0 and highest_score - total_runs <= 10: 
        strike_rate = strike_rate - 0.2*strike_rate
    else:
        return strike_rate
    
    return strike_rate

# Main Score_Function
def score_function(matches_played, not_out, hundreds, fifties, sixes, fours, highest_score, total_runs, balls_faced, strike_rate):
    not_out_value = not_out_score(not_out, matches_played)
    hnf_value = h_n_f_score(hundreds, fifties, matches_played)
    snf_value = s_n_f_score(sixes, fours, balls_faced)
    pure_average_value = pure_average_score(total_runs, matches_played)
    potential_score_value = potential_score(highest_score, total_runs, matches_played)
    strike_rate_value = strike_rate_score(highest_score, total_runs, strike_rate)
    
    score = not_out_value + 2 * hnf_value + snf_value + pure_average_value + potential_score_value + strike_rate_value
    
    return round(score, 2)