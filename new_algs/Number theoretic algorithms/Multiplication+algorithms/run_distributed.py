# Wesley Layton Ellington
# Fault Tolerant Computing
# Fall 2019
# Term Project: ABFT Multiplication 

# Over all run script for running DISTRIBUTED version of ABFT multiplication 
# This script will create Mininet environment, check connectivity, start servers, then call
#	'multi_driver.py' to execute distributed application
#run: python multi_driver.py <input_csv_1> <input_csv_2>

from mininet.net import Mininet
from topo_16_star import center_star
import sys

input_cmd = ""
if len(sys.argv) > 2:
	input_1 = sys.argv[1]
	input_2 = sys.argv[2]
	input_cmd = "%s %s" % (input_1, input_2)
	print("Using inputs %s" % input_cmd)


network_topo = center_star()
net = Mininet(topo=network_topo)
net.start()

server_port = 9999

h00 = net.hosts[0]
servers = net.hosts[1:]

print("Testing connections...")
for host in servers:
	print(host)
	print(host.cmd('ping -c1 %s' % h00.IP()))


print("Starting servers")
for server in servers:
	command = 'python -u ../src/abft_server.py %s %s' % (server.IP(), server_port) 
	log_cmd = '> output/%s.log 2>&1 &'% (server)
	command = command + " " + log_cmd
	print("Starting server %s : %s" % (server, command))
	server.cmd(command)
	#print(server.cmd(command))

print("Starting client process...")
command = 'python ../src/multi_driver.py %s' % (input_cmd)
log_cmd = '> output/client_%s.log' % (h00)
command = command + " " + log_cmd
print(command)
print(h00.cmd(command))
#h1, h4  = net.hosts[0], net.hosts[3]
#print h1.cmd('ping -c1 %s' % h4.IP())
print("Processing finished!")

print("Cleaning up")
#for server in servers:
#	command = 'kill %%python'
#	print("Stopping server %s : %s" % (server, command))
#	server.cmd(command)

print("Done!")
net.stop()
