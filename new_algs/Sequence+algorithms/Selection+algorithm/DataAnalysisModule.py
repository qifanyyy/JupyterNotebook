import matplotlib
import pandas as pd
import numpy as np

# These are the plotting modules adn libraries we'll use:
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score


class DataAnalysisClass:
    # general information display it generates a plot consisting
    # of two subplots which contain the raw data and the skewed data regarding a feature
    #
    # Arguments:
    # - data_frame represents the data frame that you need to be displayed
    # - feature is the feature that you are interested in
    #
    # return type is plot
    @staticmethod
    def general_information_plotting(data_frame, feature):
        print('General information about the data \n')
        print(data_frame.describe(), '\n\n')

        try:
            print(feature + ' of the data \n')
            print(data_frame[feature].describe(), '\n\n')
        except:
            print('#' * 100, '\n\nWrong data frame format')
            exit(0)

        fig = plt.figure(figsize=(20, 5))
        plt.suptitle(feature + 'Analysis')
        fig.add_subplot(121)
        subtitle = 'Skew is ' + str(data_frame[feature].skew())
        plt.title(subtitle)
        plt.hist(feature, data=data_frame)

        fig.add_subplot(122)
        subtitle = 'Skew after logarithm is ' + str(np.log(data_frame[feature]).skew())
        plt.title(subtitle)
        plt.hist(np.log(data_frame[feature]))

        return plt

    # This function makes a ranking of the most influential features
    # of the end result, making the data analysis and ML decisions faster
    #
    # There are 2 variables, one for the positive features and the other for the
    # negative features, that can be tweaked for other data frames
    #
    # Arguments:
    # - data_frame represents the data frame that you need to be displayed
    # - correlation is the feature that you are interested in
    # - size_ranking is the number of positive and negative features that you need to display
    #
    # return type is plot
    @staticmethod
    def feature_ranking_plotting(data_frame, correlation, size_ranking):
        print('Features that we care about \n')
        data_frame_numeric_features = data_frame.select_dtypes(include=[np.number])
        data_frame_corr = data_frame_numeric_features.corr()
        # take the first 5 best increasing factors and
        # the best indicators of the decrease of the final feature
        data_frame_pos_features = data_frame_corr[correlation].sort_values(ascending=False)[1:size_ranking + 1]
        data_frame_neg_features = data_frame_corr[correlation].sort_values(ascending=False)[-size_ranking:]
        print(data_frame_pos_features, '\n')
        print(data_frame_neg_features, '\n\n')

        fig = plt.figure(figsize=(10, 5))
        plt.suptitle('Overall Features: Their correlation with the ' + correlation)
        fig.add_subplot(121)
        plt.plot(data_frame_pos_features)
        plt.xticks(rotation=90)
        plt.yticks(rotation=90)
        plt.ylabel('Importance/ Relative Value to feature')

        fig.add_subplot(122)
        plt.plot(data_frame_neg_features)
        plt.xticks(rotation=90)
        plt.yticks(rotation=90)
        plt.ylabel('Importance/ Relative Value to feature')

        return plt

    # This function plots the null distribution in the data frame
    #
    # Arguments:
    # - data_frame represents the data frame that you need to be displayed
    #
    # return type is plot
    @staticmethod
    def null_distribution_plotting(data_frame):
        nans = data_frame.isna().sum().sort_values(ascending=False)
        nans = nans[nans > 0]
        print('Decide what to delete and see the distribution of the most null elements')
        print(nans.describe())
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.grid()
        ax.bar(nans.index, nans.values, zorder=2, color='#3f72af')
        ax.set_ylabel('No. of missing values', labelpad=10)
        ax.set_xlim(-0.6, len(nans) - 0.4)
        ax.xaxis.set_tick_params(rotation=90)
        plt.suptitle('Missing data in DB')

        return plt

    # This function prints the composition of unique values and their datatypes
    # From the data frame
    #
    # Arguments:
    # - data_frame represents the data frame
    #
    # returns nothing
    @staticmethod
    def print_composition_dataframe(data_frame):
        print(data_frame.info())
        print('\n\n')
        for i in range(11):
            out_string = '{:>30}: {:>5}, with type: {}'.format(data_frame.columns[i],
                                                               str(data_frame[data_frame.columns[i]].nunique()),
                                                               type(data_frame[data_frame.columns[i]][0]))
            print(out_string)

    # This function cleans the data frame of null values
    #
    # Arguments:
    # - data_frame represents the data frame
    #
    # returns the data_frame
    @staticmethod
    def clean_dataset(data_frame):
        data_frame.dropna(inplace=True)
        indices_to_keep = ~data_frame.isin([np.nan, np.inf, -np.inf]).any(1)
        return data_frame[indices_to_keep]

    # This function fills the data frame from null values
    #
    # Arguments:
    # - data_frame represents the data frame
    # - feature that needs to be analysed
    #
    # returns the data_frame
    @staticmethod
    def fill_data_set(data_frame, feature):

        if data_frame[feature].dtype == 'object':
            data_frame[feature] = data_frame[feature].fillna(data_frame[feature].mode()[0])
        else:
            data_frame[feature] = data_frame[feature].fillna(data_frame[feature].mean())

        return data_frame

    # This function encodes the str states into float types
    #
    # Arguments:
    # - data_frame represents the data frame
    # - feature that needs to be analysed
    #
    # returns the data_frame
    @staticmethod
    def label_encoder_array(data_frame, array_features):
        le = preprocessing.LabelEncoder()
        for i in array_features:
            data_frame[i] = le.fit_transform(data_frame[i])

        return data_frame
