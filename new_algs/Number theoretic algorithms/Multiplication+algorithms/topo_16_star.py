# Wesley Layton Ellington
# Fault Tolerant Computing
# Fall 2019
# Term Project: ABFT Multiplication 

# Definition of star topology for Mininet simulation

from mininet.topo import Topo

class center_star( Topo ):

    def __init__( self ):

        # Initialize topology
        Topo.__init__( self )

            # Add hosts and switches
        host_00 = self.addHost( 'h00' )
        host_01 = self.addHost( 'h01' )
        host_02 = self.addHost( 'h02' )
        host_03 = self.addHost( 'h03' )
        host_04 = self.addHost( 'h04' )
        host_05 = self.addHost( 'h05' )
        host_06 = self.addHost( 'h06' )
        host_07 = self.addHost( 'h07' )
        host_08 = self.addHost( 'h08' )
        host_09 = self.addHost( 'h09' )
        host_10 = self.addHost( 'h10' )
        host_11 = self.addHost( 'h11' )
        host_12 = self.addHost( 'h12' )
        host_13 = self.addHost( 'h13' )
        host_14 = self.addHost( 'h14' )
        host_15 = self.addHost( 'h15' )
        host_16 = self.addHost( 'h16' )
        switch_0 = self.addSwitch( 's0')

        # Add links
        self.addLink(switch_0, host_00)

        self.addLink(switch_0, host_01)
        self.addLink(switch_0, host_02)
        self.addLink(switch_0, host_03)
        self.addLink(switch_0, host_04)

        self.addLink(switch_0, host_05)
        self.addLink(switch_0, host_06)
        self.addLink(switch_0, host_07)
        self.addLink(switch_0, host_08)

        self.addLink(switch_0, host_09)
        self.addLink(switch_0, host_10)
        self.addLink(switch_0, host_11)
        self.addLink(switch_0, host_12)

        self.addLink(switch_0, host_13)
        self.addLink(switch_0, host_14)
        self.addLink(switch_0, host_15)
        self.addLink(switch_0, host_16)

topos = { 'center_star': ( lambda: center_star() ) }

