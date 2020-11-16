import os
import numpy as np
import tensorflow as tf
import pickle

"""
The class for constructing network, training, evaluating and testing network
"""


class Network(object):
    def __init__(self, config):
        self.config = config

    def cnn_model(self, features, labels, mode, params):
        """ building a concrete cnn model function """

        # get a input layer by features and labels, its size is 128*128*1

        # with tf.device('/GPU:0'):
        input_layer = tf.reshape(
            tf.cast(features['fea'], dtype=tf.float32), [-1, 128, 128, 1])

        # get graph
        conv1 = self.conv_layer(input_layer, [3, 3, 1, 32], name="Conv_1")
        conv2 = self.conv_layer(
            conv1, [2, 2, 32, 64], keep_rate=0.8, name="Conv_2")
        conv3 = self.conv_layer(conv2, [2, 2, 64, 128],
                                keep_rate=0.7, name='Conv_3')
        conv_flat = tf.reshape(conv3, [-1, 16 * 16 * 128])
        with tf.variable_scope('FC_1'):
            fc1 = self.fc_layer(conv_flat, 16 * 16 * 128,
                                1000, name='FullConnect')
            drop1 = tf.nn.dropout(fc1, keep_prob=0.5, name='Dropout')
        with tf.variable_scope('FC_2'):
            fc2 = self.fc_layer(drop1, 1000, 200, name='FullConnect')
        output = self.fc_layer(
            fc2, 200, self.config['label_dim'], tf.nn.sigmoid, name='Output')
        # the shape of output is [batch_size, num_labels]

        prediction = {
            'index': tf.argmax(input=output, axis=1),
            "real_output": output
        }
        if mode == tf.estimator.ModeKeys.PREDICT:
            return tf.estimator.EstimatorSpec(mode=mode, predictions=prediction)

        # labels : the shape of [-1, num_solver]
        # labels must be multi-hot
        # onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=10)
        loss = tf.losses.log_loss(
            labels=labels, predictions=output, epsilon=1e-8)

        # decay learning rate and momentum
        lr = tf.Variable(0.3, name='learning_rate')
        mom = tf.Variable(0.9, name='momentum')
        lr_step = tf.constant(-0.003)
        mom_step = tf.constant(0.001)
        gs = tf.train.get_global_step()

        log_lr = tf.logical_and(tf.less(gs, 1000), tf.equal(tf.mod(gs, 10), 0))
        log_mom = tf.logical_and(
            tf.less(gs, 1000), tf.equal(tf.mod(gs, 10), 0))

        lr = tf.cond(log_lr, lambda: tf.assign_add(lr, lr_step), lambda: lr)
        mom = tf.cond(log_mom, lambda: tf.assign_add(
            mom, mom_step), lambda: mom)

        if mode == tf.estimator.ModeKeys.TRAIN:
            with tf.device('/GPU:0'):
                optimizer = tf.train.MomentumOptimizer(
                    learning_rate=lr, momentum=mom, use_nesterov=True)
                train_op = optimizer.minimize(
                    loss, global_step=tf.train.get_global_step())
            return tf.estimator.EstimatorSpec(
                mode=mode, loss=loss, train_op=train_op)

        # custom PAR10, Percentage solved and Misclassified solvers
        # PAR10 pre-result=the time of solver corresponding to selected index which has the most high value
        # last output is mean run time of evaluation data set

        eval_metric_ops = {
            "PAR10":
                self.PAR10(labels, features['runtime'], prediction['index'],
                           params['batch_size_of_eval'], params['num_label']),
            "Misclassified_solver":
                self.Mis(
                    labels, output, self.config['misclas_threshold'], params['batch_size_of_eval']),
            "Percentage_solverd":
                self.Percentage(labels, output, params['num_label'])
        }
        if mode == tf.estimator.ModeKeys.EVAL:
            return tf.estimator.EstimatorSpec(
                mode, loss=loss, eval_metric_ops=eval_metric_ops)

    @staticmethod
    def conv_layer(inputs,
                   kernel_shape,
                   kernel_stride=[1, 1, 1, 1],
                   activition=tf.nn.relu,
                   pool_ksize=[1, 2, 2, 1],
                   pool_stride=[1, 2, 2, 1],
                   keep_rate=0.9,
                   name="Conv"):
        """
        input shape: [batch, height, width, channel]
        kernel shape: [k_height, k_width, k_channel, k_count]
        bias shape: [k_count]
        """
        with tf.variable_scope(name):
            weight = tf.get_variable(
                name='Weight',
                shape=kernel_shape,
                initializer=tf.glorot_normal_initializer(dtype=tf.float32))
            bias = tf.get_variable(
                name='Bias',
                shape=[kernel_shape[-1]],
                initializer=tf.glorot_normal_initializer(dtype=tf.float32))
            conv = tf.nn.conv2d(
                inputs,
                weight,
                strides=kernel_stride,
                padding="SAME",
                name='Convolution_Op')
            act = activition(
                tf.nn.bias_add(conv, bias, data_format='NHWC'), name='Active_Op')
            pool = tf.nn.max_pool(
                act,
                ksize=pool_ksize,
                strides=pool_stride,
                padding='SAME',
                name='Pooling_Op')
            with tf.device('/CPU:0'):
                s_wei_name = '{}_weight'.format(name)
                s_bi_name = '{}_bias'.format(name)
                tf.summary.histogram(s_wei_name, weight)
                tf.summary.histogram(s_bi_name, bias)
            return tf.nn.dropout(pool, keep_prob=keep_rate, name='Dropout_Op')

    @staticmethod
    def fc_layer(inputs,
                 in_neurons,
                 out_neurons,
                 activition=tf.nn.relu,
                 name='FullConnect'):
        """
        inputs: shape of [batch, in_neurons, 1]
        """
        with tf.variable_scope(name):
            weight = tf.get_variable(
                name='Weight',
                shape=[in_neurons, out_neurons],
                initializer=tf.glorot_normal_initializer(dtype=tf.float32))
            bias = tf.get_variable(
                name='Bias',
                shape=[out_neurons],
                initializer=tf.glorot_normal_initializer(dtype=tf.float32))
            with tf.device('/CPU:0'):
                s_wei_name = '{}_weight'.format(name)
                s_bi_name = '{}_bias'.format(name)
                tf.summary.histogram(s_wei_name, weight)
                tf.summary.histogram(s_bi_name, bias)
            return activition(
                tf.nn.bias_add(tf.matmul(inputs, weight), bias), name='Active_Op')

    @staticmethod
    def PAR10(label, runtime, index, batch, solvers):
        """
        runtime: shape of [batch, num_of_solvers] -> [batch, num, 1]
        index: shape of [batch, 1] -> [batch, solvers, 1]
        """
        onehot = tf.one_hot(
            indices=tf.cast(index, tf.int32), depth=solvers)  # PARA
        onehot_ = tf.reshape(onehot, shape=(batch, solvers, 1))
        runtime_ = tf.reshape(runtime, shape=(batch, solvers, 1))

        penalized_label = -9 * label + 10
        re_penalized_label = tf.reshape(
            penalized_label, shape=(batch, solvers, 1))
        penalized_pre = tf.multiply(
            onehot_, tf.cast(re_penalized_label, tf.float32))

        pre_time = tf.multiply(penalized_pre, tf.cast(runtime_, tf.float32))
        mean_time, update_op = tf.metrics.mean(tf.reduce_sum(pre_time, axis=1))
        return mean_time, update_op

    @staticmethod
    def Mis(labels, predictions, threshold, batch):
        fn, update_op_fn = tf.metrics.false_negatives_at_thresholds(
            labels=labels, predictions=predictions, thresholds=threshold)
        fp, update_op_fp = tf.metrics.false_positives_at_thresholds(
            labels=labels, predictions=predictions, thresholds=threshold)
        fn_ = tf.reduce_sum(fn)
        fp_ = tf.reduce_sum(fp)
        return (tf.divide(tf.cast(tf.add(fn_, fp_), tf.float32), batch),
                tf.group(update_op_fn, update_op_fp))

    @staticmethod
    def Percentage(labels, predictions, solvers):
        onehot_pre = tf.one_hot(
            indices=tf.argmax(input=predictions, axis=1, output_type=tf.int32),
            axis=1,
            depth=solvers)
        return tf.metrics.precision(labels=labels, predictions=onehot_pre)


# def main():
#     Network.PAR10()
