

import PhishingDetector as PD
import SpamDetector as SD
import numpy as np
import random
import datetime

feature_size_phishing = 30
feature_size_spam = 141

model_phishing = 1
model_spam = 0

classifier_neural_network = 1
classifier_svm = 0

class Agent():

	# Init an Agent
	def __init__(self, features_size):

		"""
			Start a random list of 0 and 1 of len = features_size
			e.g. if features_size = 5 the chromosome = [1, 1, 1, 0, 1]
			features_size represent the amount of features
		"""
		self.chromosome = []
		for x in range(features_size):
			self.chromosome.append(random.randint(0,1))

		self.chromosome = np.array(self.chromosome)
		self.fitness = -1


	def __str__(self):
		return "Chromosome: " + str(self.chromosome) + ", with fitness " + str(self.fitness)


	population = 20
	generations = 100
	selection_size = int(0.3 * population)

	def ga(model = model_phishing, classifier = classifier_svm, features_size = feature_size_phishing):

		agents = Agent.init_agents(Agent.population, features_size)

		# the agent with the best fitness
		best_agent = Agent(features_size)

		# The generation the best agent was created
		generation_best_agent = -1
		

		for generation in range(Agent.generations):

			print("Generation: "+str(generation))

			agents = Agent.fitness(agents, model, classifier)
			agents = Agent.selection(agents, features_size)

			# check if the best new agent is better than the best_agent
			if agents[0].fitness > best_agent.fitness:
				# a new agent created have better fitness
				best_agent.chromosome = agents[0].chromosome
				best_agent.fitness = agents[0].fitness
				generation_best_agent = generation

			agents = Agent.crossover(agents, features_size)
			agents = Agent.mutation(agents, features_size)

			print('----------------------------------------Best Agent So Far in '+ str(generation_best_agent)+'----------------------------------')
			print(best_agent)
			print('----------------------------------------Best Agent So Far in '+ str(generation_best_agent)+'----------------------------------')


			if any(agent.fitness >= 0.9 for agent in agents):

				print("Found an agent")
				print('\n'.join(map(str, agents)))

				#get the best agent with minimum value of 0.9
				best_agent = max(agents, key = lambda agent: agent.fitness)
				Agent.print_best_agent(best_agent, generation_best_agent, model, classifier)

				#break
				exit(0)

		# get the best agent at the end of the generation
		Agent.print_best_agent(best_agent, generation_best_agent, model, classifier)


	# This function creates initial population using the Agent class, the return is a list
	# size population and each agent in the population must be size features_size
	def init_agents(population, features_size):

		return [Agent(features_size) for _ in range(population)]

	# This function will calculate the fitness in each memeber of the population
	def fitness(agents, model, classifier):
		print("---------------------------------fitness-------------------------------")
		
			
		if model is model_phishing and classifier is classifier_svm:
			# Generate a phishing_detector for each agent with SVM
			for agent in agents:
				if agent.fitness is -1:
					pd = PD.phishing_detector(agent.chromosome)
					agent.fitness = float(pd.test_features_svm())
					#agent.fitness = random.random()
				print(agent)
					
		elif model is model_phishing and classifier is classifier_neural_network:
			# Generate a phishing_detector for each agent with ANN
			for agent in agents:
				pd = PD.phishing_detector(agent.chromosome)
				agent.fitness = float(pd.test_features_neural_network())
				print(agent)


		elif model is model_spam and classifier is classifier_svm:
			# Generate a spam detector for each agent with SVM
			for agent in agents:
				if agent.fitness is -1:
					sd = SD.spam_detector(agent.chromosome)
					agent.fitness = float(sd.test_features_svm())
				print(agent)
		
		elif model is model_spam and classifier is classifier_neural_network:
			# Generate a spam detector for each agent with ANN
			for agent in agents:
				sd = SD.spam_detector(agent.chromosome)
				agent.fitness = float(sd.test_features_neural_network())
				print(agent)

		
		

		return agents

	# The selection will select the population to be go for the next generation, 
	# the population will be decide by the highest fitness function higher the 
	# probability to be selected
	def selection(agents, features_size):
		print("---------------------------------selection-------------------------------")
		agents = sorted(agents, key = lambda agent: agent.fitness, reverse = True)
		agents = agents[:Agent.selection_size]
		print('\n'.join(map(str, agents)))
		return agents

	# The crossover will combine the agents that were selected in the selection function
	def crossover(agents, features_size):
		print("---------------------------------crossover-------------------------------")
		# Method 1: Add new population and keep part of the old population
		
		new_blood = []
		for _ in range(int((Agent.population - len(agents))/ 2)):
			parent1 = random.choice(agents)
			parent2 = random.choice(agents)
			child1 = Agent(features_size)
			child2 = Agent(features_size)
			split_point = random.randint(0, features_size)
			child1.chromosome = np.concatenate((parent1.chromosome[0:split_point], parent2.chromosome[split_point:features_size]))
			child2.chromosome = np.concatenate((parent2.chromosome[0:split_point], parent1.chromosome[split_point:features_size]))
			new_blood.append(child1)
			new_blood.append(child2)

		agents.extend(new_blood)

		return agents
		
		"""
		# Another method, create a totally new population
		new_blood = []
		for _ in range(int((Agent.population) / 2)):
			parent1 = random.choice(agents)
			parent2 = random.choice(agents)
			child1 = Agent(features_size)
			child2 = Agent(features_size)
			split_point = random.randint(0, features_size)
			child1.chromosome = np.concatenate((parent1.chromosome[0:split_point], parent2.chromosome[split_point:features_size]))
			child2.chromosome = np.concatenate((parent2.chromosome[0:split_point], parent1.chromosome[split_point:features_size]))
			new_blood.append(child1)
			new_blood.append(child2)

		# keep the best agent
		new_blood[0].chromosome = agents[0].chromosome
		new_blood[0].fitness = agents[0].fitness 
		return new_blood
		"""
		

	# The mutation will do random modification of the agents
	def mutation(agents, features_size):
		print("---------------------------------mutation-------------------------------")
		for agent in agents:
			for idx, param in enumerate(agent.chromosome):
				if agent.fitness is -1 and random.uniform(0.0, 1.0) <= 0.05:
					if agent.chromosome[idx] == 1:
						new_value = np.array([0])
					else:
						new_value = np.array([1])
					agent.chromosome = np.concatenate((agent.chromosome[0:idx], new_value, agent.chromosome[idx+1:features_size]))
		return agents


	def print_best_agent(agent, generation, model, classifier):
		# this function will print the value of the agent in a file and appendint at the end

		# get the file name
		file_name = '_error_'
		if model is model_phishing and classifier is classifier_svm:
			# file for phishing_detector for each agent with SVM
			file_name = 'result\\phishing_detector_svm.txt'
					
		elif model is model_phishing and classifier is classifier_neural_network:
			# file for phishing_detector for each agent with ANN
			file_name = 'result\\phishing_detector_ann.txt'


		elif model is model_spam and classifier is classifier_svm:
			# file for spam detector for each agent with SVM
			file_name = 'result\\spam_detector_svn.txt'
		
		elif model is model_spam and classifier is classifier_neural_network:
			# file for spam detector for each agent with ANN
			file_name = 'result\\spam_detector_ann.txt'

		# open file
		f = open(file_name, 'a')

		# get the current time
		now = datetime.datetime.now()

		# get the current time and date
		current_time_date = now.isoformat()


		f.write('By '+ current_time_date +' in the generation '+ str(generation) +' The best agent was: '+ str(agent)+'\n')
		f.close()




if __name__ == '__main__':
	"""
agent1 = Agent(30)
agent2 = Agent(30)
agent3 = Agent(30)
agent4 = Agent(30)
agent5 = Agent(30)
agent6 = Agent(30)

agent1.chromosome =  np.array([1., 1., 0., 1., 1., 1., 1., 1., 1., 1., 0., 0., 1., 1., 1., 0., 1., 0., 1., 1., 0., 1., 1., 1., 1., 0., 1., 1., 1., 0.])
agent2.chromosome =  np.array([1., 1., 1., 1., 1., 0., 1., 1., 0., 1., 1., 1., 0., 1., 1., 1., 0., 1., 1., 1., 1., 1., 1., 0., 1., 1., 1., 1., 0., 1.])
agent3.chromosome =  np.array([1., 1., 0., 0., 1., 0., 1., 1., 1., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 1., 0., 1., 0., 0., 1., 1., 0., 1., 0.])
agent4.chromosome =  np.array([1., 1., 1., 1., 1., 0., 1., 0., 1., 0., 1., 0., 0., 1., 1., 0., 0., 1., 1., 1., 1., 0., 1., 1., 1., 1., 1., 1., 1., 1.])
agent5.chromosome =  np.array([1., 1., 0., 1., 1., 0., 0., 1., 1., 1., 1., 1., 1., 1., 0., 1., 1., 1., 1., 0., 1., 0., 1., 0., 0., 0., 1., 1., 0., 0.])
agent6.chromosome =  np.array([0., 1., 1., 1., 1., 1., 1., 0., 1., 1., 1., 0., 1., 1., 0., 0., 0., 1., 1., 1., 1., 0., 0., 0., 0., 1., 1., 1., 0., 1.])

agents = [agent1, agent2, agent3, agent4, agent5, agent6]

	Agent.fitness(agents, model_phishing, classifier_neural_network)
	print('-----------------------------Fitness-------------------------------')
	print('\n'.join(map(str, agents)))

	Agent.selection(agents)
	print('-----------------------------Selection-------------------------------')
	print('\n'.join(map(str, agents)))

	Agent.crossover(agents)
	print('-----------------------------Crossover-------------------------------')
	print('\n'.join(map(str, agents)))
	
	Agent.mutation(agents)
	print('-----------------------------Mutation-------------------------------')
	print('\n'.join(map(str, agents)))

	"""
	
	# Phishing and Neural Network
	#Agent.ga(model_phishing, classifier_neural_network, feature_size_phishing)

	# Phishing and SVM
	# Agent.ga(model_phishing, classifier_svm, feature_size_phishing)

	# Spam and SVM
	Agent.ga(model_spam, classifier_svm, feature_size_spam)

	# Spam and Neural Networks
	#Agent.ga(model_spam, classifier_neural_network, feature_size_spam)

	## Run the code for the selection



