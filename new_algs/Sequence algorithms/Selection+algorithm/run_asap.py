import algsel
import argparse
import aslib_scenario
import json
import logging
import pandas as pd
import os
import subprocess
import tempfile


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--aslib_scenario_dir', type=str, default=os.path.expanduser('~/projects/aslib_data'))
    parser.add_argument('--scenario_name', type=str, default=None)
    parser.add_argument('--scenario_idx', type=int, default=None)
    parser.add_argument('--n_repetitions', type=int, default=1)
    parser.add_argument('--n_folds', type=int, default=10)
    parser.add_argument('--n_seeds', type=int, default=3)
    parser.add_argument('--asap_venv', type=str, default=os.path.expanduser('~/anaconda3/envs/asap-v2-stable/bin/python'))
    parser.add_argument('--asap_script', type=str, default=os.path.expanduser('~/projects/asap-v2-stable/src/run_asap.py'))
    parser.add_argument('--output_dir', type=str, default=os.path.expanduser('~/experiments/as_insights/ASAPv2'))

    return parser.parse_args()


def run(args):
    command = '%s %s v2' % (args.asap_venv, args.asap_script)
    if args.scenario_name is not None and args.scenario_idx is not None:
        raise ValueError('Please only set scenario name or scenario index (not both)')

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    os.makedirs(args.output_dir, exist_ok=True)
    for scenario_idx, scenario_name in enumerate(os.listdir(args.aslib_scenario_dir)):
        if args.scenario_name is not None and scenario_name != args.scenario_name:
            continue
        if args.scenario_idx is not None and scenario_idx != args.scenario_idx:
            continue
        
        scenario_results_file = os.path.join(args.output_dir, '%s_r%d_f%d_s%d.csv' % (scenario_name,
                                                                                      args.n_repetitions,
                                                                                      args.n_folds,
                                                                                      args.n_seeds))
        if os.path.isfile(scenario_results_file):
            logging.info('Skipping scenario %s, results already exist')
            continue
        results_frame = pd.DataFrame()
        for repetition in range(1, args.n_repetitions + 1):
            for fold in range(1, args.n_folds + 1):
                for seed in range(1, args.n_seeds + 1):
                    logging.info('Running scenario=%s repetition=%d fold=%d seed=%d' % (scenario_name, repetition, fold, seed))

                    # drop the fold files in the proper directory
                    temp_folder = tempfile.mkdtemp('_asap_%s' % scenario_name)
                    os.makedirs(os.path.join(temp_folder, 'output'), exist_ok=True)  # expected by ASAP
                    temp_data_folder = os.path.join(temp_folder, 'data', 'oasc_scenarios')
                    scenario_folder = os.path.join(args.aslib_scenario_dir, scenario_name)
                    algsel.scenario.save_scenario_in_oasc_format(scenario_folder, scenario_name, temp_data_folder, repetition, fold)

                    # prepare and execute cli command
                    total_command = '%s %s %d' % (command, temp_folder, seed)
                    logging.info('Command: %s' % total_command)
                    p = subprocess.Popen(total_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=r'/tmp')
                    retval = p.wait()
                    if retval != 0:
                        error_lines = [line.decode('utf-8') for line in p.stdout.readlines()]
                        logging.error("".join(error_lines))
                        raise ValueError('Error while running ASAPv2')
                    system_result_file_path = os.path.join(temp_folder, 'output', 'asap_v2_oasc', 'reg_weight_5e-03', '%s-test.json' % scenario_name)
                    with open(system_result_file_path, 'r') as fp:
                        schedules = json.load(fp)

                    # read scenarios
                    test_scenario = aslib_scenario.aslib_scenario.ASlibScenario()
                    test_scenario.read_scenario(dn=os.path.join(temp_data_folder, 'test', scenario_name))
                    train_scenario = aslib_scenario.aslib_scenario.ASlibScenario()
                    train_scenario.read_scenario(dn=os.path.join(temp_data_folder, 'train', scenario_name))

                    # validate
                    validator = algsel.scoring.Validator()

                    if test_scenario.performance_type[0] == "runtime":
                        stats = validator.validate_runtime(schedules=schedules, test_scenario=test_scenario,
                                                           train_scenario=train_scenario)
                    else:
                        stats = validator.validate_quality(schedules=schedules, test_scenario=test_scenario,
                                                           train_scenario=train_scenario)
                    # add score of system
                    result_dict = {
                        'scenario_name': scenario_name,
                        'strategy_name': 'ASAPv2',
                        'PAR10_score': stats.get_score(False),
                        'repetition': repetition,
                        'fold': fold,
                        'seed': seed,
                    }
                    results_frame = results_frame.append(pd.DataFrame([result_dict]))

                    # adds SBS score (sanity check)
                    result_dict['strategy_name'] = 'SBS'
                    result_dict['PAR10_score'] = stats.get_score_sbs(False)
                    results_frame = results_frame.append(pd.DataFrame([result_dict]))

                    # adds oracle score (sanity check)
                    result_dict['strategy_name'] = 'Oracle'
                    result_dict['PAR10_score'] = stats.get_score_oracle(False)
                    results_frame = results_frame.append(pd.DataFrame([result_dict]))
        results_frame.to_csv(scenario_results_file)
    pass


if __name__ == '__main__':
    run(parse_args())
