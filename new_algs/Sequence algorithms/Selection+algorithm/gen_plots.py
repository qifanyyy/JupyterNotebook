import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon


dataset_names = ['hepatitis', 'breastEW', 'multiple_features']
beautiful_dataset_names = {'breastEW':'BreastEW', 'hepatitis':'Hepatitis', 'multiple_features':'Multiple Features'}

dataset_title = 'Dataset'
experiment_names = ['ELM', 'NN', 'baseline_ELM', 'baseline_NN']
beautiful_experiment_names = {'ELM':'GA+ELM', 'NN':'GA+NN', 'baseline_ELM':'ELM', 'baseline_NN':'NN'}

features_size = {'breastEW':30, 'hepatitis':19, 'multiple_features':649}

def load_log(filename):

    with open(filename, 'r') as f:
        data = f.readlines()
    data = [d.strip().split(',') for d in data]
    data = np.array(data, dtype=np.float)
    data = data[:, 1:] # remove the seed values 
    return data

results = {}

for dataset in dataset_names:
    for experiment in experiment_names:

        filename = 'output/{}/{}.log'.format(dataset, experiment)

        try:
            results[dataset][experiment] = load_log(filename)
        except:
            results[dataset] = {} 
            results[dataset][experiment] = load_log(filename)


        if 'baseline' in experiment:

            data = np.zeros((20, 7))
            data[:, 0] = results[dataset][experiment][:, 0]
            data[:, 3:] = results[dataset][experiment][:, 1:]
            data[:, 1] = features_size[dataset]
            data[:, 2] = (1.0 - data[:, 3]) * 0.9 + 0.1

            results[dataset][experiment] = data



def gen_latex_table(title=None, typ=None, column=None):
    
    print('\n{}'.format(title))
    lines = [' & '.join([dataset_title] + [beautiful_experiment_names[experiment] for experiment in experiment_names])]
    for dataset in dataset_names:
        line = [beautiful_dataset_names[dataset]]
        for experiment in experiment_names:

            if typ == 'min':
                best = results[dataset][experiment][:, column].min()
                line.append('$ {:.4f} $'.format(best))
            elif typ == 'max':
                best = results[dataset][experiment][:, column].max()
                line.append('$ {:.4f} $'.format(best))
            elif typ == 'meanstd':
                best_mean = results[dataset][experiment][:, column].mean()
                best_std = results[dataset][experiment][:, column].std()
                line.append('$ {:.4f} \\pm {:.4f} $'.format(best_mean, best_std))
            
        lines.append(' & '.join(line))
    print(' \\\\ \n'.join(lines) + ' \\\\')


# gen_latex_table('generate the best fitness table', 'min', 2)
# gen_latex_table('generate the mean (std) fitness table', 'meanstd', 2)
# gen_latex_table('generate the worst fitness table', 'max', 2)
# gen_latex_table('generate the mean (std) selection size table', 'meanstd', 1)
# gen_latex_table('generate the mean (std) accuracy table', 'meanstd', 3)
# gen_latex_table('generate the mean (std) time table', 'meanstd', 0)

# exit()
###################################################################################################

# plot_name = 'Número de features'
# column = 1
# random_dists = [beautiful_experiment_names[experiment] for experiment in experiment_names]

# # fig, ax1 = plt.subplots(figsize=(10, 6))
# # fig, ax1 = plt.subplots(figsize=(5, 4))
# fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=False, figsize=(10, 5))
# # fig.canvas.set_window_title('A Boxplot Example')
# # fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
# # fig.subplots_adjust(wspace=0.1003)
# ax1.set_ylabel(plot_name, fontsize=12)

# for dataset_name, ax in zip(dataset_names, (ax1, ax2, ax3)):

#     data = [results[dataset_name]['ELM'][:, column], 
#         results[dataset_name]['NN'][:, column], 
#         results[dataset_name]['baseline_ELM'][:, column], 
#         results[dataset_name]['baseline_NN'][:, column]]

#     bp = ax.boxplot(data, notch=0, sym='+', vert=1, whis=1.5, widths=0.75)
#     plt.setp(bp['boxes'], color='black')
#     plt.setp(bp['whiskers'], color='black')
#     plt.setp(bp['fliers'], color='red', marker='+')

#     # Add a horizontal grid to the plot, but make it very light in color
#     # so we can use it for reading data values but not be distracting
#     ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
#                 alpha=0.5)

#     # Hide these grid behind plot objects
#     ax.set_axisbelow(True)
#     # ax1.set_title('Comparison of IID Bootstrap Resampling Across Five Distributions')
#     # ax.set_xlabel('Experimentos')
#     ax.set_xlabel(beautiful_dataset_names[dataset_name] , fontsize=12)
#     # ax.set_ylabel(plot_name)

#     # Now fill the boxes with desired colors
#     box_colors = ['darkkhaki', 'royalblue']
#     num_boxes = len(data)
#     medians = np.empty(num_boxes)
#     for i in range(num_boxes):
#         box = bp['boxes'][i]
#         boxX = []
#         boxY = []
#         for j in range(5):
#             boxX.append(box.get_xdata()[j])
#             boxY.append(box.get_ydata()[j])
#         box_coords = np.column_stack([boxX, boxY])
#         # Alternate between Dark Khaki and Royal Blue
#         ax.add_patch(Polygon(box_coords, facecolor=box_colors[i % 2]))
#         # Now draw the median lines back over what we just filled in
#         med = bp['medians'][i]
#         medianX = []
#         medianY = []
#         for j in range(2):
#             medianX.append(med.get_xdata()[j])
#             medianY.append(med.get_ydata()[j])
#             ax.plot(medianX, medianY, 'k')
#         medians[i] = medianY[0]
#         # Finally, overplot the sample averages, with horizontal alignment
#         # in the center of each box
#         ax.plot(np.average(med.get_xdata()), np.average(data[i]),
#                 color='w', marker='*', markeredgecolor='k')

#     # Set the axes ranges and axes labels
#     ax.set_xlim(0.5, num_boxes + 0.5)
#     # ax.set_ylim(bottom, top)
#     # ax.set_xticklabels(random_dists, rotation=45, fontsize=8)
#     ax.set_xticklabels(random_dists)#, rotation=30)

#     # Due to the Y-axis scale being different across samples, it can be
#     # hard to compare differences in medians across the samples. Add upper
#     # X-axis tick labels with the sample medians to aid in comparison
#     # (just use two decimal places of precision)
#     pos = np.arange(num_boxes) + 1
#     upper_labels = [str(np.round(s, 2)) for s in medians]
#     weights = ['bold', 'semibold']
#     for tick, label in zip(range(num_boxes), ax.get_xticklabels()):
#         k = tick % 2
#         ax.text(pos[tick], 1.05, upper_labels[tick],
#                 transform=ax.get_xaxis_transform(),
#                 horizontalalignment='center', fontsize=10,
#                 weight=weights[k], color=box_colors[k])

#     # Finally, add a basic legend
#     # fig.text(0.80, 0.08, 'N Random Numbers', backgroundcolor=box_colors[0], color='black', weight='roman', size='x-small')
#     # fig.text(0.80, 0.045, 'IID Bootstrap Resample',
#     #          backgroundcolor=box_colors[1],
#     #          color='white', weight='roman', size='x-small')
#     # fig.text(0.80, 0.015, '*', color='white', backgroundcolor='silver',
#     #          weight='roman', size='medium')
#     # fig.text(0.815, 0.013, ' Average Value', color='black', weight='roman',
#     #          size='x-small')
# plt.tight_layout()
# # plt.show()
# plt.savefig('output/boxplot_all_{}.jpg'.format(plot_name))


# exit()
###################################################################################################

plot_name = 'Fitness'
column = 2
random_dists = [beautiful_experiment_names[experiment] for experiment in experiment_names]

top = 1 # 40
bottom = 0 #-5

# fig, ax1 = plt.subplots(figsize=(10, 6))
# fig, ax1 = plt.subplots(figsize=(5, 4))
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(10, 5))
# fig.canvas.set_window_title('A Boxplot Example')
# fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
# fig.subplots_adjust(wspace=0.1003)
ax1.set_ylabel(plot_name, fontsize=12)

for dataset_name, ax in zip(dataset_names, (ax1, ax2, ax3)):

    data = [results[dataset_name]['ELM'][:, column], 
        results[dataset_name]['NN'][:, column], 
        results[dataset_name]['baseline_ELM'][:, column], 
        results[dataset_name]['baseline_NN'][:, column]]

    bp = ax.boxplot(data, notch=0, sym='+', vert=1, whis=1.5, widths=0.75)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                alpha=0.5)

    # Hide these grid behind plot objects
    ax.set_axisbelow(True)
    # ax1.set_title('Comparison of IID Bootstrap Resampling Across Five Distributions')
    # ax.set_xlabel('Experimentos')
    ax.set_xlabel(beautiful_dataset_names[dataset_name] , fontsize=12)
    # ax.set_ylabel(plot_name)

    # Now fill the boxes with desired colors
    box_colors = ['darkkhaki', 'royalblue']
    num_boxes = len(data)
    medians = np.empty(num_boxes)
    for i in range(num_boxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        box_coords = np.column_stack([boxX, boxY])
        # Alternate between Dark Khaki and Royal Blue
        ax.add_patch(Polygon(box_coords, facecolor=box_colors[i % 2]))
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            ax.plot(medianX, medianY, 'k')
        medians[i] = medianY[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        ax.plot(np.average(med.get_xdata()), np.average(data[i]),
                color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
    ax.set_xlim(0.5, num_boxes + 0.5)
    ax.set_ylim(bottom, top)
    # ax.set_xticklabels(random_dists, rotation=45, fontsize=8)
    ax.set_xticklabels(random_dists)#, rotation=30)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(num_boxes) + 1
    upper_labels = [str(np.round(s, 2)) for s in medians]
    weights = ['bold', 'semibold']
    for tick, label in zip(range(num_boxes), ax.get_xticklabels()):
        k = tick % 2
        ax.text(pos[tick], 1.05, upper_labels[tick],
                transform=ax.get_xaxis_transform(),
                horizontalalignment='center', fontsize=10,
                weight=weights[k], color=box_colors[k])

    # Finally, add a basic legend
    # fig.text(0.80, 0.08, 'N Random Numbers', backgroundcolor=box_colors[0], color='black', weight='roman', size='x-small')
    # fig.text(0.80, 0.045, 'IID Bootstrap Resample',
    #          backgroundcolor=box_colors[1],
    #          color='white', weight='roman', size='x-small')
    # fig.text(0.80, 0.015, '*', color='white', backgroundcolor='silver',
    #          weight='roman', size='medium')
    # fig.text(0.815, 0.013, ' Average Value', color='black', weight='roman',
    #          size='x-small')
plt.tight_layout()
# plt.show()
plt.savefig('output/boxplot_all_{}.jpg'.format(plot_name))
