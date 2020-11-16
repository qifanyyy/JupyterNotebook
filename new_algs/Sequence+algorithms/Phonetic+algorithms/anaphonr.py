import nltk
import string
import locale
import re
import time
import random
from nltk.corpus import cmudict

phs = nltk.corpus.cmudict.dict()
filter_characters = string.punctuation.replace("'","").replace("-","")

_PHONEMES = ["AA", "AH", "AE", "AH", "AO", "AW", "AY", "B",  "CH", "D",
			 "DH", "EH", "ER", "EY", "F",  "G",  "HH", "IH", "IY", "JH",
			 "K",  "L",  "M",  "N",  "NG", "OW", "OY", "P",  "R",  "S",
			 "SH", "T",  "TH", "UH", "UW", "V",  "W",  "Y",  "Z", "ZH"]



	
MIN_PHONE_SIZE = 1 # min size of a word in the output
MIN_WORD_SIZE = 2 # min size of a word in the output
NO_DUPLICATES = True # this means "herb slot" and "slot herb" won't both appear for "lobster"
RANDOMIZE_WORDS = True # this means all solutions have their word order NOT in alphabetical order
PRINT_LIMIT = 200
COMPUTE_LIMIT = 2000
TIME_LIMIT = 5
imported = False
startTime = 0


##### subset code #####

import collections

# determines if needle is a subset of haystack
def contained(needle_bag, haystack_bag):
	return not bool(needle_bag - haystack_bag)

# returns a list of all words which are subsets of the superset
def get_candidate_words(letters, min_word_size=1, min_phone_size=1):
	global MIN_PHONE_SIZE
	global MIN_WORD_SIZE
	
	MIN_WORD_SIZE = int(min_word_size)
	MIN_PHONE_SIZE = int(min_phone_size)
	
	candidates = []
	phonemes_superset = phonetify_string(letters)
	
	if(len(phonemes_superset)==0):
		return -1
		
	haystack_bag = collections.Counter(phonemes_superset)
    
	counter = 0;
	path = 'common_combo_dictionary.txt'
	
	for line in open(path, 'r'):
		linesplit = line.split("  ")
		encoded = linesplit[0].strip()
		if(len(encoded)<MIN_PHONE_SIZE):
			continue
		word = linesplit[1].strip()
		if(len(word)<MIN_WORD_SIZE):
			continue
			
		needle_bag = collections.Counter(decode_phonemes(encoded))
		
		if contained(needle_bag, haystack_bag):
			candidates.append(word)
    
	return candidates

## end subset code ##


class Node(object):
	def __init__(self, letter='', final=False, depth=0, originalword=''):
		self.letter = letter
		self.final = final
		self.depth = depth
		self.children = {}
		self.originalword = originalword
	def add(self, letters, originalword=''):
		node = self
		for index, letter in enumerate(letters):
			is_final = index==len(letters)-1
			if letter not in node.children:
				node.children[letter] = Node(letter, is_final, index+1, originalword)
			
			node = node.children[letter]
			
			if is_final:
				node.originalword = originalword
	def anagram(self, letters):
		tiles = {}
		for letter in letters:
			tiles[letter] = tiles.get(letter, 0) + 1
		min_length = len(letters)
		return self._anagram(tiles, [], self, min_length)
	def _anagram(self, tiles, path, root, min_length):
		global startTime
		
		if self.final and self.depth >= MIN_PHONE_SIZE:
			word = ''.join(path)
			length = len(word.replace(' ', ''))
			if length >= min_length:
				yield word 
			path.append(' ')

			

			for word in root._anagram(tiles, path, root, min_length):
				if NO_DUPLICATES:
					ws = word.split(' ')
					if ws[-1] < ws[-2]:
						continue
					if len(ws) > 2 and (ws[-1] < ws[-3] or ws[-2] < ws[-3]):
						continue
					if len(ws) > 3 and (ws[-1] < ws[-4] or ws[-2] < ws[-4] or ws[-3] < ws[-4]):
						continue
					if len(ws) > 4 and (ws[-1] < ws[-5] or ws[-2] < ws[-5] or ws[-3] < ws[-5] or ws[-4] < ws[-5]):
						continue
				yield word 
			path.pop()
		for letter, node in self.children.iteritems():
			count = tiles.get(letter, 0)
			if count == 0:
				continue
			tiles[letter] = count - 1
			path.append(letter)
			for word in node._anagram(tiles, path, root, min_length):
				yield word 
			path.pop()
			tiles[letter] = count

def load_dictionary(phoneme_to_word_dictionary, blacklist):
	result = Node()

	path = 'common_combo_dictionary.txt'

	printFlag = True
	for line in open(path, 'r'):
		linesplit = line.split("  ")
		encoded = linesplit[0].strip()
		if(len(encoded)<MIN_PHONE_SIZE):
			continue
		word = linesplit[1].strip()
		if(len(word)<MIN_WORD_SIZE):
			continue

		if word in blacklist:
			continue
		
		result.add(encoded, word)

		if(encoded not in phoneme_to_word_dictionary):
			phoneme_to_word_dictionary[encoded] = [word]
		else:
			phoneme_to_word_dictionary[encoded].append(word)
		
	return result






# makes the input neater, so that there's a better
# chance we will find the input words in the dictionary
def trim_punctuation(input):
	
	input = input.strip().lower() # parse it down
	# filter out punctuation 
	# input = input.translate(string.maketrans("",""), filter_characters)
	input = input.replace("-"," ")
	return input

# Takes a string and spits out a list of all the phonemes
def phonetify_string(input):
	
	input = trim_punctuation(input)
	word_list = string.split(input, " ")
	phoneme_list = []
	
	for word in word_list:
		phonemes = word_to_phonemes(word)
		if(len(phonemes)==0):
			#write( '\n-_- The word [' + word + '] is not in the Phoneme Dictionary' )
			return ''
		phoneme_list.append(phonemes)

	phoneme_list_joined = [j for i in phoneme_list for j in i]
	return phoneme_list_joined




""""
raleigh the lie
ernet henley indictus
misfits cover metallica


REMIX EXISTING AWESOME TIMBRES
1) they're already awesome
2) cultural synaptification
"""

# removes the ER0, ER1 business --> just ER
def parse_phonemes(phonemes):
	for p in phonemes:
		phonemes[phonemes.index(p)] = p[:2]
		
	return phonemes

def word_to_phonemes(word):
	try:
		phonemes = phs[word][0]
		parse_phonemes(phonemes)
		return phonemes
	except:
		#print '\n-_- The word [' + word + '] is not in the Phoneme Dictionary'
		return []

# returns encoded string
def encode_word(word):
	phonemes = word_to_phonemes(word)
	if(len(phonemes)==0):
		return ''
	else:
		return encode_phonemes(phonemes)

def encode_phonemes(phonemes):
	encoded = ""
	for p in phonemes:
		encoded = encoded + phoneme_to_ascii(p)
	return encoded
	
def phoneme_to_ascii(phone):
	#write( "phone: ", phone)
	return chr(_PHONEMES.index(phone) + 0x30)


def list_homonyms(string, dictionary):
	if string in dictionary:
		homonyms = []
		for w in dictionary[string]:
			if len(w)>=MIN_WORD_SIZE:
				homonyms.append(w)
				
		return homonyms
	else:
		write( "ERROR string not in dictionary")
		return []

def decode_string(string):
	phonemes = decode_phonemes(string)

	# write( "decode_string", string, phonemes, ''.join(phonemes))
	return ''.join(phonemes)
	# phoneme_list -> word

def decode_phonemes(string):
	phonemes = []
	for a in string:
		phonemes.append(ascii_to_phoneme(a))
	return phonemes

def ascii_to_phoneme(ascii):
	return _PHONEMES[ord(ascii) - 0x30]   #####


def build_dictionary():
	thefile = file("common_combo_dictionary.txt", "w")
	codelist = []
	wordlist = {}

	i = 0
	#for word in phs:
	for word in open('TWL06.txt', 'r'):
		word = word.strip().lower()
		code = encode_word(word)
		if(code==''):
			continue
		
		if(code in wordlist):
			code = code + "   " + str(i)
			#write( 'newcode, ' + code)
		
		codelist.append(code)	
		wordlist[code] = word
		i = i + 1

	codelist.sort()
	
	for code in codelist:
		realcode = re.sub('\s\s\s\d+','',code)
		thefile.write("%s  %s\n" % (realcode, wordlist[code]))

def main_imported(phrase, min_word_size, min_phone_size, randomize_words, blacklist, whitelist, oneAnswerOnly, themainpage):
	global imported, input_phrase, input_min_word_size, input_min_phone_size, input_randomize_words, input_blacklist, input_whitelist, feelingLucky, mainpage
	input_phrase = phrase
	input_min_word_size = min_word_size
	input_min_phone_size = min_phone_size
	input_randomize_words = randomize_words
	input_blacklist = blacklist + " " + phrase
	input_whitelist = whitelist
	feelingLucky = oneAnswerOnly
	mainpage = themainpage
	
	imported = True
	return main()
	
def write(text,br=1):
	global imported, mainpage, feelingLucky
	if imported:
		mainpage.response.out.write(text)
		if(br):
			mainpage.response.out.write("<br>")
	else:
		print (text)

def whitelistification(phoneme_list, whitelist):

	whitelist_phonemes = phonetify_string(whitelist)
	if(whitelist_phonemes == ''): 
		return []
	for phoneme in whitelist_phonemes:
		try:
			phoneme_list.remove(phoneme)
		except:	
			write("No solution exists. Try making your white list smaller. ")
			return []
	
	return phoneme_list
		
def main():
	#write( 'building dictionary')
	#build_dictionary()
	#write( 'done')
	#return
	global MIN_WORD_SIZE
	global MIN_PHONE_SIZE
	global RANDOMIZE_WORDS
	global imported, input_phrase, input_min_word_size, input_min_phone_size, input_randomize_words, input_blacklist, input_whitelist, feelingLucky, mainpage, startTime
	
	"""
	write(input_phrase)
	write(input_min_word_size)
	write(input_min_phone_size)
	write(input_randomize_words)
	write(input_blacklist)
	write(input_whitelist)
	"""
	
	while True:
		if(imported):
			letters = input_phrase
		else:
			letters = raw_input('Enter letters: ')
			if not letters:
				break
		
		phoneme_list = phonetify_string(letters)
		if(len(phoneme_list)==0):
			if(feelingLucky):
				return "I refuse to find an anaphone for this horrendous input: " + letters
			if(imported):
				write("Psh. You think I know what this sounds like?: "+letters+"")
				return
				break
			else:
				continue
		
		if not feelingLucky: 
			write(letters)
			write(phoneme_list)
		if(imported):
			MIN_WORD_SIZE = input_min_word_size
		else:
			MIN_WORD_SIZE = raw_input('MIN_WORD_SIZE: ');
		if(len(str(MIN_WORD_SIZE))==0):
			MIN_WORD_SIZE = 1
		else:
			MIN_WORD_SIZE = int(MIN_WORD_SIZE)
			
		if(imported):
			MIN_PHONE_SIZE = int(input_min_phone_size)

		if(imported):
			RANDOMIZE_WORDS = input_randomize_words
		
		if(imported):
			blacklist_string = input_blacklist
		else:	
			blacklist_string = raw_input('Blacklist [words separated by a space]: ')
		blacklist = blacklist_string.strip().lower().split(' ')
		
		if(imported):
			whitelist_string = input_whitelist
		else:	
			whitelist_string = raw_input('Whitelist [words separated by a space]: ')
		whitelist_string.strip().lower()
		whitelist = whitelist_string.split(' ')
		if(len(whitelist_string)>0):
			phoneme_list = whitelistification(phoneme_list, whitelist_string)
		if(len(phoneme_list)==0):
			return -2
		
		phoneme_to_word_dictionary = {}
		if not feelingLucky: 
			write( 'Loading word list...')
		words = load_dictionary(phoneme_to_word_dictionary, blacklist)
		
		if not feelingLucky: 
			write( 'Generating anaphone solutions...')
		
	   
		#print phoneme_list
		encoded_letters = encode_phonemes(phoneme_list)
		#print encoded_letters
		
		count = 0
		solutions = []
		
		startTime = time.time()
		
		for solution in words.anagram(encoded_letters):
			
			#decoded_solution = ""
			solution_words = solution.split(" ")

			homonym_lists = []
			for encoded_word in solution_words:
				homonym_lists.append(list_homonyms(encoded_word, phoneme_to_word_dictionary))
				
			homonym_solutions = iterate_combos(homonym_lists)

			for s in homonym_solutions:
				decoded_solution = ""
				for homonym in s:
					decoded_solution = decoded_solution + " " + homonym
				count += 1
				solutions.append(decoded_solution.strip())

			elapsed = (time.time() - startTime)
			if elapsed > TIME_LIMIT:
				if not feelingLucky: 
					write("Solution-finding time limit reached: " + str(elapsed) + " seconds.")
				break 
				
			if count > COMPUTE_LIMIT:
				break

		if not feelingLucky: 
			write( '%d results.' % count)
			if count > PRINT_LIMIT:
				write( 'Printing first %d' % PRINT_LIMIT )


		solutions.sort(wordLengthRatioComparison)
		
		if not feelingLucky: 
			write( '--------------------------')
			if count == 0:
				write ('Sorry, no words were found fitting these constraints. Try loosening it up a bit ')
				return
			
		i = 0
		for solution in solutions:
			if i == PRINT_LIMIT:
				break
			
			#if RANDOMIZE_WORDS: 
			#	temp_array = solution.split(' ')
			#	random.shuffle(temp_array)
				
				solution = ' '.join(temp_array)
			the_solution = (whitelist_string + ' ' + solution).strip()
			
			if feelingLucky: 
				if the_solution != letters:
					return the_solution
			else: 
				write("<tr><td>" + ' '.join(phonetify_string(the_solution)) + "</td><td class=solutionTableSolution>" + the_solution + "</td></tr>",0)
			i = i + 1
			
		if imported:
			break # infinite loop is only for console version
		   

# sorts solutions according to least number of small words first
def wordLengthRatioComparison(a, b):
	a = a.split(" ")
	b = b.split(" ")

	a_ratio = 1000 * sum(map(len, a))/len(a) 
	b_ratio = 1000 * sum(map(len, b))/len(b)

	
	return b_ratio - a_ratio 

# takes [[1],[2 3],[4 5],[6]] and produces [[1,2,4,6],[1,2,5,6],[1,3,4,6],[1,3,5,6]]
def iterate_combos(a=[]):
	r = [[]]
	for x in a:
		r = [ i + [y] for y in x for i in r ]
	return r

if __name__ == '__main__':
	main()

