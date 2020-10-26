# project5.py
# Eric Du
# edu1@stu.parkland.edu
# CSC 220, Spring 2016
# Parse eurail.txt and store in a graph, user interaction, output schematic

from TripPlanner import TripPlanner
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A European railway trip\
    planner.')
    
    parser.add_argument('timetable', help='EUrail timetable file.')
    parser.add_argument('--itinerary', dest='itinerary', 
                    help='Itinerary graph file.')
    args = parser.parse_args()
    
    trip = TripPlanner(args)
    trip.graph_eurail(args)