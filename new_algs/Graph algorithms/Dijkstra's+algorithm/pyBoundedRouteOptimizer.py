#!/usr/bin/env python

"""
pyBoundedRouteOptimizer.py - a bounded route optimizer using Dijkstra's Algorithm in Python
Copyright (C) Yavor Stoychev 2015 <stoychev.yavor@gmail.com>
#
pyRouteOptimizer is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyBoundedRouteOptimizer is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
#
You should have received a copy of the GNU General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.

Input
#######################
The first line contains three space-seperated integers. The first integer represents K,
the number of transportation lines, and the second represents D,
 the position of the destination. The third number is the maximum number of layovers allowed. 3*K lines follow. The lines are to be interpreted
3 at a time, with each group of 3 lines containing the information for 
one transportation line. In each group of 3 lines, the first line contains a single
integer S indicating the number of stops the transporation line makes. The second 
line has S space-seperated integers, in strictly ascending order, indicating the 
coordinates (0 <= coordinate <= D) of the transporation line's stops. 0 and D 
(the origin and the destination) will always be present in the sequence. 
The third line has S-1 space-seperated integers, with the i-th of these integers 
indicating the cost of riding the transporation line from its i-th to its (i+1)-th stop.

Output
#######################
The program outputs the cost of the cheapest route from the source to the destination constrained by the maximum number of layovers allowed.
It assumes all costs are positive.

Input Format Example Follows
#######################
3 10 1
5
0 3 5 7 10
1 2 3 4
4
0 3 7 10
4 3 3
4
0 5 7 10
8 7 2
#######################
End of Input Format
"""

from sys import stdin, exit

def find_next(stops, costs, max_layovers):
    next_cost = None
    next_stop = None
    for (stop, trains) in costs.items():
        for (cost, layovers) in trains.values():
            if stop in stops and (next_cost == None or next_cost > cost) and layovers <= max_layovers:
                next_stop = stop
                next_cost = cost
    return next_stop

if __name__ == "__main__":
    try:
        (train_count, destination, max_layovers) = [int(train_entry) for train_entry in stdin.readline().split(" ")]
        route_costs = {}
        stops = set([0])
        adjacent_stops = {}
        costs = {0:{}} # stop_id => {last_train_id => (cost, hops)}
        for train in range(1, train_count + 1):
            stop_count = int(stdin.readline())
            train_stops = [int(stop_entry) for stop_entry in stdin.readline().split(" ")]
            if len(train_stops) != stop_count:
                raise AssertionError("Expected {} stops for train {} but got {}: {}" .format(stop_count, train, len(train_stops), train_stops))
            train_stop_costs = [int(stop_cost_entry) for stop_cost_entry in stdin.readline().split(" ")]
            if len(train_stop_costs) != stop_count - 1:
                raise AssertionError("Expected {} stop costs for train {} but got {}: {}" .format(stop_count - 1, train, len(train_stop_costs), train_stop_costs))


            if train_stops[0] != 0:
                raise ValueError("Expected first stop for train {} to be 0, but it was {}" .format(train, train_stops[0]))

            for index in range(1, len(train_stops) - 1):
                if train_stops[index] not in range(1, destination):
                    raise ValueError("Expected inner stops to be between [1, {}), but found stop {} for train {}" .format(destination, train_stops[index], train))

            if train_stops[-1] != destination:
                raise ValueError("Expected last stop for train {} to be {}, but it was {}" .format(train, destination, train_stops[-1]))

            costs[0][train] = (0, 0)
            stops.update(train_stops)

            for index in range(1, len(train_stops)):
                start_stop = train_stops[index - 1]
                end_stop = train_stops[index]

                if start_stop >= end_stop:
                    raise ValueError("Expected start stop ({}) in route segment to be < end stop ({}) for train {}" .format(start_stop, end_stop, train))

                if start_stop not in adjacent_stops:
                    adjacent_stops[start_stop] = set()
                adjacent_stops[start_stop].add(end_stop)
                
                route_key = (start_stop, end_stop)
                route_cost = train_stop_costs[index - 1]
                if route_key not in route_costs:
                    route_costs[route_key] = set()

                route_costs[route_key].add((route_cost, train))
            
        while 1:
            current_stop = find_next(stops, costs, max_layovers)

            if current_stop == None:
                raise AssertionError("No possible route was found between 0 and {} with a maxiumum of {} hops." .format(destination, max_layovers))

            stops.remove(current_stop)
            
            if current_stop == destination:
                break

            for adjacent_stop in adjacent_stops[current_stop]:
                if adjacent_stop in stops:
                    route_key = (current_stop, adjacent_stop)
                    if adjacent_stop not in costs:
                        costs[adjacent_stop] = {}
                    for (route_cost, route_train) in route_costs[route_key]:
                        for (train, (cost, layovers)) in costs[current_stop].items():
                            current_layovers = layovers + (0 if train == route_train else 1)
                            if (route_train not in costs[adjacent_stop] or costs[adjacent_stop][route_train][0] > cost + route_cost) and current_layovers <= max_layovers:
                                costs[adjacent_stop][route_train] = (cost + route_cost, current_layovers)

        min_cost = None
        for (train, (cost, hops)) in costs[destination].items():
            if min_cost == None or min_cost > cost:
                min_cost = cost
        

        print min_cost

    except KeyboardInterrupt:
        exit(0)
    except Exception, e:
        print str(e)
        exit(-1)
