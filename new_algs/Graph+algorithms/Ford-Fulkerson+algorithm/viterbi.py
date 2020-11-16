# Following is an implementation of the Viterbi Algorithm
# Input data formatting is not done since the input format is not specified

# states list shows the states of the hidden markov cycle
# first element should be the "start" state and last element should be "end" state
states = ["start", "healthy", "fever", "end"]

# obs_seq is the sequence that is observed to which we need to find the highest probable markov chain
obs_seq = ["normal", "cold", "dizzy"]

# trans_prob[u][v] will give the probability of transition from state u to state v.
# (u and v are indexes of array states)
trans_prob = []

# emit_prob[u][obs] gives the probability of emitting 'obs' word at state u
emit_prob = []

# let's try filling dummy data
# sample data taken from https://en.wikipedia.org/wiki/Viterbi_algorithm
# since the data does not give an ending state, transition probability to end is taken as 1 here for all the cases.
for x in xrange(len(states)):
    trans_prob.append([])
    for y in xrange(len(states)):
        trans_prob[x].append(0)

trans_prob[0][1] = 0.6
trans_prob[0][2] = 0.4

trans_prob[1][2] = 0.3
trans_prob[1][1] = 0.7
trans_prob[1][3] = 1

trans_prob[2][1] = 0.4
trans_prob[2][2] = 0.6
trans_prob[2][3] = 1

for x in xrange(len(states)):
    emit_prob.append({})

emit_prob[0]["normal"] = 0
emit_prob[0]["cold"] = 0
emit_prob[0]["dizzy"] = 0

emit_prob[1]["normal"] = 0.5
emit_prob[1]["cold"] = 0.4
emit_prob[1]["dizzy"] = 0.1

emit_prob[2]["normal"] = 0.1
emit_prob[2]["cold"] = 0.3
emit_prob[2]["dizzy"] = 0.6

# end filling dummy data

# table is the dynamic programming table which stores results of reoccurring sub problems
# table[i][v] gives the highest probability at v th state of getting the obs_seq[0:i+1]
# table[i][v][0] stores the relevant probability value, table[i][v][1] stores the passed states
# table i%2 is taken because only the previous probabilities are needed. Others can be removed. Thus only two rows are sufficient
table = [[]]

# filling the first row using probabilities from the start state.
for state in xrange(1,len(states)-1):
    table[0].append([emit_prob[state][obs_seq[0]] * trans_prob[0][state], [0, state]])

table.append([])
# loop through rows
for i in xrange(1,len(obs_seq)):
    table[i % 2] = []
    # use the recurrence equation of Viterbi algorithm
    for x in xrange(1,len(states)-1):
        maximum = -1
        max_state = 1
        for y in xrange(1,len(states)-1):
            temp = table[(i-1) % 2][y-1][0] * trans_prob[y][x]
            if maximum<temp:
                maximum = temp
                max_state = y

        table[i % 2].append([maximum * emit_prob[x][obs_seq[i]], table[i-1][max_state-1][1] + [x]])

# get the highest probability path to get to the end state satisfying the observed sequence
maximum = 0
output = []

for state in xrange(1,len(states)-1):
    temp = trans_prob[state][len(states)-1] * table[(len(obs_seq)-1) % 2][state-1][0]

    if temp>maximum:
        maximum = temp
        output = table[(len(obs_seq)-1) % 2][state-1]
# add end state
output[1] += [len(states)-1]

print ("Probability :",output[0])

print ("States :",)

for x in xrange(len(output[1])):
    print (states[output[1][x]],)