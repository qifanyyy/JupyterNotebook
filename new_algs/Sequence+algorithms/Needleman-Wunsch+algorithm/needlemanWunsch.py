import argparse
from prepare_files import *
from NeddlemanWunschMatrix import *


parser = argparse.ArgumentParser()
parser.add_argument('-a', dest='seq_1_path', help='seq_1.txt path')
parser.add_argument('-b', dest='seq_2_path', help='seq_2.txt path')
parser.add_argument('-c', dest='config_path', help='config.txt path')
parser.add_argument('-o', dest='output_path', help='output.txt path')

args = parser.parse_args()

config = import_config(args.config_path)
seq_1, seq_2 = import_sequences(args.seq_1_path, args.seq_2_path, int(config['max_seq_length']))

NW_table = NeedlemanWunschMatrix(config, seq_1, seq_2)

create_output(NW_table, args.output_path)

print("Done")


