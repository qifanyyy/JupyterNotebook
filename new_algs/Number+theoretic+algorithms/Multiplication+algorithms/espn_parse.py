import requests
from bs4 import BeautifulSoup
import math
import re
import random

#Some Constants/Initial Variables
CORRECT = "#icon__form__check"

#Get the soup for page 
def get_soup(link):
	page = requests.get(link)
	soup = BeautifulSoup(page.text, 'html.parser')
	return soup

#Get the table that contains relevant information
def get_table(soup):
	table = soup.find("div", {"class": "Table__Scroller"})
	return table


#Get the names of all the experts
def get_experts(table):
	header = table.find("tr", {"class": "Table__TR Table__even"})
	header = header.findAll('th')
	names = []
	for th in header:
		names.append(th.find_all("div")[-1].getText())
	return names


#Get all the matchups
def get_matchups(soup):
	table = soup.find("table", {"class": "Table Table--align-center Table--fixed Table--fixed-left"})
	body = table.find("tbody", {"class": "Table__TBODY"})
	items = body.findAll("a", {"class": "AnchorLink"})
	matchups=[]
	for i in items:
		matchups.append(i.getText())
	return matchups

#Get all the games
def get_games(table):
	games = table.find("tbody", {"class": "Table__TBODY"})
	games = games.findAll("tr")
	return games[:-1]

#Given a game, get each expert's predictions
def get_predictions(game,names):
	predictions = game.findAll("td")
	# predictions = [p['src'] for p in predictions]
	for i in range(len(predictions)):
		s = predictions[i]
		if s.getText()=="No Pick":
			predictions[i]=predictions[i-1]
			continue
		s = s.find("img")
		s=s['src']
		result = re.search('teamlogos/nfl/500/(.*).png', s)
		predictions[i]=result.group(1).upper()
	expert_predictions = {}
	for i in range(len(names)):
		expert_predictions[names[i]]=predictions[i]
	return expert_predictions

# OLD DRAW, FROM MAJORITY WEIGHTS ALGORITHM
# def draw(expert_predictions, weights):
# 	weighted_predictions = {}
# 	for expert in expert_predictions:
# 		pred = expert_predictions.get(expert)
# 		weight = weights.get(expert)
# 		if pred not in weighted_predictions:
# 			weighted_predictions[pred] = weight
# 		else:
# 			weighted_predictions[pred] += weight
# 	return max(weighted_predictions, key=weighted_predictions.get)

#New Draw Implementation, Multiplicative Weights
def draw_expert(weights):
	vals = list(weights.values())
	experts = list(weights.keys())
	choice = random.uniform(0, sum(vals))
	index = 0
	for weight in vals:
		choice -= weight
		if choice <=0:
			return experts[index]
		index+=1

def draw_prediction(predictions,expert):
	return predictions.get(expert)

#Determine whether each expert was right or wrong for the game's prediction
def get_losses(game, names):
	predictions = game.findAll("td")
	losses = []
	for p in predictions:
		if p.getText()=="No Pick":
			losses.append(1)
			continue
		p = p.find("div", {"class": "PassFailWrapper__Badge"})
		if p is None:
			continue
		predicted_winner = p.find("img")
		is_correct = p.find("use")['xlink:href']
		if is_correct==CORRECT:
			losses.append(0)
		else:
			losses.append(1)
	expert_losses={}
	for i in range(len(losses)):
		expert_losses[names[i]]=losses[i]
	return expert_losses

#Determine if algorithm prediction was correct
def is_correct(losses,expert):
	if len(losses)==0:
		return "WINNER NOT KNOWN"
	return losses[expert]==0

#Update weights based on losses
def update_weights(losses,names,weights,epsilon):
	if len(losses)==0:
		return
	for expert in weights:
		weights[expert] = weights[expert] * (1-epsilon)**(losses[expert])

#Run predictions for all matchups in a week
def process_week(link,weights):
	soup = get_soup(link)
	table = get_table(soup)
	names = get_experts(table)
	matchups = get_matchups(soup)
	games = get_games(table)

	#set epsilon value
	T = 256 #Number of Games in NFL regular season
	n = len(names) #Number of experts
	epsilon = math.sqrt(math.log(n)/T)

	games_total = 0
	games_correct = 0

	for i in range(len(matchups)):
		print("GAME: ",matchups[i])
		game = games[i]
		predictions = get_predictions(game,names)
		expert = draw_expert(weights)
		# print("SELECTED EXPERT:",expert)
		prediction = draw_prediction(predictions,expert)
		print("OUR PREDICTION: ", prediction)
		losses = get_losses(game,names)
		correct = is_correct(losses,expert)
		print ("CORRECT?: ",correct )
		update_weights(losses,names,weights,epsilon)
		# print("UPDATED WEIGHTS: ", weights)
		games_total +=1
		if correct:
			games_correct+=1
		print("")

	weekly_accuracy = games_correct/float(games_total)
	print ("WEEKLY ACCURACY:", weekly_accuracy)
	print("-------------------------------")
	return weekly_accuracy

#Run predictions for all matchups in a season
def process_season(base_link):
	total_accuracy = []

	#Initialize dictionary of expert weights
	link = base_link+str(1)
	soup = get_soup(link)
	table = get_table(soup)
	names = get_experts(table)
	weights = {}
	for name in names:
		weights[name]=1

	for i in range(1,18):
		print("ANALYZING WEEK", i)
		link = base_link+str(i)
		total_accuracy.append(process_week(link,weights))
	print ("TOTAL ACCURACY:",sum(total_accuracy)/float(len(total_accuracy)))
	print("FINAL WEIGHTS:", weights)
		

base_link = "https://www.espn.com/nfl/picks/_/seasontype/2/week/"
process_season(base_link)





