#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import cgi

from google.appengine.api import users

import anaphonr

layout_top = """
<html>
	<head>
		<style>
		label, input { 
			display:inline-block
		}
		label { 
			width: 280px;
			color: #555
		}
		.headerish { width: 780px; text-align: left; font-size: 16px; margin-bottom: 10px; color: #666 }
		.sidenote { font-size: 12px; color: #666; margin-left: 5px; bottom: 2px; position: relative}
		.whiteListClick { text-decoration: none; }
		.whiteListClick:hover { text-decoration: none; cursor: hand}
		.subsetList { border-radius: 10px; text-align: left; background-color: #999; margin: 10px; padding: 20px; color: #333; }
		.solutionList { border-radius: 10px; font-size: 16px; text-align: left; background-color: #bbb; margin: 10px; padding: 20px; color: #333; }
		
		.solutionTable td { font-size:22px; padding: 5px;  color: #555;} 
		.solutionTable td.solutionTableSolution { color: #000;} 
		
		</style>
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
		<script>
			shifted = false;
			$(document).bind('keyup keydown keypress', function(e){shifted = !e.ctrlKey} );
			
			function isInList(whiteOrBlack,word){
				if(whiteOrBlack!='white'){
					whiteOrBlack = 'black'
				}else{
					whiteOrBlack = 'white'
				}
				listElement = document.getElementById(whiteOrBlack + 'list');
				listString = listElement.value;
				listArray = listString.replace(/\s+/gi, ' ').split(' ')
				listIndex = listArray.indexOf(word);
				return listIndex != -1;
			}
			function addToList(whiteOrBlack, word, remove){
				wordElement = document.getElementById('word_' + word);
				if(whiteOrBlack=='white'){
					oppositeList = 'black'
				}else{
					oppositeList = 'white'
					whiteOrBlack = 'black'
				}
				//alert("shifted "+shifted)
				word = word.toLowerCase().replace(/^\s+|\s+$/g, '');
				listElement = document.getElementById(whiteOrBlack + 'list');
				listString = listElement.value;
				listArray = listString.replace(/\s+/gi, ' ').split(' ')
				listIndex = listArray.indexOf(word);
				while(listIndex != -1){
					listArray.splice(listIndex,1);
					listIndex = listArray.indexOf(word);
				}
				if(!remove){
					wordElement.style.color = whiteOrBlack
					listArray.unshift(word)
				}else{
					wordElement.style.color = '#555';
				}
				
				listString = listArray.join(' ')
				listElement.value = listString;
				
				oppositeListElement = document.getElementById(oppositeList + 'list');
				oppositeListString = oppositeListElement.value;
				oppositeListArray = oppositeListString.replace(/\s+/gi, ' ').split(' ')
				oppositeListIndex = oppositeListArray.indexOf(word);
				while(oppositeListIndex != -1){
					oppositeListArray.splice(oppositeListIndex,1);
					oppositeListIndex = oppositeListArray.indexOf(word);
				}
				oppositeListString = oppositeListArray.join(' ')
				oppositeListElement.value = oppositeListString;
				
			}
			
			function listMouseOut(element,word){
				element.style.color=isInList('black',word)?'#000':(isInList('white',word)?'#fff':'#555')
			}
			
			function listOnClick(element,word){
				whiteOrBlack = (element.style.color=='rgb(0, 0, 0)')?'black':'white';
				addToList(whiteOrBlack,word,isInList(whiteOrBlack,word))
			}
			
			
			function findSubsets(){
				subsetLand = document.getElementById("subsetLand");
				subsetLand = document.getElementById("subsetLand");
				listLand = document.getElementById("listLand");
				document.getElementById("subsetButton").disabled = true;
				phraseValue = document.getElementById("phrase").value
				wordSize = document.getElementById("min_word_size").value
				phoneSize = document.getElementById("min_phone_size").value
				subsetLand.style.display = "block";
				solutionLand.style.display = "none";
				listLand.style.display = "none";
				subsetLand.innerHTML = "Please wait, finding subset words...";
				
				document.getElementById("whitelist").value = "";
				document.getElementById("blacklist").value = "";
				$.ajax({
					type: 'POST',
					url: '/subsets',
					data: { phrase: phraseValue, min_word_size: wordSize, min_phone_size: phoneSize },
					success:function(data){
						subsetLand.innerHTML = data
						if(data.substr(4,5)=="Sorry"){
							listLand.style.display = "none";
						}else{
							listLand.style.display = "block";
						}
						document.getElementById("subsetButton").disabled = false;
						
					}
				});
			}
			
			function findSolutions(){
				solutionLand = document.getElementById("solutionLand");
				solutionLand.style.display = "block";
				solutionLand.innerHTML = "Please wait, finding solutions...";
				document.getElementById("solutionLand").disabled = true;
				phraseValue = document.getElementById("phrase").value
				wordSize = document.getElementById("min_word_size").value
				phoneSize = document.getElementById("min_phone_size").value
				whitelistValue = document.getElementById("whitelist").value
				blacklistValue = document.getElementById("blacklist").value
				randomizeWordsValue = document.getElementById("randomize_words").value
				$.ajax({
					type: 'POST',
					url: '/solutions',
					data: { phrase: phraseValue, min_word_size: wordSize, min_phone_size: phoneSize, randomize_words: randomizeWordsValue, blacklist: blacklistValue, whitelist: whitelistValue },
					success:function(data){
						solutionLand.innerHTML = data
						
						document.getElementById("solutionLand").disabled = false;
						
					}
				});
				
			}
					
			
		</script>
	</head>
	<body style="font-family: calibri, verdana; font-size: 20px; background-color: #ccc; ">
	<center>
	<div style="width: 800px;">
	<img src="/top3.jpg">
	<div class="headerish">
		Anaphone : A word, phrase, or name formed by rearranging the sounds of another, such as <i>galaxy</i> from <i>lucky gas.</i>
	</div>
		<div style="border-radius: 10px; text-align: left; background-color: #e2e2e2; margin: 10px; padding: 20px; color: #333">
"""

layout_bottom = """
</div>
</div>
<div class="headerish">
Enexistencificated by <a href="http://cortexel.us">CJ Carr</a> in 2012
</div>
</center>
</body>
</html>
"""

class Subsets(webapp2.RequestHandler):
	def post(self):
		phrase = cgi.escape(self.request.get('phrase'))
		min_word_size = cgi.escape(self.request.get('min_word_size'))
		min_phone_size = cgi.escape(self.request.get('min_phone_size'))
	
		subsets = anaphonr.get_candidate_words(phrase, min_word_size, min_phone_size)
		#subsets = ["super","stupid","time"]

		if subsets == -1:
			# input word/phrase isn't parsable or isn't in the dictionary
			self.response.write("<!--Sorry--><div class='subsetList'>Sorry, I don't know how to pronounce all these words. Blame CMU for not having your words in their pronouncing dictionary</div>")
			return
			
		if len(subsets)==0:
			# constraints are too strong
			self.response.write("<!--Sorry--><div class='subsetList'>Sorry, no words were found fitting these constraints. Try loosening it up a bit </div>")
			return
		
		self.response.write("""
				Subsets <span class=sidenote>[click word: add to blacklist. CTRL+click word: add to whitelist]</span>
				<div class="subsetList" id="subsetList">
					""")
		for word in subsets:
			self.response.write("""
				<span style='color: #555' class=whiteListClick id='word_"""+word+"""' onclick="listOnClick(this,'"""+word+"""')" 
						onmouseover="this.style.color=shifted?'#000':'#fff'"
						onmouseout="listMouseOut(this,'"""+word+"')\">"+word+"</span>")

		self.response.write("</div>")
								
class Solutions(webapp2.RequestHandler):
    def post(self):
    	phrase = cgi.escape(self.request.get('phrase'))
		min_word_size = cgi.escape(self.request.get('min_word_size'))
		min_phone_size = cgi.escape(self.request.get('min_phone_size'))
		randomize_words = cgi.escape(self.request.get('randomize_words'))
		if randomize_words == "on" :
			randomize_words = True
		else: 
			randomize_words = False
			
		blacklist = cgi.escape(self.request.get('blacklist'))
		whitelist = cgi.escape(self.request.get('whitelist'))
		
		self.response.out.write('<div class=solutionList>')
		self.response.out.write('<table class=solutionTable> ')
		anaphonr.main_imported(phrase, min_word_size, min_phone_size, randomize_words, blacklist, whitelist, False, self)
		
		self.response.out.write(' </table>')
		self.response.out.write('</div>')

class FeelingLucky(webapp2.RequestHandler):
    def get(self):
		
		phrase = cgi.escape(self.request.get('p'))
		
		if(len(phrase)<=0):
			self.response.out.write(":|?")
			return 
		
		min_word_size = 1
		
		if(len(phrase)>9):
			min_word_size = 2
			
		if(len(phrase)>12):
			min_word_size = 3
			
		min_phone_size = 1
		randomize_words = True
		blacklist = ''
		whitelist = '' 
		while True:
			solution = anaphonr.main_imported(phrase, min_word_size, min_phone_size, randomize_words, blacklist, whitelist, True, self)
			if len(solution) == 0:
				if(min_word_size == 1):
					self.response.out.write(":( couldn't find one")
					return
				else:
					min_word_size = min_word_size - 1
			else:
				self.response.out.write(solution)
				return
		
		
		
class MainHandler(webapp2.RequestHandler):
	global layout_top, layout_bottom
	
	def get(self):
		self.response.write(layout_top)
		
		self.response.write("""
			
				  <form>
					<label for="phrase" style="font-weight:bold; font-size: 30px">Find anaphones for</label>
					<input type="text" name="phrase" id="phrase" size=30 style="font-size: 24px; border: 2px solid #555; padding-left: 6px"><br><br>
					<label for="min_word_size">Minimum letters per word</label>
					<input type="text" name="min_word_size" id="min_word_size" size=1 maxlength=1 value=1><br>
					<label for="min_phone_size">Minimum phonemes per word</label>
					<input type="text" name="min_phone_size" id="min_phone_size" size=1 maxlength=1 value=1>
					<!-- <br>
					 <label for="randomize_words">Randomize word order</label> -->
					<input type="checkbox" name="randomize_words" id="randomize_words" CHECKED style="display: none"><br><br>
					
					<input type="submit" value="Find subsets" id="subsetButton" onclick="findSubsets(); return false;">
					
					<div id="subsetLand" style="display:none"><br>""")
					
					# :@
		
		self.response.write("""
					</div>
					
					<div id="listLand" style="display:none">
					<label for="blacklist">Blacklist<span class=sidenote>[solutions will not have these words]</span></label>
					<input type="text" name="blacklist" id="blacklist" style="color: black; background-color: #bbb;  padding-left:5px; border: 1px solid #555"  size=50 readonly="readonly" ><Br>
					<label for="whitelist">Whitelist<span class=sidenote>[solutions must have these words]</span></label>
					<input type="text" name="whitelist" id="whitelist" style="color: black; background-color: #bbb; padding-left:5px; border: 1px solid #555" size=50 readonly="readonly" >
					</div>
					
					<br><br>
					
					<input type="submit" value="Find full solutions" id="solutionButton" onclick="findSolutions(); return false;">
					
					<div id="solutionLand" style="display:none">
					
					</div>
					
				  </form>
				""")
		self.response.write(layout_bottom)
		

		
		
		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/solutions', Solutions),
	('/lucky.*', FeelingLucky),
	('/subsets', Subsets)
], debug=True)
