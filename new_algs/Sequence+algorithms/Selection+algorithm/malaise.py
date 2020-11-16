import numpy as np
import pickle
import csv
import multiprocessing
import shutil

from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split

from autosklearn.classification import AutoSklearnClassifier
from autosklearn.metrics import accuracy
from autosklearn.constants import *

from cause.predictor import GenericClassifier
from cause.predictor import RandomClassifier
from cause.predictor import BestAlgoClassifier
from cause.predictor import Predictor
from cause.predictor import ClassificationSet


class MLClassifier(GenericClassifier):

    def __init__(self, train, dataset_name, weight, num_processes=1):
        super().__init__(train)
        # init shared tmp folders for parallel automl
        automl_tmp_folder = "/tmp/autosklearn_parallel_tmp_%.1f" % weight
        automl_output_folder = "/tmp/autosklearn_parallel_out_%.1f" % weight
        for dir in [automl_tmp_folder, automl_output_folder]:
            try:
                shutil.rmtree(dir)
            except OSError as e:
                pass
        
        # parallel automl
        processes = []
        spawn_classifier = MLClassifier.__get_spawn_classifier(train.X, train.y)
        for i in range(num_processes):
            p = multiprocessing.Process(target=spawn_classifier, args=(
                i, dataset_name, automl_tmp_folder, automl_output_folder))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()

        self.__cls = AutoSklearnClassifier(
#            time_left_for_this_task=15,
#            per_run_time_limit=15,
#            ml_memory_limit=1024,
            shared_mode=True,
            ensemble_size=50,
            ensemble_nbest=200,
            tmp_folder=automl_tmp_folder,
            output_folder=automl_output_folder,
            initial_configurations_via_metalearning=0,
            seed=1,
        )
        self.__cls.fit_ensemble(
            train.y,
            task=MULTICLASS_CLASSIFICATION,
            metric=accuracy,
            precision='32',
            dataset_name=dataset_name,
            ensemble_size=20,
            ensemble_nbest=50,
        )

    @property
    def name(self):
        return "MALAISE"

    @property
    def cls(self):
        return self.__cls

    def dump(self, pickle_file):
        # print models
        self.__cls.show_models()
        # dump model to file
        with open(pickle_file, 'wb') as fio:
            pickle.dump(self.cls, fio)

    def predict(self, test):
        return self.cls.predict(test.X)

    @staticmethod
    def __get_spawn_classifier(X_train, y_train):
        def spawn_classifier(seed, dataset_name, automl_tmp_folder, automl_output_folder):
            if seed == 0:
                initial_configurations_via_metalearning = 25
                smac_scenario_args = {}
            else:
                initial_configurations_via_metalearning = 0
                smac_scenario_args = {'initial_incumbent': 'RANDOM'}

            automl = AutoSklearnClassifier(
    #            time_left_for_this_task=60, # sec., how long should this seed fit process run
    #            per_run_time_limit=15, # sec., each model may only take this long before it's killed
    #            ml_memory_limit=1024, # MB, memory limit imposed on each call to a ML algorithm
                shared_mode=True, # tmp folder will be shared between seeds
                tmp_folder=automl_tmp_folder,
                output_folder=automl_output_folder,
                delete_tmp_folder_after_terminate=False,
                ensemble_size=0, # ensembles will be built when all optimization runs are finished
                initial_configurations_via_metalearning=initial_configurations_via_metalearning,
                seed=seed,
                smac_scenario_args=smac_scenario_args,
            )
            automl.fit(X_train, y_train, dataset_name=dataset_name)
        return spawn_classifier


class MALAISEPredictor(Predictor):

    def __init__(self, lstats, features):
        super().__init__(lstats)
        self.__clsset = ClassificationSet.sanitize_and_init(
            features.features, lstats.winners, lstats.costs)
        self.__dataset_name = features.name
  
    @property
    def clsset(self):
        return self.__clsset

    @property
    def dataset_name(self):
        return self.__dataset_name

    def run(self, outfolder="/tmp", num_processes=1):
        stats_file = "%s/%s_stats_%.1f" % (outfolder, self.dataset_name, self.weight)
        pickle_file = "%s/%s_cls_model_%.1f" % (outfolder, self.dataset_name, self.weight)

        # split into training and test set
        train, test = self._preprocess_and_split()

        # random prediction -> run 100 times
        rand_cls = RandomClassifier(train)
        for _ in range(100):
            self.__dump_stats(stats_file, rand_cls, train, test)

        # best algo on average prediction
        algo_cls = BestAlgoClassifier(train)
        self.__dump_stats(stats_file, algo_cls, train, test)
        
        # ml-based prediction
        ml_cls = MLClassifier(train, self.dataset_name, self.weight, num_processes)
        self.__dump_stats(stats_file, ml_cls, train, test)
        ml_cls.dump(pickle_file)

    def __dump_stats(self, stats_file, clsf, train, test):
        acc_train, mre_train = clsf.evaluate(train)
        acc_test, mre_test = clsf.evaluate(test)
        stats = [clsf.name, self.weight,
                 self.clsset.le.inverse_transform(clsf.algo),
                 acc_train, acc_test, mre_train, mre_test]
        with open(stats_file, "a") as f:
            csv.writer(f).writerow(stats)

    def _preprocess_and_split(self):
        X_train, X_test, y_train, y_test, c_train, c_test = train_test_split(
            self.clsset.X, self.clsset.y, self.clsset.c,
            test_size=0.3, stratify=self.clsset.y, random_state=8)
        sc = RobustScaler()  # StandardScaler()
        X_train_std = sc.fit_transform(X_train)
        X_test_std = sc.transform(X_test)

        train = ClassificationSet(X_train_std, y_train, c_train, self.clsset.le)
        test = ClassificationSet(X_test_std, y_test, c_test, self.clsset.le)

        return train, test


