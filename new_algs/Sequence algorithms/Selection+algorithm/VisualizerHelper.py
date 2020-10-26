import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix


class VisualizerHelper:
    @staticmethod
    def make_plot(plot, data):
        data = data.drop(['<built-in function id>', 'Unnamed: 0', 'id'], axis=1)
        if plot == 'all':
            # VisualizerHelper.__correlation_matrix_plot(data)
            # VisualizerHelper.__triangle_correlation_matrix_plot(data)
            # VisualizerHelper.__scatter_matrix_plot(data)
            # VisualizerHelper.__whiskers_plot(data)
            # # VisualizerHelper.__density_plots(data)
            # VisualizerHelper.__histogram_plots(data)
            VisualizerHelper.__pairplot(data)

    @staticmethod
    def __correlation_matrix_plot(data):
        # Correction Matrix Plot
        correlations = data.corr()
        # plot correlation matrix
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.matshow(correlations, vmin=-1, vmax=1)
        fig.colorbar(cax)
        ax.set_xticklabels(data.columns.values, rotation=90)
        ax.set_yticklabels(data.columns.values)
        ax.set_xticks(np.arange(len(data.columns.values)))
        ax.set_yticks(np.arange(len(data.columns.values)))
        plt.show()

    @staticmethod
    def __triangle_correlation_matrix_plot(data):

        sns.set(style="white")

        # Compute the correlation matrix
        corr = data.corr()

        # Generate a mask for the upper triangle
        mask = np.zeros_like(corr, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True

        # Set up the matplotlib figure
        f, ax = plt.subplots(figsize=(11, 9))

        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(220, 10, as_cmap=True)

        # Draw the heatmap with the mask and correct aspect ratio
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                    square=True, linewidths=.5, cbar_kws={"shrink": .5})

    @staticmethod
    def __scatter_matrix_plot(data):
        scatter_matrix(data)
        plt.show()
        # plt.savefig('plots/scatter_matrix_plot.png', bbox_inches='tight')

    @staticmethod
    def __whiskers_plot(data):
        # Box and Whisker Plots
        data.plot(kind='box', subplots=True, layout=(5, 5), sharex=False, sharey=False)
        # plt.show()
        # plt.savefig('plots/whiskers_plot.png', bbox_inches='tight')

    @staticmethod
    def __density_plots(data):
        data.plot(kind='density', subplots=True, layout=(3, 3), sharex=False)
        plt.show()
        # plt.savefig('plots/density_plots.png', bbox_inches='tight')

    @staticmethod
    def __histogram_plots(data):
        data.hist()
        plt.show()
        # plt.savefig('plots/histogram_plots.png', bbox_inches='tight')

    @staticmethod
    def __pairplot(data):
        sns.pairplot(data, hue='length')