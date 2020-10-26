import socket
import json
import sys
import nltk
import re
import csv
import tweepy
import string
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pprint import pprint
from nltk.corpus import *
tmos = ' '

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
print 'Start'

#Access Twitter API
consumer_key = 'SpI3mgC7UKQOHnUcr3jRlQ'
consumer_secret = 'p7Qt4QHCrTWIOYszr9uy7lgrOcgjLyL1bgMSo9U4yM'
access_token = '2206833558-PmY7kN9MbvUbbxqaVc7g5mpKG9mn5Kod0lqcDy1'
access_token_secret = 'Df48hcvchUSZqnt3bpk1raJeao22AXsUEum2sZzZhujox'

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Define pronunciation dictionary and entries
entries = nltk.corpus.cmudict.entries()
prondict = nltk.corpus.cmudict.dict()

#Define variables
dic= {}
text = ''


#Define Stress
def stress(pron):
            return [i[-1] for i in pron if i[-1].isdigit()]

#Stress categories
words_one_two = [w for w, pron in entries if stress(pron) == ['0', '1', '0', '2', '0']]
words_two_one = [w for w, pron in entries if stress(pron) == ['0', '2', '0', '1', '0']]
words_one_zero = [w for w, pron in entries if stress(pron) == ['1', '0', '2', '0', '0']]
words_new = [w for w, pron in entries if stress(pron) == ['0', '1', '0', '0', '0']]
words_new_new = [w for w, pron in entries if stress(pron) == ['0', '1', '0']]

#POS-Tagging
def get_pos(raw):
        #Tag text
        text = nltk.word_tokenize(raw)
        for w in text:
            tagged_text = nltk.pos_tag(text)
        #Print tagged words
        for w in tagged_text:

            print w
            print ' '

while True:

	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	tmos = data
  	print tmos
	if tmos.startswith('y'):
		print "Let's start!"
		for tweet in tweepy.Cursor(api.search, q="google", lang="en").items():

			
			
		#Remove noise from data[links, hashtags, @user]
		    for c in string.punctuation:
		        tweet.text = tweet.text.replace(c, "")
		        #Open  file
		        myFile = open('saving.txt', 'a')
		    clean_tweet = re.sub(r'http\S+|#(\w+)|@(\w+)|RT|"|[^\x00-\x7F]', "", tweet.text)

		    
		    #Tokenize
		    tokens = nltk.word_tokenize(clean_tweet)
		    words = [word.lower() for word in tokens]
		    #print tweet.text
		    print ''
		    print "Tweet"
		    print clean_tweet
		    print '_____________'

		    #POS-Tag streaming data (noise already removed)
		    ##print ' '
		    ##print 'Printing tagged words'
		    get_pos(clean_tweet)
		    myFile.write(str(clean_tweet))
		    #Loop over words in data
		    for word in words:
		        tag = nltk.pos_tag(words)
		        for t in tag:
		            pos = t[1]
		        double = ''
		        single = ''
		        single_pron = ''
		        double_pron = ''
		        homographs = ''
		        homo_pron = ''
		        #Loop over pronunciations in pronunciation corpus
		        for pronunciation in prondict:
		            break
		            #pronunciation = prondict[word]
		            #Check if the word is in the pronunciation corpus
		            
		        while word in prondict:
		            pronunciation = prondict[word]
		            dic[word] = pronunciation
		            if word in prondict and len(prondict[word]) == 2:
		                double = word
		                pronunciation = prondict[double]
		                
		                ##print 'Doubles: ', double, pronunciation
		                break
		            if word in prondict and len(prondict[word]) == 2 and (pos.startswith('V') or pos.startswith('N')): 
		            #(pos == 'NN' or pos == 'NNS' or pos == 'NNP' or pos == 'NNP' or pos == 'NNPS' or pos == 'VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN' or pos == 'VBP' or pos == 'VBZ'):
		                homographs = word
		                pronunciation = prondict[homographs]
		               ## print 'Homographs: ', homographs
		                break
		            if word in prondict and len(prondict[word]) == 1:
		                single = word
		                pronunciation = prondict[single]
		               
		                ##print 'Not doubles: ', single, pronunciation
		                break

		            else:
		                break

		        else:
		            words.remove(word)
		            print word, 'Not here'

		        if word in words:
		            total = (word, pronunciation)
		            myFile.write(str(total))
	                myFile.write('\n') 
		            
	        

		    #Loop over the keys(words) in the dictionary
		    for key in dic.keys():
		        #Write a row to the csv file/ I use encode utf-8
		        
		#print key
		        #Loop over the values(pronunciations)
		        for val in dic.get(key):
		             #print key, val
		            pronunciation = val
		       
		    print 'Tweet words' , words

		    tmos = "End"
		   
		    break
		

	
	if tmos.startswith('En'):

		print 'End!!'


   
  
