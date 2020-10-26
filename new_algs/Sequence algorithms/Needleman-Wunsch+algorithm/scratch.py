from grade_matrix import GradeMatrix
from score_matrix import ScoreMatrix
from copy import deepcopy
import argparse


def get_arg():
    verbose = True
    parser = argparse.ArgumentParser(
        prog="Global Alignment Algorithm(Needleman and Wunsch,1970) based on python",
        usage="Global Alignment Algorithm(Needleman and Wunsch,1970) based on python")
    parser.add_argument("-v", "--copyright", help="The information of version and author", action="count", default=0)
    parser.add_argument("-s", "--scoring_matrix", help="The path of scoring matrix for alignment")
    parser.add_argument("-f", "--file", help="The path of file of sequence in FASTA")
    parser.add_argument("-o", "--output", help="Specify output path for result, Default:output on screen")
    parser.add_argument("-q", "--quiet", help="without status prompt", action='count', default=0)
    parser.add_argument("-g", "--gap", help="Input the gap panel, Default:-5.", default=-5)
    parser.add_argument("-a", "--seq1", help="Input the sequence1 directly without option '-f'")
    parser.add_argument("-A", "--seq2", help="Input the sequence2 directly without option '-f'")
    parser.add_argument("-m", "--max_output", help="Set the max number of alignment results to output.,Default:100",
                        default=100)
    args = parser.parse_args()
    print("Global Alignment Algorithm(Needleman and Wunsch,1970) based on python")
    if args.copyright != 0:
        print("Author: Xingyu Chen\nLab:HeX Lab, TJMC, HUST, China\nEmail:chenxywork@gmail.com\nVersion:1.0 2019/11/18")
    if args.quiet != 0:
        verbose = False
    if args.scoring_matrix is None:
        print("Please provide scoring matrix by -s, -h for details")
        exit(1)
    if args.file is None and (args.seq1 is None or args.seq2 is None):
        print("Please provide the sequence to alignment with -a -A or -f, -h for details")
        exit(1)
    return args, verbose


def get_sequence(args, verbose):
    seq1_name = "sequence 1"
    seq2_name = "sequence 2"
    seq1 = ""
    seq2 = ""
    if args.file is None:
        seq1 = args.seq1
        seq2 = args.seq2
    else:
        if verbose:
            print("from", args.file, "......")
        file = open(args.file)
        a = file.read()
        a = a.split(">")
        for i in range(len(a)):
            a[i] = a[i].split("\n")
        del (a[0])
        seq1_name = a[0][0]
        seq2_name = a[1][0]
        for i in range(1, len(a[0])):
            seq1 = seq1 + a[0][i]
        for i in range(1, len(a[1])):
            seq2 = seq2 + a[1][i]
    return seq1_name, seq2_name, seq1, seq2


def calculate(seq1, seq2, gap, filename, verbose):
    if verbose:
        print("Now get scoring matrix from", filename)
    test = ScoreMatrix(gap=gap)
    test.input_matrix(filename=filename)
    if verbose:
        print("Now initialize the main process...It may take a long time.")
    test_2 = GradeMatrix()
    test_2.initialize(seq1=seq1, seq2=seq2, score_matrix=test)
    score = test_2.calculate_matrix(verbose=verbose)
    seq1, seq2, quality = test_2.get_sequence(verbose=verbose)
    for i in range(len(seq1)):
        seq1[i].reverse()
        seq2[i].reverse()
        quality[i].reverse()
    return seq1, seq2, quality, score


def output(args, seq1, seq2, quality, seq1_name, seq2_name, score, verbose):
    result_output = []
    if verbose:
        print("Now prepare the format of output")
    if len(seq1) > int(args.max_output):
        o = int(args.max_output)
    else:
        o = len(seq1)
    for i in range(o):
        line = len(seq1[i]) // 60
        result = []
        if line < 1:
            a = "".join(seq1[i]) + "\n" + "".join(quality[i]) + "\n" + "".join(seq2[i])
            result.append(deepcopy(a))
        else:
            k = 0
            for k in range(line):
                a = "".join(seq1[i][60 * k:60 * k + 60]) + "\n" + "".join(
                    quality[i][60 * k:60 * k + 60]) + "\n" + "".join(seq2[i][60 * k: 60 * k + 60])
                result.append(deepcopy(a))
            a = "".join(seq1[i][60 * k + 60:len(seq1[i])]) + "\n" + "".join(
                quality[i][60 * k + 60:len(seq1[i])]) + "\n" + "".join(seq2[i][60 * k + 60:len(seq1[i])])
            result.append(deepcopy(a))
        result_output.append(deepcopy(result))
    if args.output is None:
        for i in range(len(result_output)):
            print(">alignment result NO.", i + 1, "  score:", score, "  line1:", seq1_name, "  line2:quality  line3:",
                  seq2_name)
            for k in range(len(result_output[i])):
                print(result_output[i][k])
    else:
        if verbose:
            print("Now output the", o, "result to", args.output)
        file = open(args.output, 'w')
        for i in range(len(result_output)):
            kkk = [">alignment result NO.", i + 1, "  score:", score, "  line1:", seq1_name, "  line2:quality  line3:",
                   seq2_name, "\n"]
            kkk = ("".join('%s' % id for id in kkk))
            a = file.write(kkk)
            for k in range(len(result_output[i])):
                a = file.write(result_output[i][k])
                a = file.write("\n")
        file.close()


def main():
    args, verbose = get_arg()
    if verbose:
        print("Now get sequence...")
    seq1_name, seq2_name, seq1, seq2 = get_sequence(args=args, verbose=verbose)
    seq1, seq2, quality, score = calculate(seq1=seq1, seq2=seq2, gap=int(args.gap), filename=args.scoring_matrix,
                                           verbose=verbose)
    output(args=args, seq1=seq1, seq2=seq2, quality=quality, seq1_name=seq1_name, seq2_name=seq2_name, score=score,
           verbose=verbose)
    print("Done! Thanks for using!")


main()
