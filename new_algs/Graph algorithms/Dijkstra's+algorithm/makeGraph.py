#!/usr/bin/python

# Convert an OSM file into a D3 Graph JSON file, to demonstrate Dijkstra's algorithm in the browser
# Usage: makeGraph.py file.osm.{xml, pbf} graph.json

# Copyright (C) 2014 Matthew Wigginton Conway.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from imposm.parser import OSMParser
from sys import argv
from pyproj import Proj, transform
from collections import defaultdict
import json

# define an OSM parser
class GraphBuilder(object):
    def __init__(self):
        # Track all loaded nodes, with x, y, etc.
        self.nodes = {}

        # track edge counts for nodes
        # we use a separate dict so that ways and nodes don't have to load in order
        self.node_refs = defaultdict(lambda: 0)

        # a list of the node IDs in each relevant way
        self.ways = []

        # tuples (from, to, distance)
        self.edges = []

        # Projection information
        # State Plane California Zone 5 meters
        self.statePlane = Proj(init='epsg:26945')
        self.wgs84 = Proj(init='epsg:4326')

    # use a coords callback because we want all intersections even if there are no tags
    def coords_callback(self, coords):
        for osmid, lon, lat in coords:
            # project to State Plane Zone 5, meters
            x, y = transform(self.wgs84, self.statePlane, lon, lat)
            self.nodes[osmid] = dict(osmid=osmid, x=x, y=y, ways=0, names=set())

    def ways_callback(self, ways):
        for osmid, tags, nodes in ways:
            if 'highway' in tags and tags['highway'] not in ['motorway', 'motorway_link']:
                self.ways.append(nodes)

                if 'ref' in tags:
                    name = tags['ref']
                elif 'name' in tags:
                    name = tags['name']
                else:
                    name = tags['highway']

                for node in nodes:
                    self.node_refs[node] += 1
                    self.nodes[node]['names'].add(name)

                # give the end nodes an extra 'fake' edge so that they are included for sure
                # even if they only have one edge we still want to include them
                self.node_refs[nodes[0]] += 1
                self.node_refs[nodes[-1]] += 1

    # remove nodes that don't have more than one way
    def filter_nodes(self):
        self.filtered_nodes = {k: v for k, v in self.nodes.iteritems() if self.node_refs[k] > 1}

    # give nodes names based on their ways
    def name_nodes(self):
        for node in self.filtered_nodes.values():
            node['name'] = ' and '.join(node['names'])
            del node['names']

    # Make edges and set the distances
    def make_edges(self):
        for way in self.ways:
            edge = None
            previous_node = None

            for nodeRef in way:
                node = self.nodes[nodeRef]

                if edge is not None and previous_node is not None:
                    # distance: pythagorean theorem
                    # coordinates are projected so we can use Euclidean math
                    edge[2] += pow(pow(node['x'] - previous_node['x'], 2) + pow(node['y'] - previous_node['y'], 2), .5)

                previous_node = node

                if nodeRef in self.filtered_nodes:
                    # this is a node that will end up in the final graph

                    if edge is not None:
                        edge[1] = nodeRef
                        self.edges.append(edge)

                    edge = [nodeRef, None, 0]

    # Write the graph as JSON to the writeable file specified
    def write_json(self, outfile):
        # Map from osm node IDs to 0-based integers
        nodeIndices = {}

        data = {'nodes': [], 'edges': []}

        idx = 0

        # create the nodes
        for nodeRef, node in self.filtered_nodes.iteritems():
            nodeIndices[nodeRef] = idx
            idx += 1

            node = {k: v for k, v in node.iteritems() if k in ['name', 'x', 'y']}

            data['nodes'].append(node)

        # create the edges
        for edge in self.edges:
            edge = {'from': nodeIndices[edge[0]], 'to': nodeIndices[edge[1]], 'length': edge[2]}
            data['edges'].append(edge)

        json.dump(data, outfile)

    def parse(self, filename):
        parser = OSMParser(concurrency=4, coords_callback=self.coords_callback, ways_callback=self.ways_callback)
        parser.parse(filename)

if __name__ == '__main__':
    builder = GraphBuilder()

    print 'reading osm'
    builder.parse(argv[1])

    print 'filtering nodes'
    builder.filter_nodes()

    print 'naming nodes'
    builder.name_nodes()

    print 'making edges'
    builder.make_edges()

    print 'writing json'
    otf = open(argv[2], 'w')
    builder.write_json(otf)
    otf.close()
