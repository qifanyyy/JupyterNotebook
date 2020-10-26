"""
    Author: Marina Ibrishimova
    Purpose: Fimal project for ECE 569A
    Title: Feature Selection Using Genetic Algorithm
    Description: contains 3 different Genetic algorithms
    which differ in how the population changes
    from one generation to the next:
    - steadystate: the two chromosomes with the highest fitness mate and produce 2
    children while the remaining 2 survive to the next generation
    if manhattan distance between a child and another individual is smaller than 20,
    replace individual using mutation function
    - generational: 4 offspring individuals are generated, where 4 is the population size,
    and the entire population is replaced
"""
import math
import random
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.datasets import make_classification
from sklearn.metrics import log_loss
import tensorflow as tf
from tensorflow.python.data import Dataset

tf.logging.set_verbosity(tf.logging.ERROR)
pd.options.display.max_rows = 10
pd.options.display.float_format = '{:.1f}'.format

#needed during mutation
def manhattan_d(x,y):
    return sum(abs(a-b) for a,b in zip(x,y))

#function to generate a synthetic dataset with 1000 examples
def generate_dataset():
    x, y = make_classification(n_samples=300, n_features=100, random_state=0)
    ds = np.column_stack([x, y]).tolist()
    np.savetxt('c.csv', ds, delimiter=',')

dataframe = pd.read_csv("c.csv", sep=",")

#returns accuracy of the model using a given set of selected features
#uses linear classifier as described in Google Developers' ML Course
def fitness_func(selected, dataframe):
    def preprocess_features(dataframe):
      """Prepares input features
      Args:
         A Pandas DataFrame expected to contain data
          from the data set.
      Returns:
        A DataFrame that contains the features to be used for the model, including
        synthetic features.
      """
      selected_features = dataframe[selected]
      processed_features = selected_features.copy()
      return processed_features

    def preprocess_targets(dataframe):
      """Prepares target features (i.e., labels) from data set.

      Args:
         A Pandas DataFrame expected to contain data
          from the synthetic dataset.
      Returns:
        A DataFrame that contains the target feature.
      """
      output_targets = pd.DataFrame()
      output_targets["Target1"] = dataframe["Target1"];
      return output_targets

    # Choose the first 12000 (out of 17000) examples for training.
    training_examples = preprocess_features(dataframe.head(200))
    training_targets = preprocess_targets(dataframe.head(200))
    # Choose the last 5000 (out of 17000) examples for validation.
    validation_examples = preprocess_features(dataframe.tail(100))
    validation_targets = preprocess_targets(dataframe.tail(100))


    def construct_feature_columns(input_features):
      """Construct the TensorFlow Feature Columns.

      Args:
        input_features: The names of the numerical input features to use.
      Returns:
        A set of feature columns
      """
      return set([tf.feature_column.numeric_column(my_feature)
                  for my_feature in input_features])

    def my_input_fn(features, targets, batch_size=1, shuffle=True, num_epochs=None):
        """Trains a linear regression model of multiple features.

        Args:
          features: pandas DataFrame of features
          targets: pandas DataFrame of targets
          batch_size: Size of batches to be passed to the model
          shuffle: True or False. Whether to shuffle the data.
          num_epochs: Number of epochs for which data should be repeated. None = repeat indefinitely
        Returns:
          Tuple of (features, labels) for next data batch
        """

        # Convert pandas data into a dict of np arrays.
        features = {key:np.array(value) for key,value in dict(features).items()}
        if targets is None:
            # No labels, use only features.
            inputs = features
        else:
            inputs = (features, targets)
        # Construct a dataset, and configure batching/repeating.
        ds = Dataset.from_tensor_slices(inputs) # warning: 2GB limit
        ds = ds.batch(batch_size).repeat(num_epochs)


        # Shuffle the data, if specified.
        if shuffle:
          ds = ds.shuffle(100)

        # Return the next batch of data.
        return ds.make_one_shot_iterator().get_next()

    def eval_input_fn(features, labels=None, batch_size=None):
        """An input function for evaluation or prediction"""
        if labels is None:
            # No labels, use only features.
            inputs = features
        else:
            inputs = (features, labels)

        # Convert inputs to a tf.dataset object.
        dataset = tf.data.Dataset.from_tensor_slices(inputs)

        # Batch the examples
        assert batch_size is not None, "batch_size must not be None"
        dataset = dataset.batch(batch_size)

        # Return the read end of the pipeline.
        return dataset.make_one_shot_iterator().get_next()

    def train_linear_classifier_model(
        learning_rate,
        steps,
        batch_size,
        training_examples,
        training_targets,
        validation_examples,
        validation_targets):
      """Trains a linear classification model.

      Args:
        learning_rate: A `float`, the learning rate.
        steps: A non-zero `int`, the total number of training steps. A training step
          consists of a forward and backward pass using a single batch.
        batch_size: A non-zero `int`, the batch size.
        training_examples: A `DataFrame` containing one or more columns from
          `incident_dataframe` to use as input features for training.
        training_targets: A `DataFrame` containing exactly one column from
          `incident_dataframe` to use as target for training.
        validation_examples: A `DataFrame` containing one or more columns from
          `incident_dataframe` to use as input features for validation.
        validation_targets: A `DataFrame` containing exactly one column from
          `incident_dataframe` to use as target for validation.

      Returns:
        A `LinearClassifier` object trained on the training data."""


      periods = 1
      steps_per_period = steps / periods

      # Create a linear classifier object.
      my_optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
      my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(my_optimizer, 5.0)
      linear_classifier = tf.estimator.LinearClassifier(
          feature_columns=construct_feature_columns(training_examples),
          optimizer=my_optimizer
      )

      # Create input functions.
      training_input_fn = lambda: my_input_fn(training_examples,
                                              training_targets["Target1"],
                                              batch_size=batch_size)
      predict_training_input_fn = lambda: my_input_fn(training_examples,
                                                      training_targets["Target1"],
                                                      num_epochs=1,
                                                      shuffle=False)
      predict_validation_input_fn = lambda: my_input_fn(validation_examples,
                                                        validation_targets["Target1"],
                                                        num_epochs=1,
                                                        shuffle=False)

      # Train the model
      training_log_losses = []
      validation_log_losses = []
      for period in range (0, periods):
        # Train the model, starting from the prior state.
        linear_classifier.train(
            input_fn=training_input_fn,
            steps=steps_per_period
        )
        # Take a break and compute predictions.
        training_probabilities = linear_classifier.predict(input_fn=predict_training_input_fn)
        training_probabilities = np.array([item['probabilities'] for item in training_probabilities])

        validation_probabilities = linear_classifier.predict(input_fn=predict_validation_input_fn)
        validation_probabilities = np.array([item['probabilities'] for item in validation_probabilities])

        training_log_loss = metrics.log_loss(training_targets, training_probabilities)
        validation_log_loss = metrics.log_loss(validation_targets, validation_probabilities)
        # Occasionally print the current loss.
        #print ("  period %02d : %0.2f" % (period, training_log_loss))
        # Add the loss metrics from this period to our list.
        training_log_losses.append(training_log_loss)
        validation_log_losses.append(validation_log_loss)

      evaluation_metrics = linear_classifier.evaluate(input_fn=predict_validation_input_fn)

      print ("---Fitness: %0.2f ---" % evaluation_metrics['accuracy'])

      return evaluation_metrics['accuracy']

    fitness = train_linear_classifier_model(
        learning_rate=0.05,
        steps=10,
        batch_size=2,
        training_examples=training_examples,
        training_targets=training_targets,
        validation_examples=validation_examples,
        validation_targets=validation_targets)
    return fitness

#function to encode phenotype to genotype
def encode_features_phengen(chromosome,dataset):
    i = 0
    selected = []
    for x in chromosome:
        if x == 1:
            selected.append(dataset.columns.get_values()[i])
        i = i + 1
    return selected

#function to introduce new genetic material
#uses manhattan distance to determine how close
#chromosome is to another chromosome
def mutation_func(chromoa):
    chromob = np.random.choice(2,100).tolist()
    if manhattan_d(chromoa,chromob) > 20:
        return chromob
    else:
        return mutation_func(chromoa)

#mating function to create a new chromosome
#from two other chromosomes
def crossover_func(x,y,flag):
    if(flag==0):
        parenta= x[:50]
        parentb= y[:50]
    else:
        parenta= x[50:100]
        parentb= y[50:100]
    child = parenta + parentb
    return child

# checks fitness function for each chromosome in the current generation
# adds chromosomes and corresponding fitness values to a 2D array
# sorts the array by fitness value so that the
# chromososme with the highest fitness is at the top of the array
def selection_func(sample):
    cntr = 0
    for i in sample:
        print("---Chromosome:---")
        print(i[0])
        feat_vals = encode_features_phengen(i[0],dataframe)
        candidate = fitness_func(feat_vals, dataframe)
        sample[cntr].append(candidate)
        cntr = cntr +1
    #sort sampl by secondcolumn (candidate value)
    sample = sorted(sample, key=lambda x: x[1], reverse=True)
    return sample

"""
    Elitist Generational GA:
    4 offspring individuals are generated, where 4 is the population size,
    and the entire population is replaced but only the two best individuals
    are allowed to mate;
    mutation is introduced at every generation.
    creates new chromosome from two most fit candidates by splitting
    them in half and taking the first half of the first one and second half of second
    one and vice versa
    terminates if the chromosome with the highest fitness in population > 0.8
    or if 10 generations have gone through without finding a solution
"""
def elitist_generational_ga_func(sample, gen_num):
    newsampl = []
    gen = selection_func(sample)
    print(gen[0][1])
    if(gen[0][1] > 0.8):
        print("Solution found:")
        #print the chromosome
        print(gen[0][0])
        #print chromosome's fitness
        print(gen[0][1])
        return gen[0][0]
    else:
        print("---------------New Population---------------")
        del newsampl[:]
        child1 = crossover_func(gen[0][0],gen[1][0],0)
        child2 = crossover_func(gen[0][0],gen[1][0],1)
        mutantchild1 = mutation_func(child1)
        mutantchild2 = mutation_func(child2)
        newsampl.append([])
        newsampl[0].append(child1)
        newsampl.append([])
        newsampl[1].append(child2)
        newsampl.append([])
        newsampl[2].append(mutantchild1)
        newsampl.append([])
        newsampl[3].append(mutantchild2)
        print("Generation number is:")
        print(gen_num)
        if (gen_num > 10):
            print("Solution not found:")
            return 0
        else:
            gen_num = gen_num + 1
            return elitist_generational_ga_func(newsampl,gen_num)
"""
    Pure Generational GA:
    4 offspring individuals are generated, where 4 is the population size,
    and the entire population is replaced
    mutation only when the population starts degenerating.
    creates new chromosome from two most fit candidates by splitting
    them in half and taking the first half of the first one and second half of second
    one and vice versa
    terminates if the chromosome with the highest fitness in population > 0.8
    or if 10 generations have gone through
"""
def pure_generational_ga_func(sample, gen_num):
    newsampl = []
    gen = selection_func(sample)
    print(gen[0][1])
    if(gen[0][1] > 0.8):
        print("Solution found:")
        #print the chromosome
        print(gen[0][0])
        #print chromosome's fitness
        print(gen[0][1])
        return gen[0][0]
    else:
        print("---------------New Population---------------")
        del newsampl[:]
        child1 = crossover_func(gen[0][0],gen[1][0],0)
        child2 = crossover_func(gen[0][0],gen[1][0],1)
        child3 = crossover_func(gen[2][0],gen[3][0],0)
        child4 = crossover_func(gen[2][0],gen[2][0],1)
        if (manhattan_d(child4,child1) < 20 or manhattan_d(child4,child2) < 20 or manhattan_d(child4,child3) < 20):
            child4 = mutation_func(gen[2][0])
        newsampl.append([])
        newsampl[0].append(child1)
        newsampl.append([])
        newsampl[1].append(child2)
        newsampl.append([])
        newsampl[2].append(child3)
        newsampl.append([])
        newsampl[3].append(child4)
        print("Generation number is:")
        print(gen_num)
        if (gen_num > 10):
            print("Solution not found:")
            return 0
        else:
            gen_num = gen_num + 1
            return pure_generational_ga_func(newsampl,gen_num)

"""
    Steady state selection GA for comparison
    the two chromosomes with the highest fitness mate and produce 2
    children while the remaining 2 survive to the next generation
    if manhattan distance between a child and another individual is smaller than 20,
    replace individual using mutation function
"""
def steadystate_ga_func(sample, gen_num):
    newsampl = []
    gen = selection_func(sample)
    print("--------------------------------------------")
    if(gen[0][1] > 0.8):
        print("Solution found:")
        #print the chromosome
        print(gen[0][0])
        #print chromosome's fitness
        print(gen[0][1])
        return gen[0][0]
    else:
        print("---------------New Population---------------")
        del newsampl[:]
        child1 = crossover_func(gen[0][0],gen[1][0], 0)
        child2 = crossover_func(gen[0][0],gen[1][0], 1)
        chromo3 = gen[2][0]
        if (manhattan_d(gen[3][0],child1)< 20 or manhattan_d(gen[3][0],child2) < 20 or manhattan_d(gen[3][0],chromo3) < 20):
            chromo4 = mutation_func(gen[3][0])
        else:
            chromo4 = gen[3][0]
        newsampl.append([])
        newsampl[0].append(child1)
        newsampl.append([])
        newsampl[1].append(child2)
        newsampl.append([])
        newsampl[2].append(chromo3)
        newsampl.append([])
        newsampl[3].append(chromo4)
        print("Generation number is:")
        print(gen_num)
        if (gen_num > 10):
            print("Solution not found:")
            return 0
        else:
            gen_num = gen_num + 1
            return steadystate_ga_func(newsampl,gen_num)

#initializes the genetic algorithm with semi-random population
def init_func():
    chromo1 = np.random.choice(2,100).tolist()
    chromo2 = mutation_func(chromo1)
    chromo3 = mutation_func(chromo2)
    chromo4 = mutation_func(chromo3)
    print("---------------First Population---------------")
    print("Generation number is 1")
    sampl = []
    sampl.append([])
    sampl[0].append(chromo1)
    sampl.append([])
    sampl[1].append(chromo2)
    sampl.append([])
    sampl[2].append(chromo3)
    sampl.append([])
    sampl[3].append(chromo4)
    #try different GA variations by uncommenting
    #starts = elitist_generational_ga_func(sampl,2)
    starts = pure_generational_ga_func(sampl,2)
    #starts = steadystate_ga_func(sampl,2)
    return starts

init_func()
