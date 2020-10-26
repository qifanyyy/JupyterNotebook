import sys
from KNN import KNN
from NB import NB


def main():
    train_filename = sys.argv[1]
    # This command is to cross validate the given training data set
    if sys.argv[2] == 'cross_validate':
        # cross validate the given training data set with kNN algorithm
        if sys.argv[3][1] == 'N':
            k_value = int(sys.argv[3][0])
            knn = KNN()
            print(knn.cross_validation(k_value, train_filename))
        # cross validate the given training data set with NB algorithm
        else:
            nb = NB()
            print(nb.cross_validation(train_filename))

    # This command will generate a 10‐fold stratified data with given train dataset in required format
    # The required format is described in assignment documentation
    elif sys.argv[2] == 'write_stratification':
        knn = KNN()
        knn.writeStratification(train_filename, "10_folds_stratified.csv")
    else:
        test_filename = sys.argv[2]
        if sys.argv[3][1] == 'N':
            k_value = int(sys.argv[3][0])
            knn = KNN()
            train_dataset = knn.getData(train_filename)
            test_data = knn.getData(test_filename)
            train_data, label_data = knn.splitAttributeLabels(train_dataset)
            results = knn.knn_predict(train_data, label_data, test_data, k_value)
            for i in results:
                print(i)
        elif sys.argv[3] == 'NB':
            nb = NB()
            train_data = nb.getTrainData(train_filename)
            test__data = nb.getTestData(test_filename)
            result = nb.getPredictions(test__data, train_data)
            for i in range(len(result)):
                if result[i][-1] == 1:
                    print('yes')
                else:
                    print('no')



if __name__ == '__main__':
    main()
