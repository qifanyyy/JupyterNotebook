import math, random
import numpy as np
import copy
import collections
from players.player import Player
from abc import abstractmethod
from collections import defaultdict

class Node:
    def __init__(self, state, parent=None):
        """
        - n_visits is the number of visits in this node
        - n_a is a dictionary {key, value} where key is the action taken from 
          this node and value is the number of times this action was chosen.
        - q_a is a dictionary {key, value} where key is the action taken from
          this node and value is the mean reward of the simulation that passed
          through this node and used action 'a'.
        - p_a is a dictionary {key, value} where key is the action taken from
          this node and value is the probability given by the trained network
          to choose this action. Value updated in the expand_children() method
          from the MCTS class.
        - parent is a Node object. 'None' if this node is the root of the tree.
        - children is a dictionary {key, value} where key is the action 
          taken from this node and value is the resulting node after applying 
          the action.
        - action_taken is the action taken from parent to get to this node.
        """
        self.state = state
        self.n_visits = 0
        self.n_a = {}
        self.q_a = {}
        self.p_a = {}
        # These will initialize value = 0 for whichever keys yet to be added.
        self.n_a = defaultdict(lambda: 0, self.n_a)
        self.q_a = defaultdict(lambda: 0, self.q_a)
        self.p_a = defaultdict(lambda: 0, self.q_a)
        self.parent = parent
        self.children = {}
        self.action_taken = None


    def is_expanded(self):
        """Return a boolean."""
        return len(self.children) > 0

class UCTPlayer(Player):
    @abstractmethod
    def __init__(self, c, n_simulations):
        """
        - root is a Node instance representing the root of the game tree.
        - action stores the action this player will return for the game passed
          as parameter in the get_action method.
        - dist_probability stores the distribution probability over all actions
          regarding the probability of choosing a certain action given the game
          passed as parameter in the get_action method.
        - c is the constant the balance exploration and exploitation.
        - n_simulations is the number of simulations made in the UCT algorithm.
        """
        self.root = None
        self.action = None
        self.dist_probability = None
        self.c = c
        self.n_simulations = n_simulations


    @abstractmethod
    def expand_children(self, parent):
        """Expand the children of the "parent" node"""
        pass

    @abstractmethod
    def rollout(self, node, scratch_game):
        """
        Return the game value of the end of the current simulation.
        Concrete classes must implement this method.
        """
        pass

    @abstractmethod
    def calculate_ucb_max(self, node):
        """
        Return the node UCB value of the MAX player.
        Concrete classes must implement this method.
        """
        pass

    @abstractmethod
    def calculate_ucb_min(self, node):
        """
        Return the node UCB value of the MIN player.
        Concrete classes must implement this method.
        """
        pass

    def get_action(self, game):
        """ Return the action given by the UCT algorithm. """
        action, dist_probability = self.run_UCT(game)
        self.action = action
        self.dist_probability = dist_probability
        # Reset the tree for the future run_UCT call
        self.root = None
        return action

    def get_dist_probability(self):
        """ 
        Return the actions distribution probability regarding
        the game passed as parameter in get_action. Should be 
        called after get_action.
        """
        return self.dist_probability

    def run_UCT(self, game):
        """Main routine of the UCT algoritm."""
        if self.root == None:
            self.root = Node(game.clone())
        else:
            self.root.state = game.clone()
        #Expand the children of the root before the actual algorithm
        self.expand_children(self.root)

        for _ in range(self.n_simulations):
            node = self.root
            scratch_game = game.clone()
            search_path = [node]
            while node.is_expanded():
                action, new_node = self.select_child(node)
                node.action_taken = action
                scratch_game.play(action)
                search_path.append(new_node)
                node = copy.deepcopy(new_node)
            #At this point, a leaf was reached.
            #If it was not visited yet, then perform the rollout and
            #backpropagates the reward returned from the end of the simulation.
            #If it has been visited, then expand its children, choose the one
            #with the highest ucb score and do a rollout from there.
            if node.n_visits == 0:
                rollout_value = self.rollout(node, scratch_game)
                self.backpropagate(search_path, action, rollout_value)
            else:
                self.expand_children(node)
                action_for_rollout, node_for_rollout = self.select_child(node)
                search_path.append(node)
                rollout_value = self.rollout(node_for_rollout, scratch_game)
                self.backpropagate(search_path, action_for_rollout, rollout_value)
        action = self.select_action(game, self.root)
        dist_probability = self.distribution_probability()
        self.root = self.root.children[action]
        return action, dist_probability    

    def select_action(self, game, root):
        """Return the action with the highest visit score."""
        visit_counts = [(child.n_visits, action)
                      for action, child in root.children.items()]
        # Sort based on the number of visits
        visit_counts.sort(key=lambda t: t[0])
        _, action = visit_counts[-1]
        return action

    def backpropagate(self, search_path, action, value):
        """Propagate the value from rollout all the way up the tree to the root."""
        for node in search_path:
            node.n_visits += 1
            node.n_a[node.action_taken] += 1 
            # Incremental mean calculation
            node.q_a[node.action_taken] = (node.q_a[node.action_taken] * 
                                            (node.n_visits - 1) + value) / \
                                                node.n_visits

    def select_child(self, node):
        """Return the child Node with the highest UCB score."""
        ucb_values = []
        for action, child in node.children.items():
            if node.state.player_turn == 1:
                if child.n_visits == 0:
                    ucb_max = float('inf')
                else:
                    ucb_max =  self.calculate_ucb_max(node, action)
                ucb_values.append((ucb_max, action, child))
            else:
                if child.n_visits == 0:
                    ucb_min = float('-inf')
                else:
                    ucb_min =  self.calculate_ucb_min(node, action)
                ucb_values.append((ucb_min, action, child))
        # Sort the list based on the ucb score
        ucb_values.sort(key=lambda t: t[0])
        if node.state.player_turn == 1:
            best_ucb, best_action, best_child = ucb_values[-1]
        else:
            best_ucb, best_action, best_child = ucb_values[0]
        return best_action, best_child

    def distribution_probability(self):
        """
        Return the distribution probability of choosing an action according
        to the number of visits of the children.
        """
        dist_probability = {}
        total_visits = sum(self.root.n_a.values())
        for action, visits in self.root.n_a.items():
            dist_probability[action] = visits/total_visits
        return dist_probability