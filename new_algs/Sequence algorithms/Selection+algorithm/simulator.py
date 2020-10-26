import traci
import re
class Simulator():
    def __init__(self, route_manager, algorithm_module, connection_module, map_folder, visual = True):
        self.map_folder = map_folder
        self.visual = visual
        self.algorithm_module = algorithm_module
        self.connection_module = connection_module
        if visual:
            self.sumo_binary = "sumo-gui"
        else:
            self.sumo_binary = "sumo"
        self.sumoCmd = [self.sumo_binary, "--step-length", "0.1", "-c", self.map_folder + "/traffic.sumocfg"]
        self.route_manager = route_manager
        self.time = 0
        self.vehicle_list = {}
        # Some constants
        self.silent_time_threshold = 2  # If a group leader experiences a certain time period without any message, it will start a leader selection.
        self.selection_time_threshold = 2  # The time length for a leader selection proposer to select messages
        self.leader_time_threshold = 200  # The time length for a leader. If the time is beyond the threshold, the leader will choose a new leader.
        # For the log file
        self.log = open("log.txt", "w")

    def init_params(self):
        self.route_manager.init_routes()
        traci.start(self.sumoCmd)
        self.deltaT = traci.simulation.getDeltaT()

    def start_simulation(self):
        self.init_params()
        while traci.simulation.getMinExpectedNumber() > 0: 
            self.step()
            self.time += self.deltaT

    def step(self):
        traci.simulationStep()
        self.route_manager.step()
        self.maintain_vehicle_list()
        # Refresh parameters.
        for vid in self.vehicle_list:
            self.vehicle_list[vid].get_lane_position()
        for vid in self.vehicle_list:
            self.vehicle_list[vid].step()
        self.print_vehicle()
        # Do actions
        for vid in self.vehicle_list:
            self.vehicle_list[vid].algorithm_manager.action()

    def maintain_vehicle_list(self):
        departed_id_list = traci.simulation.getDepartedIDList()
        for id in departed_id_list:
            if not id in self.vehicle_list.keys():
                self.vehicle_list[id] = Vehicle(id)
                v = self.vehicle_list[id]
                v.bind_simulator(self)
                v.bind_connection_manager(self.connection_module(v))
                v.bind_algorithm(self.algorithm_module(v))
        arrived_id_list = traci.simulation.getArrivedIDList()
        for id in arrived_id_list:
            if id in self.vehicle_list.keys():
                self.vehicle_list.pop(id)
        for id in list(self.vehicle_list):
            v = self.vehicle_list[id]
            if traci.vehicle.getLaneID(id) != v.original_lane:
                self.vehicle_list.pop(id)
            if v.algorithm_manager.is_prev_leader == True:
                self.vehicle_list.pop(id)

    def print_vehicle(self):
        for _ in range(100):
            self.log.write("-")
        self.log.write("\n")
        self.log.write("time:" + str(self.time) + 
                       " traffic_light:" + traci.trafficlight.getRedYellowGreenState("0") + "\n")
        for vid in self.vehicle_list:
            v = self.vehicle_list[vid]
            self.log.write("vid:" + v.id + 
                           " original_lane:" + v.original_lane + 
                           " direction:" + v.direction + 
                           " lane_position:" + str(v.lane_position) + "\n")
            self.log.write("      connected_list:" + str(v.connection_manager.connected_list) + 
                           " curr_msg_buffer:" + str(v.connection_manager.curr_msg_buffer) + "\n")
            self.log.write("      leader:" + v.algorithm_manager.leader + 
                           " leader_time:" + str(v.algorithm_manager.leader_time) + "\n")
            self.log.write("      is_group_leader:" + str(v.algorithm_manager.is_group_leader) + 
                           " silent_time:" + str(v.algorithm_manager.silent_time) + 
                           " latest_control_msg_time:" + str(v.connection_manager.latest_control_msg_time) + "\n")
            self.log.write("      is_proposer:" + str(v.algorithm_manager.is_proposer) + 
                           " selection_time:" + str(v.algorithm_manager.selection_time) + "\n")
        for _ in range(100):
            self.log.write("-")
        self.log.write("\n")

class Vehicle():
    def __init__(self, id):
        self.id = id
        self.original_lane = traci.vehicle.getLaneID(self.id)
        self.direction = self.get_direction()

    def bind_algorithm(self, algorithm_manager):
        self.algorithm_manager = algorithm_manager    

    def bind_connection_manager(self, connection_manager):
        self.connection_manager = connection_manager

    def bind_simulator(self, simulator):
        self.simulator = simulator

    def get_direction(self):
        list = re.split("_", self.original_lane)
        if list[0] == "east" or list[0] == "west":
            return "east-west"
        elif list[0] == "north" or list[0] == "south":
            return "north-south"

    #return distance toward the next intersection
    def get_lane_position(self): 
        from_origin = traci.vehicle.getLanePosition(self.id)  
        lane_length = traci.lane.getLength(self.original_lane)
        self.lane_position = lane_length - from_origin
    
    def step(self):
        self.connection_manager.step()
        self.algorithm_manager.step()