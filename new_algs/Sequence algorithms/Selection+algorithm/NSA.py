# -*- coding: utf-8 -*-


import random
import collections
import numpy.random as npr

class Teacher:
  def __init__(self,nr, name):
    self.nr = nr
    self.name = name # "Jaak Vilo"
#    self.suitable_slots = suitable_slots # [ [0,1],[2,1]  ]  Suitable monday 8 am and wednesday 10 am

class Room:
  def __init__(self,nr,capacity):
    self.nr = nr
    self.capacity = capacity # max number of students

class Event:
  #This is a thing that is actually happening. A timetable consists of events.
    def __init__(self, name,room, timeslot, teacher,typee,nr_of_students,curriculum):
        self.name = name # "Advanced algorithms"
        self.timeslot = timeslot # [x,y]  x =day [0,1,2,3] = Monday,Tuesday,Wednesday,...   y= slot = [0,1,2,3,4,5] = 8am,10am,
        self.room = room # randomly assined room class
        self.teacher = teacher # Teacher class
        self.typee = typee # lecture, practice
        self.nr_of_students = nr_of_students # number of students in the event 
        self.curriculum = curriculum #  "MASTERS_INFORMATICS_1" or "MASTERS_INFORMATICS_2" or ...
    def EventPrint(self):
        #Prints the event values
        print(str(self.name) + " " + str(self.room) + " " + str(self.timeslot) + " " + str(self.teacher) + " " + str(self.typee) + " " + str(self.nr_of_students) + " " + str(self.curriculum) )

#Generating random events

def room_generator(n=20):
    rooms = []
    for i in range(n):
      room = Room(i+1,random.choice([30, 30, 30, 30, 30, 60, 60, 60, 60, 60, 200, 200]))
      rooms.append(room)
    return rooms

def teacher_generator(n=25):
    names = ["Mysterio","Chameleon","Vulture","Green Goblin","Venom","Doctor Octopus","Sandman","Lizard","Electron","Scorpio", "Joker", "Riddler", "Batman", "Superman", "Ironman", "Arrow", "Flash", "Dr. Doom", "Mr. Fantastic", "Elastiknaine", "Catwoman", "Penguin", "Hulk", "Black Panther", "Thor", "Captain America", "Wolverine", "Magneto", "Phoneix", "Storm", "Beast"]
    print("Teacher listi pikkus on: " + str(len(names)))
    teachers = []
    #available_slots = [(day,time) for day in range(4) for time in range(5)]
    for i in range(n):
      teacher = Teacher(n,
                        random.choice(names))
                        #random.sample(available_slots,int(len(available_slots)*0.9)))
      teachers.append(teacher)
    return teachers

def find_curriculum(curriculums,subject):
  for key,value in curriculums.items():
    if subject in value:
      return key

def RandomEventsGenerator(n=80, rooms = [], teachers=[]):

    curriculums = {
        "MASTERS_INFORMATICS_1": ["Algorithmics","Design and Analysis of Algorithms","Distributed Systems","Machine Learning","Agile Software Development"],
        "MASTERS_INFORMATICS_2": ["Quantum Computing","Timetraveling","Natural Language Processing"],
        "BACHELOR_INFORMATICS_1": ["Object-oriented Programming","Programming Practicum","Transition to Advanced Mathematics","Computer Architecture and Hardware I","Calculus I","Discrete Mathematics I","Probability and Mathematical Statistics","Computer Programming"],
        "BACHELOR_INFORMATICS_2": ["Algorithms and Data Structures","Software Quality and Standards","Cooking","Systems Modelling"],
        "BACHELOR_INFORMATICS_3": ["Automata, Languages and Compilers","Databases","Advanced Programming","Bioinformatics","Computational Neuroscience"]
    }
    #This function is created for basic testing. Generates a totally random list of elements to test other functions.
    subjects = ["Algorithmics","Design and Analysis of Algorithms","Distributed Systems","Machine Learning","Quantum Computing","Timetraveling","Natural Language Processing",
                "Bioinformatics","Computational Neuroscience","Advanced Programming","Agile Software Development","Software Quality and Standards","Cooking","Systems Modelling",
                "Calculus I","Discrete Mathematics I","Probability and Mathematical Statistics","Transition to Advanced Mathematics","Computer Architecture and Hardware I",
                "Computer Programming","Databases","Algorithms and Data Structures","Automata, Languages and Compilers"," Object-oriented Programming","Programming Practicum"]
    #print("ainete arv: " + str(len(subjects)))              
    #rooms = room_generator()
    #teachers = teacher_generator()

    event_types = ["LECTURE","PRACTICE"]

    events = []
    for i in range(n):
        #Defining event variables
        subject = random.choice(subjects)
        curriculum = find_curriculum(curriculums,subject)
        room = random.choice(rooms)
        timeslot = (random.randint(0,4),random.randint(0,5))
        teacher = random.choice(teachers)
        event_type = random.choice(event_types)
        nr_of_students = room.capacity - 1
        #random.choice([29, 29, 29, 29, 29, 29, 29, 50, 50, 50, 190])

        #Generating a single event
        random_event = Event(subject,
                             room,
                             timeslot,
                             teacher,
                             event_type,
                             nr_of_students,
                             curriculum)
        events.append(random_event)
    return events





def feasibility(events):
  #are_events_not_overlapping()
  #are_room_capacity_constraints_met()
  #are_lectures_and_practises_not_concurrent()
  #are_mandatory_lectures_not_concurrent()
  #
  room_events = {}
  subject_events = {}
  curriculum_lectures = {}
  teacher_events = {}
  for e in events:
    if e.nr_of_students > e.room.capacity:
      return False
    else:
      current = room_events.get(e.room,[])
      current.append(e)
      room_events[e.room] = current
      current2 = subject_events.get(e.name,[])
      current2.append(e)
      subject_events[e.name] = current2
      current4 = teacher_events.get(e.teacher,[])
      current4.append(e)
      teacher_events[e.teacher] = current4
      if e.typee == "LECTURE":
        current3 = curriculum_lectures.get(e.curriculum,[])
        current3.append(e)
        curriculum_lectures[e.curriculum] = current3
      

  
  for room,event in room_events.items():
    if len(event) > 1:
      requested_timeslots = []
      for ev in event:
        if ev.timeslot in requested_timeslots:
          return False
        requested_timeslots.append(ev.timeslot)

  for subject, event in subject_events.items():
    if len(event) > 1:
        timeslot_events = {}
        
        for single_event in event:
           current = timeslot_events.get(single_event.timeslot,[]) 
           current.append(single_event)
           timeslot_events[single_event.timeslot] = current

        for time_slot, event_ in timeslot_events.items():
          if len(event_) > 1:
            event_types = [ee.typee for ee in event_]
            if "LECTURE" in event_types:
              return False

  for curriculum, event in curriculum_lectures.items():
    if len(event) > 1:
        timeslot_events = {}
        
        for single_event in event:
           current = timeslot_events.get(single_event.timeslot,[]) 
           current.append(single_event)
           timeslot_events[single_event.timeslot] = current

        for time_slot, event_ in timeslot_events.items():
          if len(event_) > 1:
            return False


  for teacher, event in teacher_events.items():
    if len(event) > 1:
      teacher_times = []
      for ev in event:
        if ev.timeslot in teacher_times:
          return False
        teacher_times.append(ev.timeslot)
  return True











#Checks that several events are not happening at the same time in the same room
def are_events_not_overlapping(events):
  room_events = {}
  for e in events:
    current = room_events.get(e.room,[])
    current.append(e)
    room_events[e.room] = current

  for room,event in room_events.items():
    if len(event) > 1:
      requested_timeslots = []
      for ev in event:
        if ev.timeslot in requested_timeslots:
          return False
        requested_timeslots.append(ev.timeslot)
  return True

# Check whether all rooms are large enough for any given event
def are_room_capacity_constraints_met(events):
  for e in events:
    if e.nr_of_students > e.room.capacity:
      return False
  return True

# Check whether a teacher is assigned to more than 1 event at a time and if their timeslots fit
def are_teachers_not_violating_the_laws_of_physics(events):
  teacher_events = {}
  for e in events:
    current = teacher_events.get(e.teacher,[])
    current.append(e)
    teacher_events[e.teacher] = current

  #Checking whether more than 1 event is happening at the same time for the same teacher
  for teacher, event in teacher_events.items():
    if len(event) > 1:
      teacher_times = []
      for ev in event:
        if ev.timeslot in teacher_times:
          return False
        teacher_times.append(ev.timeslot)

  #Checking whether events are happening at times that are not suitables for teachers
 # for teacher, event in teacher_events.items():
 #   if all(e.timeslot in teacher.suitable_slots  for e in event) == False:
 #     return False
  return True














#THIS IS MY ALTERNATIVE FOR THIS FUNCTION!
def are_teachers_not_violating_the_laws_of_physics2(events):
  teacher_events = {}
  for e in events:
    current = teacher_events.get(e.teacher,[])
    current.append(e)
    teacher_events[e.teacher] = current

  #Checking whether more than 1 event is happening at the same time for the same teacher
  for teacher, event in teacher_events.items():
    if len(event) > 1:
      teacher_times = []
      for ev in event:
        if ev.timeslot in teacher_times:
          return False
        teacher_times.append(ev.timeslot)

  #Checking whether events are happening at times that are not suitables for teachers
 # for teacher, event in teacher_events.items():
 #   if all(e.timeslot in teacher.suitable_slots  for e in event) == False:
 #     return False
  return True














#Checks that a lecture and practice in the same subject are not happening at the same time
def are_lectures_and_practises_not_concurrent(events):
  subject_events = {}
  for e in events:
    current = subject_events.get(e.name,[])
    current.append(e)
    subject_events[e.name] = current

  for subject, event in subject_events.items():
    if len(event) > 1:
        timeslot_events = {}
        
        for single_event in event:
           current = timeslot_events.get(single_event.timeslot,[]) 
           current.append(single_event)
           timeslot_events[single_event.timeslot] = current

        for time_slot, event_ in timeslot_events.items():
          if len(event_) > 1:
            event_types = [ee.typee for ee in event_]
            if "LECTURE" in event_types:
              return False
  return True

# Checks wheter lectures for mandatory subjects (e.g Algorithmics and Machine Learning) are not happening at the same time

def are_mandatory_lectures_not_concurrent(events):
  curriculum_lectures = {}
  for e in events:
    if e.typee == "LECTURE":
      current = curriculum_lectures.get(e.curriculum,[])
      current.append(e)
      curriculum_lectures[e.curriculum] = current

  for curriculum, event in curriculum_lectures.items():
    if len(event) > 1:
        timeslot_events = {}
        
        for single_event in event:
           current = timeslot_events.get(single_event.timeslot,[]) 
           current.append(single_event)
           timeslot_events[single_event.timeslot] = current

        for time_slot, event_ in timeslot_events.items():
          if len(event_) > 1:
            return False
  return True



# Fitness functions

# Decrease fitness for extremely early and extremely late occurrences, and increase for normal ones 
def punish_early_and_late_occurrences(events):
  fitness_update = 0
  for e in events:
    # if the event starts at 8.15 or 18.15 
    if e.timeslot[1] == 0 or e.timeslot[1] == 5:
      fitness_update -= 1
    else:
      fitness_update += 1
  return fitness_update

# Increase fitness if a lab session happens directly after the lecture (more convenient for students)
def reward_consecutive_lectures_and_labs(events):
  fitness_update = 0
  subject_events = {}
  for e in events:
    current = subject_events.get(e.name,[])
    current.append(e)
    subject_events[e.name] = current
  
  for subject, event in subject_events.items():
    if len(event) > 1:
      lect_times = []
      lab_times = []
      for e in event:
        if e.typee == 'LECTURE':
          lect_times.append(e.timeslot)
        if e.typee == 'LAB':
          lab_times.append(e.timeslot)
      for t in lect_times:
        if (t[0],t[1]+1) in lab_times: # if there is a lab on the same day and in the timeslot following the lecture
          fitness_update +=1
  return fitness_update

class Timetable:  
    def __init__(self, events):
        self.valid = False
        self.events = events
        self.fitness = 0
        
    def CalculateFitness(self):
        #This function calculates the fitness value of a timetable.
        #The Fitness calculation is based on the soft criteria.
        self.fitness = 0
        #Penalyse for every course at  0815 and 1815.
        time_punishment = punish_early_and_late_occurrences(self.events)
        self.fitness += time_punishment
        # Reward for every lab taking place immediately after the lecture
        lab_reward = reward_consecutive_lectures_and_labs(self.events)
        self.fitness += lab_reward
        return self.fitness
    
    def IsFeasible(self):
        #Tests if Timetable has no clashes (it matches all the hard constraints)
        if (are_events_not_overlapping(self.events) == True 
            and are_room_capacity_constraints_met(self.events) == True 
            and are_teachers_not_violating_the_laws_of_physics(self.events) == True 
            and are_lectures_and_practises_not_concurrent(self.events) == True
            and are_mandatory_lectures_not_concurrent(self.events) == True):
          self.valid = True
        else:
            self.valid = False
        return self.valid


    def equals(self,other):
      #Checks whether two timetables are equal
      if self.valid != other.valid:
        return False
      if self.fitness != other.valid:
        return False
      return collections.Counter(self.events) == collections.Counter(other.events)

        
    def PrintTable(self):
        #Prints the timetable
        tableoftimes = {}
        for i in range(5):
          for j in range(6):
            tableoftimes[(i,j)] = []
        for e in self.events:
            tableoftimes[e.timeslot].append([e.name, e.room.nr, e.teacher.name])
        return tableoftimes
    
    def Mutate(self):
      #Make a mutation to the timetable -> move an event.
        #select random event
        selected = random.choice(self.events)
        #move the selected event
        selected.room = random.choice(roomslist)
        return selected

#Chceks whether a timetable already exists in the set of timetables or if it's a new one (can be added to the set of potential timetables).
def is_timetable_already_in_set(Timetable_set,new_timetable):
    for current in Timetable_set:
      if current.equals(new_timetable):
        return True
    return False


# Initialization
#Create population of candidate detectors  (feasible timetables)
#for each timetable:
#randomly select event one by one
#assign event to random timeslot and room (satisfying all hard constraints)
#check if timetable already excists in population
#if new add to the inital population

#These things are fix for the problem.
rooms = room_generator()
teachers = teacher_generator()
timeslots = []
for i in range(5):
  for j in range(6):
    timeslots.append((i,j))


def create_population(size = 20):
  population = []
  i = 0
  while i < size:
    #60 - enam vähem normaalne arvutusaeg veel.
    potential_timetable = Timetable(RandomEventsGenerator(45, rooms, teachers))
    if potential_timetable.IsFeasible() == True:
    #if feasibility(potential_timetable.events) == True:
      population.append(potential_timetable)
      print("Populaion size: " + str(i))
      i = i + 1
  return population

def average_fitness_of_population(population):
  summa = 0
  n = len(population)
  for timetable in population:
    summa = summa + timetable.CalculateFitness()
  average = summa / n
  return average

def mutate_timetable(Timetable):
  #OMG see vist isegi töötab.
  random_event = random.choice(Timetable.events)
  Timetable.events.remove(random_event)
  Timetable.valid = False
  while Timetable.valid == False:
    random_event.room = random.choice(rooms)
    random_event.timeslot = random.choice(timeslots)
    Timetable.events.append(random_event)
    if Timetable.IsFeasible() == True:
      Timetable.valid = True
      return Timetable
    else:
      Timetable.events.remove(random_event)


def Negative_selection(population):
  print("FUnktsioon algab!")
  fitness_list = []
  population_avg = average_fitness_of_population(population)
  print("Esialgne keskmine fitness on: " + str(population_avg))
  j = 0
  newpopulation = []
  while j < len(population):
    population[j].fitness = population[j].CalculateFitness()
    if population[j].fitness < population_avg:
    #testpopulation.remove(testpopulation[j])
    #testpopulation = [timetable for timetable in testpopulation if timetable != timetable]
    #people = [person for person in people if person.name != 'Bob']
    #del testpopulation[i]
      j = j +1
    #testpopulation.remove(timetable)
    else:
      fitness_list.append(population[j].fitness)
      newpopulation.append(population[j])
      j = j+1

    print("allesjäänud populatsiooni suurus on: " + str(len(newpopulation)))
  i = 0
  while len(newpopulation) < 20:
  #print(len(newpopulation))
    for timetable in newpopulation:
      potential_new = mutate_timetable(timetable)

#    print(is_timetable_already_in_set(testpopulation, potential_new))
      if is_timetable_already_in_set(newpopulation, potential_new) == False:
      #i = i+1
      #print(i)
        newpopulation.append(potential_new)
        if len(newpopulation) == 20:
          break

  print("Final size of the new population: " + str(len(newpopulation)))
  print("Average fitness of new population: " + str(average_fitness_of_population(newpopulation)))
  print("Funktsioon done")
  return newpopulation


def selectOne(population):
    max = sum([c.fitness for c in population])
    selection_probs = [c.fitness/max for c in population]
    return population[npr.choice(len(population), p=selection_probs)]

def Negative_selection_wheel(population, population_size):
  print("FUnktsioon algab!")
  fitness_list = []
  population_avg = average_fitness_of_population(population)
  print("Esialgne keskmine fitness on: " + str(population_avg))
  j = 0
  newpopulation = []
  while j < len(population):
    population[j].fitness = population[j].CalculateFitness()
    if population[j].fitness < population_avg:
      j = j +1
    else:
      fitness_list.append(population[j].fitness)
      newpopulation.append(population[j])
      j = j+1
    wheel_probs = []
    for e in fitness_list:
      wheel_probs.append(e/sum(fitness_list))
  i = 0
  while len(newpopulation) < population_size:
    timetable = selectOne(newpopulation)
    potential_new = mutate_timetable(timetable)
    if is_timetable_already_in_set(newpopulation, potential_new) == False:
      if potential_new.CalculateFitness() > population_avg:
        newpopulation.append(potential_new)
        if len(newpopulation) == population_size:
          break
  print("Final size of the new population: " + str(len(newpopulation)))
  print("Average fitness of new population: " + str(average_fitness_of_population(newpopulation)))
  print("Funktsioon done")
  return newpopulation
  #Negative_selection_wheel(newpopulation, n-1)

population_size = 200
test_pop = create_population(population_size)
i = 0
for i in range(50):
  test_pop = Negative_selection_wheel(test_pop, population_size)

#print(Negative_selection_wheel(test_pop))
#print(Negative_selection_wheel(Negative_selection_wheel(Negative_selection_wheel(test_pop))))

#Negative_selection(Negative_selection(Negative_selection(Negative_selection(Negative_selection(Negative_selection(Negative_selection(Negative_selection(test_pop))))))))

#print(Negative_selection(create_population()))
#for timetable in population:
#  new_timetable = timetable.mutate()
#  if new_timetable not in population:
#    population.append(new_timetable)


#Population loop
#for each population of timetables

#Censoring (negative deletion)
# for each timetable in the population
# calculate fintess of the timetable
# calculate average fitness of the population
# for each timetable in the population 
# if fitness >= average then eliminate
# if fitnes valuesa are equal, eliminate only the second half

#Monitoring
# While number of timetables < population size
# randomly select timetables according to fitness using roulette wheel
# clone the detectors, mutation = faulre
# while mutation = failure, randomly select and event
# reassign event to random timeslot and best room
# if all hard constraints are satisfied and no identical detectors
# mutations = success
# calculate fintess of new clone
# if new clone fitness > average fitness of pop
# muration = failure
# eliminate the new clone, and reset the reassignment
# else add the new clone to the new population

#Cycle
#repeat population loop until a given convergence criterion is met
#Roulette Wheel selection method?!?

"""Negative selection algorithm.

1. Generate a population of timetables that match the hard criteria.
2. Mutate timetables of the inital population and add new mutants to the population.
3. Remove timetables which are not with good fitness from the population and mutate again.
4.
"""
