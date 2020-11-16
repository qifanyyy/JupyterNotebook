from datetime import datetime
from algorithms import *
import os

param_cache = ['nei', 'ng', 'ngm', 'nem', 'meta']
param_converter = {'nei': ['Neighborhood distance'], 'ng': ['NGram distance', 'NGram threshold'],
                   'ngm': ['Metaphone nG threshold', 'Metaphone nGrams'], 'nem': ['Metaphone neighbors'],
                   'meta': []}



def init_cache(params, dictionary):

    approxAlgs = {}

    param_log = {}

    for name in param_cache:
        param_log[name] = open('../log/' + name, 'r')

    factory = AlgoFactory(dictionary, params)

    log_strings = log_param(params)

    for name in param_cache:
        cached = False

        for line in param_log[name].readlines():

            if log_strings[name] == line or line == 'meta\n':
                cached = True

        if not cached:
            approxAlgs[name] = factory.getAlgo(name)

    return approxAlgs


def write_cache(approxAlgs, params):
    log_strings = log_param(params)
    param_log = {}
    cache = open('../out/cache.txt', 'a')
    for name in approxAlgs:
        param_log[name] = open('../log/' + name, 'a')
        param_log[name].write(log_strings[name])
        if name == 'meta':
            param_log[name].write('meta\n')
        param_log[name].close()

    # log data in a latex table format
    log_data(approxAlgs, params)
    #tex_tbl_end()
    # cache and print results human readable
    cache.write('\n' + str(datetime.now())+'\n')

    for name in param_cache:
        try:
            string = approxAlgs[name].name + '\n'
            for param in param_converter[name]:
                string += '{ ' + str(param) + ' ' + str(params[param]) + ' }\n'

            string += str(approxAlgs[name].evaluation) + '\n' + str(approxAlgs[name].stats) + "\n\n"

            cache.write(string)
            print (string)
        except KeyError:
            pass
    cache.close()


def clearCache(CLEAR_CACHE, BACKUP_CACHE):
    from time import time

    if CLEAR_CACHE:
        if not BACKUP_CACHE:
            key = str(raw_input("WARNING: Cache will be cleared without backing up\nAre you sure you want this? (Y/n)\n"))
            while key != 'Y' and key != 'n':
                os.system('clear')
                key = str(raw_input("Clear cache? (Y/n)\n"))

            if key == 'Y':
                os.system('rm -r ../out/* ../log/*')
                param_log = []
                for name in param_cache:
                    param_log.append(open('../log/' + name, 'w'))

                for doc in param_log:
                    doc.close()
            else:
                time = str(time()).strip('.')
                os.system('mkdir ../log/.old/' + time)
                os.system('cp -r ../log/* ../log/.old/' + time)
                os.system('cp -r ../out/* ../log/.old/' + time)
                os.system('rm -r ../out/* ../log/*')

        else:
            time = str(time()).strip('.')
            os.system('mkdir ../log/.old/' + time)
            os.system('cp -r ../log/* ../log/.old/' + time)
            os.system('cp -r ../out/* ../log/.old/' + time)

            os.system('rm -r ../out/* ../log/*')
            param_log = {}
            for name in param_cache:
                param_log[name] = (open('../log/' + name, 'w'))

            for doc in param_log:
                param_log[doc].close()
        os.system('mkdir ../out/tex/')


def log_param(params):
    # parse a param dict to log string
    log_strings = {}
    for name in param_cache:
        log = ''
        for param in param_converter[name]:
            log += param + ':' + str(params[param]) + ' '
        log += '\n'
        log_strings[name] = log

    return log_strings

def log_data(approxAlgs, param):

    log_strings = log_param(param)
    param_log = {}
    for name in param_cache:

        try:
            algo = approxAlgs[name]
            check=algo.stats['match']
            path = '../out/tex/' + name + '.tex'
            # see if data file exists yet, and make latex table header if not
            if not os.path.isfile(path):
                param_log[name] = open(path, 'a')
                param_log[name].write   ('\\begin{table}[h!]\n\t\\caption{' + approxAlgs[name].name +
                                        '}\n\t\\label{tab:table1}\n\t\\begin{tabular}{|l|S|r|}' +
                                        '\\hline\n\t\t' + 'Parameters & Recall & Precision\\\\\n\t\t\\hline\n')


            param_log[name] = open(path, 'a')
            param_log[name].write('\t\t' + log_strings[name].strip('\n') + ' & ')
            param_log[name].write(str(float(algo.stats['match']) / (algo.stats['incorrect'] + algo.stats['match'])))
            param_log[name].write(' & ' + str(float(algo.stats['match']) / algo.stats['num_attempted']))
            param_log[name].write('\\\\\n\t\t\\hline\n')
        except KeyError:
            pass
    for doc in param_log:
        param_log[doc].close()
