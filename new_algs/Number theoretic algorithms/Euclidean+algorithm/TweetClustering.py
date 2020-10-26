from __future__ import division
import json
from nltk.tokenize import RegexpTokenizer
import random
import copy
import sys
import math

#Authors : Gokul & Padma

def tokenize(tweet):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(tweet)
    words = [str(token.lower()) for token in tokens]
    return words

def jaccard(entry1, entry2):
    words1 = set(entry1); words2 = set(entry2)
    return ((len(words1.union(words2)))-(len(words1.intersection(words2))))/(len(words1.union(words2)))

def run_kmeans(tweets, seed, max_iter, k):
    centroid = random.sample(seed, k)
    flag = False
    classes = dict()
    for i in range(max_iter):
        classes.clear()
        for j in range(k):
            classes[j] = list()

        for entry in tweets:
            distances = [jaccard(tweets[entry], tweets[cent]) for cent in centroid]
            class_index = distances.index(min(distances))
            classes[class_index].append(entry)

        prev = copy.deepcopy(centroid)
        #Update Centroid
        for index in classes.keys():
            min_dist = sys.maxint
            cent = None
            if len(classes[index])!=0:
                for m in range(len(classes[index])):
                    dist = 0
                    for n in range(len(classes[index])):
                        dist += jaccard(tweets[classes[index][m]], tweets[classes[index][n]])
                    if dist<min_dist:
                        min_dist = dist
                        cent = classes[index][m]
            if cent is not None:
                centroid[index] = cent


        for cent_index in range(len(centroid)):
            new_val = centroid[cent_index]
            old_val = prev[cent_index]
            if new_val == old_val:
                flag = True
            else:
                flag = False
        if flag:
            break
    return classes, centroid

def evaluate_sse(output, centroid, data):
    sse=0
    for key, entry in output.iteritems():
        for value in entry:
            sse+= math.pow(jaccard(data[value],data[centroid[key]]), 2)
    return sse

def main():
    k_value = int(sys.argv[1])
    seed_path = sys.argv[2]
    file_path = sys.argv[3]
    output_path = sys.argv[4]
    tweets = dict()
    seed = list()
    max_iter = 25

    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            tweets[str(data['id'])] = tokenize(data['text'])

    with open(seed_path, 'r') as seed_file:
        for line in seed_file:
            seed.append(line.strip(',\n'))

    output, centroid = run_kmeans(tweets, seed, max_iter, k_value)
    sse = evaluate_sse(output, centroid, tweets)
    output_file = open(output_path,'w')
    print sse
    for index, val in output.iteritems():
        output_file.write(str(index)+"\t"+(str(val))+"\n")
    output_file.write("SSE: "+str(sse))
    output_file.close()
    seed_file.close()
    file.close()
if __name__ == '__main__':
    main()