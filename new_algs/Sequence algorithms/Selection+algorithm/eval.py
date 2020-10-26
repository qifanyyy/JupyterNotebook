import json
import argparse
from datetime import datetime, timedelta
import pandas as pd
import pickle
import numpy as np
import os
import glob


def generate_features(points):
    """
    Generate features from timestamps
    """
    return np.array([(point.year, point.month, point.day, point.hour, point.minute, point.second, point.weekday()) for point in points])


def create_data_points(period, freq):
    """
    Generate timestamps for a given number
    of days at a given frequency (in minutes)
    """

    start, end = period.split('-')
    aux = datetime.strptime(start, '%Y,%m,%d')
    end = datetime.strptime(end, '%Y,%m,%d') + timedelta(days=1)
    points = []

    # generate the data points
    while aux < end:
        points.append(aux)
        aux = aux + timedelta(minutes = freq)

    return points


def get_models_list(models_path, filename, sources=None):
    """
    Get all the models for a dataset and sources
    """
    # if no sources are given, we use them all
    if sources is None:
        all_sources = True
    else:
        sources = sources.split(',')
        all_sources = False

    # list all the files in the models directory (this includes the encoders dictionaries)
    models = os.listdir(models_path)
    # filter just by models
    models = filter(lambda x: x.endswith('.model'), models)
    res = []
    sources_res = []
    for model in models:
        aux = model.split('-SEP-')
        dataset, source, id_ = aux[0], aux[1:-1], aux[-1].split('.')[0]
        source_name = ' '.join(source)
        # we keep the models for the specific dataset and sources listed
        if dataset.lower() == filename.lower() and (all_sources or source_name.lower() in sources):
            res.append(os.path.join(models_path, model))
            sources_res.append(source_name)
    return res, sources_res


def get_predictions(models, points):
    """
    Get predictions for each model and data point
    """
    # create the timestamps from the features
    points_df = pd.to_datetime(pd.DataFrame(points[:, :-1], columns=['year', 'month', 'day', 'hour', 'minute', 'second'])).to_frame('timestamp')

    res = pd.DataFrame(columns=['source', 'id', 'timestamp', 'predictions'])
    for model_path in models:
        has_encoder = False
        # separate path into dataset name, source and id
        aux = model_path.split('-SEP-')
        dataset, source, id_ = aux[0], ' '.join(aux[1:-1]), aux[-1].split('.')[0]
        # just values for the source and id columns
        aux = [(source, id_)] * points.shape[0]
        # load the model
        with open(model_path, 'rb') as fp:
            model = pickle.load(fp)
        # check if this models uses an encoder
        if os.path.exists(model_path.replace('.model', '-SEP-' + 'encoder.json')):
            has_encoder = True
            # load encoder dictionary
            with open(model_path.replace('.model', '-SEP-' + 'encoder.json')) as fp:
                encoder = {int(k): v for k, v in json.load(fp).items()}
        # get predictions
        preds = model.predict(points)
        # add the predictions to the data points
        aux_df = points_df.join(pd.DataFrame(preds, columns=['predictions']))
        # if the model uses an encoder, we map the numerical values to the strings
        if has_encoder:
            aux_df['predictions'] = aux_df['predictions'].replace(encoder)
        # add source column
        aux_df.insert(0, column='source', value=source)
        # add id column
        aux_df.insert(1, column='id', value=id_)
        # append to final data frame and try next model
        res = res.append(aux_df, ignore_index=True)

    return res


if __name__ == '__main__':
    # timestamp for filenames and directories
    now = datetime.now()
    timestamp_dir = '{0}/{1}/{2}/'.format(now.year, now.month, now.day)
    timestamp_file = '{0}{1}{2}{3}{4}_'.format(now.year, now.month, now.day, now.hour, now.minute)
    OUTPUT = os.path.join('output', timestamp_dir)
    LOGS = os.path.join('logs/eval', timestamp_dir)
    # create directories
    os.makedirs(OUTPUT, exist_ok=True)
    os.makedirs(LOGS, exist_ok=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, required=True, help="name of data file running the predictions on")
    parser.add_argument('--models', type=str, required=True, help="path to the trained models")
    parser.add_argument('--sources', type=str, default=None, help="list of sources for getting the predictions, separated by commas, eg, “Docks Available,Bikes Available,Commercial Flow - CA” (if no sources are provided, then the predictions will run for every source trained with that dataset)")
    parser.add_argument('--period', type=str, required=True, help="specifies the period of time for which the predictions are computed, it is a string with the following format: <year_start>,<month_start>,<day_start>-<year_end>,<month_end>,<day_end>")
    parser.add_argument('--frequency', type=int, required=True, help="distance between data points (measured in minutes)")

    args = parser.parse_args()

    fname = args.filename.split('.')[0]
    sources = args.sources
    period = args.period
    freq = args.frequency
    models = args.models
    # get the models and sources for this predictions
    models, sources = get_models_list(models, fname, sources)
    # data points for the predictions
    points = generate_features(create_data_points(period, freq))
    # generate the predictions
    preds = get_predictions(models, points)
    # save predictions to disk
    preds.to_csv(os.path.join(OUTPUT, timestamp_file + fname + '_predictions.csv'), index=None)
    # save statistics
    with open(os.path.join(LOGS, timestamp_file + 'statistics.json'), 'w') as fp:
        json.dump({'sources': ', '.join(set(sources)), 'number of data points': len(points), 'frequency': freq, 'period': period}, fp)
