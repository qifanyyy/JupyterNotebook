"""
This class is for BellmanFord Algorithm Calculations
 Pooya Khandel, Mohammad Hussein Tavakoli Bina
"""

from socket import *
import re


class BFA:
    def __init__(self, r_count, initial_cost, my_name, which_port, adr_to_name):
        self.use_who = dict()
        self.new_pm = None
        self.pm_adr = None
        self.initial_cost = initial_cost
        self.old_pm = {}
        self.ports = which_port
        self.my_port = which_port[my_name]
        self.name = my_name
        self.r_count = r_count
        self.adr_to_name = adr_to_name
        self.table = []
        self.lie_table = []
        self.init_tables()
        self.bf_show()
        self.permission = []
        self.router_sock = socket(AF_INET, SOCK_DGRAM)
        self.router_sock.bind(('', self.my_port))
        self.sock_ip = '127.0.0.1'
        self.router_sock.settimeout(0.5)

    def init_tables(self):
        for m in range(self.r_count):
            self.table.append([])
            self.lie_table.append([])
            for n in range(self.r_count):
                self.table[m].append('99')
                self.lie_table[m].append(self.initial_cost[n])
        for m in range(self.r_count):
            self.table[int(self.name) - 1][m] = self.initial_cost[m]
            if self.initial_cost[m] == 'N':
                self.use_who[m + 1] = ''
            else:
                self.use_who[m + 1] = str(m + 1)

    def who_to_send(self):
        self.permission.clear()
        for m in range(self.r_count):
            if self.initial_cost[m] == 'N':
                self.permission.append(False)
            else:
                self.permission.append(True)

    def send(self):
        message = str()
        for sending_router in range(self.r_count):
            if self.permission[sending_router]:
                if not(sending_router + 1 == int(self.name)):
                    for m in range(self.r_count):
                        message = message + self.lie_table[sending_router][m] + '@'
                    self.router_sock.sendto(bytes(message, 'UTF-8'),
                                            (self.sock_ip, self.ports[str(sending_router + 1)]))
                    message = str()

    def receive(self):
        try:
            message, client_address = self.router_sock.recvfrom(2048)
            self.new_pm = re.split("@", message.decode())
            self.new_pm.remove('')
            self.pm_adr = client_address[1]
            if self.pm_adr in list(self.old_pm.keys()):
                if not(self.old_pm[self.pm_adr] == self.new_pm):
                    self.old_pm[self.pm_adr] = self.new_pm
                    self.table[self.adr_to_name[self.pm_adr] - 1] = self.new_pm
                    print("router {} send new update: {}".format(self.pm_adr, self.new_pm))
                    self.do_alg()
            else:
                self.old_pm[self.pm_adr] = self.new_pm
                self.table[self.adr_to_name[self.pm_adr] - 1] = self.new_pm
                print("router {} send new update: {}".format(self.pm_adr, self.new_pm))
                self.do_alg()
        except:
            pass

    def do_alg(self):
        distance = []
        for d_r_iter in range(self.r_count):
            if not(int(self.name) - 1 == d_r_iter):
                # Determine current cost to destination router
                if self.table[int(self.name) - 1][d_r_iter] == 'N':
                    temp = '99'
                else:
                    temp = self.table[int(self.name) - 1][d_r_iter]
                for c_r_iter in range(self.r_count):
                    if self.initial_cost[c_r_iter] == 'N':
                        cost1 = 99
                    else:
                        cost1 = int(self.initial_cost[c_r_iter])
                    # Determine cost from neighbor to destination
                    if self.table[c_r_iter][d_r_iter] == 'N':
                        cost2 = 99
                    else:
                        cost2 = int(self.table[c_r_iter][d_r_iter])
                    distance.append(cost1 + cost2)
                min_dis = min(distance)
                # Check whether router has found new best path?
                if min_dis < int(temp):
                    self.table[int(self.name) - 1][d_r_iter] = str(min_dis)
                    for m in range(self.r_count):
                        self.lie_table[m][d_r_iter] = str(min_dis)
                    min_through = distance.index(min_dis)
                    self.use_who[d_r_iter + 1] = str(min_through + 1)
                    # lie to middle router with a high cost(Poisoned reverse)
                    lie_to = min_through
                    self.lie_table[lie_to][d_r_iter] = '99'
                    self.send()
                distance.clear()
        self.bf_show()

    def bf_show(self):
        print("\nThe Cost table of router {} is :".format(self.name))
        print("        ", end="")
        for h in range(self.r_count):
                print("{:<8}".format(h + 1), end="")
        print("\n----------------------------------------------------")
        for row in range(self.r_count):
            print("{}|      ".format(row + 1), end="")
            for col in range(self.r_count):
                if row == int(self.name) - 1:
                    print("{:<2}\{:<5}".format(self.table[row][col], self.use_who[col + 1]), end="")
                else:
                    print("{:<8}".format(self.table[row][col]), end="")
            print()
        print("----------------------------------------------------")

    def check_cost(self, new_cost):
        # Determine whether any cost has changed?
        if self.initial_cost == new_cost:
            print("No Cost Change!")
        else:
            # 1- update its row for new costs
            # 2- update lie table
            # 3- update use who
            # 4- update permissions
            # 5- solve pp cost
            # 6- do alg()
            # 7- show the results
            self.initial_cost = new_cost
            print("link costs of router {} is changed!".format(self.name))
            self.table[int(self.name) - 1] = new_cost
            self.lie_table = []
            for m in range(self.r_count):
                self.lie_table.append([])
                for n in range(self.r_count):
                    self.lie_table[m].append(new_cost[n])
            for m in range(self.r_count):
                if new_cost[m] == 'N':
                    self.use_who[m + 1] = ''
                else:
                    self.use_who[m + 1] = str(m + 1)
            self.who_to_send()
            self.do_alg()
