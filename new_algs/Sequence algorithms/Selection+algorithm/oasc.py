import algsel
import arff
import openmlcontrib
import os
import pandas as pd
import typing
import shutil
import yaml


def get_oasc_train_and_test_frame(oasc_scenario_dir: str, scenario_name: str) \
        -> typing.Tuple[pd.DataFrame, pd.DataFrame, typing.Dict]:
    meta_arff_train_location = os.path.join(oasc_scenario_dir, 'train', scenario_name, 'feature_values.arff')
    runs_arff_train_location = os.path.join(oasc_scenario_dir, 'train', scenario_name, 'algorithm_runs.arff')
    status_arff_train_location = os.path.join(oasc_scenario_dir, 'train', scenario_name, 'feature_runstatus.arff')

    meta_arff_test_location = os.path.join(oasc_scenario_dir, 'test', scenario_name, 'feature_values.arff')
    runs_arff_test_location = os.path.join(oasc_scenario_dir, 'test', scenario_name, 'algorithm_runs.arff')
    status_arff_test_location = os.path.join(oasc_scenario_dir, 'test', scenario_name, 'feature_runstatus.arff')

    description_location = os.path.join(oasc_scenario_dir, 'test', scenario_name, 'description.txt')

    with open(description_location, 'r') as fp:
        description = yaml.load(fp)

    train_frame = algsel.scenario.obtain_dataframe_scenario(meta_arff_train_location, runs_arff_train_location, status_arff_train_location)
    test_frame = algsel.scenario.obtain_dataframe_scenario(meta_arff_test_location, runs_arff_test_location, status_arff_test_location)
    return train_frame, test_frame, description


def save_scenario_in_oasc_format(scenario_folder: str, scenario_name: str,
                                 to_folder: str, repetition: int, fold: int) -> None:
    """
    Extracts a single repetition / fold from the scenario and saves it in oasc
    format
    """
    for test_bool in [True, False]:
        res = algsel.scenario.scenario_to_fold(scenario_folder, test_bool, repetition, fold)
        algorithm_runs, feature_costs, feature_runstatus, feature_values = res
        out_folder = os.path.join(to_folder, 'test' if test_bool else 'train', scenario_name)
        os.makedirs(out_folder, exist_ok=True)

        with open(os.path.join(out_folder, 'algorithm_runs.arff'), 'w') as fp:
            arff.dump(openmlcontrib.meta.dataframe_to_arff(algorithm_runs, 'algorithm_runs', None), fp)
        if feature_costs is not None:
            with open(os.path.join(out_folder, 'feature_costs.arff'), 'w') as fp:
                arff.dump(openmlcontrib.meta.dataframe_to_arff(feature_costs, 'feature_costs', None), fp)
        with open(os.path.join(out_folder, 'feature_runstatus.arff'), 'w') as fp:
            arff.dump(openmlcontrib.meta.dataframe_to_arff(feature_runstatus, 'feature_runstatus', None), fp)
        with open(os.path.join(out_folder, 'feature_values.arff'), 'w') as fp:
            arff.dump(openmlcontrib.meta.dataframe_to_arff(feature_values, 'feature_values', None), fp)
        # also copy description
        shutil.copyfile(
            os.path.join(scenario_folder, 'description.txt'),
            os.path.join(out_folder, 'description.txt')
        )
