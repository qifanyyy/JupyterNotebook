#!/usr/bin/python -u
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import Ice
Ice.loadSlice('-I {} container.ice'.format(Ice.getSliceDir()))
import Services


class ContainerI(Services.Container):
    def __init__(self):
        self.proxies = {}

    def link(self, key, proxy, current=None):
        if key in self.proxies:
            raise Services.AlreadyExists(key)

        self.proxies[key] = proxy
        
        print "{} ha sido agregado".format(key)

    def unlink(self, key, current=None):
        if not key in self.proxies:
            raise Services.NoSuchKey(key)
		
        del self.proxies[key]
        
        print "{} ha sido eliminado".format(key)

    def list(self, current=None):
        return self.proxies


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ContainerI()

        adapter = broker.createObjectAdapter('ContainerAdapter')
        proxy = adapter.add(servant, broker.stringToIdentity("container"))

        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
