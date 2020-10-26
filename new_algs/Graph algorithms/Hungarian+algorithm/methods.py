import data_generator
import argparse
import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment
import networkx as nx
import matplotlib.pyplot as plt
import time
import progressbar
import os
from pathlib import Path

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def run_stable_marriage(data):
    terminated = False
    applied_to = dict()
    unmatched = set()
    for candidate in data.candidates:
        applied_to[candidate] = set()
        unmatched.add(candidate)
    qualified = dict()
    for candidate, qualification in data.qualification.items():
        for course, score in qualification.items():
            if score == 1:
                courses = qualified.get(candidate, set())
                courses.add(course)
                qualified[candidate] = courses
            else:
                courses = qualified.get(candidate, set())
                qualified[candidate] = courses
    course_list = list(data.courses)
    current_match = dict()
    for course in data.courses:
        current_match[course] = list()
    while not terminated:
        curr_purpose = dict()
        for candidate in unmatched:
            courses_sorted = sorted(course_list, key = lambda x: data.candidate_preference[candidate][x], reverse = True)
            for course in courses_sorted:
                if course not in applied_to[candidate] and course in qualified[candidate]:
                    applied_to[candidate].add(course)
                    curr_purpose[candidate] = course
                    break
        for candidate, course in curr_purpose.items():
            current_match[course].append(candidate)
        new_match = dict()
        curr_matched_candidates = set()
        for course, candidates in current_match.items():
            new_candidates = sorted(candidates, key = lambda x: data.course_preference[course][x], reverse = True)
            if len(new_candidates) > data.course_capacity[course]:
                new_candidates = new_candidates[0:data.course_capacity[course]]
            new_match[course] = new_candidates
            for c in new_candidates:
                curr_matched_candidates.add(c)
        current_match = new_match.copy()
        unmatched = set()
        for candidate in data.candidates:
            if candidate not in curr_matched_candidates:
                unmatched.add(candidate)
        terminated = True
        for candidate in unmatched:
            if len(applied_to[candidate]) < len(qualified[candidate]):
                terminated = False
    return current_match

def hungarian(data):
    rows = list(data.candidates)
    columns = []
    for course in data.courses:
        for i in range(data.course_capacity[course]):
            columns.append(course + '_' + str(i))
    counter = 0
    while len(columns) < len(rows):
        columns.append('dummy' + str(counter))
        counter += 1
    cost_mx = np.zeros((len(rows), len(columns)))
    not_qualify_penalty = 500000
    dummy_pref = 10
    for i in range(len(rows)):
        for j in range(len(columns)):
            if 'dummy' in columns[j]:
                cost_mx[i][j] = dummy_pref
            else:
                course = columns[j].split('_')[0]
                if data.qualification[rows[i]][course] == 0:
                    cost_mx[i][j] = not_qualify_penalty
                else:
                    cost_mx[i][j] = 2 - data.candidate_preference[rows[i]][course] - data.course_preference[course][rows[i]]
    row_ind, col_ind = linear_sum_assignment(cost_mx)
    total_cost = cost_mx[row_ind, col_ind].sum()
    if total_cost >= not_qualify_penalty:
        print('Error: data is generated badly, try again :)')
        exit(0)
    matching = dict()
    for course in data.courses:
        matching[course] = list()
    for i in range(len(rows)):
        if 'dummy' not in columns[col_ind[i]]:
            candidate = rows[row_ind[i]]
            course = columns[col_ind[i]].split('_')[0]
            matching[course].append(candidate)
    return matching
    
def maximum_matching(data):
    candidates = data.candidates
    courses = [course+'_'+str(i) for course in data.courses\
                for i in range(data.course_capacity[course])]
    g = nx.Graph()
    for candidate in candidates:
        for course in courses:
            if data.qualification[candidate][course.split('_')[0]] == 1:
                sum_of_preference = data.candidate_preference[candidate][course.split('_')[0]] +\
                                    data.course_preference[course.split('_')[0]][candidate]
                g.add_edge(candidate, course, weight=sum_of_preference)
    matching = nx.max_weight_matching(g)
    output = dict()
    for assignment in matching:
        assignment = sorted(assignment)
        candidate, course = assignment[0], assignment[1].split('_')[0]
        try:
            output[course].append(candidate)
        except(KeyError):
            output[course] = [candidate]
    return output

def write_to_file(data, matching, output, score, course_satisfaction, candidate_satisfaction):
    output_file = open(output, 'w')

    output_file.write('candidates preference to courses:\n')
    column_list = list(data.courses)
    column_list.insert(0, 'candidate')
    candidate_preference = pd.DataFrame(columns = column_list)
    for candidate, preference in data.candidate_preference.items():
        new_data = preference.copy()
        for course, qualification_score in data.qualification[candidate].items():
            if qualification_score == 0:
                new_data[course] = 'Unqualified'
        new_data['candidate'] = candidate
        candidate_preference = candidate_preference.append(new_data, ignore_index = True)
    output_file.write(candidate_preference.to_string(index=False) + '\n')

    output_file.write('\ncourses capacity and preference to candidates:\n')
    column_list = list(data.candidates)
    column_list.insert(0, 'course')
    column_list.insert(1, 'capacity')
    course_preference = pd.DataFrame(columns = column_list)
    for course, preference in data.course_preference.items():
        new_data = preference.copy()
        for candidate in new_data.keys():
            if data.qualification[candidate][course] == 0:
                new_data[candidate] = 'Unqualified'
        new_data['course'] = course
        new_data['capacity'] = data.course_capacity[course]
        course_preference = course_preference.append(new_data, ignore_index = True)
    output_file.write(course_preference.to_string(index=False) + '\n')
    output_file.write('\n')

    output_file.write('Final TA assignment:\n')
    for course, TAs in matching.items():
        new_data = dict()
        people = ''
        if len(TAs) == 1:
            people = TAs[0]
        else:
            people = TAs[0]
            for i in range(1, len(TAs)):
                people += ', ' + TAs[i]
        new_data['assigned candidates'] = people
        output_file.write(course + ':,' + people + '\n')
    
    output_file.write('\n')
    output_file.write('Score for assignment: {}\n'.format(round(score,2)))
    output_file.write('Percentage of courses get top 3 choice of candidates: {}\n'.format(round(course_satisfaction,2)))
    output_file.write('Percentage of candidates get top 3 choice of courses: {}\n'.format(round(candidate_satisfaction,2)))

def evaluate_matching(data, matching):
    score = 0
    total_matching = 0
    top_3_candidate = 0
    top_3_course = 0
    for course, candidates in matching.items():
        total_matching += len(candidates)
        all_candidate_scores = sorted(list(set(data.course_preference[course].values())), reverse=True)
        for candidate in candidates:
            score += data.candidate_preference[candidate][course] + data.course_preference[course][candidate]
            all_course_scores = sorted(list(set(data.candidate_preference[candidate].values())), reverse=True)
            if all_candidate_scores.index(data.course_preference[course][candidate]) < 3:
                top_3_course += 1
            if all_course_scores.index(data.candidate_preference[candidate][course]) < 3:
                top_3_candidate += 1
    return score, top_3_course * 100.0/total_matching, top_3_candidate * 100.0/total_matching

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_candidate', type=int)
    parser.add_argument('--num_course', type=int)
    parser.add_argument('--if_figure', type=bool, default=False)
    parser.add_argument('--save_to', type=str, default='result/trail')
    parser.add_argument('--num_simulations', type=int, default=100)
    args = parser.parse_args()
    if not args.if_figure:
        data = data_generator.generate(args.num_candidate, args.num_course)
        output_file_name = args.save_to.split('.')[0]
        matching_sm = run_stable_marriage(data)
        score, course_satisfaction, candidate_satisfaction = evaluate_matching(data, matching_sm)
        write_to_file(data, matching_sm, output_file_name+'_sm.csv', score, course_satisfaction, candidate_satisfaction)
        matching_hg = hungarian(data)
        score, course_satisfaction, candidate_satisfaction = evaluate_matching(data, matching_hg)
        write_to_file(data, matching_hg, output_file_name+'_hg.csv', score, course_satisfaction, candidate_satisfaction)
        matching_mm = maximum_matching(data)
        score, course_satisfaction, candidate_satisfaction = evaluate_matching(data, matching_mm)
        write_to_file(data, matching_mm, output_file_name+'_mm.csv', score, course_satisfaction, candidate_satisfaction)
    else:
        n = args.num_simulations
        dir = str(args.num_candidate) + 'candidates_' + str(args.num_course) + 'courses_' + str(n) + 'simulations'
        while n < 100:
            n = int(input('Try a number > 100: ') or '100')
        if not Path('./figures/'+dir).exists():
            Path('./figures/'+dir).mkdir(parents=True)
        score = np.zeros([n, 3])
        prof_rate = np.zeros([n, 3])
        can_rate = np.zeros([n, 3])
        for i in progressbar.progressbar(range(n)):
            data = data_generator.generate(args.num_candidate, args.num_course)
            sm = run_stable_marriage(data)
            hg = hungarian(data)
            mm = maximum_matching(data)
            score[i, 0], prof_rate[i, 0], can_rate[i, 0] = evaluate_matching(data, sm)
            score[i, 1], prof_rate[i, 1], can_rate[i, 1] = evaluate_matching(data, hg)
            score[i, 2], prof_rate[i, 2], can_rate[i, 2] = evaluate_matching(data, mm)
        plt.figure(1)
        plt.hist(score[:,0], bins=10, label='Stable Marriage', alpha=0.6, color='c')
        plt.axvline(sum(score[:,0])/n, linestyle='--', \
                    label='Mean of Stable Marraige={0:.{1}f}'.format(sum(score[:,0])/n,2), color='c')
        plt.hist(score[:,1], bins=10, label='Hungarian', alpha=0.6, color='limegreen')
        plt.axvline(sum(score[:,1])/n, linestyle='--', \
                    label='Mean of Hungarian={0:.{1}f}'.format(sum(score[:,1])/n,2), color='limegreen')
        plt.hist(score[:,2], bins=10, label='Maximum Matching', alpha=0.6, color='orange')
        plt.axvline(sum(score[:,2])/n, linestyle='--', \
                    label='Mean of Maximum Matching={0:.{1}f}'.format(sum(score[:,2])/n,2), color='orange')
        plt.title('Score, Monte Carlo n ={}'.format(n))
        plt.legend()
        plt.savefig(Path('./figures/'+dir+'/scores.png'))
        plt.figure(2)
        plt.hist(prof_rate[:,0], bins=10, label='Stable Marriage', alpha=0.6, color='c')
        plt.axvline(sum(prof_rate[:,0])/n, linestyle='--', \
                    label='Mean of Stable Marraige={0:.{1}f}'.format(sum(prof_rate[:,0])/n,2), color='c')
        plt.hist(prof_rate[:,1], bins=10, label='Hungarian', alpha=0.6, color='limegreen')
        plt.axvline(sum(prof_rate[:,1])/n, linestyle='--', \
                    label='Mean of Hungarian={0:.{1}f}'.format(sum(prof_rate[:,1])/n,2), color='limegreen')
        plt.hist(prof_rate[:,2], bins=10, label='Maximum Matching', alpha=0.6, color='orange')
        plt.axvline(sum(prof_rate[:,2])/n, linestyle='--', \
                    label='Mean of Maximum Matching={0:.{1}f}'.format(sum(prof_rate[:,2])/n,2), color='orange')
        plt.title('Professors satisfaction rate, Monte Carlo n ={}'.format(n))
        plt.legend()
        plt.savefig(Path('./figures/'+dir+'/prof_rate.png'))
        plt.figure(3)
        plt.hist(can_rate[:,0], bins=10, label='Stable Marriage', alpha=0.6, color='c')
        plt.axvline(sum(can_rate[:,0])/n, linestyle='--', \
                    label='Mean of Stable Marraige={0:.{1}f}'.format(sum(can_rate[:,0])/n,2), color='c')
        plt.hist(can_rate[:,1], bins=10, label='Hungarian', alpha=0.6, color='limegreen')
        plt.axvline(sum(can_rate[:,1])/n, linestyle='--', \
                    label='Mean of Hungarian={0:.{1}f}'.format(sum(can_rate[:,1])/n,2), color='limegreen')
        plt.hist(can_rate[:,2], bins=10, label='Maximum Matching', alpha=0.6, color='orange')
        plt.axvline(sum(can_rate[:,2])/n, linestyle='--',\
                    label='Mean of Maximum Matching={0:.{1}f}'.format(sum(can_rate[:,2])/n,2), color='orange')
        plt.title('Candidates satisfaction rate, Monte Carlo n ={}'.format(n))
        plt.legend()
        plt.savefig(Path('./figures/'+dir+'/can_rate.png'))



if __name__ == '__main__':
    main()
