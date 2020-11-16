import argparse

parser = argparse.ArgumentParser(description= "specify hyperparameter for shortest path algorithm")


# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument('--iteration')
# parser.add_argument('bar')
# parser.parse_args('X --foo Y'.split())
# parser.print_help()
# args = parser.parse_args()
# print(args)


parser.add_argument("--iteration",
                    dest    = "iteration",
                    help    = "number of iteration to run on each algorithm",
                    # action  = "store_true",
                    default = 5
                    )
parser.add_argument("--size",
                    dest    = "size",
                    help    = "number of node",
                    # action  = "store_true",
                    default = 10
                    )
parser.add_argument("--ratio",
                    dest    = "ratio",
                    help    = "number of iteration to run on each algorithm",
                    # action  = "store_true",
                    default = 2
                    )
parser.add_argument("--repeat",
                    dest    = "repeat",
                    help    = "number of iteration to run on each algorithm",
                    # action  = "store_true",
                    default = 1
                    )
parser.add_argument("--verbose",
                    dest    = "verbose",
                    help    = "be more verbose",
                    action  = "store_true",
                    )

args = parser.parse_args()

# if args.iteration:
#     print(args.iteration)
print(args)
# for arg in args:
#     print(arg)
