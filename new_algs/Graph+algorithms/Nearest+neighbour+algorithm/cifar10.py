from collections import Counter
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import pickle
from sklearn.model_selection import KFold, GridSearchCV, RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier

def print_same_line(string):
	sys.stdout.write('\r' + string)
	sys.stdout.flush()

"""
CIFAR-10 Dataset: "Learning Multiple Layers of Features from Tiny Images" Alex Krizhevsky, 2009.
"""
class CIFAR10:
        def __init__(self, data_path):
                """Extracts CIFAR10 data from data_path"""
                file_names = ['data_batch_%d' % i for i in range(1,6)]
                file_names.append('test_batch')
                X = []
                y = []
                for file_name in file_names:
                        with open(data_path + file_name,'rb') as fin:
                                data_dict = pickle.load(fin, encoding='bytes')
                                X.append(data_dict[b'data'].ravel())
                                y = y + data_dict[b'labels']

                #3072 comes from the 32x32 picture  size and color channels
                self.X = np.asarray(X).reshape(60000, 32*32*3)
                self.y = np.asarray(y)

                fin = open(data_path + 'batches.meta', 'rb')
                self.LABEL_NAMES = pickle.load(fin)['label_names']
                fin.close()

        def train_test_split(self):
                """Splits the data into testing set and training set."""
                X_train = self.X[:50000]
                y_train = self.y[:50000]
                X_test = self.X[50000:]
                y_test = self.y[50000:]
                return X_train, y_train, X_test, y_test

        def all_data(self):
                """Returns all data from the batches. For hyperparameter tuning
                and cross-validation."""
                return self.X, self.y

        def __prep_img(self, idx):
		"""Changes a given image to the proper format so that the AI can predict what class it's in."""
                img = self.X[idx].reshape(3,32,32).transpose(1,2,0).astype(np.uint8)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                return img

        def show_img(self, idx):
                """Shows an image at a given index with its label."""
                cv2.imshow(self.LABEL_NAMES[self.y[idx]], self.__prep_img(idx))
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        def show_examples(self):
                """Uses matplotlib to show 25 random example images from CIFAR10."""
                fig, axes = plt.subplots(5, 5)
                fig.tight_layout()
                for i in range(5):
                        for j in range(5):
                                rand = np.random.choice(range(self.X.shape[0]))
                                axes[i][j].set_axis_off()
                                axes[i][j].imshow(self.__prep_img(rand))
                                axes[i][j].set_title(self.LABEL_NAMES[self.y[rand]])
                plt.show()
		
class NearestNeighbor:
	def __init__(self, distance_func='l1'):
		self.distance_func = distance_func
		
	def train(self, X, y):
		"""X is an N x D matrix such that each row is a training example. y is a N x 1 matrix of true values."""
		self.X_tr = X.astype(np.float32)
		self.y_tr = y
		
	def predict(self, X):
		"""X is an M x D (3072) matrix such that each row is a testing example. Finds Nearest Neighbour by comparing the image
		to the training set of images."""
		X_te = X.astype(np.float32)
		num_test_examples = X.shape[0]
		y_pred = np.zeros(num_test_examples, self.y_tr.dtype)
		
		for i in range(num_test_examples):
			if self.distance_func == 'l2':
				distances = np.sum(np.square(self.X_tr - X_te[i]), axis=1)
			else:
				distances = np.sum(np.abs(self.X_tr - X_te[i]), axis=1)

			smallest_dist_idx = np.argmin(distances)
			y_pred[i] = self.y_tr[smallest_dist_idx]
		return y_pred
		
		

dataset = CIFAR10('./cifar-10-batches-py/')
X_train, y_train, X_test, y_test = dataset.train_test_split()
X, y = dataset.all_data()

dataset.show_examples()

#Uses the Nearest Neighbour algorithm on the first 100 images in the CIFAR10 dataset.
nn = NearestNeighbor()
nn.train(X_train, y_train)
y_pred = nn.predict(X_test[:100])

accuracy = np.mean(y_test[:100] == y_pred)
print (accuracy)

#Uses the K-Nearest Neighbour class from sklearn for comparison. Not coded from scratch.
knn = KNeighborsClassifier(n_neighbors=5, p=1, n_jobs=-1)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

accuracy = np.mean(y_test == y_pred)
print (accuracy)

#Uses grid search to help tune the hyperparameters.
param_grid = {'n_neighbors': [1, 3, 5, 10, 20, 50, 100], 'p': [1, 2]}
grid_search = GridSearchCV(knn, param_grid, cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)
print (grid_search.best_params_)


