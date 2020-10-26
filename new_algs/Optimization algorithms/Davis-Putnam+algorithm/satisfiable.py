import parse
from ete3 import Tree, TextFace

# determine the next atom to be split on
def findNextSplit(stmt_set):
    # pick most common atom

    matches = {}
    # for each statement in the set
    for stmt in stmt_set:
        # get the list of atoms from each statement
        contains = stmt.contains()
        # for each atom in the list
        for c in contains:
            # update the count for how many times an atom has been seen
            c_count = matches.get(c, 0)
            matches[c] = c_count + 1

    # return the atom which has occured the most times
    return max(matches.iterkeys(), key=(lambda key: matches[key]))


# the Satisfiable() algorithm
def satisfiable(stmt_set):
    # create a Tree node for the current set
    t = Tree()
    t.name = str(stmt_set)

    if stmt_set == []:
        # if the set is empty, the starting set was Satisfiable, OPEN BRANCH
        # construct an extra "child" tree that is just an "O" to represent an open branch
        ob = Tree()
        ob.name = "O"
        t.children.append(ob)
        # return True and the final node
        return True, t

    if False in stmt_set:
        # if there is a False in the set, then something was unsatisfiable, CLOSE BRANCH
        # construct an extra "child" tree that is just an "X" to represent an closed branch
        cb = Tree()
        cb.name = "X"
        t.children.append(cb)
        # return False and the final node
        return False, t

    # determine the next atom to split on
    nxt_atm = findNextSplit(stmt_set)

    # get Statements of this atom and its negation
    nxt_l = parse.parse(nxt_atm)
    nxt_r = parse.parse("~(%s)" % nxt_atm)

    # create two new statement sets for the left and right branches
    l = []  # for the statements reduced on the "positive" atom
    r = []  # for the statements reduced on the "negative" atom

    for stmt in stmt_set:
        # reduce the statement on the "positive" atom
        stmt_l = stmt.reduce(nxt_l)
        if stmt_l is not True:
            # don't add it to the new list if the recution was a True
            l.append(stmt_l)

        # reduce the statement on the "negative" atom
        stmt_r = stmt.reduce(nxt_r)
        if stmt_r is not True:
            # don't add it to the new list if the recution was a True
            r.append(stmt_r)

    # get the satisfiablity of the left and right branches, plus the tree representations of both
    ret_l, tree_l = satisfiable(l)
    ret_r, tree_r = satisfiable(r)

    # add an extra marker to the tree to represent which literal the resulting branch was reduced on
    tree_l.add_face(TextFace(str(nxt_l), fgcolor="red"), column=0, position="branch-bottom")
    tree_r.add_face(TextFace(str(nxt_r), fgcolor="red"), column=0, position="branch-bottom")

    # add the left and right child branches to the current node
    t.children.append(tree_l)
    t.children.append(tree_r)

    # return ether the left or right branch and the current tree
    return ret_l or ret_r, t
