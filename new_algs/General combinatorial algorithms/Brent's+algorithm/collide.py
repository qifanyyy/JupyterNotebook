'''
    File name: collisions.py
    Author: Ken Koyanagi
    Course: CSC 152
    Date: 11/7/16
    Python Version: 2.7

    Finds a k collision in the last k bytes of two hashes.

    Hardware Specs:
      Intel Core i7-870 @ 2.93 GHz 
      4 Cores, 8 Threads. Turbo boost to 3.60 GHz

      Intel Core i7-2820QM @ 2.30 GHz
      4, Cores, 8 Threads, Turbo boost to 3.40 GHz 

    Sources:
      https://pdaian.com/blog/collision-finding-the-maxwell-way/
      https://en.wikipedia.org/wiki/Cycle_detection
      https://raw.githubusercontent.com/Simmesimme/cry-hash/master/03/collisions.py
      Crypto Lib:
      https://docs.python.org/2/library/hashlib.html
'''

import hashlib, random, time, os
from string import digits, ascii_uppercase, ascii_lowercase
from itertools import product 

chars = digits + ascii_uppercase + ascii_lowercase

# Define our f(x), uses hashlib
def getHash(message, k, prefix):
  #return the last 2k hex values since 2 hex values = 1 byte
  return hashlib.sha256(prefix + message).hexdigest()[-k*2:]


# Brent's algorithm Implementation for Cycle Detection
# Uses much less than 1GB of memory with single thread
# Birthday Attack used 17GB, compressed mem and used swaps 
# before being killed. Brent's algorithm returned k=7 in 
# ~1.25 hours. Could not find k=8 after ~24 hours of continuous 
# running. Process kept getting killed after hogging up the CPU
# for too long. 
# https://gist.github.com/pdaian/2e10d273210cc02fd510f02ce8a8e12c
# https://en.wikipedia.org/wiki/Cycle_detection#Brent.27s_algorithm
def brent(k, prefix, initial):
  #Prefix is for output purposes. 
  x0 = initial
  m0 = None
  m1 = None

  # Search successive powers of two
  # lam = length of cycle
  power  = lam = 1 
  tortoise = x0
  hare   = getHash(tortoise, k, prefix)       # f(x0) 

  # Search for a match
  while tortoise != hare: 
    if power == lam:                          # Checks to see if it needs a new power of 2
      tortoise = hare
      power *= 2
      lam = 0
    hare = getHash(hare, k, prefix)
    lam += 1                                  # length+1

  # At this point, same hash is found
  # Find Position of the first repetition
  mu = 0                                      # Index of the first element of the cycle
  tortoise = hare = x0                        # Set back to initial
  for i in range(lam):
    # "range(lam) produces list with values 0, 1, ..., lam-1"
    hare = getHash(hare, k, prefix)           # distance b/w tortoise and hare is now lambda

  # Hare and tortoise move at same speed until they agree
  while tortoise != hare:
    m0 = tortoise
    m1 = hare
    tortoise = getHash(tortoise, k, prefix)   # f(tortoise)
    hare   = getHash(hare, k, prefix)         # f(hare)
    mu += 1                                   # Looking from the point of first repetition

  if mu is 0:
    print "Failed to find a collision: x0 was in a cycle!"
    return

  print_results(m0, m1, getHash(m0, k, prefix), k, prefix)


def print_results(m0, m1, hash, k, prefix):
  print "===== Collision Found! ====="
  print "Message A:  ", prefix + m0 
  print "Full Hash:  ", hashlib.sha256(prefix + m0).hexdigest()
  print "Message B:  ", prefix + m1
  print "Full Hash:  ", hashlib.sha256(prefix + m1).hexdigest() 
  print "k Collision:", hash
  print "k Size:     ", k
  print "Time taken: ", time.time() - start_time 
  print "\n"
  # Let me know when a collision is found
  print ('\a')      
  os.system ("say Found a Collision!")

  # Print the information to file
  print >> f, "Message A:  ", prefix + m0 
  print >> x, prefix + m0,    #comma needed to avoid carriage return
  print >> f, "Full Hash:  ", hashlib.sha256(prefix + m0).hexdigest()
  print >> f, "Message B:  ", prefix + m1
  print >> y, prefix + m1,
  print >> f, "Full Hash:  ", hashlib.sha256(prefix + m1).hexdigest() 
  print >> f, "k Collision:", hash
  print >> f, "k Size      ", k
  print >> f, "Time taken: ", time.time() - start_time 
  print >> f, "\n"


if __name__ == '__main__':
    # Keep track of how long it takes to find a k collision
    start_time = time.time()
    print "Script started at:", start_time
    print "\n"

    # Store the collisions found for record
    f = open('collisions.txt', 'w')
    # Outputs for assignment
    x = open('x.bin', 'w')
    y = open('y.bin', 'w')

    # Call Brent's alg.
    # Using only a single thread. No advantage with multithreading found throughout
    # my tests. Turbo boosting with a single core is going to be better than creating
    # multiple threads.  
    brent(8, "Try. ", "1")

    # Close files
    f.close()
    x.close()
    y.close()
