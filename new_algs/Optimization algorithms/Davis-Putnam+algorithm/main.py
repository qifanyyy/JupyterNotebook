import sys
import parse
import statement
import satisfiable

from ete3 import Tree, TreeStyle, TextFace


# read an argument from a file and return a set of the statements contained within
def open_argument(filename):
    try:
        f = open(filename)  # open the file
    except:
        print "Could not open file: %s" % filename
        exit(1)

    stmt_set = []
    for line in f:
        line = line.strip().replace(" ", "")  # strip all of the whitespace
        stmt = parse.parse(line)  # parse the line to get a statement

        # make sure that the line was properly parsed
        if stmt is None:
            print "Parsing Error: %s" % line
            exit(1)

        stmt_set.append(stmt)  # add the statement to the set

    # take the last statement out of the set, and negate it
    conclusion = stmt_set[-1]
    neg = statement.Statement("~", conclusion)
    stmt_set = stmt_set[:-1]

    # re-add the negated conclusion to the set
    stmt_set.append(neg)

    # return the set
    return stmt_set

if __name__ == "__main__":
    # ensure proper usage
    if len(sys.argv) != 3:
        print "Incorrect Usage: python main.py <input file> <output directory>"
        exit(1)

    # get a statement set from the given file
    stmt_set = open_argument(sys.argv[1])

    # call the Satisfiable() algorithm to determine whether or not the argument is valid
    sat, tree = satisfiable.satisfiable(stmt_set)
    print tree.get_ascii(show_internal=True)

    # say if the argument was valid or not
    if sat:
        print "Satisfiable! Therefore, Invalid Argument!"
    else:
        print "Unsatisfiable! Therefore, Valid Argument!"

    # set teh tree style...
    ts = TreeStyle()
    # don't show the name of the leaf nodes (which are just a x/o for a open/closed branch) in the final graph
    ts.show_leaf_name = False

    for child in tree.traverse():
        # add a marker with the name of each node, at each node
        child.add_face(TextFace(child.name), column=0, position="branch-top")

    # the file that the resulting graph will be saved as
    outputfile = sys.argv[2] + "/" + sys.argv[1].split("/")[-1][:-4] + ".png"

    # render the file and save it
    tree.render(outputfile, tree_style=ts, w=5000)
