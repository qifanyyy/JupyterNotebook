import tensorflow as tf
import numpy as np

from config_card_matching import CONFIG

class CardPatternMatchingCore(object):

    def __init__(self, hidden_dim=100, state_dim=128, batch_size=1, device='/cpu:0'):
        with tf.device(device):
            self.hidden_dim, self.state_dim, self.bsz = hidden_dim, state_dim, batch_size
            self.env_dim = CONFIG["ENVIRONMENT_ROW"] * CONFIG["ENVIRONMENT_DEPTH"]  # rows * cols
            self.arg_dim = CONFIG["ARGUMENT_NUM"] * CONFIG["ARGUMENT_DEPTH"]  # rows * cols
            self.program_dim = CONFIG["PROGRAM_EMBEDDING_SIZE"]

            # Setup Environment Input Layer
            self.env_in = tf.placeholder(tf.float32, shape=[self.bsz, self.env_dim], name="Env_Input")

            # Setup Argument Input Layer
            self.arg_in = tf.placeholder(tf.float32, shape=[self.bsz, self.arg_dim], name="Arg_Input")

            # Setup Program ID Input Layer
            self.prg_in = tf.placeholder(tf.int32, shape=[None, 1], name='Program_ID')

            # Build Environment Encoder Network (f_enc)
            self.state_encoding = self.f_enc()

            # Build Program Matrices
            PROGRAM_NUM = CONFIG['PROGRAM_NUM']
            self.program_key = tf.get_variable(name='Program_Keys',
                initializer=tf.truncated_normal_initializer()(shape=[PROGRAM_NUM, PROGRAM_NUM - 1]))

            with tf.device('/cpu:0'):
                self.program_embedding = self.build_program_store()


    def f_enc(self):
        """
        Build the Encoder Network (f_enc) taking the environment state (env_in) and the program
        arguments (arg_in), feeding through a Multilayer Perceptron, to generate the state encoding
        (s_t).
        Reed, de Freitas only specify that the f_enc is a Multilayer Perceptron => As such we use
        two ELU Layers, up-sampling to a state vector with dimension 128.
        Reference: Reed, de Freitas [9]
        """
        net = tf.concat((self.env_in, self.arg_in), axis=-1)
        net = tf.keras.layers.Dense(self.hidden_dim, activation=tf.keras.activations.elu)(net)
        net = tf.keras.layers.Dense(self.hidden_dim, activation=tf.keras.activations.elu)(net)
        net = tf.keras.layers.Dense(self.state_dim)(net)
        return net


    def build_program_store(self):
        """
        Build the Program Embedding (M_prog) that takes in a specific Program ID (prg_in), and
        returns the respective Program Embedding.
        Reference: Reed, de Freitas [4]
        """
        input_dim, output_dim = CONFIG['PROGRAM_NUM'], CONFIG['PROGRAM_EMBEDDING_SIZE']

        input_shape = self.prg_in.get_shape().as_list()
        assert len(input_shape) == 2, "Incoming Tensor shape must be 2-D"
        n_inputs = int(np.prod(input_shape[1:]))

        with tf.device('/cpu:0'):
            W = tf.get_variable("Program_Embedding_W",
                            initializer=tf.truncated_normal_initializer()(shape=[input_dim, output_dim]), trainable=True)

        inference = tf.cast(self.prg_in, tf.int32)
        inference = tf.nn.embedding_lookup(W, inference)
        inference = tf.transpose(inference, [1, 0, 2])
        inference = tf.reshape(inference, shape=[-1, output_dim])
        inference = tf.split(inference, n_inputs, 0)

        return inference