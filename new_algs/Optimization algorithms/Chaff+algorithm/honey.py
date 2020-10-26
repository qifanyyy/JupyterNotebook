'''

    1. Preprocessing:

    For each input password, generate a look-alike password, a high-probability password and a tough nut password.
    The three passwords will then be sent into the noise password generation pipeline

        - Look-alike
             |
              -- Generate a look-alike password by randomly finding a password from the RockYou dataset
             |   according to the arbitrarily truncated input password
             |   e.g. michael1215 -> michel0998s@1
             |
              -- Modify some digits of numbers
                 e.g. john19960216 -> john19960215

        - High-probability Passwords
             |
              -- Add a healthy mix of high-probability passwords from the dataset to the honeywords
             |
              -- Ensemble of high-probability passwords (not implemented)
                 e.g. 'daniel' + '123456'

        - Tough Nut Passwords
             |
              -- Add pwds that are random combination of chars and nums



    2. Honeywords Generation Pipeline:

        - Permutation
             |
              -- Permute the position of charater and numbers present in the password (not implemented)
             |   e.g. michael1215 -> 1215michael
             |
              -- Permute the position of numbers by chunks of two digits (not implemented)
             |   e.g. michael0206 -> michael0602
             |
              -- Permute the position of charaters with one another in chunks (not implemented)
                 e.g. michael0206 -> leamich0206

        - Shorten
             |
              -- Delete even number of digits from numbers at the end of the password
                 e.g. john19960216 -> john199602, john1996

        - Lengthen
             |
              -- Extend with numbers that look like date, since according to the heat map, birthdays are often used as passwords
             |   e.g. john -> john20161015, john161015
             |
              -- Add punctuations at the beginning or end of chars or numbers (whitespaces, underscore, period)
                 e.g. john19960216 -> john19960216!

        - Other Methods
             |
              -- Capitalize and de-capitalize leading character
                 e.g. john19960216 -> John19960216

'''

import random
import string
import sys
import time
import pygtrie
import pdb

class honey_words_generator():

    def main(self, T):

        try:
            assert (len(sys.argv) == 4)
            self.n, self.input_file, self.output_file = sys.argv[1:]
        except:
            sys.exit('Please provide three arguments')

        assert (self.n.isdigit() and 0 < int(self.n) <= 100), 'First argument should be the number of honeywords to output, between 0 and 100'

        self.T = T
        self.n = int(self.n)
        self.readfile()
        self.import_dataset()

        f = open(self.output_file, 'w')

        for pwd in self.input_pwds:
            # don't forget to include the real password in the honeywords
            honeywords = set( self.generate_honeywords(pwd) )
            honeywords.remove(pwd)

            if self.T == 'full' and len(honeywords) < self.n - 1:
                honeywords.append( random.sample( self.trie.keys(), self.n - len(honeywords) ) )
            if self.T == 'top100' and len(honeywords) < self.n - 1:
                honeywords.append( random.sample( self.data, self.n - len(honeywords) ) )

            honeywords = set( self.generate_honeywords(pwd) )
            honeywords.remove(pwd)
            honeywords = random.sample( honeywords, self.n - 1 ) + [pwd]
            random.shuffle( honeywords )

            print pwd, honeywords, '\n'
            for honeyword in honeywords:
                f.write(honeyword + ', ')
            f.write('\n')

        f.close()


    def generate_test_input(self, size):

        rockyou_dataset = open('./rockyou-withcount.txt', 'r')
        example_input = open('./example_input.txt', 'w')
        random_indice = random.sample(xrange(10000000), size)

        for i, line in enumerate(rockyou_dataset):
            if i in random_indice:
                random_pwd = line.strip().split(' ', 1)[1]
                example_input.write(random_pwd + '\n')

        rockyou_dataset.close()
        example_input.close()
        print 'Generated example input file with random passwords'


    def readfile(self):

        self.input_pwds = []
        f = open(self.input_file, 'r')

        for i, line in enumerate(f):
            self.input_pwds.append( line.strip() )

        print '{} passwords found in input file'.format(i + 1)
        print self.input_pwds


    def import_dataset(self):

        if self.T == 'full':
            self.trie = pygtrie.CharTrie()
        elif self.T == 'top100':
            self.data = []

        f = open('./rockyou-withcount.txt', 'r')
        start = time.time()

        for i, line in enumerate(f):
            try:
                freq, pwd = line.strip().split(' ', 1)
                freq = int(freq)

                if self.T == 'top100':
                    self.data.append( (freq, pwd) )
                    if len(self.data) == 100:
                        break

                if self.T == 'full':
                    if freq >= 10:
                        self.trie[pwd] = freq
                    else:
                        break
            except:
                pass

        end = time.time()
        if self.T == 'full':
            print 'Successfully imported {0} passwords from RockYou dataset ({1:.5f}s)'.format(len(self.trie), (end - start))
        else:
            print 'Successfully imported {0} passwords from RockYou dataset ({1:.5f}s)'.format(len(self.data), (end - start))
        f.close()


    def generate_honeywords(self, input_pwd):

        honeywords = []

        if self.T == 'top100':
            high_prob = random.sample(self.data, 5)
            preprocessed = [ input_pwd ] + [ pwd[1] for pwd in high_prob ]

        elif self.T == 'full':
            # Step 1: generate 3 input-based variations (look-alike, digits modified, original input) of password, 1 high-probability passwords, 2 look-alikes of the high-probability password, and 3 tough nut password
            #         for the look-alike password, find a password that shares the prefix with the arbitratily truncated input password from the dataset
            #         if such a password cannot be found, use the truncated input password

            # create 3 tough nut passwords
            tough_nuts = self.tough_nut( 3, len(input_pwd) )

            # create 1 look alike
            truncate_len = random.randrange(-3, 0)
            try:
                candidates = self.trie.keys( prefix=input_pwd[:truncate_len] )
            except:
                candidates = self.trie.keys()
            look_alike = random.choice(candidates)

            # create 3 high probability passwords (two are look-alikes derived from the first one)
            truncate_len = random.randrange(-3, 0)
            high_prob = random.choice(self.trie.keys())
            try:
                candidates = self.trie.keys( prefix=high_prob[:truncate_len] )
            except:
                candidates = self.trie.keys()
            high_prob = [high_prob] + [random.choice(candidates), random.choice(candidates)]

            # create 1 password with modified random digits of numbers in the original input password
            digit_modified = ''
            for i, char in enumerate(input_pwd):
                if char.isdigit():
                    digit_modified += str(random.randrange(0, 10))
                else:
                    digit_modified += char

            # this is to ensure that there wont be a larger amount of output honeywords that look like the original input
            preprocessed = [ input_pwd, look_alike, digit_modified ] + high_prob + tough_nuts

        honeywords.extend(preprocessed)

        # Step 2: honeywords generation pipeline

        # Lengthen:
        # Method 1: add date-like digits to existing password
        for pwd in preprocessed:
            if pwd.isalpha():
                tmp = pwd + self.random_date_generator()
                honeywords.append(tmp)

        # Method 2: add punctuations to the beginning, end, and in between characters and digits in the existing password
        punctuations = string.punctuation
        for pwd in preprocessed:
            honeywords.append( pwd + random.choice( list(punctuations) ) )
            honeywords.append( random.choice( list(punctuations) ) + pwd )
            idx = self.end_of_alpha(pwd)
            honeywords.append( pwd[0:idx] + random.choice( list(punctuations) ) + pwd[idx:] )

        # Shorten:
        # randomly select half of the honeywords and take away even number of digits from the end of the passwords
        sample = random.sample( honeywords, len(honeywords) / 2 )
        for pwd in sample:
            digits = random.choice([2, 4])
            if pwd[-1:-digits - 1].isdigit():
                honeywords.append(pwd[:-digits])

        # Post-process
        # capitalize leading character for random passwords
        for pwd in random.sample( honeywords, len(honeywords) / 2 ):
            if pwd[0].isalpha() and pwd[0].islower():
                honeywords.append(pwd)

        return honeywords


    def random_date_generator(self):

        year = random.randrange(1950, 2020)
        month = '{0:02d}'.format( random.randrange(1, 13) )
        day = '{0:02d}'.format( random.randrange(1, 32) )
        return random.choice([ str(month)+str(day), str(year)+str(month),  str(year)+str(month)+str(day) ])


    def end_of_alpha(self, string):

        for i, char in enumerate(string):
            if not char.isalpha():
                return i


    def tough_nut(self, size, length):

        chars = string.ascii_letters + string.digits + string.punctuation
        tough_nuts = []

        for i in xrange(size):
            pwd = ''.join( random.sample( chars, length + random.randrange(-4, 5) ) )
            tough_nuts.append(pwd)

        return tough_nuts


if __name__ == '__main__':

    # number of passwords in example input
    test_input_size = 10
    # data set mode: 'full' or 'top100'
    training_set = 'full'

    honeyGen = honey_words_generator()
    honeyGen.generate_test_input(test_input_size)
    honeyGen.main(training_set)
