from scipy import stats
import pandas as pd
import numpy as np
import os
from collections import namedtuple

system_run = namedtuple("system_run", "name map")

BASE_FOLDER="/Users/ibahadiraltun/Desktop/InformationRetrieval/DocumentSelectionAlgorithms/"
# BASE_FOLDER = "";

TREC_VERSION="robust2003"
TREC_DATA_PATH= BASE_FOLDER + "trec_dataset/"
SYSTEM_RUN_RESULTS=BASE_FOLDER + "system_run_results/" + TREC_VERSION + "/"
TREC_EVAL_PATH= BASE_FOLDER +  "trec_eval/./trec_eval"
TEST_SCORES_PATH = BASE_FOLDER + "test_scores/" + TREC_VERSION + "/"
BASEDIR_DRANK = BASE_FOLDER + 'basedir_drank/'

official_qrel_path = TREC_DATA_PATH + TREC_VERSION + "/robust03_qrels.txt"
qrel_path = BASE_FOLDER + TREC_VERSION
runs_path = TREC_DATA_PATH + TREC_VERSION + "/inputfiles/"

# const_file_path = 'judgments/'
# strategies = ['algo12', 'algo13', 'algo14', 'algo15', 'algo16', 'algo2']

strategies = ['MTF2_new']

qrels_df = pd.read_csv(official_qrel_path, names = ['qid', 'x1', 'doc', 'rel'], sep = ' ')
queries = np.unique(qrels_df['qid'])

team_list = []
off_team_results = []
for subdir, dirs, files in os.walk(runs_path):
    for file in files:
        filepath = subdir + os.sep + file
        sep = file.split('.')
        if len(sep) == 2: tmp = sep[1]
        else: tmp = sep[1] + '.' + sep[2]
        if tmp != "DS_Store":
            team_list.append(tmp)

team_list.sort()

for i in range(0, len(team_list)):
    off_team_results.append(0)

cnt = 0
for cur_team in team_list:
    os.system('{} -m map {} {}input.{} > {}{}.txt'.format(TREC_EVAL_PATH, official_qrel_path, runs_path, cur_team, SYSTEM_RUN_RESULTS, cur_team ))
    # os.system('{} -q -m map {} {}input.{} > {}{}'.format(TREC_EVAL_PATH, official_qrel_path, runs_path, cur_team, BASEDIR_DRANK, cur_team ))
    score = 0
    with open('{}{}.txt'.format(SYSTEM_RUN_RESULTS,cur_team)) as tmp_file:
        line = tmp_file.readline()
        score = float(line.split('\t')[2])
    off_team_results[cnt] = system_run(cur_team, score)
    cnt = cnt + 1

print('system results finished\n')

# judge_count = 50
# while judge_count <= 500:
#     for cur_strategy in strategies:
#         new_qrel_file = BASE_FOLDER + "new_qrels/" + TREC_VERSION + '/' + cur_strategy + "_" + str(judge_count)
#         print(judge_count, new_qrel_file)
#         with open(new_qrel_file, 'w') as f_qrel:
#             total_rel = 0
#             for qid in queries:
#                 file_path = BASE_FOLDER + "new_judgments/" + TREC_VERSION + '/' +  cur_strategy + "_judgments"
#                 df = pd.read_csv(file_path, sep = ' ',  names = ['qid', 'x1', 'doc', 'rel'])
#                 # df.columns = ['id', 'doc']
#                 # df.columns = ['qid', 'x1', 'doc', 'rel']
#                 # print(df.head(5))
#                 cur_judges = df[df['qid'] == qid]
#                 cur_judges = cur_judges.iloc[0:judge_count]
#                 for k, j in cur_judges.iterrows():
#                     cur_doc = j['doc']
#                     cur_rel = j['rel']
#                     if cur_rel > 0: total_rel = total_rel + 1
#                     line = '{} 0 {} {}\n'.format(qid, cur_doc, cur_rel)
#                     f_qrel.write(line)
#     judge_count = judge_count + 50

judge_count = 50
while judge_count <= 500:
    for cur_strategy in strategies:
        predicted_team_results = []
        for cur_team in team_list:
            new_qrel_file = BASE_FOLDER + "new_qrels/" + TREC_VERSION + '/' + cur_strategy + "_" + str(judge_count)
            os.system('{} -m map {} {}input.{} > temp'.format(TREC_EVAL_PATH, new_qrel_file, runs_path, cur_team ))
            with open('temp') as tmp_file:
                line = tmp_file.readline()
                score = float(line.split('\t')[2])
            predicted_team_results.append(system_run(cur_team, score))

        groundtruth_scores = []
        predicted_scores= []
        for i in range(0,len(team_list)):
            predicted_scores.append(predicted_team_results[i].map)
            groundtruth_scores.append(off_team_results[i].map)

        print('map tau correlation')
        tau, p_value = stats.kendalltau(groundtruth_scores, predicted_scores)
        print(cur_strategy, 'judge_count === ', judge_count, 'tau === ', tau, 'p_value === ', p_value)
        with open('{}{}_map_tau'.format(TEST_SCORES_PATH, cur_strategy), 'a') as score_file:
            score_file.write('{}\n'.format(str(tau)[0:6]))

    judge_count =  judge_count + 50





