from munkres import Munkres
import googlemaps
import csv
import sys


class Subject:
    """
    Stores the information of of workers and jobs as a class instance.
    For workers, subject_type = 'worker',
    for jobs, subject_type = 'job'.
    """

    def __init__(self, name, subject_type, location):
        self.name = name
        self.subject_type = subject_type
        self.location = location


def read_file(filename):
    """
    Reads a file containing information about workers and jobs,
    creates an instance of a Subject class for each worker and job,
    stores and returns all subjects in a list.
    """
    subjects = []

    # Reads and initialize a csv data file
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skips the header

        # Iterates through each line and create an instance of a subject class
        for line in csv_reader:

            # Initializes class attributes
            name = line[0]
            subject_type = line[1]
            location = line[2]

            # Creates an instance of the subject class and stores it in a list
            subject = Subject(name, subject_type, location)
            subjects.append(subject)

    return subjects


def calculate(gmaps, subjects):
    """
    Takes in a subjects list,
    perform the matching algorithm,
    then writes a csv file containing the matching information.
    """
    workers = []
    jobs = []
    matrix = []

    # Iterates through all the subjects and classify them as either a worker or a job
    for subject in subjects:
        if subject.subject_type == 'job':
            jobs.append(subject)
        else:
            workers.append(subject)

    # Create a cost matrix based on the travel duration between the workers and jobs
    for i in range(len(jobs)):
        matrix.append([])
        for j in range(len(workers)):
            distance = distance_calculator(gmaps, workers[j].location, jobs[i].location)
            matrix[i].append(distance)

    # Performs the Hungarian Algorithm for solving the assignment problem
    m = Munkres()
    indexes = m.compute(matrix)

    # Writes a csv file containing the matches
    with open('Assigned Jobs.csv', 'w', newline='') as new_file:

        # Initializes the csv file
        csv_writer = csv.writer(new_file, delimiter=',')
        csv_writer.writerow(['Worker', 'Job Assigned'])  # Header
        csv_writer.writerow('')

        # Iterates through the matches and write out their names in a single row
        for job, worker in indexes:
            csv_writer.writerow([workers[worker].name, jobs[job].name])


def distance_calculator(gmaps, location1, location2):
    """
    Given two location strings of addresses and a Google Maps Client,
    calculate and return the distance between them,
    in the form of driving time in seconds.
    """
    distance_matrix = gmaps.distance_matrix(location1, location2)
    distance = distance_matrix['rows'][0]['elements'][0]['duration']['value']  # JSON syntax
    return distance


def main():
    """
    Puts the entire program together,
    mains evaluates the console arguments,
    takes in filename of the original data and a Google Maps API Key, respectively,
    then outputs a csv file of the resulting matches.
    """
    # Takes in console arguments
    filename = sys.argv[1]
    key = sys.argv[2]
    
    # Initializes the googlemaps client
    gmaps = googlemaps.Client(key=key)

    # Performs the matching algorithm and outputs a csv file
    subjects = read_file(filename)
    calculate(gmaps, subjects)


# Python boilerplate
if __name__ == '__main__':
    main()

