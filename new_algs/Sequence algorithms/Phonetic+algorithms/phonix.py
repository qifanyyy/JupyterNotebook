'''
# Phonix and Soundex Python implementation
This is an implementation of the phonix phonetic search algorith [1,2]. This follows the perl[3] and [4] C implementations.

Phonix (phonetic indexing) is a technique based on Soundex, but to which
'phonetic substitution' has been added as an integral part of both the encoding
and the retrieval processes [1]. It is fairly complex, consisting of about 100-160 rules (several rules can be collapsed if they are described using regular expressions. This causes wildly different reports on the number of rules in the litterature)

The main jist of the algorithm is that rules based on phonetic spelling are applied to the search and target strings, after which the initial character is saved and all other characters are represented by a numeric value depending on which of 8 groups it belongs to. Finally the 0-group is pruned.

Phonix is the same as soundex, only with different groups, a pre-processing step that applies the rules and a seperation of codes into a search key and an ending-sound. If we use the soundex groups and skip the pre-processing and splitting parts, we have soundex. Since this can be achieved in about 3 lines of code, I have decided to include soundex here, even though it is widely available.

## Outline of phonix algorithm

This algorithm maps a string `name` -> string `phonix code`, consisting of 1 letter followed by several digits. The algorithm assumes all characters in `name` are Alphabetic.

a) Perform phonetic substitutions (see Appendix);
    - only the specified characters are dropped, eg. the V or vowel is not 
      dropped in the substitution of 'N' for 'PN' when 'PNv' is true;
    - the parameters are applied in the specified order;
    - process all occurrences of one substitution before proceeding to the next
    - the result of a substitution may create new target strings for substitution 
      by subsequent parameters.
b) Retain the first character for the retrieval code.

c) Replace by 'v' if A, E, I, O, U or Y.

d) Where names end in ES, drop the E.

e) Append an E where names end in A,I,O,U or Y.

0 Drop the last character regardless.

g) Drop the new last character if not A,E,I,O,U or Y.

h) Repeat g) until a vowel (including Y) is found. This results in a word or name without its ending-sound.

i) Strip all occurrences of A,E,I,O,U,Y,H and W.

j) Remove one of all duplicate successive consonants.

k) Replace ALL consonants by their numeric values.

1) Prefix the retrieval code with the retained first character (may be a 'v'[lowercase - see above]).

m) Repeat i), j) and k) on the characters removed as stripped ending-sounds

---

### The PHONIX ending-sound algorithm is:

a) If the ending-sound values of an entered name and a retrieved name are the same, the retrieved name is a LIKELY candidate.

b) If an entered name has ending-sound value, and the retrieved name does not, then the retrieved name is a LEAST-LIKELY candidate.

c) If the two ending-sound values are the same for the length of the shorter, and the difference in length between the two ending-sound values is one digit only, then the retrieved name is a LESS-LIKELY candidate.

d) All other cases result in LEAST-LIKELY candidates.

## Variations of PHONIX and PHONIX Common

According to [5] there are several variants of the Phonix algorithm, such as Phonix4, Phonix8 and PhonixE, which are different in code lengths and components. However, Gong fails to cite these different variations, so it is not possible to implement them.

However, looking at examples of phonix keys from the sencondary litterature, it appears that the common interpretation of PHONIX differs from how it was described by Gadd. I have made a second implementation called *PHONIX Common* which matches examples in the secondary litterature by skipping the splitting steps (O-M) and doesn't include the numeric value of the first letter.

---

(C) Copyright 2015, Mads Olsgaard, http://olsgaard.dk
released under [BDS 3](http://opensource.org/licenses/BSD-3-Clause)

---

1. Gadd, T. N. “‘Fisching Fore Werds’: Phonetic Retrieval of Written Text in Information Systems.” Program 22, no. 3 (1988): 222–37.
2. ———. “PHONIX: The Algorithm.” Program 24, no. 4 (1990): 363–66.
3. https://github.com/maros/Text-Phonetic/blob/master/lib/Text/Phonetic/Phonix.pm
4. soundex.c in [freeWAIS-sf-2.2.10.tar.gz](https://github.com/walkingintopeople/freeWAIS/raw/master/wais/freeWAIS-sf-2.2/freeWAIS-sf-2.2.10.tar.gz)
5. Gong, Ruibin, and Tony K. Y. Chan. “Syllable Alignment: A Novel Model for Phonetic String Search.” IEICE TRANSACTIONS on Information and Systems E89-D, no. 1 (January 1, 2006): 332–39.


'''
import re

######################################################################
########## init variables and rules ##################################
######################################################################
# init variables and rules

vowel = '[AEIOU]';
vowely = '[AEIOUY]';
consonant = '[BCDFGHJLMNPQRSTVXZXY]';



# Define the letter groups

                # ABCDEFGHIJKLMNOPQRSTUVWXYZ
phonix_digits =  '01230720022455012683070808'
soundex_digits = '01230120022455012623010202'



# list of transformation/substitution rules
#            [pattern, substitution]

rules_a = [  [re.compile(r'[^A-Z]'), r''], #Remove all non-alphabet characters. Note that name should be uppercased before applying rules
             
             [re.compile(r'DG'),    r'G'],
             [re.compile(r'C(?=[OAU])'),    r'K'],  # Covers several rules in soundex.c [CO, CA, CU]
             [re.compile(r'C[YI]'),    r'SI'],    # Covers [CY, CI]
             [re.compile(r'CE'),    r'SE'],
             [re.compile(r'^CL(?={})'.format(vowel) ),    r'KL'],
             [re.compile(r'CK'),    r'K'],
             [re.compile(r'[GJ]C$'),    r'K'],
             [re.compile(r'^CH?R(?={})'.format(vowel)),    r'KR'],
             [re.compile(r'^WR'),    r'R'],
             [re.compile(r'NC'),    r'NK'],
             [re.compile(r'CT'),    r'KT'],
             [re.compile(r'PH'),    r'F'],
             [re.compile(r'AA'),    r'AR'], 
             [re.compile(r'SCH'),    r'SH'],
             [re.compile(r'BTL'),    r'TL'],
             [re.compile(r'GHT'),    r'T'],
             [re.compile(r'AUGH'),    r'ARF'],
             [re.compile(r'(?<={0})LJ(?={0})'.format(vowel)),    r'LD'], #
             [re.compile(r'LOUGH'),    r'LOW'],
             [re.compile(r'^Q'),    r'KW'],
             [re.compile(r'^KN'),    r'N'],
             [re.compile(r'GN$'),    r'N'],
             [re.compile(r'GHN'),    r'N'],
             [re.compile(r'GNE$'),   r'N'],
             [re.compile(r'GHNE'),   r'NE'],
             [re.compile(r'GNES$'),  r'NS'],
             [re.compile(r'^GN'),    r'N'],
             [re.compile(r'(?<=\w)GN(?={})'.format(consonant)),    r'N'],
             [re.compile(r'^PS'),    r'S'],
             [re.compile(r'^PT'),    r'T'],
             [re.compile(r'^CZ'),    r'C'],
             [re.compile(r'(?<={})WZ(?=\w)'.format(vowel)),    r'Z'],
             [re.compile(r'(?<=\w)CZ(?=\w)'),    r'CH'],
             [re.compile(r'LZ'),    r'LSH'],
             [re.compile(r'RZ'),    r'RSH'],
             [re.compile(r'(?<=\w)Z(?={})'.format(vowel)),    r'S'],
             [re.compile(r'ZZ'),    r'TS'],
             [re.compile(r'(?<={})Z(?=\w)'.format(consonant)),    r'TS'],
             [re.compile(r'HROUGH'),    r'[REW]'],
             [re.compile(r'OUGH'),    r'OF'],
             [re.compile(r'(?<={0})Q(?={0})'.format(vowel)),    r'KW'],
             [re.compile(r'(?<={0})J(?={0})'.format(vowel)),    r'Y'],
             [re.compile(r'^YJ(?={})'.format(vowel)),    r'Y'],
             [re.compile(r'^GH'),    r'G'],
             [re.compile(r'(?<={})GH$'.format(vowel)),    r'E'],
             [re.compile(r'^CY'),    r'S'],
             [re.compile(r'NX'),    r'NKS'],
             [re.compile(r'^PF'),    r'F'],
             [re.compile(r'DT$'),    r'T'],
             [re.compile(r'(?<=[TD])L$'),    r'IL'], # Combines the TL and DL rules
             [re.compile(r'YTH'),    r'ITH'],
             [re.compile(r'^TS?J(?={})'.format(vowel)),    r'CH'], #combines the TJ and TSJ rules
             [re.compile(r'^TS(?={})'.format(vowel)),    r'T'],
             [re.compile(r'TCH'),    r'CHE'],
             [re.compile(r'(?<={})WSK'.format(vowel)),    r'VSIKE'],
             [re.compile(r'^[PM]N(?={})'.format(vowel)),    r'N'],
             [re.compile(r'(?<={})STL'.format(vowel)),    r'SL'],
             [re.compile(r'TNT$'),    r'ENT'],
             [re.compile(r'EAUX$'),    r'OH'],
             [re.compile(r'EXCI'),    r'ECS'],
             [re.compile(r'X'),    r'ECS'],
             [re.compile(r'NED$'),    r'ND'],
             [re.compile(r'JR'),    r'DR'],
             [re.compile(r'EE$'),    r'EA'],
             [re.compile(r'ZS'),    r'S'],
             [re.compile(r'(?<={0})H?R(?={1})'.format(vowel, consonant)),    r'AH'], # combines R and HR rule
             [re.compile(r'(?<={})HR$'.format(vowel)),    r'AH'], 
             [re.compile(r'RE$'),    r'AR'],
             [re.compile(r'(?<={})R$'.format(vowel)),    r'AH'],
             [re.compile(r'LLE'),    r'LE'],
             [re.compile(r'(?<={})LE(S?)$'.format(consonant)),    r'ILE\1'], #combines LE and LES rules
             [re.compile(r'E$'),    r''],
             [re.compile(r'ES$'),    r'S'],
             [re.compile(r'(?<={})SS$'.format(vowel)),    r'AS'],
             [re.compile(r'(?<={})MB$'.format(vowel)),    r'M'],
             [re.compile(r'MPTS'),    r'MPS'], #Why not just change to MS, if the next rule will do it anyway?
             [re.compile(r'MPS'),    r'MS'],
             [re.compile(r'MPT'),    r'MT'],
        ]

rules_de = [ [re.compile(r'ES$'),    r'S'], #STEP D in algorithm.
             [re.compile(r'({})$'.format(vowely)),    r'\1E'], # STEP E in algorithm.
                                                               # Appending a vowel is important for splitting name
                                                               # into initial and ending-sound
            
             [re.compile(r'^({}+)$'.format(consonant)), r'\1E'], # If a name has no vowels, STEP F and G will fail in code
                                                                # Adding a dummy vowel ensures there will be a final
           ]


######################################################################
#################### FUNCTIONS #######################################
######################################################################

def _encode(name, digits, len=4):
    # The encoding step of phonix is the same as the encoding step of
    # soundex, except other codes are used.
    
    # name should be uppercased before calling this function!

    key = ''

    # translate alpha chars in name to soundex digits
        
    ord_A = 65 #No need to call ord everytime
    
    for c in name:
        if c.isalpha():
            d = digits[ord(c)-ord_A]
            
            # duplicate consecutive soundex digits are skipped
            if not key or (d != key[-1]):
                key += d

    # remove all 0s from the soundex code
    key = key.replace('0','')

    return key


def soundex(name):
    key = _encode(name.upper(), soundex_digits)
    return (name[0].upper()+key[1:]+'000')[:4]

def apply_rules(name, rules):
    for rule in rules_a:
        name = rule[0].sub(rule[1], name)    
    return name

def phonix(name, verbose = False):
    ''' Takes a string `name` and generates a phonix phonetic key.
    The key is a touple consisting of the retrieval code and ending-sound
    as described in "The Phonix Algorithm", 1990, doi: 10.1108/eb047069
    
    input:      string that needs to be converted to a key
    Returns:    a touple key consisting of a retrieval code and ending-sound 
    
    if `verbose` == true, the function also returns the name after the phonetic
    substitution rules described in step A the paper.'''
    
    name = name.upper()
    
    #Apply all phonetic substitution rules sequentially, STEP A
    name = apply_rules(name, rules_a) 
    
    #retain rule. STEP B and C
    first_char = name[0] if name[0] not in vowely else 'v' 
    
    #Apply substitution rule from STEP D and E
    name = apply_rules(name, rules_de)
    
    # Extract and remove ending-sound, STEP F and G
    # Gadd uses ending-sound instead of final, and doesn't give the initial 
    # part of the name a nomenclature.
    
    for i in range(1, len(name)):
        if name[-(i+1)] in vowely:
            initial, final = name[:-i], name[-i:]
            break
            
    else:   # If we never hit the break statement. This happens if len(name) <= 2 
            # or consist of any number of consonants ending with a vowel, like fffffu
            # It is unclear from Gadd how such edge-cases should be handled. I assume the
            # entire name, since G is described as being recursive.
        
        initial, final = "E", name  # The 'E' is a dummy vowel, that will dissappear once 
                                    # `initial` is encoded. The entire name will be stored in
                                    # `final`. Retrieval code will thus become the initial letter. 
                                    # That is "Fu" -> ('F', '7')
        
    key = (first_char+_encode(initial, phonix_digits), _encode(final, phonix_digits) ) #Apply STEP I, J and K
    if verbose:
        return name, key
    
    return key

def phonix_common(name, verbose=False, length=4):
    ''' similar to Phonix function, only it generates results similar to what is
    found in the secondary litterature about the Phonix algorithm, such as Christensen 2012
    and the freeWAIS-sf implementation.
    This algorithm does the phonetic substitution following STEP A, but then generates the key
    in a similar fashion to soundex, only using the phonix mappings. This means that no 
    retrieval code and ending-sound code are generated, instead the key consist of only 1 code.
    Moreover, the numerical value for the first letter is not stored in the key at all,
    but first letter vowels are converted to 'v', however. '''
    
    name = name.upper()
    
    #Apply all phonetic substitution rules sequentially, STEP A
    name = apply_rules(name, rules_a)
    
    first_char = name[0] if name[0] not in vowely else 'v' 
    
    key = _encode(name.upper(), phonix_digits)
    
    key = (first_char+key[1:]+'0'*length)[:length] 
    
    if verbose:
        return name, key
    
    return key

def phonix_search_key(search_key, key_corpus):
    ''' Search for a key in a corpus of names. `key_corpus` should
    be an iterable of keys generated by the `phonix()` function.
    Return likely, less-likely and least-likely candidates according to
    the phonix search algorithm (or phonix ending-sound algorithm) as described 
    in "The Phonix Algorithm", 1990, doi: 10.1108/eb047069
    
    input:       search_key: a single key generated by the `phonix()` function
                 corpus_key: a list of keys generated by the `phonix()` function.
    
    returns:     3 lists of integers. Integers represent index keys to the key_corpus variable
                 likely, less_likely, least_likely '''
    
    likely, less_likely, least_likely = [],[],[]
    
    initial, final = search_key
    
    for i, (ini, fin) in enumerate(key_corpus):
        if initial == ini:
            
            # STEP A
            if fin == final:
                likely.append(i)
                continue # ignore remaining code and continue the for-loop 
            # STEP B            
            if len(final) > 1 and len(fin) ==0:
                least_likely.append(i)
                continue
            # STEP C            
            shortest = max(len(fin), len(final))
            if fin[:shortest] == final[:shortest] and abs(len(fin)-len(final)) == 1:
                less_likely.append(i)
                continue
            #STEP D
            least_likely.append(i)
            
    return likely, less_likely, least_likely  


######################################################################
####################### Main #########################################
######################################################################


def main():
	# Do some sanity tests
	# Names and codes taken from "Data-centric systems and applications" 
    # By Peteer Christensen, Springer 2012

    columns = '{:14}'*7
    hr = "-"*7*14

    test_names = ['peter', 'pete', 'pedro', 'stephen', 'steve', 'smith', 'smythe', 'gail', 'gayle', 'christine', 
                  'christina', 'kristina']
    soundex_codes = ['p360', 'p300', 'p360', 's315', 's310', 's530', 's530', 'g400', 'g400', 'c623', 'c623', 
                     'k623']
    phonix_codes = ['p300', 'p300', 'p360', 's375', 's370', 's530', 's530', 'g400', 'g400', 'c683', 'c683', 
                    'k683']

    print( columns.format('Name', "sndx code", 'Christensen', 'phonix', 'phonix code', 'Christensen', 
                         'phonix_common') )
    print( hr )
    for i, n in enumerate(test_names):
        p = phonix(n, verbose=True)
        print( columns.format(n, soundex(n), soundex_codes[i], p[0], ','.join(p[1]), phonix_codes[i], 
                             phonix_common(n)))

    # Now let's test against codes published by Gadd himself in "Fisching fore werds",
    # 1988. Gadd doesn't publish any examples split into retrieval code and ending-sound, 
    # but if we collapse the touples, we see that this algorithm matches the one outlined 
    # by Gadd.
    print('\n'*3)
    test_names = ['Knight', 'Night', 'Nite', 'Write', 'Wright', 'Rite', 'White', 'Weight', 
                  'Yaeger', 'Yoga', 'Eager', 'Auger']
    soundex_codes = ['K523', 'N230', 'N300', 'W630', 'W623', 'R300', 'W300', 'W230',
                     'Y230', 'Y800', 'E230', 'A230']
    phonix_codes = ['N53','N53','N53', 'R63', 'R63', 'R63', 'W3','W3',
                    'v2', 'v2', 'v2', 'v2']

    print( 'Name, \t soundex_code, \ttrue, \tphonix,\t phonix code,\ttrue\n' )
    for i, n in enumerate(test_names):
        p = phonix(n, verbose=True)
        print( '\t'.join([n+'    ', soundex(n), soundex_codes[i], p[0]+'\t', ','.join(p[1]), phonix_codes[i]]) )

    # Let's do some retrieval! Here we load about 155.947 names collected
    # from the 1990 US census, and do some retrievals.

    try:
        corpus = open("names.csv", "r").read().split(',')
        print('\n'*3)
        key_corpus =[phonix(name) for name in corpus]
        term = "knight"
        key = phonix(term)
        likely, less_likely, least_likely = phonix_search_key(key, key_corpus)

        columns = '{:<13}'*4
        hr = "-"*4*13

        print( "Showing the first  likely 10 results from names.csv that match", term )
        print( hr )
        print( columns.format("Search term", "Result term", "phonix phono", "phonix key") )
        print( hr )
        for l in likely[:10]:
            k = phonix(corpus[l], verbose=True)
            print( columns.format(term, corpus[l], k[0].lower(), ','.join(k[1])) )

        print( '\n', hr)
        print( columns.format("Number of:", "Likely", "Less-likely", "Least-likely") )
        print( columns.format('', len(likely), len(less_likely), len(least_likely)) )
    except IOError:
        print("<names.csv> not found")

if  __name__ =='__main__':main()