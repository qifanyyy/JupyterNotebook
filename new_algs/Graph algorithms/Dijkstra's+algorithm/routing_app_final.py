from ryu.base import app_manager
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls

portmatrix =    [[0, 2, 3, 0, 0, 4], 
                [2, 0, 3, 4, 0, 0], 
                [2, 3, 0, 4, 0, 5], 
                [0, 2, 3, 0, 4, 0], 
                [0, 0, 0, 2, 0, 3], 
                [2, 0, 3, 0, 4, 0]]

graph = [[0,  70,  90,  0,   0,   140], 
        [70,  0,   100, 150, 0,   0], 
        [90,  100, 0,   110, 0,   20], 
        [0,   150, 110, 0,   60,  0], 
        [0,   0,   0,   60,  0,   90], 
        [140, 0,   20,  0,   90,  0]]

switches = {}
up_down = {}

class Routing(app_manager.RyuApp):

    # route IP and ARP packets from switch n to host n
    def route_to_host(self,n,sw):
        ofproto = sw.ofproto
        parser = sw.ofproto_parser
            # check the destination IP address of IP packets
        match = parser.OFPMatch(nw_dst=(10 << 24)+n, dl_type=0x800)
        action = parser.OFPActionOutput(1)
        cmd = parser.OFPFlowMod(
                datapath=sw, match=match, cookie=0,
                command=ofproto.OFPFC_ADD, idle_timeout=0,
                hard_timeout=0, priority=10,
                flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
        sw.send_msg(cmd)

            # check the destination IP address of ARP packets
        match = parser.OFPMatch(nw_dst=(10 << 24)+n, dl_type=0x806)
        action = parser.OFPActionOutput(1)
        cmd = parser.OFPFlowMod(
                datapath=sw, match=match, cookie=0,
                command=ofproto.OFPFC_ADD, idle_timeout=0,
                hard_timeout=0, priority=10,
                flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
        sw.send_msg(cmd)


    # route IP and ARP packets to a specific output port according to both source and destination addresses
    def route(self, src_id, dst_id, out_port, sw):
        ofproto = sw.ofproto
        parser = sw.ofproto_parser

        match = parser.OFPMatch(nw_src=(10 << 24)+src_id, nw_dst=(10 << 24)+dst_id, dl_type=0x800)
        action = parser.OFPActionOutput(out_port)
        cmd = parser.OFPFlowMod(
                datapath=sw, match=match, cookie=0,
                command=ofproto.OFPFC_ADD, idle_timeout=0,
                hard_timeout=0, priority=10,
                flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
        sw.send_msg(cmd)

        match = parser.OFPMatch(nw_src=(10 << 24)+src_id, nw_dst=(10 << 24)+dst_id, dl_type=0x806)
        action = parser.OFPActionOutput(out_port)
        cmd = parser.OFPFlowMod(
                datapath=sw, match=match, cookie=0,
                command=ofproto.OFPFC_ADD, idle_timeout=0,
                hard_timeout=0, priority=10,
                flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
        sw.send_msg(cmd)

    def minDistance(self, dist, visited): 
  
        minn = float('inf')
  
        for v in range(6): 
            if dist[v] < minn and visited[v] == False: 
                minn = dist[v] 
                min_index = v 
  
        return min_index 

    def dijkstra(self, id):
        dist = [float('inf')] * 6
        dist[id] = 0
        visited = [False] * 6
        ports = [0] * 6
  
        for cout in range(6): 
  
            # Closest vertex not yet processed
            u = self.minDistance(dist, visited) 
  
            # Put the minimum distance vertex in the tree
            visited[u] = True
  
            # Update dist value of the adjacent vertices
            for v in range(6): 
                if (graph[u][v] > 0 and visited[v] == False and dist[v] > dist[u] + graph[u][v]): 
                        dist[v] = dist[u] + graph[u][v]
                        if(u == id):
                            ports[v] = portmatrix[u][v]
                        else:
                            ports[v] = ports[u]

        return ports

    # when a switch is connected to the controller, send forwarding rules to it.
    def switch_connected(self, sw):

        ofproto = sw.ofproto
        parser = sw.ofproto_parser

        # acquire the ID of the switch
        id=int(str(sw.id))
        print ('S'+str(id)+' is connected!')

        switches[id - 1] = sw
        self.route_to_host(id,sw)
        ports = self.dijkstra(id - 1)
        for i in range(6):
            for j in range(6):
                if(i != j and j + 1 != id):
                    self.route(i+1,j+1,ports[j],sw)


    # when network topology changes, this function will be triggered.
    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def _port_status_handler(self, ev):
        msg = ev.msg
        reason = msg.reason
        port_no = msg.desc.port_no

        # acquire the ID of the switch
        id=int(str(msg.datapath.id))

        ofproto = msg.datapath.ofproto
        if reason == ofproto.OFPPR_ADD:
            self.logger.info("port added %s at switch %s", port_no, str(id))
        elif reason == ofproto.OFPPR_DELETE:
            self.logger.info("port deleted %s at switch %s", port_no, str(id))
        elif reason == ofproto.OFPPR_MODIFY:
            self.logger.info("port modified %s at switch %s", port_no, str(id))
            if(port_no < 6):
                if((id,port_no) in up_down):
                    for i in range(6):
                        if(portmatrix[id-1][i] == port_no):
                            change = i
                    graph[id-1][change] = up_down[(id,port_no)]
                    self.logger.info("port %s at switch %s set to original", port_no, str(id))
                    del up_down[(id,port_no)]
                else:
                    for i in range(6):
                        if(portmatrix[id-1][i] == port_no):
                            change = i
                    up_down[(id,port_no)] = graph[id-1][change]
                    graph[id-1][change] = 0
                    self.logger.info("port %s at switch %s set to infinity", port_no, str(id))
                for i in range(1,7):
                    ports = self.dijkstra(i - 1)
                    for j in range(1,7):
                        for k in range(1,7):
                            if(j != k and k != i):
                                self.route(j,k,ports[k-1],switches[i-1])

        else:
            self.logger.info("Illeagal port state %s %s", port_no, reason)


    @set_ev_cls(dpset.EventDP)
    def switch_events(self, ev):
        if ev.enter:
            self.switch_connected(ev.dp)