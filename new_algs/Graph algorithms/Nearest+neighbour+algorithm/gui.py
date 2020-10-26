from tkinter import Label, Button, Entry, Tk
from rf import *
from knnPredictor import *
import matplotlib.pyplot as plt
import time
from sensitivity_specificity import true_false

class GUI:
	def __init__(self):
		accuracy = 0
		box = Tk()
		box.title("Heart Disease Prediction")
		box.minsize(400, 400)

		def rf_clicked():
			plt.close()

			rf_time = time.time()
			test = rf_algorithm()
			accuracy, plot_original, plot_predicted = test.rf_code()
			rf_total_time = time.time()-rf_time
			print("it took ",rf_total_time," to compute using RF")
			print("the accuracy is : ")
			print(accuracy*100)
			result1.config(text=accuracy*100)

			
			plt.plot(plot_original, 'ko', ms=0.8)
			plt.plot(plot_predicted, 'ro', ms=0.5)
			plt.show()

		def knn_clicked():
			plt.close()
			# prepare data
			temp = []
			trainingSet = []
			testSet = []
			split = 0.67

			knn_time = time.time()

			loadDataSet('pc.csv', split, trainingSet, testSet)
			print('Train set:' + repr(len(trainingSet)))
			print('Test set:' + repr(len(testSet)))
			# generate predictions
			predictions = []
			actual = []
			k = 11
			for x in range(len(testSet)):
				temp.append(float(testSet[x][-1]))
				neighbors = getNeighbors(trainingSet, testSet[x], k)
				result = getResponse(neighbors)
				predictions.append(result)
				actual.append(testSet[x][-1])
				print(('>predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1])))
			acc = getAccuracy(testSet, predictions)
			knn_total_time = knn_time - time.time()
			print("it took ",knn_total_time," to compute using KNN")
			print('Accuracy: ' + repr(acc) + '%')

			result2.config(text=acc)

			print("Confusion matrix is : ")
			cm = confusion_matrix(actual, predictions)
			print(cm)

			true_false(cm)

			plt.plot(predictions, 'ro', ms=2)
			plt.plot(temp, 'ko', ms=1.5)
			plt.show()

		rf_button = Button(box, text="random forest algorithm", command=rf_clicked).pack(pady=(20, 5))
		result1 = Label(box, text="click the button for Random Forest accuracy")
		result1.pack(pady=(20, 5))
		#box.mainloop()

		knn_button = Button(box, text="KNN algorithm", command=knn_clicked).pack(pady=(20, 5))
		result2 = Label(box, text="click the button for KNN accuracy")
		result2.pack(pady=(20, 5))

		# userPrediction_button = Button(box, text="User Prediction", command=userPrediction_clicked).pack(pady=(20, 5))
		# result2 = Label(box, text="Click the button for user prediction")
		# result2.pack(pady=(20, 5))

		box.mainloop()

if __name__ == '__main__':
	GUI()