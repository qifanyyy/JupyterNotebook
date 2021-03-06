import time
import datetime
import os
import sys
import hyperopt
import numpy
import random

from surprise import Dataset
from surprise import Reader

sys.path.insert(1, "./")

from auto_surprise.engine import Engine

random.seed(1)
numpy.random.seed(1)

if __name__ == "__main__":
    # Load Movielens 100k dataset Dataset
    file_path = os.path.expanduser("../datasets/ml-100k/u.data")
    reader = Reader(
        line_format="user item rating timestamp", sep="\t", rating_scale=(1, 5)
    )

    data = Dataset.load_from_file(file_path, reader=reader)

    # Run auto surprise
    start_time = time.time()
    engine = Engine(verbose=True, random_state=numpy.random.RandomState(1))
    best_model, best_params, best_score, tasks = engine.train(
        data=data,
        target_metric="test_rmse",
        cpu_time_limit=180,
        max_evals=100,
        hpo_algo=hyperopt.tpe.suggest,
    )
    cv_time = str(datetime.timedelta(seconds=int(time.time() - start_time)))

    print("--------- Done ----------")
    print("Time taken: ", cv_time)
    print("Best model: ", best_model)
    print("Best params: ", best_params)
    print("Best score: ", best_score)
    print("All tasks: ", tasks)
