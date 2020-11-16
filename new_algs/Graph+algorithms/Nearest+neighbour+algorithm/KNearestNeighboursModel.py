import numpy as np
import numpy.linalg as LA

class KNearestNeighboursModel:
    __train_X, __train_y = None, None
    __pred_class, __pred_prob = None, None
    __k_neighbours = None

    def __L2(self, X, train_data_X):
        X = X[:, np.newaxis, ...]
        train_data_X = train_data_X[np.newaxis, ...]
        delta = X - train_data_X
        distance_table = LA.norm(delta, axis=2)
        # print_ndarray(distance_table, 'distance_table')
        return distance_table

    def __get_top_predictions(self, X, distance_table):
        I = np.argsort(distance_table, axis=1)
        I = I[:, :self.__k_neighbours]
        # print_ndarray(I, 'I')

        get_y = lambda x: self.__train_y[x]
        candidate_y = get_y(I)
        # print_ndarray(candidate_y, 'top_predictions')
        return candidate_y

    def __elect_y(self, top_predictions):
        all_classes = np.unique(self.__train_y)
        class_membership = (all_classes[np.newaxis, np.newaxis, :] ==
                top_predictions[..., np.newaxis])
        # print_ndarray(class_membership, 'class_membership')
        class_freq = np.sum(class_membership, axis=1)
        # print_ndarray(class_freq, 'class_freq')
        pred_class_ix = np.argmax(class_freq, axis=1)
        pred_class_freq = np.max(class_freq, axis=1)
        # print_ndarray(pred_class_freq, 'pred_class_freq')

        get_y = lambda x: all_classes[x]
        pred_class = get_y(pred_class_ix)
        pred_prob = pred_class_freq / self.__k_neighbours
        # print_ndarray(pred_class, 'pred_class')
        # print_ndarray(pred_prob, 'pred_prob')
        return pred_class, pred_prob

    def __init__(self, k_neighbours=3):
        self.__k_neighbours = k_neighbours

    def fit(self, X, y):
        self.__train_X = X
        self.__train_y = y

    def predict(self, X):
        if (self.__train_X is None or
                self.__train_y is None or
                self.__k_neighbours is None):
            # Should we raise exception?
            return None

        # print_ndarray(self.__train_y, 'train_y')

        distance_table = self.__L2(X, self.__train_X)
        top_predictions = self.__get_top_predictions(X, distance_table)
        (self.__pred_class, self.__pred_prob) = self.__elect_y(top_predictions)

        return self.__pred_class

    def predict_proba(self, X):
        if self.__pred_prob is None:
            if self.predict(X) is None:
                return None

        return self.__pred_prob


def print_ndarray(arr, arr_name):
    print('{arr_name} = {arr}'.format(arr_name=arr_name, arr=arr))

