#!/usr/bin/env python

'''
Wrapper for benchmarking the SW algo
Input: ref file, fastq file of reads
Output: tsv with times for each read'''

import sys
import os
import subprocess
from Bio import SeqIO

def process(lines=None):
    keys = ['name', 'seq', 'optional', 'quality']
    return {key: value for key, value in zip(keys, lines)}

def read_fastq(fn):
    '''Reads a fastq file'''
    n = 4
    fastq_records = []
    with open(fn, 'r') as fh:
        lines = []
        for line in fh:
            lines.append(line.rstrip())
            if len(lines) == n:
                record = process(lines)
                fastq_records.append(record)
                #print("Record: %s\n" % (str(record)))
                lines = []

    return fastq_records

def read_fasta(fn):
    '''Reads a fasta file'''
    fasta_records = []

    for seq_record in SeqIO.parse(fn, "fasta"):
        fasta_records.append(seq_record)

    return fasta_records

def run_test(ref, target):
    '''Runs test on a single read'''
    run_test_comm = 'node run_Myers.js -r {0} -t {1}'.format(
        ref,
        target)

    output = subprocess.check_output(run_test_comm.split(' '))
    time = output.decode('utf-8').strip()
    return time

def benchmark(ref_records, target_records):
    import pandas

    output_data = {'Reference Sequence': [], 'Target Sequence': [], 'Length(N)': [],  'Time': []}

    for ref_record in ref_records:
        # Save the sequence to a temp file
        temp_ref = 'temporary_ref'
        with open(temp_ref, 'w') as ref_file:
            SeqIO.write(ref_record, ref_file, 'fasta')
            #ref_file.write(ref_record.seq)
        for target_record in target_records:
            # Save target sequence to a temp file
            read_name = target_record['name'].split()[0]
            temp_target = 'temporary_read'
            with open(temp_target, 'w') as target_file:
                target_file.write(target_record['seq'])

            print('Running test on {}'.format(read_name))
            
            # Pass temp file paths instead of strings
            target_length = len(target_record['seq'])
            time = run_test(temp_ref, temp_target)   
            print ('Time: {0}, Length: {1}'.format(time,target_length))
            output_data['Reference Sequence'].append(ref_record.id)
            output_data['Target Sequence'].append(read_name)
            output_data['Length(N)'].append(target_length)
            output_data['Time'].append(time)

    output_df = pandas.DataFrame(data=output_data)
    return output_df



try:
    fasta_file = sys.argv[1]
    fastq_file = sys.argv[2]
except IndexError as ie:
    raise SystemError("Error: Specify file name\n")

if not (os.path.exists(fastq_file) or os.path.exists(fasta_file)):
    raise SystemError("Error: File does not exist\n")



fastq_records = read_fastq(fastq_file)
fasta_records = read_fasta(fasta_file)
output_df = benchmark(fasta_records, fastq_records[0:50])
output_df.to_csv('Myers_Cost_benchmark.tsv', sep='\t')



