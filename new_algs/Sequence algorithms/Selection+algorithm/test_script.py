import Classifier, DataSet
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt
from collections import defaultdict

data = DataSet.DataSet()

labels = data.all_labels  # the 10 most frequent classes
methods = ["freq", "mi", "chisq"]
num_features = [10, 50, 150, 500, 1000, 5000]  # x axis!
colours = ["r", "g", "m", "c", "b", "y", "orange", "indigo", "steelblue", "darkolivegreen"]


f1s = defaultdict(list)  # method: [ 6 vals ]

for method in methods:
    precisions = defaultdict(list)  # (True, ship): [ 6 vals ]
    recalls = defaultdict(list)
    
    for k in num_features:
        f1total = 0
        for label in labels:
            print("{} features selected using {} method, on label {}".format(k, method, label))
            clf = Classifier.Classifier(data, label, k, method)
            scores = clf.evaluate()  # (precFalse, precTrue, recFalse, recTrue, f1av)
            key = (False, label)
            precisions[key].append(scores[0])
            recalls[key].append(scores[2])
            key = (True, label)
            precisions[key].append(scores[1])
            recalls[key].append(scores[3])
            f1total += scores[4]
            print("\n\n")
        f1s[method].append(f1total/10)
        
    # make precision and recall charts here
    for key in precisions:
        if key[0] == False:
            dot = "^"
        else:
            dot = "o"
        colour = colours[labels.index(key[1])]
        plt.plot(num_features, precisions[key], color=colour, marker=dot, label=key)
    
    plt.xlabel("Number of features")
    plt.ylabel("Precision")
    plt.title('Class Precision for {} method'.format(method))
    plt.xscale('log')
    lgd=plt.legend(loc="upper left",  bbox_to_anchor=(1.05,1), fontsize=8)
    plt.tight_layout(pad=7)
    plt.savefig("prec{}.pdf".format(method),bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()
    
    for key in recalls:
        if key[0] == False:
            dot = "^"
        else:
            dot = "o"
        colour = colours[labels.index(key[1])]
        plt.plot(num_features, recalls[key], color=colour, marker=dot, label=key)
    
    plt.xlabel("Number of features")
    plt.ylabel("Recall")
    plt.title('Class Recall for {} method'.format(method))
    plt.xscale('log')
    lgd=plt.legend(loc="upper left",  bbox_to_anchor=(1.05,1), fontsize=8)
    plt.tight_layout(pad=7)
    plt.savefig("recall{}.pdf".format(method),bbox_extra_artists=(lgd,), bbox_inches='tight')        
    plt.clf()

for label in labels:
    clf = Classifier.Classifier(data, label)
    print("Baseline classifier with no feature selection, on label", label)
    print(clf.evaluate())
    print("\n\n")

# make the f1 chart here
col = 0
for key in f1s:
    plt.plot(num_features, f1s[key], color=colours[col], marker="o", label=key)
    col += 1

plt.xlabel("Number of features")
plt.ylabel("F1")
plt.title('Average F1 score')
plt.xscale('log')
lgd=plt.legend(loc="upper left",  bbox_to_anchor=(1.05,1), fontsize=8)
plt.tight_layout(pad=7)
plt.savefig("f1.pdf",bbox_extra_artists=(lgd,), bbox_inches='tight')        
plt.clf()
