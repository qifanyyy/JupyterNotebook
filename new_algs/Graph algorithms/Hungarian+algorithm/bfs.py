# imports
from collections import deque
from dotenv import load_dotenv
from src.util import is_equals, display_path
from src.rotate import equator_clockwise, equator_anticlockwise, long_0_anticlockwise, long_0_clockwise, long_90_anticlockwise, long_90_clockwise
import copy, os, logging


# Load Env variables
load_dotenv()
log_file_path = os.getenv('LOG_FILE_PATH')

#Logging
log_file = open(log_file_path, 'w')# Clearing log file
log_file.seek(0,0)
log_file.close()
logging.basicConfig(filename=log_file_path, filemode='w' ,level=logging.DEBUG)

#BFS Algorithm
def bfs(initial_state,goal_state):
    max_length = 0
    explored = []
    queue = deque()
    graph_state = {'state':[], 'cost':0, 'moves':[]}                          # Initial Graph State
    
    start_state = graph_state.copy()
    start_state = {'state':initial_state, 'cost':0, 'moves':[0]}              # Start State
    
    if is_equals(start_state['state'],goal_state):                            # Check if goal state found
        solution = {'explored':len(explored),'max_length':max_length, 'state':start_state}
        return solution
    
    queue.append(start_state)                                                 # Append to queue 
    
    while True:
        if not queue:                                                         # If Queue is empty
            return {'state':'', 'cost':-1, 'moves':[]}
        
        if (max_length < len(queue)):
            max_length = len(queue)
#       Explore state and append to queue        
        current_state = queue.popleft()
        logging.info('\nCurrent State: %s',current_state)
        logging.info('\nStates Explored: %d',len(explored))
        logging.info('\nQueue Length: %d',len(queue))
        explored.append(current_state['state'])
        
#       Equator Clockwise
        new_state = graph_state.copy()
        new_state['state'] = equator_clockwise(current_state['state'])        # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                        # Increase path length(cost) by 1
        new_state['moves']  = list(current_state['moves'])                    # Update path(moves)
        new_state['moves'].append(1)
        if is_equals(new_state['state'],goal_state):                          # Check if new state is goal state
            solution = {'explored':len(explored),'max_length':max_length, 'state':new_state}
            return solution
        if new_state['cost'] < 20 and new_state['state'] not in explored and new_state['state'] not in queue:
            queue.append(new_state)                                           # Append the queue

#       Equator Anti-Clockwise
        new_state = graph_state.copy()
        new_state['state'] = equator_anticlockwise(current_state['state'])    # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                        # Increase path length(cost) by 1
        new_state['moves']  = list(current_state['moves'])                    # Update path(moves)
        new_state['moves'].append(2)
        if is_equals(new_state['state'],goal_state):                          # Check if new state is goal state
            solution = {'explored':len(explored),'max_length':max_length, 'state':new_state}
            return solution
        if new_state['cost'] < 20 and new_state['state'] not in explored and new_state['state'] not in queue:
            queue.append(new_state)

#       0-180 Clockwise
        new_state = graph_state.copy()
        new_state['state'] = long_0_clockwise(current_state['state'])         # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                        # Increase path length(cost) by 1
        new_state['moves']  = list(current_state['moves'])                    # Update path(moves)
        new_state['moves'].append(3)
        if is_equals(new_state['state'],goal_state):                          # Check if new state is goal state
            solution = {'explored':len(explored),'max_length':max_length, 'state':new_state}
            return solution
        if new_state['cost'] < 20 and new_state['state'] not in explored and new_state['state'] not in queue:
            queue.append(new_state)

#       0-180 Anti-Clockwise
        new_state = graph_state.copy()
        new_state['state'] = long_0_anticlockwise(current_state['state'])     # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                        # Increase path length(cost) by 1
        new_state['moves']  = list(current_state['moves'])                    # Update path(moves)
        new_state['moves'].append(4)
        if is_equals(new_state['state'],goal_state):                          # Check if new state is goal state
            solution = {'explored':len(explored),'max_length':max_length, 'state':new_state}
            return solution
        if new_state['cost'] < 20 and new_state['state'] not in explored and new_state['state'] not in queue:
            queue.append(new_state)

 #      90-270 Clockwise
        new_state = graph_state.copy()
        new_state['state'] = long_90_clockwise(current_state['state'])        # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                        # Increase path length(cost) by 1
        new_state['moves']  = list(current_state['moves'])                    # Update path(moves)
        new_state['moves'].append(5)
        if is_equals(new_state['state'],goal_state):                          # Check if new state is goal state
            solution = {'explored':len(explored),'max_length':max_length, 'state':new_state}
            return solution
        if new_state['cost'] < 20 and new_state['state'] not in explored and new_state['state'] not in queue:
            queue.append(new_state)

#       90-270 Anti-Clockwise
        new_state = graph_state.copy()
        new_state['state'] = long_90_anticlockwise(current_state['state'])    # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                        # Increase path length(cost) by 1
        new_state['moves']  = list(current_state['moves'])                    # Update path(moves)
        new_state['moves'].append(6)
        if is_equals(new_state['state'],goal_state) :                         # Check if new state is goal state
            solution = {'explored':len(explored),'max_length':max_length, 'state':new_state}
            return solution
        if new_state['cost'] < 20 and new_state['state'] not in explored and new_state['state'] not in queue:
            queue.append(new_state)
    logging.shutdown()
    
#-----------------------------------------------------------------------------#