import aslib_scenario
import algsel
import argparse
import json
import logging
import os


def parse_args():
    parser = argparse.ArgumentParser(description='Runs a sklearn algorithm on Oberon splits')
    parser.add_argument('--oasc_scenario_dir', type=str, default='../../oasc/oasc_scenarios/')
    parser.add_argument('--scenario_name', type=str, default='Camilla')
    parser.add_argument('--SBS_on_testset', action='store_true', help='Determines how the Single Best Solver is ' +
                                                                      'calculated: as the best on the train set or ' +
                                                                      'the best on the test set. ')
    parser.add_argument('--submissions_dir', type=str, default='../../oasc/submissions/')
    parser.add_argument('--system', type=str, default='ASAP.v2')
    return parser.parse_args()


if __name__ == '__main__':
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    args = parse_args()

    # read scenarios
    test_scenario = aslib_scenario.aslib_scenario.ASlibScenario()
    test_scenario.read_scenario(dn=os.path.join(args.oasc_scenario_dir, 'test', args.scenario_name))
    train_scenario = aslib_scenario.aslib_scenario.ASlibScenario()
    train_scenario.read_scenario(dn=os.path.join(args.oasc_scenario_dir, 'train', args.scenario_name))

    # read schedule
    schedule_file = args.submissions_dir + '/' + args.system + '/' + args.scenario_name + '.json'
    with open(schedule_file) as fp:
        schedules = json.load(fp)

    validator = algsel.scoring.Validator()

    if test_scenario.performance_type[0] == 'runtime':
        validator.validate_runtime(schedules=schedules, test_scenario=test_scenario, train_scenario=train_scenario)
    else:
        validator.validate_quality(schedules=schedules, test_scenario=test_scenario, train_scenario=train_scenario)
