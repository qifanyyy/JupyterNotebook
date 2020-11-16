import torch

import data_handler as dh
import train_net as trn
import test_net as tst
from construct_model import construct_model

MODEL_SAMPLING = 25


def main_relevance(df_all):
    """
    Automatically reduce our network size by removing inputs that we deemed irrelevant by neuron relevance.
    We iteratively reduce the network until empty, returning best performing network (via sampling).
    """
    training_results = dict()  # store standard errors
    test_results = dict()  # store accuracy
    global_model = dict()  # store best local model
    validation_pruned = dict()  # validation df
    model_pruned = True

    # get validation data set (10% of data set)
    validation_df, in_sample_df = dh.split_data(df_all, 0.1)
    validation_pruned[len(in_sample_df.columns) - 1] = validation_df

    while len(in_sample_df.columns) - 1 >= 1 and model_pruned:
        total_error = 0
        total_accuracy = 0
        local_best = [0, 0]

        for i in range(MODEL_SAMPLING):
            # get training and validation data sets
            train_df, test_df = dh.split_data(in_sample_df, 0.63)

            training_array = train_df.as_matrix()
            # split x (features) and y (target)
            x_array, y_array = training_array[:, 1:], training_array[:, 0]
            # create Tensors to hold inputs and outputs, and wrap them in Variables,
            x = torch.tensor(x_array, dtype=torch.float, requires_grad=True)
            y = torch.tensor(y_array, dtype=torch.float, requires_grad=False)

            # construct and train model
            model, optimiser, trained_model, model_se = construct_model(x, y)

            # test the nn using test data
            model_accuracy = tst.test_net(trained_model, test_df)
            # evaluate model data
            total_error = total_error + model_se
            total_accuracy = total_accuracy + model_accuracy
            if model_accuracy > local_best[1]: local_best = [trained_model, model_accuracy]

        # update dictionary and global best model
        training_results[len(in_sample_df.columns) - 1] = total_error / MODEL_SAMPLING
        test_results[len(in_sample_df.columns) - 1] = total_accuracy / MODEL_SAMPLING
        global_model[len(in_sample_df.columns) - 1] = local_best[0]

        # prune model based on relevance measure on inputs
        prune_input = trn.get_min_phat(model, x, y, optimiser)
        if prune_input is not None:
            in_sample_df = trn.remove_input(in_sample_df, prune_input)
            prior_val_df = validation_pruned[len(in_sample_df.columns)]
            validation_pruned[len(in_sample_df.columns) - 1] = trn.remove_input(prior_val_df, prune_input)
            print("Model has been pruned to include " + str(len(in_sample_df.columns) - 1) +
                  " inputs. Best performance was " + str(local_best[1])
                  + ". Average performance was " + str(total_accuracy / MODEL_SAMPLING))
            print(in_sample_df.columns.values)
        else:
            model_pruned = False

    # select best model, and test validation set
    best_acc = max(test_results, key=test_results.get)
    best_model = global_model[best_acc]
    validation_results = tst.test_net(best_model, validation_pruned[best_acc])

    dh.plot_data(test_results, training_results)
    print("the best model had " + str(best_acc) + " inputs, with " + str(test_results[best_acc]) + " accuracy.")
    print("validation results: " + str(validation_results))
    return best_model


if __name__ == "__main__":
    df = dh.get_data()  # returns data frame
    print(main_relevance(df))
