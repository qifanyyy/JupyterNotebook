import os
from datetime import datetime

from _helpers.Database import Database
from _helpers.GenericModel import GenericModel
from config import TRAIN_TARGET_OUTPUT, TRAIN_DATA, DB_TRAIN_FEATURE_TABLE, DB_PATH, DIR

# EXTRACT_FEATURES = False

chunksize = 10
start_time = datetime.now()
try:
    os.remove(DB_PATH)
except OSError:
    pass

db = Database(DB_PATH)

# if EXTRACT_FEATURES:
iterations = GenericModel.extract_features(DIR + TRAIN_TARGET_OUTPUT, DIR + TRAIN_DATA, chunksize, DB_TRAIN_FEATURE_TABLE)
if iterations == 0:
    print('Extract Feature is disabled. CSV file was generated')
else:
    delta_time = (datetime.now() - start_time)
    print('Feature Extraction ended in {} seconds: completed {} iterations of {} chunk'.format(delta_time, iterations, chunksize))
# else:
#     db.db_table_to_csv(DB_FEATURE_TABLE, '../csv_files/features.csv')
#     print('Extract Feature is disabled. CSV file was generated')
