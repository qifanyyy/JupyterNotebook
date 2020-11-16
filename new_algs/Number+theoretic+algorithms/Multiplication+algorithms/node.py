"""
A module for implementing a Node (party) participating in BGW MPC.
"""

from utils import log, enum, copy
from serializer import *
from config import Config
from messenger import NodeClient, Message
from gf import Zmod, FFE
from circuit import Circuit
from transformation import Truncinator, Resampler
from operator import add

if Config.USE_GW_SSS1:
    from secretsharing import GWSSS as SSS
else:
    from secretsharing import ShamirSSS as SSS

if Config.USE_GW_SSS2:
    from secretsharing import GWSSS as SSS2
else:
    from secretsharing import ShamirSSS as SSS2

class Node(object):
    """A party in BGW MPC.
    Each party has an id and a messaging client, used to communicate with other Nodes and the Master.
    The Node uses a secret sharing scheme to share inputs and perform various calculation.
    Every Node has an internal state machine - for more info see automata diagram.
    """
    
    # Node possible states. See automata diagram.
    State = enum(
        "UNINITIALIZED"       , \
        "INITIALIZED"         , \
        "RECEIVING_INPUTS"    , \
        "RUNNING"             , \
        "GEN_BULK_MUL_MASKS"  , \
        "GEN_BULK_REGEN_MASKS", \
        "MUL_DIK_DEALER"      , \
        "MUL_DIK_NON_DEALER"  , \
        "MUL_RANDPOLY_SHARE"  , \
        "MUL_RANDPOLY_DONE"   , \
        "MUL_REDUCTION_SHARE" , \
        "MUL_REDUCTION_CALC"  , \
        "MUL_RECONSTRUCTION"  , \
        "RECEIVING_OUTPUTS"   , \
        "DONE"
    )
    
    def __init__(self, id, messenger_client, n_parties, master_id):
        """Initialize a Node.
        @id - the Node's unique id (for communication).
        @messenger_client - a NodeClient used for communication with Nodes and Master.
        @party_ids - ordered list of ids of all parties (including self).
        @master_id - id of the Master.
        @ss_args - additional arguments to the secret sharing schemes.
        """
        self._id = id
        self._master_id = master_id
        self._io = messenger_client
        self._n_parties = n_parties
        self.reset()
        
    def reset(self):
        """Reinitialize Node. Deletes any state gained after __init__, except NodeClient's state"""
        self._input = None
        self._circuit = None
        self._truncinator = None
        self._resampler = None
        self._ss = None
        self._ss2 = None

        self._t = Config.THRESHOLD(self._n_parties)
        self._t2 = Config.THRESHOLD2(self._n_parties)
        
        # Random mask shares for DIK10 multiplication
        if Config.MULT_METHOD == Config.MULT_METHODS.DIK:
            self._dik_low = []
            self._dik_high = []
            self._dik_ptr = 0
        
        self._state = self.State.UNINITIALIZED
    
    def __repr__(self):
        """String representation of object"""
        ret  = "** Node %d: %s **\n" % \
            (self._id, self.State.reverse_mapping[self._state])
        ret += repr(self._io)
        return ret
    
    def run(self, runs=1):
        """Make @runs steps of execution.
        A step includes the following sub-steps:
        1. Check and handle all of CTRL messages received from Master
        2. Perform additional operations according to the current inner state
           (evaluate a gate / send shares / collect shares / ...)
        """
        for i in xrange(runs):
            # Check for ctrl (high-priority) messages
            ctrl_msgs, reg_msgs = self._io.queue_status()
            while ctrl_msgs > 0:
                m = self._io.get_ctrl_msg()
                assert m is not None, "No message received..."
                self._handle_ctrl_msg(m)
                ctrl_msgs, reg_msgs = self._io.queue_status()
            
            # Perform additional operations according to the current inner state
            self._run_step()
        return

    def _handle_ctrl_msg(self, m):
        """Handle all types of CTRL messages.
        May change inner state (see diagram).
        @m - a CTRL message
        """
        # switch case on msg type
        typ = m.get_type()
        
        # Reset Node
        if typ == Message.TYPE.Reset:
            self._io.reset()
            self.reset()
            self._state = self.State.UNINITIALIZED
        
        # Send debug data to Master
        elif typ == Message.TYPE.DebugData:
            self._send_to_master(Message.TYPE.DebugData, repr(self))
        
        # Read and set given serialized circuit
        elif typ == Message.TYPE.SetCircuit:
            self._assert_state("SetCircuit", self.State.UNINITIALIZED)
            if self._circuit is not None:
                log.warn("Setting new circuit without reset!")
            c = unserialize(m.get_msg(), Circuit)
            self._set_circuit(c)
            if self._fully_initialized():
                self._state = self.State.INITIALIZED
        
        # Read and set given parameters for secret sharing schemes
        elif typ == Message.TYPE.SetSecretSharing:
            self._assert_state("SetSecretSharing", self.State.UNINITIALIZED)
            ss_args, ss2_args = unserialize(m.get_msg())
            self._set_secret_sharing(ss_args, ss2_args)
            if self._fully_initialized():
                self._state = self.State.INITIALIZED
        
        # Read and set given input as party's input (FFE)
        elif typ == Message.TYPE.SetInput:
            self._assert_state("SetInput", self.State.UNINITIALIZED)
            secret_input = unserialize(m.get_msg(), FFE)
            self._set_input(secret_input)
            if self._fully_initialized():
                self._state = self.State.INITIALIZED
        
        # Set party's input to a random input in the given serialized field
        elif typ == Message.TYPE.SetRandInput:
            self._assert_state("SetRandInput", self.State.UNINITIALIZED)
            field = unserialize(m.get_msg())
            secret_input = field.rand()
            log.info("Node %d: Setting my input to %r (random)", self._id, secret_input)
            self._set_input(secret_input)
            if self._fully_initialized():
                self._state = self.State.INITIALIZED
        
        # Share party's input. Node must INITIALIZED (input and circuit received)
        elif typ == Message.TYPE.ShareInput:
            self._assert_state("ShareInput", self.State.INITIALIZED)
            self._input_shares = [None] * self._n_parties
            self._share(self._ss, self._input, Message.TYPE.InputShare)
            self._state = self.State.RECEIVING_INPUTS
        
        # Read and set given Truncinator as party's truncinator (for multiplication)
        elif typ == Message.TYPE.SetTruncinator:
            self._assert_state("SetTruncinator", [self.State.UNINITIALIZED, self.State.INITIALIZED, self.State.RUNNING])
            msg = m.get_msg()
            self._truncinator = unserialize(msg, Truncinator)
        
        # Read and set given Resampler as party's resampler (for bulk random masks)
        elif typ == Message.TYPE.SetResampler:
            self._assert_state("SetResampler", [self.State.UNINITIALIZED, self.State.INITIALIZED, self.State.RUNNING])
            msg = m.get_msg()
            self._resampler = unserialize(msg, Resampler)
        
        # Generate a bulk of masks for DIK10 multiplication
        elif typ == Message.TYPE.GenBulkMulMasks:
            self._assert_state("GenBulkMulMasks", [self.State.INITIALIZED, self.State.RUNNING])
            assert self._resampler is not None, "Cannot generate bulk masks - Resampler not set!"
            rand_val = self._field.rand()
            self._share(self._ss, rand_val, Message.TYPE.DIKBulkShareLow)
            self._share(self._ss2, rand_val, Message.TYPE.DIKBulkShareHigh)
            self._dik_low_shares = [None] * self._n_parties
            self._dik_high_shares = [None] * self._n_parties
            self._old_state = self._state
            self._state = self.State.GEN_BULK_MUL_MASKS
        
        # Generation of a bulk of masks for node going down - Phase1
        elif typ == Message.TYPE.GenBulkRegenMasks:
            self._assert_state("GenBulkRegenMasks", [self.State.INITIALIZED, self.State.RUNNING])
            assert self._resampler is not None, "Cannot generate bulk masks - Resampler not set!"
            
            # Choose a random polynomial with zero in the position to be regenerated & send shares
            self._regen_pos = unserialize(m.get_msg())
            zero = self._field.zero()
            self._share(self._ss, zero, Message.TYPE.RegenRandPolyShare, pos=self._regen_pos)
            
            # Init structures for collecting shares and masks
            self._regen_shares = [None] * self._n_parties
            if self._regen_pos not in self._regen_masks:
                self._regen_masks[self._regen_pos] = []
            self._old_state = self._state
            self._state = self.State.GEN_BULK_REGEN_MASKS
        
        # Evaluate a linear gate. Gate's name received in message
        elif typ == Message.TYPE.EvalGate:
            self._assert_state("EvalGate", self.State.RUNNING)
            self._eval_linear_gate(m.get_msg())
        
        ### <DIK multiplication> ###
        
        # Initialize and start evaluation of multiplication gate. Gate's name received in message
        elif typ == Message.TYPE.EvalMulGateDIK:
            self._assert_state("EvalMulGateDIK", self.State.RUNNING)
            assert len(self._dik_low) == len(self._dik_high), "DIK sanity check fail - low & high masks out of sync!"
            assert self._dik_ptr < len(self._dik_low), "Cannot multiply DIK - Not enough masks generated!"
            
            # Parse message for gate's name and the party performing the calculation
            self._mul_gate, self._mul_party = unserialize(m.get_msg())
            
            # Calculate local multiplication, add current (high degree) random mask & send to "dealer"
            naive_mult = self._circuit.evaluate_gate(self._mul_gate)
            masked_mult = self._dik_high[self._dik_ptr] + naive_mult
            processed_share = self._ss2.preprocess(masked_mult, self._id, pos=None) # pos=None for secret pos
            self._send_to_party(self._mul_party, Message.TYPE.DIKMulHighShare, processed_share)
            
            # Am I the dealer?
            if self._id == self._mul_party:
                self._state = self.State.MUL_DIK_DEALER
                self._mul_shares = [None] * self._n_parties
            else:
                self._state = self.State.MUL_DIK_NON_DEALER
        
        ### </DIK multiplication> ###
        
        ### <BGW multiplication> ###
        
        # Initialize and start evaluation of multiplication gate. Gate's name received in message
        elif typ == Message.TYPE.EvalMulGateInit:
            self._assert_state("EvalMulGateInit", self.State.RUNNING)
            assert self._truncinator is not None, "Cannot multiply - Truncinator not set!"
            
            # Init data structures for multiplication
            self._mul_gate = m.get_msg()
            self._mul_shares = [None] * self._n_parties
            
            # Generate a my part in the random mask & share
            zero = self._field.zero()
            self._share(self._ss2, zero, Message.TYPE.BGWMulRandPolyShare)
            self._state = self.State.MUL_RANDPOLY_SHARE
        
        # Perform local multiplication and mask result using the joint mask by received shares
        elif typ == Message.TYPE.EvalMulGateReduce:
            self._assert_state("EvalMulGateReduce", self.State.MUL_RANDPOLY_DONE)
            
            # Calculate regular multiplication and add joint random mask
            naive_mult = self._circuit.evaluate_gate(self._mul_gate)
            masked_mult = sum(self._mul_shares, naive_mult)
            
            # Share result (in high dimension) & reset data structure for new shares
            self._share(self._ss2, masked_mult, Message.TYPE.BGWMulReductionShare)
            self._mul_shares = [None] * self._n_parties
            self._state = self.State.MUL_REDUCTION_SHARE
        
        # Perform degree reduction on shares received, and send each party back its appropriate part
        elif typ == Message.TYPE.EvalMulGateFinalize:
            self._assert_state("EvalMulGateFinalize", self.State.MUL_REDUCTION_CALC)
            
            # Calculate linear degree reduction on the vector of evaluations
            reduced = self._truncinator.reduce(self._mul_shares)
            
            # Send back the reduced result & reset data structure for new shares
            processed_shares = [self._ss2.preprocess(s, self._id, pos=None) for s in reduced]
            self._send_to_parties(Message.TYPE.BGWMulReductionResult, processed_shares)
            self._mul_shares = [None] * self._n_parties
            self._state = self.State.MUL_RECONSTRUCTION
        
        ### </BGW multiplication> ###
        
        # Send my final output to all of the parties
        elif typ == Message.TYPE.EvalOutput:
            self._assert_state("ShareOutput", self.State.RUNNING)
            self._output_shares = [None] * self._n_parties
            out_share = self._circuit.get_output()
            output_msg = self._ss.preprocess(out_share, self._id, pos=None) # pos=None for secret pos
            msgs = [output_msg] * self._n_parties
            self._send_to_parties(Message.TYPE.OutputShare, msgs)
            self._state = self.State.RECEIVING_OUTPUTS

        else:
            log.error("Unknown ctrl msg received:\n%r", m)
    
    def _run_step(self):
        """Run additional operations according to inner state"""
        
        # switch case on states
        
        # UNINITIALIZED - Nothing to do (waiting for orders)
        if self._state is self.State.UNINITIALIZED:
            pass
        
        #RECEIVING_INPUTS - collect inputs received so far, initialize circuit when all inputs received
        elif self._state is self.State.RECEIVING_INPUTS:
            is_done = self._parse_shares(
               Message.TYPE.InputShare,
               self._input_shares
            )
            # All input shares received?
            if is_done:
                # Set in right order and initialize circuit
                self._circuit.init_all_inputs(self._input_shares)
                self._state = self.State.RUNNING
                del self._input_shares
        
        # RUNNING - Nothing to do (waiting for orders)
        elif self._state is self.State.RUNNING:
            pass
        
        # GEN_BULK_MUL_MASKS - collect shares received so far, until all shares received
        elif self._state is self.State.GEN_BULK_MUL_MASKS:
            is_done_low = self._parse_shares(
               Message.TYPE.DIKBulkShareLow,
               self._dik_low_shares
            )
            is_done_high = self._parse_shares(
               Message.TYPE.DIKBulkShareHigh,
               self._dik_high_shares
            )
            
            # All shares received?
            if is_done_low and is_done_high:
                # Create vector of the random evaluations and calculate linear combinations
                self._dik_low += self._resampler(self._dik_low_shares)
                self._dik_high += self._resampler(self._dik_high_shares)
                
                self._state = self._old_state
                del self._old_state
                del self._dik_low_shares
                del self._dik_high_shares
        
        # MUL_DIK_DEALER - collect shares received so far, until all received
        #                  then reconstruct masked multiplication and reshare
        elif self._state is self.State.MUL_DIK_DEALER:
            is_done = self._parse_shares(
               Message.TYPE.DIKMulHighShare,
               self._mul_shares
            )
            # All shares received?
            if is_done:
                # Reconstruct masked mult (in high dimension) & reshare in low dimension
                log.debug("Node %d Redealing", self._id)
                masked_mul = self._ss2.reconstruct(self._mul_shares, pos=None)
                self._share(self._ss, masked_mul, Message.TYPE.DIKMulLowShare)
                
                # Back to being like everybody else (wait for the share I sent myself)
                self._state = self.State.MUL_DIK_NON_DEALER
                del self._mul_shares
        
        # MUL_DIK_NON_DEALER - receive masked multiplication, remove mask & update the circuit
        elif self._state is self.State.MUL_DIK_NON_DEALER:
            result = {self._mul_party : None}
            is_done = self._parse_shares(
               Message.TYPE.DIKMulLowShare,
               result,
               expected_parties = [self._mul_party]
            )
            # Result received?
            if is_done:
                # Remove the mask from the output -> finally update the circuit
                masked_output = result[self._mul_party]
                output = masked_output - self._dik_low[self._dik_ptr]
                self._circuit.set_gate_output(self._mul_gate, output)
                self._dik_ptr += 1 #Done with this random mask pair
                self._state = self.State.RUNNING
                del self._mul_gate
                del self._mul_party
        
        # GEN_BULK_REGEN_MASKS - collect shares received so far, until all shares received
        elif self._state is self.State.GEN_BULK_REGEN_MASKS:
            is_done_low = self._parse_shares(
               Message.TYPE.RegenRandPolyShare,
               self._regen_shares
            )
            # All shares received?
            if is_done:
                # Create vector of the random evaluations and calculate linear combinations
                self._regen_masks[self._regen_pos] += self._resampler(self._regen_shares)
                self._state = self._old_state
                del self._old_state
                del self._regen_shares
                del self._regen_pos
        
        # MUL_RANDPOLY_SHARE - collect shares received so far, until all shares received
        elif self._state is self.State.MUL_RANDPOLY_SHARE:
            # Read all received shares to _mul_shares
            is_done = self._parse_shares(
               Message.TYPE.BGWMulRandPolyShare,
               self._mul_shares
            )
            # All shares received?
            if is_done:
                self._state = self.State.MUL_RANDPOLY_DONE
        
        # MUL_RANDPOLY_DONE - Nothing to do (waiting for orders)
        elif self._state is self.State.MUL_RANDPOLY_DONE:
            # Nothing to do (waiting for orders)
            pass
        
        # MUL_REDUCTION_SHARE - collect shares received so far, until all shares received
        elif self._state is self.State.MUL_REDUCTION_SHARE:
            is_done = self._parse_shares(
               Message.TYPE.BGWMulReductionShare,
               self._mul_shares
            )
            # All shares received?
            if is_done:
                self._state = self.State.MUL_REDUCTION_CALC
        
        # MUL_RANDPOLY_DONE - Nothing to do (waiting for orders)
        elif self._state is self.State.MUL_REDUCTION_CALC:
            pass
        
        # MUL_RECONSTRUCTION - collect shares received so far, until all received
        #                      then reconstruct gate's output & update the circuit
        elif self._state is self.State.MUL_RECONSTRUCTION:
            is_done = self._parse_shares(
               Message.TYPE.BGWMulReductionResult,
               self._mul_shares
            )
            # All shares received?
            if is_done:
                # Reconstruct our output (now in low dimension) -> finally update the circuit
                output = self._ss2.reconstruct(self._mul_shares, pos=None) #Reconstruct secret pos
                self._circuit.set_gate_output(self._mul_gate, output)
                self._state = self.State.RUNNING
                del self._mul_shares
                del self._mul_gate
        
        # RECEIVING_OUTPUTS - collect outputs received so far, until all received
        #                      then reconstruct circuit's output 
        elif self._state is self.State.RECEIVING_OUTPUTS:
            is_done = self._parse_shares(
               Message.TYPE.OutputShare,
               self._output_shares
            )
            # All outputs received?
            if is_done:
                self._output = self._ss.reconstruct(self._output_shares, pos=None)
                self._circuit.set_gate_output(self._circuit.OUTPUT, self._output)
                self._state = self.State.DONE
                log.info("Node %d outputs %r, I'm done.", self._id, self._output)
                del self._output_shares
        
        # DONE - Nothing to do (waiting for orders)
        elif self._state is self.State.DONE:
            pass
    
    def _assert_state(self, msg_type, state):
        """Make sure inner state is @state. If not - raises an AssertionError with @msg_type in error message"""
        if hasattr(state, '__iter__') == False:
            valid_state = (self._state == state)
            state_name = self.State.reverse_mapping[state]
        else:
            valid_state = (self._state in state)
            state_name = map(self.State.reverse_mapping.get, state)
        assert valid_state, \
            "Invalid state for %s, expected state/s %s\n%s" % (msg_type, state_name, repr(self))
        
    def _set_input(self, secret_input):
        """Sets the Node's input to the FFE @secret_input"""
        self._input = secret_input
        self._field = secret_input.get_field()
    
    def _set_secret_sharing(self, ss_args, ss2_args):
        """Sets the Node's circuit according to the serialized @circuit"""
        if ss_args is None:
            ss_args = []
        if isinstance(ss_args, dict):
            self._ss = SSS(self._n_parties, self._t, **ss_args)
        else:
            self._ss = SSS(self._n_parties, self._t, *ss_args)
        
        if ss2_args is None:
            ss2_args = []
        if isinstance(ss2_args, dict):
            self._ss2 = SSS2(self._n_parties, self._t2, **ss2_args)
        else:
            self._ss2 = SSS2(self._n_parties, self._t2, *ss2_args)
    
    def _set_circuit(self, circuit):
        """Sets the Node's circuit according to the given @circuit"""
        assert circuit.get_num_inputs() == self._n_parties, \
            "Number of circuit inputs (%d) != (%d) Number of parties" % (circuit.get_num_inputs(), self._n_parties)
        self._circuit = circuit
        self._cur_gate = None
    
    def _fully_initialized(self):
        """Check if Node is fully initialized (input & circuit set).
        Note that Truncinator is not a must (as some circuits have no multiplication gates)
        """
        return (self._circuit is not None and \
                self._input is not None and \
                self._ss is not None and \
                self._ss2 is not None \
                )
    
    def _parse_shares(self, msg_type, shares, expected_parties=None):
        """Reads shares received from other nodes.
        Expects that all messages are of @msg_type, containing serialized objects.
        @shares - a dict / list of length _n_parties holding current party->share/None mapping, that will be updated during the run.
        @expected_parties - a list of party ids of which inputs are to be received. If None - all parties needed.
        Returns True iff all expected shares received.
        """
        
        m = self._io.get_data_msg(msg_type)
        while m is not None:
            assert m.get_type() == msg_type, "Unexpected message received, expecting %d:\n%r" % (msg_type, m)
            data = m.get_msg()
            share = unserialize(data)
            src = m.get_src()
            if shares[src] is not None:
                log.warn("Src %d already sent a share...", src)
            shares[src] = share
            m = self._io.get_data_msg(msg_type)
        
        # Are we done?
        if expected_parties is None:
            expected_parties = xrange(self._n_parties)
        remaining = [p for p in expected_parties if (shares[p] is None)]
        return (remaining == [])
    
    def _eval_linear_gate(self, gate_name):
        """Evaluate a linear gate @gate_name"""
        self._circuit.evaluate_gate(gate_name)

    def _share(self, ss, secret, msg_type, *args, **kwargs):
        """Share @secret using the initialized SecretSharingScheme @ss.
        Then send each party a Message with their share, of type @msg_type.
        Additional positional/keyword arguments may be supplied for @ss.
        """
        log.debug("Sharing %r with msg_type %r", secret, msg_type)
        shares = ss.share(secret, *args, **kwargs)
        self._send_to_parties(msg_type, shares)
    
    def _send_to_parties(self, msg_type, msgs):
        """Sends a Message of type @msg_type to multiple parties.
        @msgs - n-long list of messages to send or a party->msg dictionary.
        """
        items = msgs.iteritems() if isinstance(msgs, dict) else enumerate(msgs)
        for party, data in items:
            self._send_to_party(party, msg_type, data)
    
    def _send_to_party(self, dst, msg_type, data):
        """Sends a Message of type @msg_type to party @dst with the payload @data"""
        assert 0 <= dst < self._n_parties, "Invalid party id %d for msg sending" % dst
        if not isinstance(data, str):
                data = serialize(data)
        m = Message(self._id, dst, msg_type, data)
        self._io.send(m)

    def _send_to_master(self, msg_type, data):
        """Build & send the Master a Message of type @msg_type and data (str) @data"""
        if not isinstance(data, str):
                data = serialize(data)
        m = Message(self._id, self.MASTER_ID, msg_type, data)
        self._io.send(m)
