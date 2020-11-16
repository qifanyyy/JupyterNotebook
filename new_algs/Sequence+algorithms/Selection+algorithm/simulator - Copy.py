import traci
import re
class Simulator():
    def __init__(self,
        route_manager, 
        algorithm_module,
        connection_module,
        map_folder,
        visual = True,
        ):
        self.map_folder = map_folder
        self.visual = visual
        self.algorithm_module = algorithm_module
        self.connection_module = connection_module
        if visual:
            self.sumo_binary = "sumo-gui"
        else:
            self.sumo_binary = "sumo"
        self.sumoCmd = [self.sumo_binary, "--step-length", "0.01", "-c", self.map_folder + "/traffic.sumocfg"]
        self.route_manager = route_manager
        self.time = 0
        self.vehicle_list = {}
        # Some constants
        self.silent_time_threshold = 20  # If a group leader experiences a certain time period without any message, it will start a leader selection.
        self.selection_time_threshold = 2  # The time length for a leader selection proposer to select messages
        self.leader_time_threshold = 2000  # The time length for a leader. If the time is beyond the threshold, the leader will choose a new leader.
        self.should_print = False
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
        for vid in self.vehicle_list:
            self.vehicle_list[vid].get_lane_position()
        for vid in self.vehicle_list:
            if self.vehicle_list[vid].is_deleted == False:
                self.vehicle_list[vid].step()

        if self.should_print == True:
            for _ in range(100):
                self.log.write("-")
            self.log.write("\n")
            self.log.write("time: " + str(self.time) + " traffic light: " + traci.trafficlight.getRedYellowGreenState("0") + "\n")
            for vid in self.vehicle_list:
                self.log.write("vid: " + str(vid) + " lane: " + str(self.vehicle_list[vid].original_lane) + " direction: " + self.vehicle_list[vid].direction
                    + " is_group_leader: " + str(self.vehicle_list[vid].is_group_leader) + " position: " + str(self.vehicle_list[vid].lane_position)
                    + " connected_list:")
                for cvid in self.vehicle_list[vid].connected_list:
                    self.log.write(" " + str(cvid))
                self.log.write("\n")
                self.log.write("       leader: " + str(self.vehicle_list[vid].leader) + " silent_time: " + str(self.vehicle_list[vid].silent_time) + "\n")
                self.log.write("       curr_msg_buffer: " + str(self.vehicle_list[vid].curr_msg_buffer) + "\n")
            for _ in range(100):
                self.log.write("-")
            self.log.write("\n")
        self.should_print = False

        for vid in self.vehicle_list:
            self.vehicle_list[vid].action()

    def maintain_vehicle_list(self):
        depart_id_list = traci.simulation.getDepartedIDList()
        for id in depart_id_list:
            if not id in self.vehicle_list.keys():
                self.vehicle_list[id] = Vehicle(id)
                v = self.vehicle_list[id]
                v.bind_simulator(self)
                v.bind_algorithm(self.algorithm_module(v))
                v.bind_connection_manager(self.connection_module(v))
        
        arrived_id_list = traci.simulation.getArrivedIDList()
        for id in arrived_id_list:
            if id in self.vehicle_list.keys():
                self.vehicle_list.pop(id)

        for id in list(self.vehicle_list):
            v = self.vehicle_list[id]
            if traci.vehicle.getLaneID(id) != v.original_lane:
                self.vehicle_list.pop(id)

class Vehicle():
    def __init__(self, id):
        self.id = id
        self.original_lane = traci.vehicle.getLaneID(self.id)
        self.direction = self.get_direction()
        self.curr_msg_buffer = []
        self.next_msg_buffer = []
        self.connected_list = []
        self.latest_control_msg_time = -1.0    # The last time when the vehicle receives a traffic control message
        self.silent_time = 0    # The time length of no message received
        self.selection_time = 0    # The time length of a leader selection process
        self.leader_time = 0    # The time length after a vehicle becomes the leader
        self.leader = "-1"
        self.is_deleted = False
        self.is_proposer = False    # The vehicle is currently the proposer of a leader selection
        self.selection_start_time = 0    # The start time of the current leader selection
        
    def bind_algorithm(self, algorithm):
        self.algorithm = algorithm    

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
        
    def get_lane_position(self): 
        #return distance toward the next intersection
        from_origin = traci.vehicle.getLanePosition(self.id)  
        lane_length = traci.lane.getLength(self.original_lane)
        self.lane_position = lane_length - from_origin

    def connected(self, vid):
        v = self.simulator.vehicle_list[vid]
        if self.original_lane == v.original_lane:
        # if self.direction == v.direction:
            return True
        if self.lane_position <= 20 and v.lane_position <= 20:
            return True
        return False

    def step(self):
        # self.algorithm.step()

        # Get connected list
        self.connected_list = []
        self.is_group_leader = True
        for vid in self.simulator.vehicle_list:
            if self.id != vid and self.connected(vid) == True:
                self.connected_list.append(vid)
                v = self.simulator.vehicle_list[vid]
                if v.original_lane == self.original_lane and v.lane_position < self.lane_position:
                    self.is_group_leader = False

        # Refresh message buffer
        self.curr_msg_buffer = self.next_msg_buffer
        self.next_msg_buffer = []

    def broadcast(self, msg):
        for vid in self.connected_list:
            if vid in self.simulator.vehicle_list.keys():
                self.simulator.vehicle_list[vid].next_msg_buffer.append(msg)

    # message type: traffic control message (1), selection initialization message (2), selection response message (3)
    # traffic control message: 1,<time of message>,<id of leader>
    # selection initialization message: 2,<time of message>,<id of proposor>
    # selection response message: 3,<id of proposer>,<id of acceptor>,<direction of acceptor>,<position of acceptor>
    def action(self):
        # If the vehicle is the leader
        if self.leader == self.id:
            self.leader_action()
        # If the vehicle is the group leader
        elif self.is_group_leader == True:
            self.group_leader_action()
        # If the vehicle is neither leader nor group leader, it only parses the most recent traffic control message
        # else:
            # self.non_leader_action()

    def leader_action(self):
        if self.leader_time == self.simulator.leader_time_threshold:
            successive_leader = self.choose_successive_leader()
            print("successive_leader: " + successive_leader)
            # No matter whether the new leader exists or not, broadcast the result.
            control_message = str(1) + "," + str(self.simulator.time) + "," + str(successive_leader)
            self.broadcast(control_message)
            self.leader = "-1"
            self.is_group_leader = False
            self.is_deleted = True # The vehicle is no longer valid in the vehicle list.
            # If there is no successive leader, change the traffic light. Give itself the green light.
            if successive_leader == "-1":
                self.simulator.log.write("time: " + str(self.simulator.time) + " vid: " + str(self.id) + " no successive leader\n")
                self.simulator.should_print = True
                # traci.trafficlight.setRedYellowGreenState("0", "GGGGGGGGGGGG")
                if self.direction == "east-west":
                    traci.trafficlight.setRedYellowGreenState("0", "rrrGGgrrrGGg")
                elif self.direction == "north-south":
                    traci.trafficlight.setRedYellowGreenState("0", "GGgrrrGGgrrr")
            else:
                self.simulator.log.write("time: " + str(self.simulator.time) + " vid: " + str(self.id) + " select " + successive_leader + " as the successive leader\n")
                self.simulator.should_print = True
        else:
            # Broadcast control message, tell others that itself is the leader
            control_message = str(1) + "," + str(self.simulator.time) + "," + str(self.id)
            self.broadcast(control_message)
            if self.leader_time == 0:
                # Give itself the red light
                if self.direction == "east-west":
                    traci.trafficlight.setRedYellowGreenState("0", "GGgrrrGGgrrr")
                elif self.direction == "north-south":
                    traci.trafficlight.setRedYellowGreenState("0", "rrrGGgrrrGGg")
            elif self.leader_time == self.simulator.leader_time_threshold - 2:
                # Initialize a new leader selection
                initialization_message = str(2) + "," + str(self.simulator.time) + "," + str(self.id)
                self.broadcast(initialization_message)
        self.leader_time += 1

    def group_leader_action(self):
        # Broadcast control message. If there is control message, refresh silent_time and abort possible selection.
        self.broadcast_latest_control_message()
        # See if there are some other initialization message.
        # If the current vehicle is a proposer, and if there are earlier initialization message,
        # or the message is at the same time but the id of other proposer is smaller, then abort the current leader selection.
        self.check_other_initialization_message()
        # If the current leader selection is not aborted
        if self.is_proposer == True:
            self.selection_time += 1
            if self.selection_time == self.simulator.selection_time_threshold:
                new_leader = self.choose_new_leader()
                self.leader = new_leader
                if new_leader != "-1":
                    print("new_leader: " + new_leader)
                    self.simulator.log.write("time: " + str(self.simulator.time) + " vid: " + str(self.id) + " select " + new_leader + " as the leader\n")
                    self.simulator.should_print = True  
                    # If the vehicle selects itself as the new leader
                    if self.leader == self.id:
                        self.leader_time = 0
                    control_message = str(1) + "," + str(self.simulator.time) + "," + str(new_leader)
                    self.broadcast(control_message)
                self.silent_time = 0
                self.is_proposer = False
        else:
            if len(self.curr_msg_buffer) == 0:
                self.silent_time += 1
                # If the listening time is beyond the threshold, initialize a new leader selection.
                if self.silent_time == self.simulator.silent_time_threshold:
                    self.simulator.log.write("time: " + str(self.simulator.time) + " vid: " + str(self.id) + " initialize selection\n")
                    self.simulator.should_print = True
                    initialization_message = str(2) + "," + str(self.simulator.time) + "," + str(self.id)
                    self.broadcast(initialization_message)
                    self.is_proposer = True
                    self.selection_start_time = float(self.simulator.time)
                    self.selection_time = 0
            else:
                self.silent_time = 0

    def non_leader_action(self):
        self.broadcast_latest_control_message()

    def broadcast_latest_control_message(self):
        former_leader = self.leader
        latest_control_message = ""
        for msg in self.curr_msg_buffer:
            message_parsed = re.split(",", msg)
            if message_parsed[0] == "1":
                time = float(message_parsed[1])
                if time > self.latest_control_msg_time:
                    self.leader = message_parsed[2]
                    self.latest_control_msg_time = time
                    latest_control_message = msg
        # If the vehicle changes the leader, write it to the log.
        if former_leader != self.leader:
            self.simulator.log.write("time: " + str(self.simulator.time) + " vid: " + str(self.id) + " change its leader to " + self.leader + "\n")
            self.simulator.should_print = True
        # If there is a new control message, broadcast it.
        if latest_control_message != "":
            self.broadcast(latest_control_message)
            self.is_proposer = False
        # If the vehicle becomes the new leader
        if self.leader == self.id:
            self.leader_time = 0

    def check_other_initialization_message(self):
        earliest_vid = -1
        earliest_selection_start_time = float(self.simulator.time)
        for msg in self.curr_msg_buffer:
            message_parsed = re.split(",", msg)
            if message_parsed[0] == "2":
                time = float(message_parsed[1])
                if time < earliest_selection_start_time:
                    earliest_vid = int(message_parsed[2])
                    earliest_selection_start_time = time
        # If the vehicle is a group leader and a proposer, check whether it should abort the selection
        if self.leader != self.id and self.is_proposer == True:
            # Abort own selection
            if earliest_selection_start_time < self.selection_start_time or (earliest_selection_start_time == self.selection_start_time and earliest_vid < int(self.id)):
                self.is_proposer = False
            # Not abort own selection
            else:
                earliest_vid = -1
        # Send selection response message
        if earliest_vid >= 0:
            self.simulator.log.write("time: " + str(self.simulator.time) + " vid: " + str(self.id) + " respond to " + str(earliest_vid) + "\n")
            self.simulator.should_print = True
            response_message = "3," + str(earliest_vid) + "," + str(self.id) + "," + self.direction + "," + str(self.lane_position)
            self.broadcast(response_message)

    # The current leader selects the successive leader
    def choose_successive_leader(self):
        for msg in self.curr_msg_buffer:
            message_parsed = re.split(",", msg)
            if message_parsed[0] == "3" and message_parsed[3] != self.direction:
                return message_parsed[2]
        return "-1"

    # The group leader selects the new successive leader
    def choose_new_leader(self):
        dict = {self.direction: [self.id, self.lane_position]}
        shortest_lane_position = self.lane_position
        shortest_direction = self.direction
        for msg in self.curr_msg_buffer:
            message_parsed = re.split(",", msg)
            if message_parsed[0] == "3" and message_parsed[1] == self.id:
                id = message_parsed[2]
                direction = message_parsed[3]
                lane_position = float(message_parsed[4])
                if lane_position < shortest_lane_position:
                    shortest_lane_position = lane_position
                    shortest_direction = direction
                if direction in dict.keys():
                    if lane_position > dict[direction][1]:
                        dict[direction] = [id, lane_position]
                else:
                    dict[direction] = [id, lane_position]
        if len(dict) <= 1:
            return "-1"
        else:
            return dict[shortest_direction][0]