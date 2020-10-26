class meta:
	length=0
	#def __init__(self):
	#	print self.process("schmidt")	
	
	def isSlavoGermanic(self,str):
		for each in ["W","K","CZ","WITZ"]:
			if(each in str):
				return 1;
		return 0;
		
	def isVowel(self,word,start):
		return self.sub(word,start,1,['A','E','I','O','U','Y'])
	
	def sub(self,word,start,count,arr):
		if(start<0 or start>=len(word)):
			return 0
		if(word[start:start+count] in arr):
			return 1
		return 0
	
	def process(self,word):
		primary,secondary="",""
		word=word.upper()
		self.length=len(word)
		current,last=0,self.length-1
		word+="    "
		
		if(word[0:2] in ['GN', 'KN', 'PN', 'WR', 'PS']):
			current+=1
		
		if(word[0] =='X'):
			primary+="S"
			secondary+="S"
			current+=1
		
		while ((len(primary)<4 or len(secondary)<4) and current<self.length):
			symbol = word[current]
			
			if(symbol in ['A','E','I','O','U','Y']):
				if(current==0):
					primary+="A"
					secondary+="A"
				current+=1
				continue
			elif(symbol=="B"):
				primary+="P"
				secondary+="P"
				if(self.sub(word,current+1,1,["B"])):
					current+=2
				else:
					current+=1
				continue
			elif(symbol=='C'):
				if(current>1 \
					and not self.isVowel(word,current-2) \
					and self.sub(word,current-1,3,["ACH"]) \
					and ( not self.sub(word,current+2,1,['I']) \
					and ( not self.sub(word,current+2,1,['E']) \
					or self.sub(word,current-2,6,['BACHER','MACHER'])))):
					primary+='K'
					secondary+='K'
					current+=2
					continue
				#special case 'caesar'
				elif(current==0 and self.sub(word,current,6,["CAESAR"])):
					primary+="S"
					secondary+="S"
					current+=2
					continue
				#	italian 'chianti'
				elif(self.sub(word,current,4,["CHIA"])):
					primary+="K"
					secondary+="K"
					current+=2
					continue
					
				elif(self.sub(word,current,2,["CH"])):
				#find 'michael'
					if(current>0 and self.sub(word,current,4,["CHAE"])):
						primary+="K"
						secondary+="X"
						current+=2
						continue
					
				#greek roots e.g. 'chemistry', 'chorus'
					if(current==0 and \
					(self.sub(word,current+1,5,["HARAC", "HARIS"]) or \
					 self.sub(word,current+1,3,["HOR", "HYM", "HIA", "HEM"])) 
					 and not self.sub(word,0,5,["CHORE"])):
						primary+="K"
						secondary+="K"
						current+=2
						continue
					# germanic, greek, or otherwise 'ch' for 'kh' sound
					#print self.sub(word,current-1,1,["A","O","U","E"])
					#print self.sub(word,current+2,1,["L","R","N","M","B","H","F","V","W","$"])
					#print "#"+word[current+2:current+3]+"#"
					if( (self.sub(word,0,4,["VAN ","VON "]) or \
					self.sub(word,0,3,["SCH"])) \
					or self.sub(word,current-2,6,["ORCHES", "ARCHIT", "ORCHID"])
					or self.sub(word,current+2,1,["T","S"]) \
					or ((self.sub(word,current-1,1,["A","O","U","E"])
					or current==0) \
					and self.sub(word,current+2,1,["L","R","N","M","B","H","F","V","W"," "]))):
						primary+="K"
						secondary+="K"
					else:
					#	print symbol
						if(current>0):
							if(self.sub(word,0,2,["MC"])):
								primary+="K"
								secondary+="K"
							else:
								primary+="X"
								secondary+="K"
						else:
							primary+="X"
							secondary+="X"
					current+=2
					continue
				#e.g. 'czerny'
				if(self.sub(word,current,2,["CZ"]) and \
				not self.sub(word,current-2,4,["WICZ"])):
					primary+="S"
					secondary+="X"
					current+=2
					continue
				#e.g. 'focaccia'
				if(self.sub(word,current+1,3,["CIA"])):
					primary+="X"
					secondary+="X"
					current+=3
					continue
				#double 'C', but not McClellan'
				if(self.sub(word,current,2,["CC"]) \
				and not ( current==1 \
				and self.sub(word,0,1,["M"]))):
					if(self.sub(word,current+2,1,["I","E","H"])\
					and not self.sub(word,current+2,2,["HU"])):
						if((current==1 and self.sub(word,current-1,1,["A"])) \
						or self.sub(word,current-1,5,["UCCEE", "UCCES"])):
							primary+="KS"
							secondary+="KS"
						else:
							primary+="X"
							secondary+="X"
						current+=3
						continue
					else:
						#Pierce's rule
						primary+="K"
						secondary+="K"
						current+=2
						continue
				if(self.sub(word,current,2,["CK","CG","CQ"])):
					primary+="K"
					secondary+="K"
					current+=2
					continue
				
				if(self.sub(word,current,2,["CI","CE","CY"])):
					if(self.sub(word,current,3,["CIO","CIE","CIA"])):
						primary+="S"
						secondary+="X"
					else:
						primary+="S"
						secondary+="S"
					current+=2
					continue
				
				primary+="K"
				secondary+="K"
				
				if(self.sub(word,current+1,2,[" C"," Q"," G"])):
					current+=3
				else:
					if(self.sub(word,current+1,1,["C","K","Q"]) \
					and not self.sub(word,current+1,2,["CE","CI"])):
						current+=2
					else:
						current+=1
				
				continue
			
			elif(symbol=="D"):
				if(self.sub(word,current,2,['DG'])):
					if(self.sub(word,current+2,1,['I','E','Y'])):
						primary+='J'
						secondary+='J'
						current+=3
						continue
					else:
						primary+="TK"
						secondary+="TK"
						current+=2
						continue
				elif(self.sub(word,current,2,['DT','DD'])):
					primary+="T"
					secondary+="T"
					current+=2
					continue
				else:
					primary+="T"
					secondary+="T"
					current+=1
				continue
			
			elif(symbol=="F"):
				if(self.sub(word,current+1,1,["F"])):
					current+=2
				else:
					current+=1
				primary+="F"
				secondary+="F"
				continue
				
			elif(symbol=="G"):
				if(self.sub(word,current+1,1,['H'])):
					if(current>0 and not self.isVowel(word,current-1)):
						primary+="K"
						secondary+="K"
						current+=2
						continue
						
					elif(current<3):
						if(current==0):
							if(self.sub(word,current+2,1,['I'])):
								primary+="J"
								secondary+="J"
							else:
								primary+="K"
								secondary+="K"
							current+=2
							continue
							
					if( (current>1 and self.sub(word,current-2,1,['B','H','D'])) \
							or (current>2 and self.sub(word,current-3,1,['B','H','D'])) \
							or (current>3 and self.sub(word,current-4,1,['B','H'])) ):
						current+=2
						continue
					else:
						if(current>2 and self.sub(word,current-1,1,['U']) \
						and self.sub(word,current-3,1,['C','G','L','R','T'])):
							primary+="F"
							secondary+="F"
						elif(current>0 and word[current-1]!="I"):
							primary+="K"
							secondary+="K"
						current+=2
						continue
				
				elif(self.sub(word,current+1,1,['N'])):
					if(current==1 and self.isVowel(word,0)\
					and not self.isSlavoGermanic(word)):
						primary+="KN"
						secondary+="N"
					else:
						if(not self.sub(word,current+2,2,['EY']) \
						and not self.sub(word,current+1,1,['Y']) \
						and not self.isSlavoGermanic(word)):
							primary+="N"
							secondary+="KN"
						else:
							primary+="KN"
							secondary+="KN"
					current+=2
					continue
				
				elif(self.sub(word,current+1,2,['LI']) and not self.isSlavoGermanic(word)):
					primary+="KL"
					secondary+="L"
					current+=2
					continue
				
				elif(current==0 \
				and (self.sub(word,current+1,1,['Y']) \
				or self.sub(word,current+1,2,["ES","EP","EB","EL","EY","IB","IL","IN","IE","EI","ER"]))):
					primary+="K"
					secondary+="J"
					current+=2
					continue
				
				elif((self.sub(word,current+1,2,["ER"]) \
				or (self.sub(word,current+1,1,["Y"])) ) and \
				not self.sub(word,0,6,["DANGER","RANGER","MANGER"]) \
				and not self.sub(word,current-1,1,["E","I"]) and \
				not self.sub(word,current-1,3,["RGY","OGY"]) ):
					primary+="K"
					secondary+="J"
					current+=2
					continue
				
				elif(self.sub(word,current+1,1,["E","I","Y"]) \
				or self.sub(word,current-1,4,["AGGI","OGGI"]) ):
					if(self.sub(word,0,4,["VAN","VON"]) or \
					self.sub(word,0,3,["SCH"]) or \
					self.sub(word,current+1,2,["ET"]) ):
						primary+="K"
						secondary+="K"
					else:
						if(self.sub(word,current+1,4,["IER "])):
							primary+="J"
							secondary+="J"
						else:
							primary+="J"
							secondary+="K"
					current+=2
					continue
					
				if(self.sub(word,current+1,1,["G"])):
					current+=2
				else:
					current+=1
				
				primary+="K"
				secondary+="K"
				continue
				
			elif(symbol=="H"):
				if((current==0 or self.isVowel(word,current-1) ) \
				and self.isVowel(word,current+1)):
					primary+="H"
					secondary+="H"
					current+=2
				else:
					current+=1
				continue
					
			elif(symbol=="J"):
				if(self.sub(word,current,4,["JOSE"]) or \
				self.sub(word,0,4,["SAN "]) ):
					if(current==0 and self.sub(word,current+4,1,[' ']) or \
					self.sub(word,0,4,["SAN "])):
						primary+="H"
						secondary+="H"
					else:
						primary+="J"
						secondary+="H"
					current+=1
					continue
				
				if((current==0 and not self.sub(word,current,4,["JOSE"]))):
					primary+="J"
					secondary+="A"
				else:
					if(self.isVowel(word,current-1) \
					and not self.isSlavoGermanic(word) and \
					(self.sub(word,current+1,1,["A"]) or \
					self.sub(word,current+1,1,["O"]))):
						primary+="J"
						secondary+="H"
					else:
						if(current==last):
							primary+="J"
						else:
							if(not self.sub(word,current+1,1,["L","T","K","S","N","M","B","Z"])\
							and not self.sub(word,current-1,1,["S","K","L"])):
								primary+="J"
								secondary+="J"
				if(self.sub(word,current+1,1,["J"])):
					current+=2
				else:
					current+=1
				continue
			
			elif(symbol=="K"):
				if(self.sub(word,current+1,1,["K"])):
					current+=2
				else:
					current+=1
				primary+="K"
				secondary+="K"
				continue
			
			elif(symbol=="L"):
				if(self.sub(word,current+1,1,["L"])):
					if((current==self.length-3 and self.sub(word,current-1,4,["ILLO","ILLA","ALLE"]))\
					or ((self.sub(word,last-1,2,["AS","OS"]) or self.sub(word,last,1,["A","O"])) \
					and self.sub(word,current-1,4,["ALLE"]))):
						primary+="L"
						current+=2
						continue;
					else:
						current+=2
				else:
					current+=1
				primary+="L"
				secondary+="L"
				continue
			
			elif(symbol=="M"):
				if((self.sub(word,current-1,3,["UMB"]) and \
				(current+1==last or self.sub(word, current+2,2,["ER"]))) or \
				self.sub(word,current+1,1,["M"])):
					current+=2
				else:
					current+=1
				primary+="M"
				secondary+="M"
				continue
			
			elif(symbol=="N"):
				if(self.sub(word,current+1,1,["N"])):
					current+=2
				else:
					current+=1
				primary+="N"
				secondary+="N"
				continue
			
			elif(symbol=="P"):
				if(self.sub(word,current+1,1,["H"])):
					current+=2
					primary+="F"
					secondary+="F"
					continue
				
				if(self.sub(word,current+1,1,["P","B"])):
					current+=2
				else:
					current+=1
				
				primary+="P"
				secondary+="P"
				continue
			
			elif(symbol=="Q"):
				if(self.sub(word,current+1,1,["Q"])):
					current+=2
				else:
					current+=1
				
				primary+="K"
				secondary+="K"
				continue
			
			elif(symbol=="R"):
				if(current==last and not self.isSlavoGermanic(word)\
				and self.sub(word,current-2,2,["IE"]) and \
				not self.sub(word,current-4,2,["ME","MA"])):
					secondary+="R"
				else:
					primary+="R"
					secondary+="R"
				
				if(self.sub(word,current+1,1,["R"])):
					current+=2
				else:
					current+=1
				continue
			
			elif(symbol=="S"):
				if(self.sub(word,current-1,3,["ISL","YSL"])):
					current+=1
					continue
				
				if(current==0 and self.sub(word,current,5,["SUGAR"])):
					primary+="X"
					secondary+="S"
					current+=1
					continue
				
				if(self.sub(word,current,2,["SH"])):
					if(self.sub(word,current+1,4,["HEIM","HOEK","HOLM","HOLZ"])):
						primary+="S"
						secondary+="S"
					else:
						primary+="X"
						secondary+="X"
					current+=2
					continue
				 
				if(self.sub(word,current,3,["SIO","SIA"]) \
				or self.sub(word,current,4,["SIAN"])):
					if(not self.isSlavoGermanic(word)):
						primary+="S"
						secondary+="X"
					else:
						primary+="S"
						secondary+="S"
					current+=3
					continue
					
				if(( current==0 and self.sub(word,current+1,1,["M","N","L","W"]) ) \
				or self.sub(word,current+1,1,["Z"])):
					primary+="S"
					secondary+="X"
					if(self.sub(word,current+1,1,["Z"])):
						current+=2
					else:
						current+=1
					continue
						
				if(self.sub(word,current,2,["SC"])):
					if(self.sub(word,current+2,1,["H"])):
						if(self.sub(word,current+3,2,["OO","ER","EN","UY","ED","EM"])):
							if(self.sub(word,current+3,2,["ER","EN"])):
								primary+="X"
								secondary+="SK"
							else:
								
								primary+="SK"
								secondary+="SK"
							current+=3
							continue
						else:
							if(current==0 and not (self.isVowel(word,3)) \
							and not self.sub(word,current+3,1,["W"]) ):
								primary+="X"
								secondary+="S"
							else:
								primary+="X"
								secondary+="X"
							current+=3
							continue
					if(self.sub(word,current+2,1,["I","E","Y"])):
						primary+="S"
						secondary+="S"
						current+=3
						continue
					
					primary+="SK"
					secondary+="SK"
					current+=3
					continue
				if(current==last and self.sub(word,current-2,2,["AI","OI"])):
					primary+=""
					secondary+="S"
							
				else:
					primary+="S"
					secondary+="S"
				
				if(self.sub(word,current+1,1,["S","Z"])):
					current+=2
				else:
					current+=1
				continue
			
			elif(symbol=="T"):
				if(self.sub(word,current,4,["TION"])):
					primary+="X"
					secondary+="X"
					current+=3
					continue
				
				if(self.sub(word,current,3,["TIA","TCH"])):
					primary+="X"
					secondary+="X"
					current+=3
					continue
				
				if(self.sub(word,current,2,["TH"]) or \
				self.sub(word,current,3,["TTH"]) ):
					if(self.sub(word,current+2,2,["OM","AM"]) or \
					self.sub(word,0,4,["VAN ","VON "]) or \
					self.sub(word,0,3,["SCH"])):
						primary+="T"
						secondary+="T"
					else:
						primary+="0" # its a zero here represents TH
						secondary+="T"
					current+=2
					continue
				
				if(self.sub(word,current+1,1,["T","D"])):
					current+=2
				else:
					current+=1
				primary+="T"
				secondary+="T"
				continue
					
			elif(symbol=="V"):
				if(self.sub(word,current+1,1,["V"])):
					current+=2
				else:
					current+=1
				primary+="F"
				secondary+="F"
				continue
				
			elif(symbol=="W"):
				if(self.sub(word,current,2,["WR"])):
					primary+="R"
					secondary+="R"
					current+=2
					continue
					
				if(current==0 and \
				((self.isVowel(word,current+1)) \
				or self.sub(word,current,2,["WH"]))):
					if(self.isVowel(word,current+1)):
						primary+="A"
						secondary+="F"
					else:
						primary+="A"
						secondary+="A"
				
				if((current==last and self.isVowel(word,current-1)) or \
				 self.sub(word,current-1,5,["EWSKI","EWSKY","OWSKI","OWSKY"]) or \
				 self.sub(word,0,3,["SCH"])):
					secondary+="F"
					current+=1
					continue
					
				if(self.sub(word,current,4,["WICZ","WITZ"])):
					primary+="TS"
					secondary+="FX"
					current+=4
					continue
				
				current+=1
				continue

			elif(symbol=="X"):
				if(not(current==last and \
				(self.sub(word,current-3,3,["IAU", "EAU"]) or \
				self.sub(word,current-2,2,["AU","OU"]))) ):
					primary+="KS"
					secondary+="KS"
				else:
					#do nothing
					primary+=""
					
				if(self.sub(word,current+1,1,["C","X"])):
					current+=2
				else:
					current+=1
				continue
					
			
			elif(symbol=="Z"):
				if(self.sub(word,current+1,1,["H"])):
					primary+="J"
					secondary+="J"
					current+=2
					continue
				elif(self.sub(word,current+1,2,["ZO", "ZI", "ZA"]) or 
				(self.isSlavoGermanic(word) and \
				(current>0 and word[current-1]!='T'))):
					primary+="S"
					secondary+="TS"
				else:
					primary+="S"
					secondary+="S"
				
				if(self.sub(word,current+1,1,['Z'])):
					current+=2
				else:
					current+=1
				continue
				
			
			else:
				current+=1
				
		primary=primary[0:4]			
		secondary=secondary[0:4]
		return primary,secondary
		
					
#How to use metaphone algorithm				
x=meta()
#to produce primary and secondary hash just use the following
word="sleep"
primary,secondary=x.process(word)
print primary
print secondary
			
		
		
		