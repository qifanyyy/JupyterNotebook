import sys
import json
import socket
import pickle

from multiprocessing import Process
from select import select
from datetime import datetime

now = datetime.now

# algo:
# every node gets a file wth neighbour weights
# any weight updates are realized through the file


# for setting up tcp connections, have 2 tcps con with every neighbr
# one for one direction i.e semi duplex connection
# one tcp connection is only for receiving updates
# and the other for sending updates

# every node also maintains in memory:
# dv of current node - shortest est to all nodes from current node
# previous nodes - next hop node (neighbour) on the shortest path for each dst
# dv for all neighbours

# on every new update from neigh, upd shortest tables

# if shortest path to any node from current node changed
# or if say 30s passed since last update/read of links, send an update to all neighbrs with current best paths from source

# this algorithm was done in collaboration with Deepika Peringanji - 110614748

if len(sys.argv) < 3:
    print 'Please pass the 2 args, node name and periodic refresh value'
    sys.exit()

node_name = sys.argv[1]
timeout = int(sys.argv[2])

# we are assuming we have a file named with node name, containing the neighbour details
neighbour_wts_f = node_name

# last time the neighbour file was read
last_read_time = now()

# last time the neighbours were updated
last_upd_time = now()

def get_neighbours(fn):

    f = open(fn, 'r')
    neighbours_txt = f.read().split('\n')
    f.close()

    # the cost dict
    # this is cost of direct neighbours and got through file
    # {neighbour : cost}
    c = {}

    # dict of neighbour ip interfaces to neighbour name
    ips = {}

    # dict of source intf (ip) to dest intf (ip)
    links = {}

    for neighbour in neighbours_txt:
        src_ip, n, dst_ip, cost = neighbour.strip().split(':')
        cost = int(cost)
        c[n] = cost
        ips[dst_ip] = n
        links[src_ip] = dst_ip

    global last_read_time
    last_read_time = now()

    return c, ips, links

c, ips, links = get_neighbours(neighbour_wts_f)

# this is the dv of current node
# the estimate of least distance to dst
# {dst : est of least dist to dst from current node}
d = {}
max_d = 100000
for neighbour, cost in c.iteritems():
    d[neighbour] = cost

# this is the pre
p = {}

# neighbours dv
# neighbour: {dst : est least dist to dst from neighbour}
dv = {}

socks_connected = {}
socks_accepted = {}


port = 9999

def connect_to_neighbours(neighbours):
    for ip, name in neighbours.iteritems():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.connect((ip, port))
        socks_connected[name] = s


def listen_neighbour_on(ip, neighbour):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    s.bind((ip, port))

    s.listen(1)
    sock, addr = s.accept()
    socks_accepted[neighbour] = sock

    print 'Accepted connection from',  str(addr)


threads = []
# for each link, start a thread to accept connection
# from its neigbour
for src_ip, dst_ip in links.iteritems():
    neighbour = ips[dst_ip]
    t = Process(target=listen_neighbour_on, args=(src_ip, neighbour, ))
    threads.append(t)

# start a thread to connect to all neighbours
threads.append(Process(target=connect_to_neighbours, args=(ips, )))

for t in threads:
    t.start()

for t in threads:
    t.join()

read_socks = []
read_names = []

for name, sock in socks_accepted.iteritems():
    read_socks.append(sock)
    read_names.append(name)

write_socks = socks_connected.values()

read_timeout = 0

while True:

    ready_to_read, _, in_error = select( read_socks, [], read_socks, read_timeout)

    update = False

    # we now have new dvs from neighbours or a timeout
    for sock in ready_to_read:
        # for all sock that have data
        # we have a new corresponding dv from a neighbour
        data = sock.recv(100000)
        neighbour = read_names[read_socks.index(sock)]
        nd = json.loads(data)
        dv[neighbour] = nd
        cost = c[neighbour]
        for dst, est in nd.iteritems():
            if est + cost < d.get(dst, max_d):
                d[dst] = est + cost
                p[dst] = neighbour
                update = True

    if (not update) and ((now() - last_upd_time).seconds >= timeout):
        update = True

    if (now() - last_read_time).seconds >= timeout:
        # last time we read was more than timeout sec
        # read the neighbours file again to check for link changes
        c_new, ips, links = get_neighbours(neighbour_wts_f)
        if c != c_new:
            # if links changed
            c = c_new

            d_new = {}
            for neighbour, cost in c.iteritems():
                d[neighbour] = cost

            # calculate new latest dv for current node
            for neighbour, ndv in dv.iteritems():
                cost = c[neighbour]
                for dst, est in ndv.iteritems():
                    if cost + est < d_new.get(dst, max_d):
                        d_new[dst] = cost + est
                        p[dst] = neighbour 

            # if dv changed
            if d_new != d:
                d = d_new
                update = True

    if update:
        # send d to all neighbours
        data = json.dumps(d)
        for sock in write_socks:
            sock.sendall(data)
        last_upd_time = now()
        # also put the routing tables into a file
        pickle.dump(dv, open( node_name + '_dv.p', "wb"))
        pickle.dump(p, open( node_name + '_p.p', "wb"))
        pickle.dump(d, open( node_name + '_d.p', "wb"))

    read_timeout = timeout - (now() - max(last_upd_time, last_read_time)).seconds


