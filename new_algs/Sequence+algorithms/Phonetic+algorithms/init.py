#! /usr/bin/env python3

license =\
'''
    This program is intended for transcription, of any compatible, phonetically
    consistent, rule-based, orthography in Devanagari, particularly Sanskrit,
    to the International Phonetic Alphabet (IPA).
	
    Copyright (C) 2017-2018 Aalok Sathe

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    https://www.gnu.org/licenses
'''

from cmd import Cmd
import os
from transcriber_data import transcribe
from transcriber_data import charInRange as checkChar

class Transcriber(Cmd):
	
	inPath = None
	outPath = None
	license = None
	transDict = {}

	def __init__(self, *args):
		super(Transcriber, self).__init__()
		self.license = args[0]
		
	def do_showLicence(self, arg):
		"""Shows a short version of the license of this software."""
		print(self.license)
		
	def do_setInPath(self, arg):
		"""Sets a new path of the input plain-text file (encoded UTF-8)"""
		if self.inPath == None:
			print("No path is currently set.\n")
		else:
			print("Current path is: %s" % self.inPath)
		
		path = input("Please enter a path to a file from which to take input.\n\
Else, input '#' to cancel.\n>\t")
		
		if path != '#':
			try:
				s = open(path, 'r')
				self.inPath = path
			except IOError:
				print("Error: unable to read file from %s.\n\
Please make sure you've entered the correct path." % path)
	
	def do_transcribe(self, arg):
		"""Transcribes either provided string or string read from file"""
		toTranscribe = ""	# The string to be transcribed to IPA
		if len(arg):
			toTranscribe = arg
			#print(toTranscribe)
		else:
			try:
				inFile = open(self.inPath, 'r')
				toTranscribe = inFile.read()
				if self.outPath == None:
					self.outPath = str(self.inPath) + "_SanskritToIPA.out"
			except Exception:
				print("Error: unable to read input from file '%s'"%self.inPath)
		for c in toTranscribe:
			#print(str(c))
			if not checkChar(c):
				#raise Exception("Invalid character: %s"%str(c))
				print("Potential invalid character found: %s. May be represented as-is or ignored."%repr(c))
		self.transDict[toTranscribe] = transcribe(toTranscribe)
		print(self.transDict.get(toTranscribe, "Error: could not transcribe. Please report a bug."))
	
	def do_exit(self, arg):
		"""Exits the program."""
		print ("Quitting.")
		raise SystemExit
		
	def do_quit(self, arg):
		"""Quits the program."""
		self.do_exit(arg)
		
	def do_reportBug(self, arg):
		return None
    	
if __name__ == '__main__':
    prompt = Transcriber(license)
    prompt.prompt = '> '
    try:
    	prompt.cmdloop('''
    SanskritIPA. Copyright (C) 2017-2018  Aalok S.
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions. Use "showLicence" to see the license.''')
    except KeyboardInterrupt :
    	print("\nExiting due to KeyboardInterrupt")
    	raise SystemExit
