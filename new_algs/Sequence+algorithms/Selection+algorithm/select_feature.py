import pandas

from _helpers.GenericModel import GenericModel
from _helpers.VisualizerHelper import VisualizerHelper
from config import DB_TRAIN_FEATURE_TABLE

csv = '../csv_files/' + DB_TRAIN_FEATURE_TABLE + '.csv'

# Print a lot of plots
data = pandas.read_csv(csv)
VisualizerHelper.make_plot('all', data)

# Feature Selection
# GenericModel.feature_selection(csv)
