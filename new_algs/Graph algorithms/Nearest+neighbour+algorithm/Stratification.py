import sys
import numpy
from lib.Instance import Instance
from lib.NaiveBayes import naive_bayes
from lib.KNearestNeighbour import k_nearest_neighbour


def parse_input_file(filename):
    yes_instances = []
    no_instances = []
    with open(filename, "r") as infile:
        for line in infile:
            attributes = line.split(',')
            for i in range(len(attributes)-1):
                attributes[i] = numpy.float(attributes[i])
            attributes[-1] = attributes[-1].replace('\n', '')
            instance = Instance(attributes=attributes[0:len(attributes)-1], class_variable=attributes[-1])
            if instance.class_variable == 'yes':
                yes_instances.append(instance)
            else:
                no_instances.append(instance)
    return yes_instances, no_instances


def write_output_file(folds):
    with open('pima-folds.csv', 'w') as outfile:
        count = 0
        for fold in folds:
            count += 1
            outfile.write('fold{}\n'.format(count))
            for instance in folds[fold]:
                outfile.write(convert_instance_to_string(instance))
            if count < 10:
                outfile.write('\n')


def make_folds(yes_instances, no_instances):
    folds = dict()
    for i in range(10):
        folds[i] = []
    i = 0
    while len(yes_instances) > 0:
        folds[i % 10].append(yes_instances.pop())
        i += 1
    while len(no_instances) > 0:
        folds[i % 10].append(no_instances.pop())
        i += 1

    for i in range(10):
        print(len(folds[i]))
    return folds


def convert_instance_to_string(instance):
    string = ",".join(instance.attributes)
    string = '{0},{1}\n'.format(string, instance.class_variable)
    return string


def ten_fold_cross_validation(folds):
    nb_accuracy = []
    one_nn_accuracy = []
    five_nn_accuracy = []
    for i in range(10):
        validation_instances = folds[i]
        training_instances = []
        for j in range(10):
            if j != i:
                training_instances += folds[j]
        nb_results = naive_bayes(testing_set=validation_instances,
                                 training_set=training_instances)
        one_nn_results = k_nearest_neighbour(training_set=training_instances,
                                             testing_set=validation_instances,
                                             k=1)
        five_nn_results = k_nearest_neighbour(training_set=training_instances,
                                              testing_set=validation_instances,
                                              k=5)
        # get accuracies
        nb_score = 0
        one_nn_score = 0
        five_nn_score = 0
        for k in range(len(validation_instances)):
            if nb_results[k] == validation_instances[k].class_variable:
                nb_score += 1
            if one_nn_results[k] == validation_instances[k].class_variable:
                one_nn_score += 1
            if five_nn_results[k] == validation_instances[k].class_variable:
                five_nn_score += 1
        nb_accuracy.append(nb_score/len(validation_instances))
        one_nn_accuracy.append(one_nn_score/len(validation_instances))
        five_nn_accuracy.append(five_nn_score / len(validation_instances))
        print('Round {} accuracy for Naive Bayes: {}'.format(i+1, nb_accuracy[i]))
        print('Round {} accuracy for 1-Nearest Neighbours: {}'.format(i + 1, one_nn_accuracy[i]))
        print('Round {} accuracy for 5-Nearest Neighbours: {}'.format(i + 1, five_nn_accuracy[i]))

    nb_average_acc = numpy.mean(nb_accuracy)
    one_nn_average_acc = numpy.mean(one_nn_accuracy)
    five_nn_average_acc = numpy.mean(five_nn_accuracy)
    print('Average accuracy for Naive Bayes: {}%'.format(nb_average_acc))
    print('Average accuracy for 1-Nearest Neighbours: {}%'.format(one_nn_average_acc))
    print('Average accuracy for 5-Nearest Neighbours: {}%'.format(five_nn_average_acc))


if __name__ in '__main__':
    input_file = sys.argv[1]
    yes, no = parse_input_file(input_file)
    stratified_folds = make_folds(yes, no)
    ten_fold_cross_validation(stratified_folds)
    # write_output_file(stratified_folds)
