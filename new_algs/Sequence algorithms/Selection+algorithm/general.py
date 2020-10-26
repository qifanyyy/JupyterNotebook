import arff
import logging
import openmlcontrib
import os

import pandas as pd


def obtain_dataframe_scenario(meta_features_path: str, evaluations_path: str, feature_status_path: str):
    """
    Loads the scenario files and returns a dataframe with (meta)-features and
    evaluations joined.
    """
    run_cols = {'instance_id', 'repetition', 'algorithm', 'runstatus'}

    # load features
    features_arff = arff.load(open(meta_features_path))
    features_columns = [att[0] for att in features_arff['attributes']]
    features = pd.DataFrame(features_arff['data'], columns=features_columns)
    features = features.set_index(['instance_id', 'repetition'])

    # load feature status
    feature_status_arff = arff.load(open(feature_status_path))
    feature_status_columns = [att[0] for att in feature_status_arff['attributes']]
    feature_status = pd.DataFrame(feature_status_arff['data'], columns=feature_status_columns)
    feature_status = feature_status.set_index(['instance_id', 'repetition'])

    # merge feature with feature status
    features = features.join(feature_status)

    # load evaluations
    evaluations_arff = arff.load(open(evaluations_path))
    evaluations_columns = [att[0] for att in evaluations_arff['attributes']]

    # deduce objective function (based on evaluation columns)
    candidates = set(evaluations_columns) - run_cols
    if len(candidates) == 0:
        raise ValueError('No candidate for objective_function')
    elif len(candidates) > 1:
        raise ValueError('Multiple candidate for objective_function')
    objective_function = list(candidates)[0]

    # further pre-process evaluations
    relevant_fields = ['instance_id', 'algorithm', 'repetition', objective_function]
    evaluations = pd.DataFrame(evaluations_arff['data'], columns=evaluations_columns)[relevant_fields]
    evaluations = evaluations.set_index(['instance_id', 'repetition'])

     # merge
    evaluations = evaluations.join(features).reset_index()
    evaluations = evaluations.reindex(sorted(evaluations.columns), axis=1)
    evaluations = evaluations.rename(index=str, columns={objective_function: 'objective_function'})

    # sort columns
    evaluations = evaluations[sorted(evaluations.columns.values)]

    # sort rows and return
    return evaluations.sort_values(['instance_id', 'algorithm']).reset_index().drop('index', axis=1)


def scenario_to_fold(scenario_folder, test_set, repetition, fold):
    """
    Returns the subset of a scenario, i.e., instances given a repetition, fold
    and whether to return the test set (train set otherwise).
    """
    with open(os.path.join(scenario_folder, 'cv.arff')) as fp:
        cv_arff = arff.load(fp)

    cv_frame = openmlcontrib.meta.arff_to_dataframe(cv_arff, None)
    cv_frame = cv_frame.loc[(cv_frame['repetition'] == repetition) & (cv_frame['fold'] == fold)]
    instance_ids = cv_frame['instance_id'].values

    result_types = ('algorithm_runs', 'feature_costs', 'feature_runstatus', 'feature_values')
    result = []

    for file_type in result_types:
        filepath = os.path.join(scenario_folder, '%s.arff' % file_type)
        if not os.path.isfile(filepath):
            logging.warning('Scenario folder %s does not have file type: %s' % (scenario_folder, file_type))
            result.append(None)
            continue
        with open(filepath) as fp:
            scenario_arff = arff.load(fp)

        scenario_frame = openmlcontrib.meta.arff_to_dataframe(scenario_arff, None)
        if test_set:
            scenario_frame = scenario_frame.loc[scenario_frame['instance_id'].isin(instance_ids)]
        else:
            scenario_frame = scenario_frame.loc[~scenario_frame['instance_id'].isin(instance_ids)]
        result.append(scenario_frame)
    return tuple(result)
