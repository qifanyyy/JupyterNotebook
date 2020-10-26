import algsel
import aslib_scenario
import argparse
import logging
import operator
import os
import pandas as pd
import sklearn

import sklearn.pipeline
import sklearn.preprocessing
import sklearn.ensemble


def parse_args():
    parser = argparse.ArgumentParser(description='Runs a sklearn algorithm on ASLib splits')
    parser.add_argument('--oasc_scenario_dir', type=str, default='../../oasc/oasc_scenarios/')
    parser.add_argument('--scenario_name', type=str, default='Camilla')
    parser.add_argument('--random_seed', type=int, default=42)
    parser.add_argument('--impute', type=str, default='median')
    parser.add_argument('--model', type=str, default='forest_256')
    parser.add_argument('--verbose', action='store_true', default=False)
    return parser.parse_args()


def run_on_scenario(oasc_scenario_dir, scenario_name, meta, random_seed):
    train_frame, test_frame, description = algsel.scenario.get_oasc_train_and_test_frame(oasc_scenario_dir, scenario_name)
    maximize = description['maximize'][0]

    meta.model_template.set_params(classifier__random_state=random_seed)
    meta.fit(train_frame)
    predictions = meta.predict(test_frame)

    return_format = dict()
    for task_id, pred in predictions.items():
        if maximize:
            predicted_algorithm = max(pred.items(), key=operator.itemgetter(1))[0]
        else:
            predicted_algorithm = min(pred.items(), key=operator.itemgetter(1))[0]
        return_format[task_id] = [[predicted_algorithm, 99999]]
    return return_format


def run(args):
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    if args.scenario_name is not None:
        scenarios = [args.scenario_name]
    else:
        scenarios = [
            'Camilla',
            'Oberon',
            # 'Titus'
        ]

    models = {
        'tree': sklearn.tree.DecisionTreeRegressor(),
        'forest_16': sklearn.ensemble.RandomForestRegressor(n_estimators=16),
        'forest_256': sklearn.ensemble.RandomForestRegressor(n_estimators=256)
    }

    pipeline = sklearn.pipeline.Pipeline(steps=[('imputer', sklearn.preprocessing.Imputer(strategy=args.impute)),
                                                ('classifier', models[args.model])])

    for scenario_name in scenarios:
        for single_model in [True, False]:
            meta = algsel.models.SklearnModelWrapper(pipeline, single_model)
            logging.info('%s on %s; single model = %s' % (args.model, scenario_name, single_model))
            schedules = run_on_scenario(args.oasc_scenario_dir, scenario_name, meta, args.random_seed)

            print(schedules)

            # read scenarios
            test_scenario = aslib_scenario.aslib_scenario.ASlibScenario()
            test_scenario.read_scenario(dn=os.path.join(args.oasc_scenario_dir, 'test', scenario_name))
            train_scenario = aslib_scenario.aslib_scenario.ASlibScenario()
            train_scenario.read_scenario(dn=os.path.join(args.oasc_scenario_dir, 'train', scenario_name))

            validator = algsel.scoring.Validator()
            # this script assumes quality scenario
            validator.validate_quality(schedules=schedules, test_scenario=test_scenario,
                                       train_scenario=train_scenario)


if __name__ == '__main__':
    pd.options.mode.chained_assignment = 'raise'
    run(parse_args())
