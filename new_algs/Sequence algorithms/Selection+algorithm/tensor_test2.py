import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
import json
import time
import datetime
import sonnet as snt


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

    acc = (test_labels == (1 if major else 0)).sum() / float(test_labels.shape[0])

    print("Load dataset for %s and %s in %f seconds (Default accuracy: %f)"\
          % (tool1, tool2, (time.time() - start), acc))

    # Sanity check
    clf = LogisticRegression()
    clf.fit(train, train_labels)

    train_score = clf.score(train, train_labels)
    test_score = clf.score(test, test_labels)

    print("Logistic Regression Sanity check: Train %f Test %f" % (train_score, test_score))


    train_dataset = tf.data.Dataset.from_tensor_slices((train, train_labels))
    test_dataset = tf.data.Dataset.from_tensor_slices((test, test_labels))

    return train_dataset, test_dataset


if __name__ == '__main__':

    learning_rate = 0.001
    batch = 32
    epoch = 10000
    C = 0.01

    float_precision = tf.float64

    train_dataset, test_dataset = load_binary_data("Klee", "ESBMC-incr")

    train_dataset = train_dataset.shuffle(2*batch).repeat(epoch).batch(batch)
    train_it = train_dataset.make_one_shot_iterator()

    x_train, y_train = train_it.get_next()

    x_train = tf.cast(x_train, float_precision)
    y_train = tf.cast(y_train, float_precision)

    initializers={"w": tf.truncated_normal_initializer(stddev=1),
              "b": tf.truncated_normal_initializer(stddev=1)}
    regularizers = {"w": tf.contrib.layers.l2_regularizer(scale=0.0001),
                    "b": tf.contrib.layers.l2_regularizer(scale=0.01)}


    with tf.name_scope("Logistic_Model") as scope:
        #W = tf.Variable(tf.random.uniform([156, 1], maxval=1, dtype=float_precision))
        #b = tf.Variable(tf.zeros([1], dtype=float_precision))
        #logit = tf.matmul(x_train, W)
        #logit = tf.nn.bias_add(logit, b)
        #y_sig = tf.sigmoid(logit)

        hidden = snt.Linear(32, initializers=initializers, regularizers=regularizers)
        out = snt.Linear(1, initializers=initializers, regularizers=regularizers)
        model = snt.Sequential([hidden, tf.nn.relu, out, tf.sigmoid])
        y_sig = model(x_train)
        y_pred = tf.round(y_sig)

    tf.summary.histogram("LR_W", hidden.w)
    tf.summary.histogram("LR_b", hidden.b)

    graph_regularizers = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
    total_regularization_loss = tf.reduce_sum(graph_regularizers)

    with tf.name_scope("cost_function") as scope:
        cross_y = tf.reshape(y_train, [-1, 1])

        epsilon = 0.0001
        logits_ = tf.clip_by_value(y_sig, epsilon, 1-epsilon)
        logits_ = tf.log(logits_ / (1 - logits_))
        cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(
            labels=cross_y, logits=logits_
        )

        cost = tf.reduce_mean(cross_entropy) + total_regularization_loss
        tf.summary.scalar("mean_entropy", cost)

    optimizer = tf.train.RMSPropOptimizer(0.001).minimize(cost)

    # Performance
    with tf.name_scope("Performance") as scope:
        correct_prediction = tf.equal(y_pred, cross_y)
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        tf.summary.scalar("accuracy", accuracy)

        #Test
        test_dataset = test_dataset.batch(420).repeat()
        x_test, y_test = test_dataset.make_one_shot_iterator().get_next()

        x_test = tf.cast(x_test, float_precision)
        y_test = tf.cast(y_test, float_precision)

        test_sig = model(x_test)

        cross_y_test = tf.reshape(y_test, [-1, 1])

        epsilon = 0.0001
        logits_ = tf.clip_by_value(test_sig, epsilon, 1-epsilon)
        logits_ = tf.log(logits_ / (1 - logits_))
        test_cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(
            labels=cross_y_test, logits=logits_
        )
        test_cost = tf.reduce_mean(test_cross_entropy)

        test_pred = tf.reshape(test_sig, [-1, 1])
        test_pred = tf.cast(test_pred > 0.5, y_test.dtype)
        correct_test = tf.equal(test_pred, cross_y_test)
        test_accuracy = tf.reduce_mean(tf.cast(correct_test, tf.float32))
        tf.summary.scalar("test_loss", test_cost)
        tf.summary.scalar("test_accuracy", test_accuracy)

    init = tf.global_variables_initializer()
    merge_op = tf.summary.merge_all()

    time_string = datetime.datetime.now().isoformat()

    name = f"MLP_Test_{time_string}"
    avg_loss = []

    with tf.Session() as sess:

        sess.run(init)

        summary_writer = tf.summary.FileWriter("/Users/cedricrichter/Documents/Arbeit/Ranking/GCNSelection/summary/"+name, graph=sess.graph)

        i = 0

        try:
            while True:
                #print(sess.run(tf.stack([y_pred, cross_y, tf.cast(correct_prediction, tf.float64)], axis=1)))
                _, loss, acc, test_loss, test = sess.run(
                            [optimizer, cost, accuracy, test_cost, test_accuracy])
                avg_loss.append(loss)

                if i % 10 == 0:
                    loss = np.mean(avg_loss)
                    print("Iteration %i Loss %f Acc %f Test_Loss %f Test_Acc %f" % (i, loss, acc, test_loss, test))
                    avg_loss = []

                summary_str = sess.run(merge_op)
                summary_writer.add_summary(summary_str, i)
                i += 1
        except tf.errors.OutOfRangeError:
            pass
