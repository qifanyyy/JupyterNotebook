import numpy as np
import tensorflow as tf


"""
This is a custom class that uses TensorFlow to generate a neural network with two hidden layers
"""
class NeuronNetworkTwoHiddenLayer():

	"""
	This generate the neural network
	"""
	def neural_net(x):
		x_matrix = tf.reshape(x, [-1, self.num_input])
		# Hidden fully connected layer with 256 neurons
		layer_1 = tf.add(tf.matmul(x_matrix, self.weights['h1']), self.biases['b1'])
		# Hidden fully connected layer with 256 neurons
		layer_2 = tf.add(tf.matmul(layer_1, self.weights['h2']), self.biases['b2'])
		# Output fully connected layer with a neuron for each class
		out_layer = tf.matmul(layer_2, self.weights['out']) + self.biases['out']
		return out_layer


	"""
	Init the instance
	default values
		learning_rate=0.001;
		batch_size = 128;
		n_hidden_1 = 256;
		n_hidden_2 = 256;
		num_input = 22;
		num_classes = 2
	"""
	def __init__(self, learning_rate=0.001, batch_size = 128, n_hidden_1 = 256, n_hidden_2 = 256,num_input = 22, num_classes = 2):
		lr = learning_rate
		self.batch_size = batch_size
		n_hidden_1 = n_hidden_1
		n_hidden_2 = n_hidden_2
		self.num_input = num_input
		num_classes = num_classes
		self.X = tf.placeholder(tf.float32, [None], name="input")
		self.Y = tf.placeholder(tf.int32, [None, num_classes], name="outputY")

		self.weights = {
			'h1': tf.Variable(tf.random_normal([num_input, n_hidden_1])),
			'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
			'out': tf.Variable(tf.random_normal([n_hidden_2, num_classes]))
		}
		self.biases = {
			'b1': tf.Variable(tf.random_normal([n_hidden_1])),
			'b2': tf.Variable(tf.random_normal([n_hidden_2])),
			'out': tf.Variable(tf.random_normal([num_classes]))
		}

		x_matrix = tf.reshape(self.X, [-1, num_input])
		# Hidden fully connected layer with 256 neurons
		layer_1 = tf.add(tf.matmul(x_matrix, self.weights['h1']), self.biases['b1'])
		# Hidden fully connected layer with 256 neurons
		layer_2 = tf.add(tf.matmul(layer_1, self.weights['h2']), self.biases['b2'])
		# Output fully connected layer with a neuron for each class
		logits = tf.matmul(layer_2, self.weights['out']) + self.biases['out']


		sofmax_out = tf.nn.softmax(logits)
		# Define loss and optimizer
		out = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=self.Y)
		loss_op = tf.reduce_mean(out)
		optimizer = tf.train.AdamOptimizer(learning_rate=lr)
		self.train_op = optimizer.minimize(loss_op)

	
	"""
	Train the data
	"""
	def train(self, X_train, y_train):
		init = tf.global_variables_initializer()
		num_steps = int(X_train.shape[0]/self.batch_size)
		sess = tf.Session()

		# Run the initializer
		sess.run(init)

		for i in range(1, num_steps+1):
			batch_x = X_train[(i-1)*self.batch_size: (i-1)*self.batch_size + self.batch_size] #take a block of 128 instances
			batch_y = y_train[(i-1)*self.batch_size: (i-1)*self.batch_size + self.batch_size] #take a block of 128 instances
			batch_x = batch_x.ravel().astype(np.float32)

			# Run optimization op (backprop)
			sess.run(self.train_op, feed_dict={self.X: batch_x, self.Y: batch_y})


		self.W1 = self.weights['h1'].eval(sess)
		self.B1 = self.biases['b1'].eval(sess)
		self.W2 = self.weights['h2'].eval(sess)
		self.B2 = self.biases['b2'].eval(sess)
		self.W_OUT = self.weights['out'].eval(sess)
		self.B_OUT = self.biases['out'].eval(sess)

		sess.close()
		del sess
		del init

	"""
	Clear the memory
	"""
	def clear(self):
		del self.W1 
		del self.B1
		del self.W2 
		del self.B2
		del self.W_OUT
		del self.B_OUT
		del self.weights
		del self.biases
		del self.X
		del self.Y
		del self.batch_size
		del self.train_op


	"""
	Test the model
	The function returns the prediction y vector
	"""
	def predict(self, X_test):

		sess = tf.Session()
		init = tf.global_variables_initializer()
		sess.run(init)

		#create the input parameter which is a vector
		x_2 = tf.placeholder(tf.float32, shape=[X_test.ravel().shape[0]], name="input_x_2")

		#reshape the vector into a matrix, this has to be done because the the op matmul
		#requires two matrix's
		x_22 = tf.reshape(x_2, [-1, self.num_input])

		#create each weight and each biase with the final value
		W1_C = tf.constant(self.W1, name="W1")
		B1_C = tf.constant(self.B1, name="B1")
		W2_C = tf.constant(self.W2, name="W2")
		B2_C = tf.constant(self.B2, name="B2")
		W_OUT_C = tf.constant(self.W_OUT, name="W_OUT")
		B_OUT_C = tf.constant(self.B_OUT, name="B_OUT")


		# the two layers as used in neural_net()
		layer_1 = tf.add(tf.matmul(x_22, W1_C, name="matmul_x_22_w1_c"), B1_C, name="add_matmul1_b1_c")
		layer_2 = tf.add(tf.matmul(layer_1, W2_C, name="matmul_l_1_w1_c"), B2_C, name="add_matmul2_b2_c")
		#the output value of the classifier with the name output
		OUTPUT = tf.nn.softmax(tf.matmul(layer_2, self.W_OUT, name="matmul_l_2_wout_c") + self.B_OUT, name="output")


		#print(sess.run(self.weights.get('h1')))

		y_out= sess.run(OUTPUT, feed_dict={x_2: X_test.ravel()})
		sess.close()
		del sess
		del init
		return y_out


	"""
	Create the model by default in the /model/ folder with the model.pb name
	"""
	def create_model(self, path='/model/', name='model.pb'):
		init = tf.global_variables_initializer()

		g = tf.Graph()
		with g.as_default():

			sess = tf.Session()
			init = tf.global_variables_initializer()
			sess.run(init)

			W1 = self.weights['h1'].eval(sess)
			B1 = self.biases['b1'].eval(sess)
			W2 = self.weights['h2'].eval(sess)
			B2 = self.biases['b2'].eval(sess)
			W_OUT = self.weights['out'].eval(sess)
			B_OUT = self.biases['out'].eval(sess)

			# this steps are the same as the function neural_net() but instead of random values will 
			# take the value in every weight and every bias at the end of the classifier

			#create the input parameter which is a vector
			x_2 = tf.placeholder(tf.float32, shape=[None], name="input")

			#reshape the vector into a matrix, this has to be done because the the op matmul
			#requires two matrix's
			x_22 = tf.reshape(x_2, [-1, self.num_input])

			#create each weight and each biase with the final value
			W1_C = tf.constant(W1, name="W1")
			B1_C = tf.constant(B1, name="B1")
			W2_C = tf.constant(W2, name="W2")
			B2_C = tf.constant(B2, name="B2")
			W_OUT_C = tf.constant(W_OUT, name="W_OUT")
			B_OUT_C = tf.constant(B_OUT, name="B_OUT")


			# the two layers as used in neural_net()
			layer_1 = tf.add(tf.matmul(x_22, W1_C, name="matmul_x_22_w1_c"), B1_C, name="add_matmul1_b1_c")
			layer_2 = tf.add(tf.matmul(layer_1, W2_C, name="matmul_l_1_w1_c"), B2_C, name="add_matmul2_b2_c")
			#the output value of the classifier with the name output
			OUTPUT = tf.nn.softmax(tf.matmul(layer_2, W_OUT, name="matmul_l_2_wout_c") + B_OUT, name="output")


			# skipped dropout for exported graph as there is no need for already calculated weights
			

			graph_def = g.as_graph_def()

			#create the model model_graph.pb
			tf.train.write_graph(graph_def, path, name, as_text=False)

