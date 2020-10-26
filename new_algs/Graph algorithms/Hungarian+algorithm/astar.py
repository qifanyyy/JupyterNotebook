# Imports
import heapq, copy, os, logging
from dotenv import load_dotenv
from src.rotate import equator_clockwise, equator_anticlockwise, long_0_anticlockwise, long_0_clockwise, long_90_anticlockwise, long_90_clockwise
from src.util import is_equals

# Load Env variables
load_dotenv()
log_file_path = os.getenv('LOG_FILE_PATH')

#Logging
log_file = open(log_file_path, 'w')# Clearing log file
log_file.seek(0,0)
log_file.close()
logging.basicConfig(filename=log_file_path, filemode='w' ,level=logging.DEBUG)

# Calculate heuristic value for a given state
def calc_heuristic(state, goal_state):
#   Calculating the manhattan distance to goal state     
    distance = 0    
    for i in range(0,30):
        distance += (abs(state['state'][i][0] - goal_state[i][1]) +
                    abs(state['state'][i][1] - goal_state[i][1]))/30
    distance = distance/12
    state['h_cost'] = distance   

#-----------------------------------------------------------------------------#
    
def a_star(initial_state,goal_state):
    max_length = 0
    heapcnt = 1
    heap = []
    explored = []
    
    graph_state = {'state':[], 'cost':0, 'h_cost':0, 'moves':[]}              # Initial State
    
    start_state = graph_state.copy()
    start_state = {'state':initial_state, 'cost':0, 'h_cost':0, 'moves':[0]}
    calc_heuristic(start_state, goal_state)
    
    if is_equals(start_state['state'],goal_state):                            # Check if goal state
        solution = {'explored':len(explored),'max_length':max_length, 'state':start_state}
        return solution
    
    heapq.heappush(heap,(start_state['cost'],heapcnt,start_state))            # Push in Heap queue(Priority queue)
    calc_heuristic(start_state, goal_state)
    heapcnt += 1
    
    while True:
        if not heap:
            return {'state':'', 'cost':-1, 'h_cost':0, 'moves':[]}
        
        if (max_length < len(heap)):
            max_length = len(heap)
        
        current_state = heapq.heappop(heap)[2]
        logging.info('\nCurrent State: %s',current_state)
        logging.info('\nStates Explored: %d',len(explored))
        logging.info('\nQueue Length: %d',len(heap))
        explored.append(current_state['state'])

#       Expand each state and append to priority queue               
#       Equator Clockwise
        new_state = graph_state.copy()
        new_state['state'] = equator_clockwise(current_state['state'])        # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                        # Increase path length(cost) by 1
        calc_heuristic(new_state, goal_state)                                 # Calculate heuristic
        new_state['moves']  = list(current_state['moves'])                    # Update path(moves)
        new_state['moves'].append(1)
        if is_equals(new_state['state'],goal_state):                          # Check if new state is goal state
            solution = {'explored':len(explored),'max_length':max_length, 'state':new_state}
            return solution
        if new_state['cost'] < 20 and new_state['state'] not in explored:
            heapq.heappush(heap,(new_state['cost'] + new_state['h_cost'],
                                 heapcnt,new_state))
            heapcnt += 1

#       Equator Anti-Clockwise
        new_state = graph_state.copy()
        new_state['state'] = equator_anticlockwise(current_state['state'])    # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                        # Increase path length(cost) by 1
        calc_heuristic(new_state, goal_state)                                             # Calculate heuristic
        new_state['moves']  = list(current_state['moves'])                    # Update path(moves)
        new_state['moves'].append(2)
        if is_equals(new_state['state'],goal_state):                          # Check if new state is goal state
            solution = {'explored':len(explored),'max_length':max_length, 'state':new_state}
            return solution
        if new_state['cost'] < 20 and new_state['state'] not in explored:
            heapq.heappush(heap,(new_state['cost'] + new_state['h_cost'],
                                 heapcnt,new_state))
            heapcnt += 1
            
#       0-180 Clockwise
        new_state = graph_state.copy()
        new_state['state'] = long_0_clockwise(current_state['state'])         # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                        # Increase path length(cost) by 1
        calc_heuristic(new_state, goal_state)                                 # Calculate heuristic
        new_state['moves']  = list(current_state['moves'])                    # Update path(moves)
        new_state['moves'].append(3)
        if is_equals(new_state['state'],goal_state):                          # Check if new state is goal state
            solution = {'explored':len(explored),'max_length':max_length, 'state':new_state}
            return solution
        if new_state['cost'] < 20 and new_state['state'] not in explored:
            heapq.heappush(heap,(new_state['cost'] + new_state['h_cost'],
                                 heapcnt,new_state))
            heapcnt += 1

#       0-180 Anti-Clockwise
        new_state = graph_state.copy()
        new_state['state'] = long_0_anticlockwise(current_state['state'])     # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                        # Increase path length(cost) by 1
        calc_heuristic(new_state, goal_state)                                 # Calculate heuristic
        new_state['moves']  = list(current_state['moves'])                    # Update path(moves)
        new_state['moves'].append(4)
        if is_equals(new_state['state'],goal_state):                          # Check if new state is goal state
            solution = {'explored':len(explored),'max_length':max_length, 'state':new_state}
            return solution
        if new_state['cost'] < 20 and new_state['state'] not in explored:
            heapq.heappush(heap,(new_state['cost'] + new_state['h_cost'],
                                 heapcnt,new_state))
            heapcnt += 1

#       90-270 Clockwise
        new_state = graph_state.copy()
        new_state['state'] = long_90_clockwise(current_state['state'])        # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                        # Increase path length(cost) by 1
        calc_heuristic(new_state, goal_state)                                 # Calculate heuristic
        new_state['moves']  = list(current_state['moves'])                    # Update path(moves)
        new_state['moves'].append(5)
        if is_equals(new_state['state'],goal_state):                          # Check if new state is goal state
            solution = {'explored':len(explored),'max_length':max_length, 'state':new_state}
            return solution
        if new_state['cost'] < 20 and new_state['state'] not in explored:
            heapq.heappush(heap,(new_state['cost'] + new_state['h_cost'],
                                 heapcnt,new_state))
            heapcnt += 1

#       90-270 Anti-Clockwise
        new_state = graph_state.copy()
        new_state['state'] = long_90_anticlockwise(current_state['state'])    # Find new coordinates
        new_state['cost']  = current_state['cost'] + 1                        # Increase path length(cost) by 1
        calc_heuristic(new_state, goal_state)                                 # Calculate heuristic
        new_state['moves']  = list(current_state['moves'])                    # Update path(moves)
        new_state['moves'].append(6)
        if is_equals(new_state['state'],goal_state) :                         # Check if new state is goal state
            solution = {'explored':len(explored),'max_length':max_length, 'state':new_state}
            return solution
        if new_state['cost'] < 20 and new_state['state'] not in explored:
            heapq.heappush(heap,(new_state['cost'] + new_state['h_cost'],
                                 heapcnt,new_state))
            heapcnt += 1
    logging.shutdown()