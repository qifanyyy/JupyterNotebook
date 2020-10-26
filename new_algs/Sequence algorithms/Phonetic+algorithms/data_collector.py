#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 20/05/2016

@author: axelg
'''
from __future__ import division

import csv
import re
import codecs
import numpy
import fuzzy
import abydos
import chardet
import sys, os
import os.path

from abydos.phonetic import bmpm, russell_index, dm_soundex, metaphone
from soundex import getInstance
from metaphone.metaphone import doublemetaphone
from collections import Counter
import shutil


sdx = getInstance()
double_metaphone=False
dict_replaceby={}
dict_phonemes={}

#-------------------------------------------------------------------------------
def carga_tabla_phon(filename):
    #tablename = nltk.defaultdict(lambda: 1)
    tablename = {}
    with open(filename, 'rU') as lineas:
            for row in csv.reader(lineas, delimiter=','):
                tablename[row[0]]= row[1]
                tablename[row[0]+"_phon"]= row[2]
    return tablename
#-------------------------------------------------------------------------------
# End of Function
dic = carga_tabla_phon('spanish_dict.csv')

#-------------------------------------------------------------------------------
def correct(word, dic, phonetic_algorithm):
    if len(word)<1: # Do not process if it has no letters!
        return word
    
    phonetic_code=phonetic_algorithm(word)
    keys=dic.keys()
    phonetic_candidates=[]
    
    # Identify phonetic candidates
    for i in keys:
        phonetic_dir = dic.get(i+"_phon")
        if phonetic_code==phonetic_dir:
            phonetic_candidates=phonetic_candidates+[i]
    

    
    return phonetic_candidates
#-------------------------------------------------------------------------------
# End of Function

#-------------------------------------------------------------------------------
def generate_double_metaphone(word):
    ## Double Metaphone
    global double_metaphone
    double_metaphone=True
    try:
        #word=unicode(word, 'UTF-8', 'ignore')
        if isinstance(word,unicode):
            word=word.encode('UTF-8')
        
        return doublemetaphone(word)
    except UnicodeEncodeError:
        print "UnicodeEncodeError: " + word
        return ('','')
#-------------------------------------------------------------------------------
# End of Function

#-------------------------------------------------------------------------------
def generate_soundex(word):
    ## Soundex
    #word=unicode(word, 'UTF-8', 'ignore')
    try:
        return [sdx.soundex(word)]
    except: # None exception is expected thus any exception mean the word could not be coded, so it should return empty
        return [""]
#-------------------------------------------------------------------------------
# End of Function

#-------------------------------------------------------------------------------
def generate_nysiis(word):
    ## https://pypi.python.org/pypi/Fuzzy
    if isinstance(word,unicode):
        word=word.encode('UTF-8')
    
    return [fuzzy.nysiis(word)]
#-------------------------------------------------------------------------------
# End of Function


#-------------------------------------------------------------------------------
def generate_russell_index(word):
    ## https://pypi.python.org/pypi/Fuzzy
    if isinstance(word,unicode):
        word=word.encode('UTF-8')
    
    return [str(russell_index(word))]
#-------------------------------------------------------------------------------
# End of Function


#-------------------------------------------------------------------------------
def generate_metaphone(word):
    ## https://pypi.python.org/pypi/Fuzzy
    if isinstance(word,unicode):
        word=word.encode('UTF-8')
    
    return [metaphone(word)]
#-------------------------------------------------------------------------------
# End of Function



#-------------------------------------------------------------------------------
def generate_dm_soundex(word):
    ## https://pypi.python.org/pypi/abydos/0.2.0
    try:
        if not isinstance(word,unicode):
            word=unicode(word, 'UTF-8', 'ignore')
        
        return dm_soundex(word)
    except UnicodeEncodeError:
        print "UnicodeEncodeError: " + word
        return ('','')
#-------------------------------------------------------------------------------
# End of Function






#-------------------------------------------------------------------------------
def generate_beider_morse(word):
    ## https://pypi.python.org/pypi/abydos/0.2.0
    try:
        if not isinstance(word,unicode):
            word=unicode(word, 'UTF-8', 'ignore')
        
        return bmpm(word).split(' ')
    except UnicodeEncodeError:
        print "UnicodeEncodeError: " + word
        return ('','')
#-------------------------------------------------------------------------------
# End of Function


#-------------------------------------------------------------------------------
def list_execute_phonetic_algorithm(word, package, function_name):
    phonetic_algorithm =getattr(package, function_name)
    word=' '+word # leading space required by: spfc 

    try: # Detect character set
        encoding=chardet.detect(word)['encoding']
        if encoding is None: #caf? ( unicode() argument 2 must be string, not None )
            encoding='UTF-8'
        # End-If: Encoding None.
    except ValueError:
        encoding='unicode'
    # End-Try: Detect character set

    try: # Call phonetic algorithm
        if not isinstance(word,unicode):
            if encoding not in ('UTF-8','ascii'):
                encoding='UTF-8'
            word=unicode(word, encoding, errors='ignore')

        result=phonetic_algorithm(word)

        if type(result) == type(('','')): # type Tuple
            aux=['']
            for code in result:
                aux.append(code)
                result=aux
        elif type(result) != type(['']): # type List
            if type(result) == int:
               result=str(result)
            else:
                if not isinstance(result,unicode):
                    result=unicode(str(result), 'UTF-8', errors='ignore')
            
            result=result.split(' ')
        # End-If: Return type

        return result
    except Exception as e: # UnicodeEncodeError:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print '[UnicodeEncodeError] ', function_name,', encoding=',encoding, '(',str(e),')[line=',exc_tb.tb_lineno,']',
        try:
            print ': ',word
        except:
            print '.'
        return ['']
    # End-Try: Call phonetic algorithm.
#-------------------------------------------------------------------------------
# End of Function


#-------------------------------------------------------------------------------
def void_update_phonetic_codes_db(item, package, function_name):
    if isinstance(item, unicode):
        item=item.encode("UTF-8")
    
    phonetic_code_list=list_execute_phonetic_algorithm(item, package, function_name)

    for phonetic_code in phonetic_code_list:
        if len(phonetic_code) >= 1:
            if dict_phonemes.has_key(phonetic_code):
                dict_phonemes[phonetic_code]=dict_phonemes[phonetic_code]+';'+item
            else:
                dict_phonemes[phonetic_code]=item


#-------------------------------------------------------------------------------
# End of Function

#-------------------------------------------------------------------------------
def generate_phonetic_codes(infilename, package, function_name):
    out_dir_name=function_name
    
    print "Algorithm: Generating phonetic codes for ", function_name,"... ",
    if os.path.isfile('phonemes_'+function_name+'.csv'):
        # If file exists use the information in it.
        print "Phonemes file already exists."
        return
    # End-If: Phonemes file exists.

    with open(infilename, 'rU') as lineas:
        for row in csv.reader(lineas, delimiter=','):
            #row=unicode(row, "UTF-8")
            if not isinstance(row[0], unicode):
                row[0]=unicode(row[0],'UTF-8')
                
            row[0]=row[0].replace(u'A',u'á')
            row[0]=row[0].replace(u'E',u'é')
            row[0]=row[0].replace(u'I',u'í')
            row[0]=row[0].replace(u'O',u'ó')
            row[0]=row[0].replace(u'U',u'ú')
                
            void_update_phonetic_codes_db(row[0], package, function_name)
    
    # Save recently generated phonemes to file.
    write_csv(dict_phonemes, 'phonemes', function_name)

    print "Done."

#-------------------------------------------------------------------------------
# End of Function


#-------------------------------------------------------------------------------
def initialize_records_file(output_file_name, phonetic_algorithm):
    
    if os.path.exists(output_file_name):
        os.remove(output_file_name)
        
    output_file=open(output_file_name, "wb")
    c = csv.writer(output_file, delimiter=',')
    
    result=["Message ID"]               # Initialize with item number.
    result.append("Item Name")          # Add the item name to the results.
    result.append("Phonetic Code") # Add phonetic code of that item.
    result.append("Alternatives to Item") # Add the identified alternatives to the result.
    result.append("Phonetic Algorithm Precision") # Add the precision of the phonetic algorithm for item
    result.append("Correct Term Identified") # Add whether or not the correct concept is identified. 
    result.append("Phonetic Algorithm") # Add the precision of the phonetic algorithm for item
    
    c.writerow(result)
    output_file.flush()
    output_file.close()
#-------------------------------------------------------------------------------
# End of Function

#
# Writes a new row to the output_file_name with the following format:
# Column#  Description
#    1     Number of the row in the natural language input file.
#    2     Item Name of item.
#    3     Phonetic code for item.
#    4     Identified alternatives for item. This is a list of words separated
#          by the colon (';') character.
#    5     Precision of the phonetic algorithm for item.
#    6     If the correct word is in the alternatives set.
#    7     Phonetic algorithm name used.
#-------------------------------------------------------------------------------
def write_record(index, item, phonetic_code, alternatives_set, alternatives, output_file_name, was_found, phonetic_algorithm):
    output_file=open(output_file_name, "a")
    c = csv.writer(output_file, delimiter=',')
    
    result=[index]               # Initialize with item number.
    result.append(item)          # Add the item name to the results.
    result.append(phonetic_code.encode('UTF-8')) # Add phonetic code of that item.
    result.append(alternatives_set) # Add the identified alternatives to the result.
                
    if len(alternatives) > 0:
        result.append(1/len(alternatives)) # Add the precision of the phonetic algorithm for item
    else:
        result.append(0) # Add the precision=0 since it does not have alternatives for item.
    
    result.append(was_found)     # Is correct item in the found alternatives.
    result.append(phonetic_algorithm) # Add the phonetic algorithm name

    c.writerow(result)
    output_file.flush()
    output_file.close()
#-------------------------------------------------------------------------------
# End of Function

#
# Writes a dictionary in a text file with CSV format.
#-------------------------------------------------------------------------------
def write_csv(data, filename_sufix, phonetic_algorithm):
    output_file=codecs.open(phonetic_algorithm+'_'+filename_sufix+'.csv', "a")
    c = csv.writer(output_file, delimiter=',')
    
    for tuple in data.items():
        # Decode first element if necesary.
        if not isinstance(tuple[0], unicode):
            tuple=(unicode(tuple[0]), tuple[1])

        # Decode second element if necesary.
        if not isinstance(tuple[0], unicode):
            tuple=(tuple[0], unicode(tuple[1]))
        
        c.writerow(tuple)

    output_file.flush()
    output_file.close()
#-------------------------------------------------------------------------------
# End of Function

#
# Reads a dictionary in a text file with CSV format. The data is returned as a
# dictionary.
#-------------------------------------------------------------------------------
def read_csv_dict(filename_sufix, phonetic_algorithm):
    result_dict={}
    file_name=phonetic_algorithm+'_'+filename_sufix+'.csv'

    if os.path.isfile(file_name):
        input_file=codecs.open(file_name, "r")
        c = csv.reader(input_file, delimiter=',')
    
        for row in c:
            result_dict[row[0]]=row[1]
        # End-For: Read file.

        input_file.close()
    # End-If: file exists.

    return result_dict
#-------------------------------------------------------------------------------
# End of Function


# It will try to read the correct replacement for the item under evaluation from
# the <replacement_dir_name>/<item> file; e.g.:
#    get_correct_item('sampleword','replaceby')
# This method will try to open replaceby/sampleword and read the contents of that
# file. Those contents are considered the correct word.
# If the file does not exist, this method will ask user input.
# If the word is in the dictionary it will be assumed that is the correct word.
# The files in <replacement_dir_name>/* are considered the database of correct.
# words.
#-------------------------------------------------------------------------------
def get_correct_item(item, replacement_dir_name):
    
    try:
        item=item.lower()
        
        if dict_replaceby.has_key(item):
            return dict_replaceby[item]
        else:
            if dic.has_key(item):
                # If the item is in the dictionary, then it is the correct word.
                return item
            # End-If: If it is in the dictionary.
            
            
            # If it is a hashtag or a user name use the same word as correct one
            if item[0] in '#@':
                correct_word=item
            else:
                correct_word_aux=raw_input('Specify correct word for "' + item +'"['+correct_word+']: ')
                # If user just hit enter then use the default correct word which is the exact same word being evaluated.
                if len(correct_word_aux)>0:
                    correct_word=correct_word_aux
                    dict_replaceby[item]=correct_word.lower()
                # End-If: Default word selection
            # End-If: Is hash tag.
        

         # End-IF: Replace-by directory exists.
    except:
        correct_word=''

    return correct_word
#-------------------------------------------------------------------------------
# End of Function


#
# This function processes each one of the words in the sample file with text in
# in natural language; i.e. 'twitter_spanish.csv'. For each word in that file,
# this function creates a record.
#-------------------------------------------------------------------------------
def collect_data(phonems_file_name, output_file_name, package, function_name):
    input_dir_name=function_name
    precision_list=[]
    
    print "Output file: ", output_file_name, "."
    if os.path.isfile(output_file_name):
        # If file exists assume it does not require to be processed again.
        print "Algorithm: Results already exist in ", output_file_name, ". Skipping."
        return
    # End-If: Data already generated.

    print "Algorithm: " + function_name + "; start data processing... "
    initialize_records_file(output_file_name, function_name)
    
    # Load CVS data
    dict_replaceby=read_csv_dict('replaceby', 'db')
    dict_phonemes=read_csv_dict('phonemes', function_name)
    
    
    with codecs.open('twitter_spanish.csv', 'rU', errors='ignore') as lineas:
        index = 1
        
        for row in csv.reader(lineas, delimiter=','):
            print str(index),"\t",row
            items_processed_count=0
            precision_idx=0 # Initialize with zero precision.
            s1 = row[0]
            s1 = re.sub('\'n','ñ',s1) # Ad hoc substitution: 'n => ñ.
            s1 = re.sub('#[^+-.,!¡ºª\\~}{–…@#$%^&*();:\/|<>"\'=?¿\s]+',' ',s1) # Removes hashtags.
            s1 = re.sub('@[^+-.,!¡ºª\\~}{–…@#$%^&*();:\/|<>"\'=?¿\s]+',' ',s1) # Removes mentions to twitter users.
            s1 = re.sub('http[s]*:\/\/[^\s]+',' ',s1) # omite urls como http://foo.co.uk/ o https://regexr.com/foo.html?q=bar
            s1 = re.sub('\*[_-]\*|[Oo]_+[Oo]|:B|B[-]*\)|>[_.]>|u[._]u|U[._]U|\.l\.|-[._]-|\^[._-]*\^|[D]-*:|[:=]-*[)(*dDpPsS$3]|[Xx][Dd]|[:=]\/|=\|',' ',s1) # omite emoticones; e.g: .l. -.- ^^ :) :-) :( :--* ^_^ ^-^ :-$
            s1 = re.sub(' +',' ',s1)     # deja un solo blanco entre cada palabra
            s1 = re.sub('[. ]+[0-9]+[%. ]+',' ',s1) # omite los números
            #s1 = re.sub('[-.,?!¿¡]+',' ',s1) # omite caracteres no alfabéticos, commented out since deleting the dash will brake words like "wi-fi"
            s1 = re.sub('[ \-\+$\n][\d{1,3},]*\d*\.?\d+',' ',s1) # omite cantidades de dinero; e.g.: $100, $11.50 16,500 $1
            s1 = re.sub('\/|\\\\','_ord-47_',s1) # Required to replace special file system characters to avoid execution errors.
            s1 = re.sub('[Aa]*[Jj][Aa]([Jj][Aa])+','ja',s1) # replaces the "jajaja", "jaja", "jajajajajaja" bya a single "ja"
            s1 = re.sub('[¡¿:;.,?!]+',' ',s1) # replaces exclamation, question marks and punctuation by blank space.
            s1 = re.sub('\/','-',s1) # replaces slashes by hyphens/dashes.
            items = re.split("[ .,;:\(\)¡!¿?]+", s1)
            
            # Go through all words in the natural language phrase.
            for item in items:
                if len(item)<1: # Skip empty words.
                    continue
                
                #item=item.lower() # Experiment with lowercase
                item = re.sub('[ .,;:\(\)¡!¿?]+',' ',item)
                
                correct_item=get_correct_item(item,'replaceby')
                phonetic_codes=list_execute_phonetic_algorithm(item, package, function_name)
                for phonetic_code in phonetic_codes:
                    if phonetic_code=="*":
                        continue
                    # End-If: If unknown word.

                    void_update_phonetic_codes_db(correct_item, package, function_name)
                 
                
                    # If a homophone exists use it...
                    if len(phonetic_code)>0 and dict_phonemes.has_key(phonetic_code):
                        alternatives_set=dict_phonemes[phonetic_code]

                        if isinstance(alternatives_set, unicode):
                            alternatives_set=alternatives_set.encode("UTF-8")
                        # End-If: Is data read unicode?

                        alternatives=alternatives_set.split(';')
                    # otherwise, use a label for the unsuccessful case.
                    else:
                        alternatives_set="<None>"
                        alternatives=[]
                    
                    if len(alternatives) > 0:
                        precision_idx+=1/len(alternatives)
                    # End-IF: Has alternatives
                    write_record(index, item, phonetic_code, 
                                 alternatives_set, alternatives, output_file_name, 
                                 correct_item in alternatives, function_name)
                    items_processed_count+=1
                # End-For: phonetic_codes
            # End-For: items in CVS row.
                    
            if items_processed_count>0:
                #result.append(precision_idx/items_processed_count)
                precision_list.append(precision_idx/items_processed_count)
            index += 1
        # End-For: rows in CVS file
        
        # Save replaceby words
        write_csv(dict_replaceby, 'replaceby', 'db')
        write_csv(dict_phonemes, 'phonemes', function_name)
        
        # Compute final statistics:
        mode_pa=Counter(precision_list).most_common(1)
        summary_string="Algorithm: ", function_name, "; Mode: " + str(mode_pa) + ", Median: " + str(numpy.median(precision_list)) + ", Mean: " + str(numpy.mean(precision_list)) +", StdDev: " + str(numpy.std(precision_list, ddof=1))
                
        print summary_string
    print "Processing using: " + function_name + " done."
        
    # End-With
    
#-------------------------------------------------------------------------------
# End of Function



phonetic_algorithms_list=[
    {'pkg':abydos.phonetic,'name':'russell_index'},# Robert C. Russell's Index
    {'pkg':abydos.phonetic,'name':'soundex'},      # American Soundex
    {'pkg':abydos.phonetic,'name':'dm_soundex'},   # Daitch-Mokotoff Soundex
    {'pkg':abydos.phonetic,'name':'koelner_phonetik'},   # Kölner Phonetik
    {'pkg':fuzzy,'name':'nysiis'},       # NYSIIS
    {'pkg':abydos.phonetic,'name':'mra'},          # Match Rating Algorithm
    {'pkg':abydos.phonetic,'name':'metaphone'},    # Metaphone
    {'pkg':abydos.phonetic,'name':'double_metaphone'},   # Double Metaphone
    {'pkg':abydos.phonetic,'name':'caverphone'},   # Caverphone
    {'pkg':abydos.phonetic,'name':'alpha_sis'},    # Alpha Search Inquiry System
    {'pkg':abydos.phonetic,'name':'caverphone'},   # Caverphone
    {'pkg':abydos.phonetic,'name':'fuzzy_soundex'},# Fuzzy Soundex
    {'pkg':abydos.phonetic,'name':'phonex'},       # Phonex
    {'pkg':abydos.phonetic,'name':'phonem'},       # Phonem
    {'pkg':abydos.phonetic,'name':'phonix'},       # Phonix
    {'pkg':abydos.phonetic,'name':'sfinxbis'},     # SfinxBis
    {'pkg':abydos.phonetic,'name':'phonet'},       # phonet
    {'pkg':abydos.phonetic,'name':'spfc'},         # Standardized Phonetic Frequency Code
    {'pkg':abydos.phonetic,'name':'bmpm'}         # Beider-Morse Phonetic Matching
]


if __name__ == '__main__':
    for phonetic_algorithm in phonetic_algorithms_list:
        generate_phonetic_codes("spanish_dict.csv", phonetic_algorithm['pkg'], phonetic_algorithm['name'])
    
        collect_data('spanish_dict_' + phonetic_algorithm['name'] + '.csv',
                    phonetic_algorithm['name'] + '_results.csv',
                    phonetic_algorithm['pkg'], phonetic_algorithm['name'] )
    # End-For: Algorithms list.
    


    pass
