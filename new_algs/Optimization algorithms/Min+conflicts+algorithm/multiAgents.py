# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        if successorGameState.isLose(): #Loss state is evaluated poorly
          return -10000000
    
        if successorGameState.isWin():  #Win state is the best possible 
          return  1000000

        food_list = newFood.asList()
        food_dists = []
        ghost_dists = []

        for item in food_list:
        	food_dists.append(manhattanDistance(newPos,item))

        for ghost_pos in successorGameState.getGhostPositions():
        	ghost_dists.append( manhattanDistance(newPos,ghost_pos))

        score = successorGameState.getScore()

        #The closest we are to a food more points are added to the score
        #and the farthes we are from a ghost less points are detracted.
        #Floats are used to det more accurate numbers from the division

        score += +float(10)/min_dist - float(10)/min(ghost_dists)

        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    #max function for the minimax algorithm
    def max_value(self, gameState,depth):

      v = -100000000
      if depth == 0 or gameState.isWin() or gameState.isLose(): #if we reached a final state: evaluate the state
        return self.evaluationFunction(gameState)

      else:#else get the maximum value returned from the min function of the minimax algorithm
        for action in gameState.getLegalActions(0):
    		  v = max(v,self.min_value(gameState.generateSuccessor(0,action),depth-1,1))

      return v

    #min function for the minimax algorithm
    def min_value(self,gameState,depth,agent):

      v = 1000000000

      if depth == 0 or gameState.isWin() or gameState.isLose(): #if we reached a final state: evaluate the state
        return self.evaluationFunction(gameState)

      #all agent except from the last one call another min function to make a move that depends on the previous agent's move
      #the final agent calls again a max function
      #every agent reduces the depth as the starting depth has been multiplied by the number of agents
      else: 
        if(agent!= 0 and agent != gameState.getNumAgents()-1):
          for action in gameState.getLegalActions(agent):
  				  v = min(v,self.min_value(gameState.generateSuccessor(agent,action),depth-1,agent+1))
        if(agent!= 0 and agent == gameState.getNumAgents()-1):
          for action in gameState.getLegalActions(agent):
            v = min(v,self.max_value(gameState.generateSuccessor(agent,action),depth-1))

      return v

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        act = None 
        v = -10000000000
        new = None
        
        #print gameState.getNumAgents(),self.depth
        for action in gameState.getLegalActions(0):
          dp = self.depth*gameState.getNumAgents()
          new = max(v,self.min_value(gameState.generateSuccessor(0,action),dp-1,1))
          if (new != v):
        		act = action
          v = new
        return act

        util.raiseNotDefined()





#just like minimax with the added a-b values

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def a_b_max_value(self, gameState,depth,a,b):
      v = -100000000
      if depth == 0 or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      elif depth:
        for action in gameState.getLegalActions(0):
          v = max(v,self.a_b_min_value(gameState.generateSuccessor(0,action),depth-1,1,a,b))
          if v > b:
            return v
          a = max(a,v)
      return v

    def a_b_min_value(self,gameState,depth,agent,a,b):
      v = 1000000000
      if depth == 0 or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      elif depth != 0: 
        if(agent!= 0 and agent != gameState.getNumAgents()-1):
          for action in gameState.getLegalActions(agent):
            v = min(v,self.a_b_min_value(gameState.generateSuccessor(agent,action),depth-1,agent+1,a,b))
            if v < a:
              return v
            b = min (v,b)  
        if(agent!= 0 and agent == gameState.getNumAgents()-1):
          for action in gameState.getLegalActions(agent):
            v = min(v,self.a_b_max_value(gameState.generateSuccessor(agent,action),depth-1,a,b))
            if v < a:
              return v
            b = min (v,b) 
      return v

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        act = None 
        v = -10000000000
        new = None
        b = 10000000000
        a= -10000000000
        for action in gameState.getLegalActions(0):
          dp = self.depth*gameState.getNumAgents()
          new = max(v,self.a_b_min_value(gameState.generateSuccessor(0,action),dp-1,1,a,b))
          if (new != v):
            act = action
          v = new
          if v > b:
            return v
          a = max(a,v)
        return act
        util.raiseNotDefined()

#Just like minimax with the expectimax evaluation

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def max_value(self, gameState,depth):
      v = -100000000
      if depth == 0 or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      elif depth:
        for action in gameState.getLegalActions(0):
          v = max(v,self.min_value(gameState.generateSuccessor(0,action),depth-1,1))
      return v

    def min_value(self,gameState,depth,agent):
      sumof=0
      n = len(gameState.getLegalActions(agent))
      if depth == 0 or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      elif depth != 0: 
        if(agent!= 0 and agent != gameState.getNumAgents()-1):
          for action in gameState.getLegalActions(agent):
            sumof += self.min_value(gameState.generateSuccessor(agent,action),depth-1,agent+1)
        if(agent!= 0 and agent == gameState.getNumAgents()-1):
          for action in gameState.getLegalActions(agent):
            sumof += self.max_value(gameState.generateSuccessor(agent,action),depth-1)
      return (sumof/float(n))

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        act = None 
        v = -10000000000
        new = None
        
        for action in gameState.getLegalActions(0):
          dp = self.depth*gameState.getNumAgents()
          new = max(v,self.min_value(gameState.generateSuccessor(0,action),dp-1,1))
          if (new != v):
            act = action
          v = new
        return act
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <A state is evaluated highly when: Pacman is close to food and capsules, the number 
                    of foods on the board is reduced ,And Pacman is away from ghosts. 
                    More points are added to the evaluation of a state when ghosts are scared.
                    When pacman is far from ghosts their distance is not taken into account >
    """

    

    "*** YOUR CODE HERE ***"
    food_list = currentGameState.getFood().asList()
    ghost_list = currentGameState.getGhostPositions()
    ghost_states = currentGameState.getGhostStates()
    capsule_list = currentGameState.getCapsules()
    food_dists = []
    ghost_dists = []
    capsule_dists = []
    scared_times = []
    
    if currentGameState.isWin():
      return 10000000

    if currentGameState.isLose():
      return -10000000

    for food in food_list:
      food_dists.append(manhattanDistance(currentGameState.getPacmanPosition(),food))

    for capsule in capsule_list:
      capsule_dists.append(manhattanDistance(currentGameState.getPacmanPosition(),capsule))

    for ghost_pos in ghost_list:
      ghost_dists.append(manhattanDistance(currentGameState.getPacmanPosition(),ghost_pos))

    for ghostState in currentGameState.getGhostStates():
      scared_times.append(ghostState.scaredTimer)

    score = currentGameState.getScore()

    #Pacman gets close to ghosts so this state is evaluated with less points
    if min(ghost_dists) < 2:
    score +=  -min(food_dists) -len(food_list)  - float(20)/min(ghost_dists)

    #When pacman is away from ghosts, 
    else:
    score +=  -min(food_dists) -len(food_list) 

    #being close to capsules also contributes to the score
    if(len(capsule_dists)):
      score += -min(capsule_dists)

    #if ghosts are scared we want to give more points if closer to a ghost
    for time in scared_times:
      if time > 0:
        score -= min(ghost_dists)  
        score += time

    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

