import sonnet as snt
import tensorflow as tf
import numpy as np
import json
import time
import datetime

from sklearn.preprocessing import MinMaxScaler


def parse_labels(tool1, tool2, labels, major=None):
    o = []

    pos = 0
    neg = 0

    for L in labels:
        l1 = 100
        l2 = 100

        for i, label in enumerate(L):
            if label == tool1:
                l1 = i
            elif label == tool2:
                l2 = i
            elif isinstance(label, list):
                if tool1 in label:
                    l1 = i
                if tool2 in label:
                    l2 = i

        assert(l1 < 100 and l2 < 100)

        if l1 < l2:
            pos += 1
            o.append(1)
        elif l2 < l1:
            neg += 1
            o.append(0)
        else:
            o.append(-1)

    o = np.array(o)
    if major is None:
        major = pos > neg

    o[np.where(o == -1)] = 1 if major else 0

    return o, major


def load_binary_data(tool1, tool2):
    start = time.time()

    train = np.genfromtxt("train.csv", delimiter="\t")
    test = np.genfromtxt("test.csv", delimiter="\t")

    with open("train_labels.json", "r") as inp:
        train_labels, major = parse_labels(
            tool1, tool2, json.load(inp)
        )

    with open("test_labels.json", "r") as inp:
        test_labels, _ = parse_labels(
            tool1, tool2, json.load(inp), major
        )

    scaler = MinMaxScaler()
    train = scaler.fit_transform(train)
    test = scaler.transform(test)

    train_dataset = tf.data.Dataset.from_tensor_slices((train, train_labels))
    test_dataset = tf.data.Dataset.from_tensor_slices((test, test_labels))

    acc = (test_labels == (1 if major else 0)).sum() / float(test_labels.shape[0])

    print("Load dataset for %s and %s in %f seconds (Default accuracy: %f)"\
          % (tool1, tool2, (time.time() - start), acc))

    return train_dataset, test_dataset


def mlp_train(training_iteration):

    precision = tf.float64
    learning_rate = 0.001

    train_dataset, test_dataset = load_binary_data("Klee", "ESBMC-incr")

    test_dataset = test_dataset.batch(420).repeat()
    test_iter = test_dataset.make_one_shot_iterator()

    train_dataset = train_dataset.shuffle(1024).repeat().batch(128)
    train_iter = train_dataset.make_one_shot_iterator()

    x, y = train_iter.get_next()

    x = tf.cast(x, precision)
    y = tf.cast(y, precision)

    initializers={"w": tf.truncated_normal_initializer(stddev=0.1),
              "b": tf.truncated_normal_initializer(stddev=0.1)}
    regularizers = {"w": tf.contrib.layers.l1_regularizer(scale=1.0),
                    "b": tf.contrib.layers.l1_regularizer(scale=1.0)}

    with tf.name_scope("MLP") as scope:
        model = snt.Linear(1, initializers=initializers, regularizers=regularizers)

    train_prediction = model(x)

    tf.summary.histogram("W", model.w)
    tf.summary.histogram("b", model.b)
    tf.summary.histogram("prediction", tf.sigmoid(train_prediction))

    graph_regularizers = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
    total_regularization_loss = tf.reduce_sum(graph_regularizers)

    with tf.name_scope("cost_function") as scope:
        train = tf.reshape(train_prediction, [-1])
        cost_function = tf.reduce_sum(
                            tf.nn.sigmoid_cross_entropy_with_logits(labels=y, logits=train)
                        )
        cost_function = cost_function + total_regularization_loss
        train_accuracy = tf.reduce_mean(
            tf.cast(
                tf.equal(
                    tf.round(tf.sigmoid(train_prediction)), y
                ), precision)
        )

        tf.summary.scalar("cost_function", cost_function)
        tf.summary.scalar("train_accuracy", train_accuracy)

    with tf.name_scope("train") as scope:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost_function)

    x_test, y_test = test_iter.get_next()
    x_test = tf.cast(x_test, precision)
    y_test = tf.cast(y_test, precision)

    with tf.name_scope("accuracy") as scope:
        test_prediction = model(x_test)
        test_accuracy = tf.reduce_mean(
            tf.cast(
                tf.equal(
                    tf.round(tf.sigmoid(test_prediction)), y_test
                ), precision)
        )
        # tf.summary.scalar("test_accuracy", test_accuracy)

    init = tf.global_variables_initializer()
    merged_summary_op = tf.summary.merge_all()

    time_string = datetime.datetime.now().isoformat()

    name = f"MLP_Test_{time_string}"

    with tf.Session() as sess:
        sess.run(init)

        summary_writer = tf.summary.FileWriter("/Users/cedricrichter/Documents/Arbeit/Ranking/GCNSelection/summary/"+name, graph=sess.graph)

        for epoch in range(training_iteration):

            for _ in range(120):
                _, loss, acc = sess.run([optimizer, cost_function, train_accuracy])

            print("Iteration %d Loss %f" % (epoch, loss))
            summary_str = sess.run(merged_summary_op)
            summary_writer.add_summary(summary_str, 120*epoch)
        test_acc = sess.run(test_accuracy)
        print("Test accuracy: %f" % test_acc)


if __name__ == '__main__':
    mlp_train(300)
