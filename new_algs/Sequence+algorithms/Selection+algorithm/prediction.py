import pandas as pd
import pickle

from _helpers.Database import Database
from _helpers.GenericModel import GenericModel
from config import DIR, TEST_DATA, DB_PATH

PATH_OF_BINARY_MODEL = '../bin_models/decision_tree_with_length.sav'

# load dataset from disk
db = Database(DB_PATH)

# Extract Features
chunksize = 10
iterations = GenericModel.extract_features(None, DIR + TEST_DATA, chunksize, 'test_features_data')
df_features = db.get_df_from_table('test_features_data')

# load saved model from disk
X_test_data = df_features.iloc[:, [df_features.columns.get_loc("length")]].values
loaded_model = pickle.load(open(PATH_OF_BINARY_MODEL, 'rb'))
result = loaded_model.predict(X_test_data)

df_output = pd.DataFrame()
df_output['Id'] = df_features["id"]
df_output['Predicted'] = result

# save to CSV
df_output.to_csv('output.csv', index=False, columns=['Id', 'Predict'], header=True)

