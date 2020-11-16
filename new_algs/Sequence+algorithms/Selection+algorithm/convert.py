# Reads a CSV file with features for two graphs, and writes a CSV file with a
# line of features, for each unique graph in the input file

d = {}
with open('results/mcs_features.csv') as data:
    for line in data:
        fields = line[:-1].split(',')
        graphs = fields[0].split()
        if graphs[0] not in d:
            d[graphs[0]] = fields[1:14]
        if graphs[1] not in d:
            d[graphs[1]] = fields[14:]

with open('results/mcs_features_individual.csv', 'w') as f:
    for graph in d:
        f.write(graph + ',' + ','.join(d[graph]) + '\n')
