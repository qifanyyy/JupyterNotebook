"""
A module for communication between Node-Node and Node-Master.
Exports:
Message - an object of an message sent between nodes / node-master.
NodeClient - a client for a Node used to send and receive Messages.
MasterClient - a client for the Master used to send and receive Messages.
Server - a set of MasterClient and multiple NodeClients run by the Master.
         Handles all communication and enables interactive debugging,
         logging etc' according to custom defined rules.
         The server sets up the NodeClients and MasterClient.
"""

from utils import log, enum, copy

class Server(object):
    """Main module's object - a Server containing a MasterClient & NodeClients.
    Handles all communication and enables interactive debugging,
    logging etc' according to custom defined rules. Rules can be added using
    add_rule and actions preformed are defined in Server.Action enum.
    """
    
    # ID of MasterClient in the protocol. Default client IDs are 1,...,n
    MASTER_ID = -1
    
    def __init__(self, clients):
        """ Init a new Server. @clients may be either number of clients or a list of client IDs """
    
        # Create clients, including master client
        if isinstance(clients, int):
            clients = range(clients)
        self._clients = {}
        for id in clients:
            self.add_client(id)
        self.add_client(Server.MASTER_ID, is_master=True)
        self._master = self._clients[Server.MASTER_ID]
        
        # Define basic switching and counter rules
        self._rules = {}
        is_valid_ctrl_msg = lambda m : Message.TYPE.is_ctrl_msg(m.get_type()) and Server.MASTER_ID in (m.get_src(), m.get_dst())
        is_invalid_ctrl_msg = lambda m : Message.TYPE.is_ctrl_msg(m.get_type()) and Server.MASTER_ID not in (m.get_src(), m.get_dst())
        always = lambda m : True
        self.add_rule("is_valid_ctrl_msg", is_valid_ctrl_msg, Server.Action.DEBUG | Server.Action.CTRL_ON)
        self.add_rule("is_invalid_ctrl_msg", is_invalid_ctrl_msg, Server.Action.WARN | Server.Action.DROP)
        self.add_rule("count_default", always, Server.Action.COUNTER_ON)
        #self.add_rule("log_all", always, Server.Action.LOG)
        #self.add_rule("test_bp", lambda m : m.get_type() is Message.TYPE.EvalOutput and m.get_dst()==2, Server.Action.BREAKPOINT)
        
        # Counters
        self._ctrs = {}
    
    def add_client(self, node_id, is_master=False):
        """Add a client to the Server.
        @node_id - the client's unique node id. MASTER_ID is reserved for master.
        @is_master - is this the MasterClient? Only one Master allowed. In this case @node_id must be MASTER_ID
        """
        send_msg_callback = lambda *args : self._recv(node_id, *args)
        if is_master:
            assert Server.MASTER_ID not in self._clients, "Master client already exists!"
            assert node_id == Server.MASTER_ID, "Invalid ID for master client!"
            client = MasterClient(node_id, send_msg_callback)
        else:
            assert node_id not in self._clients, "Client %d already exists!" % node_id
            assert node_id != Server.MASTER_ID, "Invalid ID for NON-master client!"
            client = NodeClient(node_id, send_msg_callback)
        self._clients[node_id] = client
    
    def get_client(self, id):
        """ Get the Client object for the given @id """
        assert id in self._clients, "Invalid client id %d" % id
        return self._clients[id]
    
    def get_master(self):
        """ Get the MasterClient """
        return self._master
    
    def _recv(self, src, msg):
        """ Handles an incoming Message @msg from source @src. All Messages are processed by _recv """
        # Make sure msg is not forged
        assert msg.get_src() == src, "Invalid message source!!"
        
        # Check rules and perform appropriate action accordingly
        is_ctrl = False
        is_ctr = False
        actions = self._check_rules(msg)
        if actions & Server.Action.DEBUG:
            log.debug("Received message: %r", msg)
        if actions & Server.Action.LOG:
            log.info("Received message: %r", msg)
        if actions & Server.Action.WARN:
            log.warning("Received message: %r", msg)
        if actions & Server.Action.BREAKPOINT:
            log.debug("Breakpoint rule jumped on: %r", msg)
            self.send_to_master(msg, breakpoint=True)
        if actions & Server.Action.DUP_TO_MASTER:
            log.debug("Duplicate rule jumped on: %r", msg)
            self.send_to_master(msg)
        if actions & Server.Action.CTRL_ON:
            is_ctrl = True
        if actions & Server.Action.CTRL_OFF:
            is_ctrl = False
        if actions & Server.Action.COUNTER_ON:
            is_ctr = True
        if actions & Server.Action.COUNTER_OFF:
            is_ctr = False
        # Drop is the last action to perform
        if actions & Server.Action.DROP:
            log.debug("Drop rule jumped on: %r", msg)
        else:
            # Message counters
            if is_ctr:
                self._ctrs[msg.get_type()] = self._ctrs.get(msg.get_type(), 0) + 1
            # Regular switching
            if msg.get_dst() == Server.MASTER_ID:
                self.send_to_master(msg)
            else:
                self.send(msg, ctrl=is_ctrl)
    
    def send(self, msg, ctrl=False):
        """Send Message @msg (source and destination are part of @msg).
        @ctrl - is this a control message? (protocol-steps / debug / reset etc')
        """
        dst = msg.get_dst()
        if dst not in self._clients or dst == Server.MASTER_ID:
            log.error("Invalid destination for message: %r", msg)
            return
        self._clients[dst].push_msg(msg, ctrl)
    
    def send_to_master(self, msg, breakpoint=False):
        """Send Message @msg to Master.
        @breakpoint - is this a breakpoint trigger message?
        """
        is_direct = (msg.get_dst() == Server.MASTER_ID)
        self._master.push_msg(msg, is_direct=is_direct, is_breakpoint=breakpoint)
    
    def get_counters(self):
        """Returns the message counters - a dictionary with keys for each message type"""
        return copy.deepcopy(self._ctrs)
    
    def get_counted_ctrl(self):
        """Returns the message counters - a dictionary with keys for each message type.
        Only for CTRL messages
        """
        ctrl_ctrs = [v for typ,v in self._ctrs.items() if Message.TYPE.is_ctrl_msg(typ)]
        return sum(ctrl_ctrs, 0)
    
    def get_counted_node(self):
        """Returns the message counters - a dictionary with keys for each message type.
        Only for (node <--> node) messages
        """
        node_ctrs = [v for typ,v in self._ctrs.items() if Message.TYPE.is_node_msg(typ)]
        return sum(node_ctrs, 0)
    
    def add_rule(self, name, rule, action):
        """Add a rule to message processing.
        @name - unique rule name (str)
        @rule - a function to be a applied on every Message sent, which returns a boolean
        @action - a bitfield (int) made out of Server.Action values, defining actions to perform in case @rule returns True
        """
        self._rules[name] = (rule, action)
    
    def del_rule(self, name):
        """Delete the rule named @name"""
        assert name in self._rules, "Rule %s doesn't exist" % name
        self._rules.pop(name)
    
    def _check_rules(self, msg):
        """Check all rules on @msg. Returns the bitfield for actions to be made"""
        actions = Server.Action.NONE
        for rule_name, (rule, action) in self._rules.items():
            if rule(msg):
                log.debug("Check rules: Rule %s activated on msg %d", rule_name, msg.get_sequence())
                actions |= action
        return actions

    # Rule actions. Multiple values can be chosen by OR-ing Actions.
    Action = enum(
        NONE            = 0x00 , # No action made
        DEBUG           = 0x01 , # Log message with log.debug
        LOG             = 0x02 , # Log message with log.info
        WARN            = 0x04 , # Log message with log.warn
        BREAKPOINT      = 0x08 , # Trigger a breakpoint
        DUP_TO_MASTER   = 0x10 , # Duplicate message to MasterClient (To sniff queue)
        DROP            = 0x20 , # Drop message (do not send to destination). Last action performed (for an example - you can log and duplicate a message before dropoing it)
        CTRL_ON         = 0x40 , # Mark this message as ctrl message
        CTRL_OFF        = 0x80 , # Don't mark this message as ctrl message. Overrides CTRL_ON
        COUNTER_ON      = 0x100, # Count this message to message counters
        COUNTER_OFF     = 0x200, # Don't count this message to message counters. Overrides COUNTER_ON
    )

class Client(object):
    """ A general client object, that has an id and a method for sending messages.
    Implementing a client requires implementing reset, push_msg, queue_status.
    """
    def __init__(self, node_id, send_callback):
        """
        @node_id - the unique node id, used as source and destination in Messages.
        @send_callback - a function receiving a single Message argument that
                         handles sending a message from this client.
        """
        self._id = node_id
        self._mailbox = []
        self.send = send_callback
    
    def get_id(self):
        """@return the Client's ID"""
        return self._id

class NodeClient(Client):
    """A Client for Nodes.
    A Node has a queue for ctrl messages (from master) and regular messages (from other nodes).
    """
    # ID of MasterClient
    MASTER_ID = Server.MASTER_ID
    
    def __init__(self, node_id, send_callback):
        """
        @node_id - the unique node id, used as source and destination in Messages.
        @send_callback - a function receiving a single Message argument that
                         handles sending a message from this client.
        """
        Client.__init__(self, node_id, send_callback)
        self._ctrl = []
    
    def reset(self):
        """Reset client's state - deletes all messages in queues"""
        self._mailbox = []
        self._ctrl = []
    
    def push_msg(self, msg, is_ctrl):
        """Receive incoming message @msg to queue
        @is_ctrl - Is this a CTRL message?
        """
        if is_ctrl:
            self._ctrl.append(msg)
        else:
            self._mailbox.append(msg)
    
    def queue_status(self):
        """@return a tuple of number of messages in (ctrl queue, regular messages queue)"""
        return (len(self._ctrl), len(self._mailbox))
    
    def get_ctrl_msg(self):
        """Get the next message from the ctrl queue.
        Return None if no messages exist.
        """
        if self._ctrl:
            return self._ctrl.pop(0)
        return None
    
    def get_data_msg(self, msg_type=None):
        """Get the next message from the regular-mailbox queue.
        @msg_type - If set, allow only Messages of this type to be returned.
        Return None if no appropriate message exist.
        """
        for i, m in enumerate(self._mailbox):
            if m.get_type() == msg_type or msg_type is None:
                self._mailbox.pop(i)
                return m
        return None
    
    def __repr__(self):
        """String representation of object"""
        ret  = "NodeClient %d\n" % self._id
        ret += "Ctrl (%d):\n" % len(self._ctrl)
        for m in self._ctrl:
            ret += "%r\n" % m
        ret += "Mailbox (%d):" % len(self._mailbox)
        for m in self._mailbox:
            ret += "\n%r" % m
        return ret

class MasterClient(Client):
    """A Client for Master.
    A Master has a queue for breakpoint messages (triggered by rules),
    regular messages (ctrl messages from nodes) and
    sniff messages (not addressed to master, but captured by a rule).
    """
    def __init__(self, node_id, send_callback):
        """
        @node_id - the unique node id, used as source and destination in Messages.
        @send_callback - a function receiving a single Message argument that
                         handles sending a message from this client.
        """
        Client.__init__(self, node_id, send_callback)
        self._sniff = []
        self._breakpoint = []
    
    def push_msg(self, msg, is_direct, is_breakpoint=False):
        """Receive incoming message @msg to queue.
        @is_directly - was this message sent directly to me?
        @is_breakpoint - this message should trigger a breakpoint?
        """
        if is_breakpoint:
            self._breakpoint.append(msg)
            
        if is_direct:
            self._mailbox.append(msg)
        else:
            self._sniff.append(msg)
    
    def queue_status(self):
        """@return a tuple of number of messages in (breakpoint queue, regular messages queue, sniff queue)"""
        return (len(self._breakpoint), len(self._mailbox), len(self._sniff))
    
    def get_breakpoint_msg(self):
        """Get the next message from the breakpoint queue.
        Return None if no messages exist.
        """
        if self._breakpoint:
            return self._breakpoint.pop(0)
        return None
        
    def get_data_msg(self):
        """Get the next message from the data-mailbox queue.
        Return None if no messages exist.
        """
        if self._mailbox:
            return self._mailbox.pop(0)
        return None
        
    def get_sniff_msg(self):
        """Get the next message from the sniffing queue.
        Return None if no messages exist.
        """
        if self._sniff:
            return self._sniff.pop(0)
        return None
    
    def get_msg(self):
        """Get the next message from the queue: ctrl first, sniffs next.
        Returns None if both queues are empty.
        """
        if self._mailbox:
            return self._mailbox.pop(0)
        elif self._sniff:
            return self._sniff.pop(0)
        else:
            return None
    
    def __repr__(self):
        """String representation of object"""
        ret  = "MasterClient %d\n" % self._id
        ret += "Breakpoint (%d):\n" % len(self._breakpoint)
        for m in self._breakpoint:
            ret += "%r\n" % m
        ret += "Mailbox (%d):\n" % len(self._mailbox)
        for m in self._mailbox:
            ret += "%r\n" % m
        ret += "Sniff (%d):" % len(self._sniff)
        for m in self._sniff:
            ret += "\n%r" % m
        return ret
    
class Message(object):
    """A message sent in the protocol between Node-Node or Node-Client.
    A Message is an immutable object made of: source, destination, message-type[, msg-data].
    Message types are defined in Message.TYPE enum.
    """
    # A global sequence number for messages factory
    _global_seq = 0
    
    def __init__(self, src, dst, msg_type, msg=""):
        """Create a new Message.
        @src - id of source client
        @dst - id of destination client
        @msg_type - message type from Message.TYPE
        @msg - optional data payload (string)
        """
        self._src = src
        self._dst = dst
        self._msg_type = msg_type
        self._msg = msg
        self._seq = self._next_sequence()
    
    def get_src(self):
        return self._src
    
    def get_dst(self):
        return self._dst
    
    def get_type(self):
        return self._msg_type
    
    def get_sequence(self):
        return self._seq
    
    def get_msg(self):
        return self._msg
    
    def __repr__(self):
        """String representation of object. Messages too long are truncated"""
        MSG_MAX_LEN = 20
        msg = self._msg
        if len(msg) > MSG_MAX_LEN:
            msg = msg[ : (MSG_MAX_LEN - 3)] + "..."
        return "Src: %d, Dst: %d, Type: %d, seq: %d, Msg: %r" % \
            (self._src, self._dst, self._msg_type, self._seq, msg)
    
    @classmethod
    def _next_sequence(cls):
        cls._global_seq += 1
        return cls._global_seq


    class TYPE():
        """Enum for message types"""
        
        #Node-Node messages
        InputShare             = 1  # Share your input
        RegenRandPolyShare     = 2  # Fallen node regen - mask shares
        RegenRandPolyResult    = 3  # Fallen node regen - shares after transformation
        BGWMulRandPolyShare    = 4  # BGW multiplication - mask
        BGWMulReductionShare   = 5  # BGW multiplication - shares of masked mult
        BGWMulReductionResult  = 6  # BGW multiplication - shares after reduction
        DIKBulkShareLow        = 7  # DIK10 multiplication masks - low degree
        DIKBulkShareHigh       = 8  # DIK10 multiplication masks - high degree
        DIKMulHighShare        = 9  # DIK10 masked share for "dealer" (high deg)
        DIKMulLowShare         = 10 # DIK10 masked share from "dealer" (low deg)
        OutputShare            = 11 # Send final results for output reconstruction
        # ...
        
        # Ctrl messages
        _CTRL_START            = 100 # Invalid message type, internal use only
        Reset                  = 101 # Reset node's whole internal state
        DebugData              = 102 # Get debug data from node to master
        SetCircuit             = 103 # Set the node's circuit
        SetTruncinator         = 104 # Set the node's truncinator for BGW multiplication
        SetResampler           = 105 # Set the node's resampler for DIK multiplication
        SetSecretSharing       = 106 # Set the node's secret sharing schemes' parameters
        SetInput               = 107 # Set the node's input to a specific value
        SetRandInput           = 108 # Node chooses a random input in the given finite field
        GenBulkMulMasks        = 109 # Generate random masks for DIK multiplication (should be used as preprocessing step)
        GenBulkRegenMasks      = 110 # Generate random masks for regenerating a falled node (may be used as preprocessing step)
        ShareInput             = 111 # Tell node to share its input
        EvalGate               = 112 # Tell node to evaluate the given gate - only for local computed gates (not multiplication)
        EvalMulGateDIK         = 113 # Tell node to start protocol for multiplication using DIK multiplication sub-protocol
        EvalMulGateInit        = 114 # Tell node to start protocol for multiplication using BGW multiplication sub-protocol
        EvalMulGateReduce      = 115 # Second step in BGW multiplication sub-protocol
        EvalMulGateFinalize    = 116 # Last step in BGW multiplication sub-protocol
        EvalOutput             = 117 # Send output to all parties for final output reconstruction
        #...
        
        @classmethod
        def is_ctrl_msg(cls, t):
            return t >= cls._CTRL_START
        
        @classmethod
        def is_node_msg(cls, t):
            return not cls.is_ctrl_msg(t)
