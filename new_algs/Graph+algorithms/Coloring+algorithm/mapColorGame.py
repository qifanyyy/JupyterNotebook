import sys
import re
from collections import OrderedDict
from copy import deepcopy


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        item = deepcopy(item)
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def output(print_statement):
    fo.write(print_statement + "\n")


lines = []
# pass one of the files in "input" folder as an argument
# with open("input/t12.txt") as f:
with open(sys.argv[2]) as f:
    lines.extend(f.read().splitlines())

# all colors sorted
global_domain_sortedG = sorted(re.split(r"\s*,\s*", lines[0]))

init_movesG = lines[1].strip()

global_depthG = int(lines[2].strip())

color_player_weightsG = {}

colorweights = re.split(r'\s*,\s*', lines[3].strip())
for colorweight in colorweights:
    arr = re.split(r'\s*:\s*', colorweight)
    color_player_weightsG.setdefault(arr[0], {})['p1'] = int(arr[1])

colorweights = re.split(r'\s*,\s*', lines[4].strip())
for colorweight in colorweights:
    arr = re.split(r'\s*:\s*', colorweight)
    color_player_weightsG.setdefault(arr[0], {})['p2'] = int(arr[1])

state_neighbourstatesG = OrderedDict()
for i in range(5, lines.__len__()):
    stateconnections = re.split(r'\s*:\s*', lines[i].strip())
    neighbourstates = sorted(re.split(r'\s*,\s*', stateconnections[1]))

    state_neighbourstatesG[stateconnections[0]] = neighbourstates

total_states = len(state_neighbourstatesG.keys())

possibleMoves = OrderedDict()
coloredStates = OrderedDict()

for init_move in re.split(r"\s*,\s*", init_movesG):
    state, color_player = re.split(r'\s*:\s*', init_move)
    color, player = re.split(r'\s*-\s*', color_player)

    if int(player) == 1:
        coloredStates[state] = {'color': color, 'player': int(player), 'value': sys.maxint, 'alpha': sys.maxint,
                                'beta': -sys.maxint}
    if int(player) == 2:
        coloredStates[state] = {'color': color, 'player': int(player), 'value': -sys.maxint, 'alpha': -sys.maxint,
                                'beta': sys.maxint}


def utility(coloredStates):
    value = 0
    for s in coloredStates:
        c = coloredStates[s]['color']
        p = coloredStates[s]['player']

        if p == 2:

            value = value - color_player_weightsG[c]['p2']

        elif p == 1:

            value = value + color_player_weightsG[c]['p1']
    return value


stack = Stack()

player = int(player)
depth = 0
alpha = -sys.maxint
beta = sys.maxint
value = sys.maxint
best_moves = OrderedDict()
fo = open("output.txt", "wb")


def getPossibleMoves(coloredStates):
    possibleMoves = OrderedDict()
    for coloredState in coloredStates.keys():
        for nbrState in state_neighbourstatesG[coloredState]:
            if not coloredStates.has_key(nbrState):
                for color in global_domain_sortedG:
                    possibleMoves[nbrState + '-' + color] = 1

    for coloredState in coloredStates.keys():
        coloredStateColor = coloredStates[coloredState]['color']
        for nbrState in state_neighbourstatesG[coloredState]:
            possibleMoves.pop(nbrState + "-" + coloredStateColor, None)

    possibleMoves = OrderedDict(sorted(possibleMoves.items(), key=lambda x: (x[0].split('-')[0], x[0].split('-')[1])))

    return possibleMoves


def maxValue(coloredStates, alpha, beta, depth):
    depth = depth + 1

    if (depth > global_depthG or len(getPossibleMoves(coloredStates)) == 0):
        v = utility(coloredStates)

        return v

    value = -sys.maxint

    possibleMoves = getPossibleMoves(coloredStates)
    for stateHiphenColor in possibleMoves.keys():
        stack.push(coloredStates)
        value = -sys.maxint
        state, color = re.split(r'\s*-\s*', stateHiphenColor)
        beta = min(beta, coloredStates[coloredStates.keys()[-1]]["value"])
        coloredStates[state] = {'color': color, 'player': 2, 'depth': depth, 'value': -sys.maxint, "alpha": alpha,
                                "beta": beta}

        if (depth >= global_depthG or len(getPossibleMoves(coloredStates)) == 0):
            coloredStates[state]['value'] = utility(coloredStates)

        st = coloredStates.keys()[-1]
        tempv = coloredStates[st]['value']
        tempa = coloredStates[st]['alpha']
        tempb = coloredStates[st]['beta']

        ## I know right! Looks lame! but an academic requirement..
        if tempa == -sys.maxint:
            tempa = "-inf"
        if tempv == -sys.maxint:
            tempv = "-inf"
        if tempb == -sys.maxint:
            tempb = "-inf"
        if tempa == sys.maxint:
            tempa = "inf"
        if tempv == sys.maxint:
            tempv = "inf"
        if tempb == sys.maxint:
            tempb = "inf"

        print_statement = st + ", " + coloredStates[st]['color'] + ", " + str(coloredStates[st]['depth']) + ", " + str(
            tempv) + ", " + str(tempa) + ", " + str(tempb)
        output(print_statement)
        r_v = minValue(coloredStates, alpha, beta, depth)

        coloredStates[coloredStates.keys()[-1]]["value"] = max(coloredStates[coloredStates.keys()[-1]]["value"], r_v)
        value = coloredStates[coloredStates.keys()[-1]]["value"]
        coloredStates = stack.pop()

        last_state = coloredStates.keys()[-1]
        beta = coloredStates[last_state]["beta"]
        alpha = coloredStates[last_state]["alpha"]

        coloredStates[last_state]["value"] = min(coloredStates[last_state]["value"], value)
        if (coloredStates[last_state]["value"] <= alpha):
            st = coloredStates.keys()[-1]
            tempv = coloredStates[st]['value']
            tempa = coloredStates[st]['alpha']
            tempb = coloredStates[st]['beta']

            ## I know right! Looks lame! but an academic requirement..
            if tempa == -sys.maxint:
                tempa = "-inf"
            if tempv == -sys.maxint:
                tempv = "-inf"
            if tempb == -sys.maxint:
                tempb = "-inf"
            if tempa == sys.maxint:
                tempa = "inf"
            if tempv == sys.maxint:
                tempv = "inf"
            if tempb == sys.maxint:
                tempb = "inf"

            print_statement = st + ", " + coloredStates[st]['color'] + ", " + str(
                coloredStates[st]['depth']) + ", " + str(
                tempv) + ", " + str(tempa) + ", " + str(tempb)
            output(print_statement)
            return coloredStates[last_state]["value"]
        coloredStates[last_state]["beta"] = min(beta, coloredStates[last_state]["value"])
        st = coloredStates.keys()[-1]
        tempv = coloredStates[st]['value']
        tempa = coloredStates[st]['alpha']
        tempb = coloredStates[st]['beta']

        ## I know right! Looks lame! but an academic requirement..
        if tempa == -sys.maxint:
            tempa = "-inf"
        if tempv == -sys.maxint:
            tempv = "-inf"
        if tempb == -sys.maxint:
            tempb = "-inf"
        if tempa == sys.maxint:
            tempa = "inf"
        if tempv == sys.maxint:
            tempv = "inf"
        if tempb == sys.maxint:
            tempb = "inf"

        if coloredStates[st]['depth'] == 1:
            best_moves.setdefault(coloredStates[last_state]["value"], {})["state"] = st
            best_moves.setdefault(coloredStates[last_state]["value"], {})["color"] = coloredStates[st]['color']
        # "z2-->" +
        print_statement = st + ", " + coloredStates[st]['color'] + ", " + str(coloredStates[st]['depth']) + ", " + str(
            tempv) + ", " + str(tempa) + ", " + str(tempb)
        output(print_statement)

    return coloredStates[last_state]["value"]


def minValue(coloredStates, alpha, beta, depth):
    depth = depth + 1

    if (depth > global_depthG or len(getPossibleMoves(coloredStates)) == 0):
        v = utility(coloredStates)
        return v
    value = sys.maxint
    possibleMoves = getPossibleMoves(coloredStates)
    for stateHiphenColor in possibleMoves.keys():
        stack.push(coloredStates)
        state, color = re.split(r'\s*-\s*', stateHiphenColor)

        value = sys.maxint

        alpha = max(alpha, coloredStates[coloredStates.keys()[-1]]["value"])
        coloredStates[state] = {'color': color, 'player': 1, 'depth': depth, 'value': sys.maxint, "alpha": alpha,
                                "beta": beta}

        if (depth >= global_depthG or len(getPossibleMoves(coloredStates)) == 0):
            coloredStates[state]['value'] = utility(coloredStates)

        st = coloredStates.keys()[-1]
        tempv = coloredStates[st]['value']
        tempa = coloredStates[st]['alpha']
        tempb = coloredStates[st]['beta']

        ## I know right! Looks lame! but an academic requirement..


        if tempa == -sys.maxint:
            tempa = "-inf"
        if tempv == -sys.maxint:
            tempv = "-inf"
        if tempb == -sys.maxint:
            tempb = "-inf"
        if tempa == sys.maxint:
            tempa = "inf"
        if tempv == sys.maxint:
            tempv = "inf"
        if tempb == sys.maxint:
            tempb = "inf"
        print_statement = st + ", " + coloredStates[st]['color'] + ", " + str(coloredStates[st]['depth']) + ", " + str(
            tempv) + ", " + str(tempa) + ", " + str(tempb)
        output(print_statement)

        r_v = maxValue(coloredStates, alpha, beta, depth)
        coloredStates[coloredStates.keys()[-1]]["value"] = min(coloredStates[coloredStates.keys()[-1]]["value"], r_v)
        value = coloredStates[coloredStates.keys()[-1]]["value"]

        coloredStates = stack.pop()
        last_state = coloredStates.keys()[-1]
        beta = coloredStates[last_state]["beta"]
        alpha = coloredStates[last_state]["alpha"]

        coloredStates[last_state]["value"] = max(coloredStates[last_state]["value"], value)
        if coloredStates[last_state]["value"] >= beta:
            st = coloredStates.keys()[-1]
            tempv = coloredStates[st]['value']
            tempa = coloredStates[st]['alpha']
            tempb = coloredStates[st]['beta']

            ## I know right! Looks lame! but an academic requirement..
            if tempa == -sys.maxint:
                tempa = "-inf"
            if tempv == -sys.maxint:
                tempv = "-inf"
            if tempb == -sys.maxint:
                tempb = "-inf"
            if tempa == sys.maxint:
                tempa = "inf"
            if tempv == sys.maxint:
                tempv = "inf"
            if tempb == sys.maxint:
                tempb = "inf"

            print_statement = st + ", " + coloredStates[st]['color'] + ", " + str(
                coloredStates[st]['depth']) + ", " + str(
                tempv) + ", " + str(tempa) + ", " + str(tempb)
            output(print_statement)
            return coloredStates[last_state]["value"]
        coloredStates[last_state]["alpha"] = max(coloredStates[last_state]["value"], alpha)

        st = coloredStates.keys()[-1]
        tempv = coloredStates[st]['value']
        tempa = coloredStates[st]['alpha']
        tempb = coloredStates[st]['beta']

        ## I know right! Looks lame! but an academic requirement..
        if tempa == -sys.maxint:
            tempa = "-inf"
        if tempv == -sys.maxint:
            tempv = "-inf"
        if tempb == -sys.maxint:
            tempb = "-inf"
        if tempa == sys.maxint:
            tempa = "inf"
        if tempv == sys.maxint:
            tempv = "inf"
        if tempb == sys.maxint:
            tempb = "inf"

        print_statement = st + ", " + coloredStates[st]['color'] + ", " + str(coloredStates[st]['depth']) + ", " + str(
            tempv) + ", " + str(tempa) + ", " + str(tempb)
        output(print_statement)

    return coloredStates[last_state]["value"]


def alphaBeta(coloredStates, alpha, beta, depth):
    st = coloredStates.keys()[-1]

    coloredStates[st]['depth'] = 0

    tempv = coloredStates[st]['value']
    tempa = coloredStates[st]['alpha']
    tempb = coloredStates[st]['beta']

    ## I know right! Looks lame! but an academic requirement..
    if tempa == -sys.maxint:
        tempa = "-inf"
    if tempv == -sys.maxint:
        tempv = "-inf"
    if tempb == -sys.maxint:
        tempb = "-inf"

    if tempa == sys.maxint:
        tempa = "inf"
    if tempv == sys.maxint:
        tempv = "inf"
    if tempb == sys.maxint:
        tempb = "inf"

    print_statement = st + ", " + coloredStates[st]['color'] + ", " + str(coloredStates[st]['depth']) + ", " + str(
        tempv) + ", " + str(tempa) + ", " + str(tempb)
    output(print_statement)
    value = minValue(coloredStates, alpha, beta, depth)
    print_statement = best_moves[value]["state"] + ", " + best_moves[value]["color"] + ", " + str(value)
    output(print_statement)


alphaBeta(coloredStates, alpha, beta, depth)
fo.close()
