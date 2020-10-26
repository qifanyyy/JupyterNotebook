from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier, ExtraTreesClassifier, RandomForestClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier


class Model:
    @staticmethod
    def get_classifiers():
        return {
            'RandomForrest': RandomForestClassifier(n_estimators=250),
            'ExtraTrees': ExtraTreesClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2, random_state=0),
            'SupportVectorMachines': svm.SVC(),
            'Multinomial Naive Bayes': MultinomialNB(),
            'Gaussian Naive Bayes': GaussianNB(),
            'Neural Networks': MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1),
            'AdaBoost': AdaBoostClassifier(base_estimator=None, n_estimators=50, learning_rate=1.0, random_state=None),
            'Gradient Boosting': GradientBoostingClassifier(loss='deviance', learning_rate=0.1, n_estimators=5,
                                                            subsample=0.3, min_samples_split=2, min_samples_leaf=1,
                                                            max_depth=3, init=None, random_state=None,
                                                            max_features=None, verbose=2),
            'Decision Trees': DecisionTreeClassifier(max_depth=None, min_samples_split=2, random_state=0),
            '3KNN-BTREE': KNeighborsClassifier(n_neighbors=3, algorithm='ball_tree'),
            '3KNN': KNeighborsClassifier(n_neighbors=3)

        }
