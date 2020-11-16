'''
Evaluate different ASlib scenarios.
'''

import os
import csv
import json
from subprocess import Popen

in_path = os.path.realpath(__file__).split('/')[:-2]
# List of the scenarios to test.
scenarios = [
  #'ASP-POTASSCO',
  #'CSP-2010',
  #'MAXSAT12-PMS',
  #'PREMARSHALLING-ASTAR-2013',
  #'PROTEUS-2014',
  #'QBF-2011',
  'SAT11-HAND',
  'SAT11-INDU',
  'SAT11-RAND',
  #'SAT12-ALL',
  #'SAT12-HAND',
  #'SAT12-INDU',
  #'SAT12-RAND',
]  

for scenario in scenarios:
  print ('Evaluating scenario',scenario)
  src_path = '/'.join(in_path) + '/src/'
  path = '/'.join(in_path) + '/data/aslib_1.0.1/' + scenario
  
  print ('Extracting runtimes')
  reader = csv.reader(open(path + '/algorithm_runs.arff'), delimiter = ',')
  runtimes = {}
  for row in reader:
    if row and row[0].strip().upper() == '@DATA':
      # Iterates until preamble ends.
      break
  for row in reader:
    inst = row[0]
    solv = row[2]
    time = float(row[3])
    info = row[4]
    if inst not in runtimes.keys():
      runtimes[inst] = {}
    runtimes[inst][solv] = [info, time]
  
  print ('Splitting scenario',scenario)
  cmd = 'python ' + src_path + 'split_scenario.py ' + path
  proc = Popen(cmd.split())
  proc.communicate()
  fsi = 0.0
  fsi_vbs = 0.0
  par10 = 0.0
  par10_vbs = 0.0
  n = 0
  m = 0
  p = 0
  for subdir, dirs, files in os.walk(path + '/cv_' + scenario):
    if 'train_' in subdir:
      
      print ('Training',subdir)
      options = ' --discard --feat-timeout +inf '
      cmd = 'python ' + src_path + 'train_scenario.py ' + options + subdir
      proc = Popen(cmd.split())
      proc.communicate()
      test_dir = subdir.replace('train_', 'test_')
      kb_name = subdir.split('/')[-1]
      pred_file = test_dir + '/predictions.csv'
      
      print ('Pre-processing',test_dir)
      options = [
	'--kb-path', subdir + '/kb_' + kb_name,
	'-E', 'weka.attributeSelection.InfoGainAttributeEval',
	#'-E', 'weka.attributeSelection.GainRatioAttributeEval',
	#'-E', 'weka.attributeSelection.SymmetricalUncertAttributeEval',
	#'-E', 'weka.attributeSelection.ReliefFAttributeEval',
	'-S', 'weka.attributeSelection.Ranker -N 5', 
	'--static-schedule', 
	'--filter-portfolio'
      ]
      cmd = ['python', src_path + 'pre_process.py'] + options + subdir.split()
      proc = Popen(cmd)
      proc.communicate()
      
      print ('Testing',test_dir)
      options = ' ' #-f container-density,group-same-mean,stacks,group-same-stdev,tiers '
      #
      # InfoGain Selected Features (5 features).
      #
      # ASP: Running_Avg_LBD-4,Learnt_from_Loop-1,Frac_Learnt_from_Loop-1,Literals_in_Conflict_Nogoods-1,Literals_in_Loop_Nogoods-1
      # CSP: stats_Local_Variance,stats_tightness_75,normalised_width_of_graph,normalised_median_degree,stats_cts_per_var_mean
      # MAX-SAT: horn,vcg_var_spread,vcg_var_min,vcg_var_max,vcg_cls_mean
      # PREMARSHALLING: container-density,group-same-mean,stacks,group-same-stdev,tiers
      # PROTEUS: csp_perten_avg_predshape,csp_perten_avg_predsize,csp_sqrt_max_domsize,csp_sqrt_avg_domsize,directorder_reducedVars
      # QBF: FORALL_POS_LITS_PER_CLAUSE,EXIST_VARS_PER_SET,LITN_LIT,OCCP_OCCN,NEG_HORN_CLAUSE
      # SAT11-HAND: BINARYp,horn_clauses_fraction,SP_bias_q25,VCG_CLAUSE_coeff_variation,lobjois_mean_depth_over_vars
      # SAT11-INDU: saps_BestAvgImprovement_Mean,VG_min,VG_coeff_variation,VG_max,CG_coeff_variation
      # SAT11-RAND: VCG_CLAUSE_min,saps_FirstLocalMinStep_Q10,gsat_BestSolution_Mean,cl_size_mean,nclauses
      # SAT12-ALL: SP_unconstraint_q25,vars_clauses_ratio,SP_unconstraint_mean,SP_unconstraint_q75,POSNEG_RATIO_CLAUSE_entropy
      # SAT12-HAND: reducedClauses,SP_bias_coeff_variation,horn_clauses_fraction,SP_unconstraint_max,POSNEG_RATIO_CLAUSE_min
      # SAT12-INDU: POSNEG_RATIO_VAR_entropy,VCG_VAR_coeff_variation,VCG_VAR_entropy,reducedVars,POSNEG_RATIO_VAR_stdev
      # SAT12-RAND: VCG_VAR_mean,VCG_CLAUSE_mean,saps_BestSolution_Mean,VCG_CLAUSE_min,VCG_CLAUSE_max
      
      cmd = 'python ' + src_path + 'test_scenario.py ' + options + ' -o ' + pred_file \
	  + ' --print-static -K ' + subdir + '/kb_' + kb_name + ' ' + test_dir
      proc = Popen(cmd.split())
      proc.communicate()
      
      if os.path.exists(path + '/feature_costs.arff'):
	print ('Extracting feature costs')
	args_file = subdir + '/kb_' + kb_name + '/kb_' + kb_name + '.args'
	with open(args_file) as infile:
	  args = json.load(infile)
	feature_steps = args['feature_steps']
	feature_cost = {}
	reader = csv.reader(open(path + '/feature_costs.arff'), delimiter = ',')
	for row in reader:
	  steps = set([])
	  i = 2
	  if row and '@ATTRIBUTE' in row[0] \
	  and 'instance_id' not in row[0] and 'repetition' not in row[0]:
	    if row[0].strip().split(' ')[1] in feature_steps:
	      steps.add(i)
	    i += 1
	  elif row and row[0].strip().upper() == '@DATA':
	    # Iterates until preamble ends.
	    break
	for row in reader:
	  feature_cost[row[0]] = sum(float(x) for x in row[2:] if x != '?')
	  feature_cost[row[0]] = 0
	  for i in steps:
	    if row[i] != '?':
	      feature_cost[row[0]] += float(row[i])
      
      print ('Computing fold statistics')
      reader = csv.reader(open(pred_file), delimiter = ',')
      old_inst = ''
      par = True
      args_file = subdir + '/kb_' + kb_name + '/kb_' + kb_name + '.args'
      with open(args_file) as infile:
        timeout = json.load(infile)['timeout']
      first = True
      for row in reader:
	if first:
	  first = False
	  continue
        inst = row[0]
        if inst == old_inst:
          if par:
            continue
        else:
	  if not par:
	    par10 += timeout * 10
	    par = True
	    p += 1
	  n += 1
	  if os.path.exists(path + '/feature_costs.arff'):
            time = feature_cost[inst]
          else:
            time = 0.0
          times = [x[1] for x in runtimes[inst].values() if x[0] == 'ok']
	  if times:
	    m += 1
	    fsi_vbs += 1
	    par10_vbs += min(times)
	  else:
	    par10_vbs += 10 * timeout
        old_inst = inst
        solver = row[2]
        solver_time = float(row[3])
        if  runtimes[inst][solver][0] == 'ok' \
	and runtimes[inst][solver][1] <= solver_time:
	  par = True
	  if time + runtimes[inst][solver][1] >= timeout:
	    par10 += 10 * timeout
	    p += 1
	  else:
	    fsi += 1
	    par10 += time + runtimes[inst][solver][1]
        elif time + min([solver_time, runtimes[inst][solver][1]]) < timeout:
	  time += min([solver_time, runtimes[inst][solver][1]])
          par = False
        else:
	  par10 += 10 * timeout
	  par = True
	  p += 1
	  
      if not par:
        par10 += timeout * 10
        par = True
        p += 1
        
  assert p + fsi == n
  print ('\n===========================================')
  print('Scenario:', scenario)
  print ('No. of instances:',n,'(',m,'solvable )')
  print('FSI SUNNY:', fsi / n)
  print('FSI VBS:', fsi_vbs / n)
  print('PAR 10 SUNNY:', par10 / n)
  print('PAR 10 VBS:', par10_vbs / n)
  print('===========================================\n')

# Results with --discard, --static-schedule, -f f1,...,f5
#		PAR10	FSI
#ASP 		600.0	0.905
#CSP 		6606.0	0.870
#MAXSAT 	3420.0	0.840
#PREMARSH 	1655.7	0.964
#PROTEUS 	5146.0	0.859
#QBF 		8980.8	0.756
#SAT11-HAND 	18241.4	0.642
#SAT11-INDU 	12765.5	0.753
#SAT11-RAND 	9921.8	0.805
#SAT12-ALL  	1458.2	0.888
#SAT12-HAND 	4633.1	0.622
#SAT12-INDU 	2854.8	0.770
#SAT12-RAND 	3291.9	0.729

