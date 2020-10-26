from dotenv import load_dotenv
from src.util import is_equals, display_path
from src.rotate import equator_clockwise, equator_anticlockwise, long_0_anticlockwise, long_0_clockwise, long_90_anticlockwise, long_90_clockwise
import copy, os, logging, sys

# Load Env variables
load_dotenv()
log_file_path = os.getenv('LOG_FILE_PATH')

#Logging
log_file = open(log_file_path, 'w')# Clearing log file
log_file.seek(0,0)
log_file.close()
logging.basicConfig(filename=log_file_path, filemode='w' ,level=logging.DEBUG)

class RecursiveBfs:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.explored_count = 0
        self.max_succ = 0
    
    def display(self, current_state):
        print('\nAlgorithm: RBFS')
        print('No of States Expanded: ',self.explored_count)
        print('Max length of successor: ',self.max_succ)
        print('Final Path Length: ',current_state['cost'])
        print('Final Path: ',display_path(current_state['moves']))

    # Calculate heuristic value for a given state
    def calc_heuristic(self, state):
    #   Calculating the manhattan distance to goal state     
        distance = 0    
        for i in range(0,30):
            distance += (abs(state['state'][i][0] - self.goal_state[i][1]) +
                        abs(state['state'][i][1] - self.goal_state[i][1]))/30
        distance = distance/12
        state['h_cost'] = distance 

    def rbfs(self, current_state, f_limit):
        successor = []
        
        graph_state = {'state':[], 'cost':0, 'h_cost':0, 'alt_cost':0, 'moves':[]}
        
        logging.info('\nCurrent State: %s',current_state)
        logging.info('\nExplored Count: %d',self.explored_count)

        self.explored_count += 1
        if is_equals(current_state['state'],self.goal_state):                          # Compare to goal state 
            self.display(current_state)
            sys.exit(0)

    #   Generate successor list     
    #   Equator Clockwise
        new_state = graph_state.copy()
        new_state['state'] = equator_clockwise(current_state['state'])            # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                            # Increase path length(cost) by 1
        self.calc_heuristic(new_state)                                                 # Calculate heuristic
        new_state['moves']  = list(current_state['moves'])                        # Update path(moves)
        new_state['moves'].append(1)
        if is_equals(new_state['state'],self.goal_state):
            self.display(current_state)
            sys.exit(0)
        if new_state['cost'] < 20:
            successor.append(new_state)                                           # Append to successor
        
    #   Equator Anti-Clockwise
        new_state = graph_state.copy()
        new_state['state'] = equator_anticlockwise(current_state['state'])        # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                            # Increase path length(cost) by 1
        self.calc_heuristic(new_state)                                                 # Calculate heuristic
        new_state['moves']  = list(current_state['moves'])
        new_state['moves'].append(2)
        if is_equals(new_state['state'],self.goal_state):
            self.display(current_state)
            sys.exit(0)
        if new_state['cost'] < 20:
            successor.append(new_state)                                           # Append to successor

    #   0-180 Clockwise
        new_state = graph_state.copy()
        new_state['state'] = long_0_clockwise(current_state['state'])             # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                            # Increase path length(cost) by 1
        self.calc_heuristic(new_state)                                                 # Calculate heuristic
        new_state['moves']  = list(current_state['moves'])
        new_state['moves'].append(3)
        if is_equals(new_state['state'],self.goal_state):
            self.display(current_state)
            sys.exit(0)
        if new_state['cost'] < 20:
            successor.append(new_state)                                           # Append to successor

    #   0-180 Anti-Clockwise
        new_state = graph_state.copy()
        new_state['state'] = long_0_anticlockwise(current_state['state'])         # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                            # Increase path length(cost) by 1
        self.calc_heuristic(new_state)                                                 # Calculate heuristic
        new_state['moves']  = list(current_state['moves'])
        new_state['moves'].append(4)
        if is_equals(new_state['state'],self.goal_state):
            self.display(current_state)
            sys.exit(0)
        if new_state['cost'] < 20:
            successor.append(new_state)                                           # Append to successor
        
    #   90-270 Clockwise
        new_state = graph_state.copy()
        new_state['state'] = long_90_clockwise(current_state['state'])            # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                            # Increase path length(cost) by 1
        self.calc_heuristic(new_state)                                                 # Calculate heuristic
        new_state['moves']  = list(current_state['moves'])
        new_state['moves'].append(5)
        if is_equals(new_state['state'],self.goal_state):
            self.display(current_state)
            sys.exit(0)
        if new_state['cost'] < 20:
            successor.append(new_state)                                           # Append to successor

    #   90-270 Anti-Clockwise
        new_state = graph_state.copy()
        new_state['state'] = long_90_anticlockwise(current_state['state'])        # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                            # Increase path length(cost) by 1
        self.calc_heuristic(new_state)                                                 # Calculate heuristic
        new_state['moves']  = list(current_state['moves'])
        new_state['moves'].append(6)
        if is_equals(new_state['state'],self.goal_state):
            self.display(current_state)
            sys.exit(0)
        if new_state['cost'] < 20:
            successor.append(new_state)                                           # Append to successor
        
        if not successor:
            return 99999
        
        if len(successor) > self.max_succ:
            self.max_succ = len(successor)                                             # Update max successor length  
        
        for succ_state in successor:                                              # Calculting alternate costs
            if (current_state['cost']+current_state['h_cost']) < current_state['alt_cost']:
                succ_state['alt_cost'] = max(current_state['alt_cost'],(succ_state['cost']+succ_state['h_cost']))
            else:
                succ_state['alt_cost'] = succ_state['cost']+succ_state['h_cost']

        successor = sorted(successor, key=lambda k: k['alt_cost'])                # Sorting the successor array
        
        best_state = successor[0]
        alternate_state = successor[1]
    
        while best_state['alt_cost'] <= f_limit and best_state['alt_cost'] <= 99999:
    #       Update alternate cost by exploring the node 
            best_state['alt_cost'] = self.rbfs(best_state,min(f_limit,alternate_state['alt_cost']))

            successor = sorted(successor, key=lambda k: k['alt_cost'])            # Sorting the successor array
            best_state = successor[0]
            alternate_state = successor[1]
        
        return best_state['alt_cost']    

