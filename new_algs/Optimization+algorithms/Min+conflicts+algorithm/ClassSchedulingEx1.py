#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Authors: Elizabeth Chan, Tessa Pham, Xinyi Wang
Description: Implements extension 1.
"""

"""
Structure:

1. Parsing the file
    - parseTXT() function parses the demo data file
        return students, preferences, classes, times, professorOfClass, classrooms, sizes
    - parseExcel() function to be added, to parse the excel data

This function incurs cheap costs.

2. Constructing the data:
    - construct(students, preferences, classes)
        return studentsInClass, overlap, classes

    After we load the data in by either parseTXT() or parseExcel(), we feed the
    data into this construct function. The construct function takes inputs:
        students, preferences, classes, classrooms, sizesOfClassrooms, times
    and outputs:
        studentsInClass, overlap, classes, availableRoomsInTime

    The complexity of this function is O(k log k)+ O(w), which is the complexity to
    process the data

3. Assigning classes to times:
    - assignClassToTime(c, availableRoomsInTime, professorsInTime, classesInTime, studentsInClass, professorOfClass, times, overlap, classes)
"""

import os
import pandas as pd
import xlrd
import copy
import csv
import datetime
import math
import numpy as np
import time

def parseTXT():
    students = []
    preferences = []
    classes = []
    times = []
    professorOfClass = []
    roomSize = {}

    # preferences
    DSP1 = open("basic/pref.txt", "r") 
    preferencesInfo = DSP1.read().replace("\t", " ").replace("\n", " ").split(" ")
 
    for i in range(1, int(preferencesInfo[1]) + 1):
       students.append(str(i))

    temp = []
    count = 0
    for i in range (2, len(preferencesInfo)):
        if (count % 5 != 0):
            temp.append(preferencesInfo[i])
        count = count + 1

    count2 = 0
    individualPref = []
    preferences.append([])
    for i in range (0, len(temp)):
        individualPref.append(temp[i])
        count2 = count2 + 1
        if (count2 == 4):
            preferences.append(individualPref)
            count2 = 0
            individualPref = []

    DSP1.close()

    DC = open("basic/constraints.txt", "r")
    splitDemoCon = DC.read().replace("\t", " ").replace("\n", " ").split(" ")

    # classes
    for i in range(0, len(splitDemoCon)):
        if splitDemoCon[i] == "Classes":
            for j in range(1, int(splitDemoCon[i + 1]) + 1): # range(1, 15)
                classes.append(j) # classes[0..13] will be stored as 1-14, same as students above

    # parse classrooms and roomSize
    i = 0    
    while splitDemoCon[i] != "Rooms":
        i += 1
    totalNumOfRooms = int(splitDemoCon[i + 1]) + 1
    count = 0
    while count < (totalNumOfRooms - 1):
        roomSize[splitDemoCon[i+2]] = int(splitDemoCon[i + 3])
        i += 2
        count += 1

    # times
    for i in range(0, int(splitDemoCon[2])):
        times.append(str(i))

    # professorOfClass
    professorOfClass = [0] # class 0 is not valid
    for i in range(0, len(splitDemoCon)):
        if splitDemoCon[i] == "Teachers":
            for j in range(i + 3, len(splitDemoCon), 2):
                professorOfClass.append(splitDemoCon[j])
    DC.close()
    ptemp = [[int(u) for u in x] for x in preferences]
    preferences = ptemp
    
    return roomSize, students, preferences, classes, times, professorOfClass

def is_nan(x):
    return (x is np.nan or x != x)

def parseHC():
    professorOfClass = []
    with open('haverford/haverfordEnrollmentDataS14.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        for row in readCSV:
            professorOfClass_ = row[11]
            professorOfClass.append(professorOfClass_)
     
        professorOfClass.pop(0)
        
        # populate arrays from haverfordConstraints.txt and haverfordConstraints_withZerios.txt 
        timeID = []
        for i in range(1,61):
            timeID.append(str(i))

        HCconstraints = open("haverford/haverfordConstraints.txt", "r")
        constraints = HCconstraints.read().replace("\t", " ").replace("\r", " ").replace("\n", " ").split(" ")

        constraints = list(filter(None, constraints))
        
        justTimes = []
        for i in range(4, 363):
            justTimes.append(constraints[i])

        startTime = []
        endTime = []
        daysOfWeek = []

        count = 0
        for i in range (len(justTimes)):
            if count % 6 == 0:
                startTime.append(justTimes[i]+""+justTimes[i+1])
            count = count + 1
        count = 0

        for i in range (2, len(justTimes)):
            if count % 6 == 0:
                endTime.append(justTimes[i]+""+justTimes[i+1])
            count = count + 1
        
        count = 0
        for i in range (4, len(justTimes)):
            if count % 6 == 0:
                daysOfWeek.append(justTimes[i])
            count = count + 1

        timeTuples = list(zip(timeID, startTime, endTime, daysOfWeek))

        f = open("haverford_times.txt","w+")
        for i in range(len(timeTuples)):
            f.write("{}\t{}\t{}\n".format(startTime[i], endTime[i], daysOfWeek[i]))

        for i in timeTuples: 
            f.write("{}\n".format(i))
        f.close()

        justRooms = []
        for i in range(365, 465):
            justRooms.append(constraints[i])

        classroomID_fromtxt = []
        classroomCap = []
        roomSize = {}
        count = 0 
        for i in range (len(justRooms)):
            if count % 2 == 0:
                classroomID_fromtxt.append(justRooms[i])
            count = count + 1; 

        count = 0
        for i in range (1, len(justRooms)):
            if count % 2 == 0:
                classroomCap.append(justRooms[i])
            count = count + 1; 

        roomSize = dict(zip(classroomID_fromtxt, classroomCap))

        f = open("haverford_roomSize.txt","w+")
        for i in roomSize:
            f.write("{}\t{}\n".format(i, roomSize[i]))
        f.close()

        HCconstraintsEnd = open("haverford/haverfordConstraints_withZeros.txt", "r")
        Endconstraints = HCconstraintsEnd.read().replace("\t", " ").replace("\r", " ").replace("\n", " ").split(" ")

        justClassesAndTeachers = []
        for i in range(564, len(Endconstraints)):
            justClassesAndTeachers.append(Endconstraints[i])

        classID = []
        teacherID = []
        classID_teacherID = {}
        count = 0 
        for i in range (len(justClassesAndTeachers)):
            if count % 2 == 0:
                classID.append(justClassesAndTeachers[i])
            count = count + 1; 

        count = 0
        for i in range (1, len(justClassesAndTeachers)):
            if count % 2 == 0:
                teacherID.append(justClassesAndTeachers[i])
            count = count + 1; 
        
        classID_teacherID = dict(zip(classID, teacherID))

        f = open("haverford_classID_teacherID.txt","w+")
        for i in classID_teacherID:
            f.write("{}\t{}\n".format(i, classID_teacherID[i]))
        f.close()

        HCconstraintsEnd.close()
        
        HCstudentprefs = open("haverford/haverfordStudentPrefs.txt", "r")
        studentprefs = HCstudentprefs.read().replace("\t", " ").replace("\r", " ").split('\n')

        studentprefs.pop(0)

        students = []
        for i in range(len(studentprefs)-1):
            temp = studentprefs[i].split(' ', 1)
            students.append(temp[0])

        preferences = []
        for i in range(len(students)):
            temp = studentprefs[i].split(' ', 1)
            individualPrefs = temp[1].split(" ")
            individualPrefs.pop(-1)
            preferences.append(individualPrefs)

        preferencesDict = dict(zip(students, preferences))

        f = open("haverford_studentPreferences.txt","w+")
        for i in students:
            f.write("{}\t{}\n".format(i, preferencesDict[i]))
        f.close()

        courseID = []
        subject = []
        classroomID = []

        with open('haverford/haverford-classroom-data.csv') as csvfile:
            readHC = csv.reader(csvfile, delimiter = ',')

            for row in readHC:
                courseID_ = row[0]
                subject_ = row[1]
                classroomID_ = row[2]

                courseID.append(courseID_)
                subject.append(subject_)
                classroomID.append(classroomID_)

            courseID.pop(0)
            subject.pop(0)
            classroomID.pop(0)
        
        classSubject = {}
        for x in range(len(courseID)):
            classSubject.update( {courseID[x] : subject[x]} )

        f = open("haverford_classSubject.txt","w+")
        for i in classSubject:
            f.write("{}\t{}\n".format(i, classSubject[i]))
        f.close()

        roomAndSubject = {}
        for x in range(len(subject)):
            roomAndSubject.update( { classroomID[x]: subject[x] } )

        sortedSubjectClassroom = {}
        for x in range(len(subject)):
            if subject[x] in sortedSubjectClassroom:
                if classroomID[x] not in sortedSubjectClassroom[subject[x]] and is_nan(classroomID[x]) == False:
                    if tuple((classroomID[x], roomSize[classroomID[x]])) not in sortedSubjectClassroom[subject[x]]: 
                        toAppend = tuple((classroomID[x], roomSize[classroomID[x]]))
                        sortedSubjectClassroom[subject[x]].append(toAppend)
            else:
                toAppend = tuple((classroomID[x], roomSize[classroomID[x]])) 
                sortedSubjectClassroom.update({subject[x] : [toAppend]})

        for k in sortedSubjectClassroom:
            sortedSubjectClassroom[k].sort(key=lambda tup: tup[1], reverse=True)

        f = open("haverford_sortedSubjectClassroom.txt","w+")
        for i in sortedSubjectClassroom:
            f.write("{}\t{}\n".format(i, sortedSubjectClassroom[i]))
        f.close()
        
        classLevel = {}
        with open('haverford/haverfordEnrollmentDataS14.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter = ',')
            for row in readCSV:
                level = row[4]
                classnum = row[1]
                classLevel[classnum] = level
                
        """
        Overview of all arrays created in this function.
        See .txt files with [college]_[name of data structure].txt for external version of parsed data.

        Following are from haverfordConstraints file:

            timeID = [] - list of times from 1-60
            startTime = [] - list of start times 
            endTime = [] - list of end times 
            daysOfWeek = [] - list of the days the times are scheduled for
            timeTuples = [] - a list of tuples of all this data meshed into one 

            classroomID_fromtxt = [] - list of room names specifically from haverfordConstraints file
            classroomCap = [] - list of room size capacity 
            roomSize = {} - dictionary of roomSizeName: classroomCap

        Following are parsed from other Haverford file (haverfordConstraints_withZeros) in which
        i filled in zeros for when there isn't a corresponding teacherID for a particular classID:

            classID = [] - list of classID 
            teacherID = [] - list of teacherID
            classID_teacherID = {} - dictionary of classID: corresponding teacherID 

        Following are parsed from haverfordStudentPrefs.txt:

            studentNumber = [] - list of student ID numbers
            student_pref = [] - list of student preferences 
            studentPreferences = {} - dictionary of student ID: corresponding list of classID preferences

        Following are parsed from haverford-classroom-data.csv:

            courseID = [] - list of IDs for each course
            subject = [] - list of subjects
            classroomID = [] = list of the IDs for each classroom 
            classSubject = {} - dictionary of courseID: subject

            roomAndSubject = {} - dictionary of classroomID: subject
            sortedSubjectClassroom = {} - dictionary of subject_: [list of tuples (classroomID, classroomCap) that are available for that key/subject]
                                        where the items in the second part of the tuple, meaning the classroomIDs
                                        are sorted in order of LARGEST-sized room to SMALLEST-sized room
        """

        return classLevel, professorOfClass, courseID, subject, classSubject, timeID, startTime, endTime, daysOfWeek, classroomID_fromtxt, classroomCap, roomSize, classID, teacherID, classID_teacherID, students, preferences, preferencesDict,sortedSubjectClassroom

def convertTimes(startTime, endTime):
    """Convert times to 24-hour format for comparision."""
    for i in range(0, len(startTime)):
        st = startTime[i]
        et = endTime[i]
        startTime[i] = datetime.datetime.strptime(st, '%I:%M%p').time()
        endTime[i] = datetime.datetime.strptime(et, '%I:%M%p').time()
    # startTime and endTime now contain time objects that can be compared to one another
    return startTime, endTime

def getOverlappingTimes(timeTuples):
    """
    Account for overlapping times.

    Parameters:
        timeTuples -- a list of 4-tuples (timeID, startTime, endTime, daysOfWeek)
    """
    # remove duplicate times
    timeIDs = [t[0] for t in timeTuples]
    MWF = [t for t in timeTuples if t[3] in ['M', 'W', 'F', 'MW', 'WF', 'MF', 'MWF']]
    TTH = [t for t in timeTuples if t[3] in ['T', 'TH', 'TTH']]
    # overlapsWithTime: {time: all times that overlap with this time}
    overlapsWithTime = {i: [] for i in timeIDs}

    # sort MWF and TR by start times
    MWF = sorted(MWF, key = lambda x: x[1])
    TTH = sorted(TTH, key = lambda x: x[1])

    for i in range(1, len(MWF) - 1):
        for j in range(i + 1, len(MWF)):
            # if start time of this slot is earlier than the finish time of the original slot => overlapping
            if MWF[j][1] < MWF[i][2]:
                overlapsWithTime[MWF[i][0]].append(MWF[j][0])
                overlapsWithTime[MWF[j][0]].append(MWF[i][0])
            else:
                break
    
    for i in range(1, len(TTH) - 1):
        for j in range(i + 1, len(TTH)):
            if TTH[j][1] < TTH[i][2]:
                overlapsWithTime[TTH[i][0]].append(TTH[j][0])
                overlapsWithTime[TTH[j][0]].append(TTH[i][0])
            else:
                break
    return overlapsWithTime

def construct(students, preferences, classes, roomSize, times, classSubject = None, relationMode = False):
    """
    Next level for constructing the inputs.

    Parameters:
        classes -- list of tuples (major, class #)
    """
    # studentsInClass: {class: list of students in that class}
    studentsInClass = {c: [] for c in classes}
    # overlap: a 2D matrix (row = all classes, column = all classes, entry at (i, j) = # of students taking both classes i and j)
    overlap = {(c1, c2): 0 for c1 in classes for c2 in classes}
    relation = None
    
    if relationMode:
        subjects = set(list(classSubject.values()))
        relation = {(s1, s2): 1 for s1 in subjects for s2 in subjects}

        for s, p in zip(students, preferences):
            for c in p:
                if c in list(classSubject.keys()):
                    for other_c in p[(p.index(c) + 1):]:
                        if other_c in list(classSubject.keys()):
                            # construct relation between 2 majors
                            relation[classSubject[c], classSubject[other_c]] += 1
                            relation[classSubject[other_c], classSubject[c]] += 1
    
    for s, p in zip(students, preferences):
            # for each class c in the preference list of student s
            for c in p:
                # add s to student list of class c
                # if c in list(classSubject.keys()):
                if c in classes:
                    if not studentsInClass[c]:
                        studentsInClass[c] = [s]
                    else:
                        studentsInClass[c].append(s)
                    # increment the overlaps of class c with each class in the rest of list p
                    for other_c in p[(p.index(c) + 1):]:
                        if other_c in classes:
                        # in overlap and any other arrays we construct, all classes are 1 less than their original numbers in the data
                            overlap[c, other_c] += 1
                            overlap[other_c, c] += 1

    # idea: we want to sort the array classes, but we have to get the size from len(studentsInClass.get(c)) for each c in classes
    sizes = [len(studentsInClass.get(c)) for c in classes]
    sortedClasses = [x for _, x in sorted(zip(sizes, classes))]
    classes = sortedClasses

    # sort the classroom from small to big, paired with their size
    sortedClassroom = [(k, roomSize[k]) for k in sorted(roomSize, key = roomSize.get, reverse = False)]
    
    # availableRoomsInTime: {time: list of tuples (room, size) sorted by size}
    availableRoomsInTime = {t: sortedClassroom for t in times}
    return studentsInClass, overlap, classes, availableRoomsInTime, relation
    
def assignClassToTime23(c, availableRoomsInTime, professorsInTime, classesInTime, studentsInClass, \
                        profOfCDict, times, overlap, classes, timeOfClass, roomSize, roomOfClass, \
                        classSubject, sortedSubjectClassroom, overlapsWithTime, relation, \
                        classLevel, classLevelTimeRecord, classLevelMode = False, \
                        overlapTimeMode = False, relationMode = False, subjectClassroomMode = False):
    min_overlap = float("inf")
    chosen_time = times[0]

    prof = profOfCDict[c]
    
    
    if (subjectClassroomMode):
        try:
            subject=classSubject[c]
        except KeyError:
            subjectClassroomMode=False
    
    for t in times:
        count=0
        # skip if the professor teaching class c is already teaching another class in this time
        if (len(professorsInTime[t]) != 0) & (prof in professorsInTime[t]):
            continue

        # skip if no more available rooms or if number of students in class c is greater 
        # than the size of the biggest available room in time t
        if (subjectClassroomMode):
            stop=False
            i=0
            lenClassroom=len(sortedSubjectClassroom[subject]) # want sorted from small to big
            while stop is False and i<lenClassroom:
                room=sortedSubjectClassroom[subject][i][0]
                if len(studentsInClass[c]) <= int(roomSize[room]):
                    if (room,roomSize[room]) in availableRoomsInTime[t]:
                        stop=True
                        tooSmall=False
                    else:
                        i += 1 # this room is taken, try next one
                else:
                    stop=True
                    tooSmall=True  # means that even the biggest subject-legit classroom isn't big enough               
            if i==lenClassroom or tooSmall==True:
                continue
            for assigned_c in classesInTime[t]:
                count += overlap[c,assigned_c]
    
            if count < min_overlap:
                min_overlap = count
                chosen_time = t
        #i == lenClassroom means all subject-eligible classrooms are taken at this time
        else:
            if (overlapTimeMode & relationMode):
                if c not in list(classSubject.keys()):
                    return
                for assigned_c in classesInTime[t]:
                    if assigned_c in list(classSubject.keys()):
                        count += overlap[c, assigned_c] * (relation[classSubject[c], classSubject[assigned_c]] / 100)
                
                # account for other classes in overlapping times
                if len(overlapsWithTime[t]) > 0:
                    for overlap_t in overlapsWithTime[t]:
                        for assigned_c in classesInTime[overlap_t]:
                            if assigned_c in list(classSubject.keys()):
                                count += overlap[c, assigned_c] * (relation[classSubject[c], classSubject[assigned_c]] / 100)
                if count < min_overlap:
                    min_overlap = count
                    chosen_time = t
            else:
                if len(availableRoomsInTime[t]) == 0:
                    continue
                if len(studentsInClass[c]) > int(availableRoomsInTime[t][-1][1]):
                    continue
                for assigned_c in classesInTime[t]:
                    count += overlap[c,assigned_c]        
                if count < min_overlap:
                    min_overlap = count
                    chosen_time = t

    # add class c to the chosen time
    classesInTime[chosen_time].append(c)
    # add the professor teaching class c to the list of professors occupied in the chosen time
    professorsInTime[chosen_time].append(prof)
    temp = copy.deepcopy(availableRoomsInTime[chosen_time])
    roomOfClass[c] = availableRoomsInTime[chosen_time].pop()[0]
    availableRoomsInTime[chosen_time] = copy.deepcopy(temp)
    timeOfClass[c] = chosen_time


def assignClassToTime1(c, availableRoomsInTime, professorsInTime, classesInTime, studentsInClass, \
                          profOfCDict, times, overlap, classes, timeOfClass, roomSize, roomOfClass, \
                          classSubject, sortedSubjectClassroom, overlapsWithTime, relation, \
                          classLevel, classLevelTimeRecord, classLevelMode = False, \
                          overlapTimeMode = False, relationMode = False, subjectClassroomMode = False):
    min_overlap = float("inf")
    chosen_time = times[0]

    prof = profOfCDict[c]
    
    
    if (subjectClassroomMode):
        try:
            subject=classSubject[c]
        except KeyError:
            subjectClassroomMode=False
    
    for t in times:
        count=0
        # skip if the professor teaching class c is already teaching another class in this time
        if (len(professorsInTime[t]) != 0) & (prof in professorsInTime[t]):
            continue
        if (classLevelMode):
            try:
                if classLevel[c] in classLevelTimeRecord[t,classSubject[c]]:
                    continue
            except KeyError:
                continue
                

        # skip if no more available rooms or if number of students in class c is greater 
        # than the size of the biggest available room in time t
        if (subjectClassroomMode):
            stop=False
            i=0
            lenClassroom=len(sortedSubjectClassroom[subject]) # want sorted from small to big
            while stop is False and i<lenClassroom:
                room = sortedSubjectClassroom[subject][i][0]
                if len(studentsInClass[c]) <= int(roomSize[room]):
                    if (room, roomSize[room]) in availableRoomsInTime[t]:
                        stop = True
                        tooSmall = False
                    else:
                        i += 1 # this room is taken, try next one
                else:
                    stop = True
                    tooSmall = True  # means that even the biggest subject-legit classroom isn't big enough               
            if i == lenClassroom or tooSmall == True:
                continue
            for assigned_c in classesInTime[t]:
                count += overlap[c,assigned_c]
    
            if count < min_overlap:
                min_overlap = count
                chosen_time = t
        # i == lenClassroom means all subject-eligible classrooms are taken at this time
        else:
            if (overlapTimeMode & relationMode):
                if c not in list(classSubject.keys()):
                    return
                for assigned_c in classesInTime[t]:
                    if assigned_c in list(classSubject.keys()):
                        count += overlap[c, assigned_c] * (relation[classSubject[c], classSubject[assigned_c]] / 100)
                
                # account for other classes in overlapping times
                if len(overlapsWithTime[t]) > 0:
                    for overlap_t in overlapsWithTime[t]:
                        for assigned_c in classesInTime[overlap_t]:
                            if assigned_c in list(classSubject.keys()):
                                count += overlap[c, assigned_c] * (relation[classSubject[c], classSubject[assigned_c]] / 100)
                if count < min_overlap:
                    min_overlap = count
                    chosen_time = t
            else:
                if len(availableRoomsInTime[t]) == 0:
                    continue
                if len(studentsInClass[c]) > int(availableRoomsInTime[t][-1][1]):
                    continue
                for assigned_c in classesInTime[t]:
                    count += overlap[c,assigned_c]        
                if count < min_overlap:
                    min_overlap = count
                    chosen_time = t
    
    # add class c to the chosen time
    classesInTime[chosen_time].append(c)
    # add the professor teaching class c to the list of professors occupied in the chosen time
    professorsInTime[chosen_time].append(prof)
    temp = copy.deepcopy(availableRoomsInTime[chosen_time])
    roomOfClass[c] = availableRoomsInTime[chosen_time].pop()[0]
    availableRoomsInTime[chosen_time] = copy.deepcopy(temp)
    timeOfClass[c] = chosen_time
    if (classLevelMode):
        try:
            classLevelTimeRecord[t,classSubject[c]].append(classLevel[c])
        except KeyError:
            pass
    
def calculateStudentsInClass(timeOfClass, classes, students, preferencesDict):
    """Calculate # of students in each class to analyze optimality."""
    studentsTakingClass = {}
    for c in classes:
        studentsTakingClass[c] = []
    for s in students:
        busyTime = []
        wishList = preferencesDict[s]
        for c in wishList:
            if c in classes:
                if timeOfClass[c] not in busyTime:
                    busyTime.append(timeOfClass[c])
                    studentsTakingClass[c].append(s)
            # else, just pass
    return studentsTakingClass
# need to change to a more complicated algorithm to maximize the overall optimality
# brute force: which class to prioritize to receive the largest # classes out of 4

def main():
    roomSize, students, preferences, classes, times, professorOfClass = parseTXT()
    studentsInClass, overlap, classes, availableRoomsInTime, relation = construct(students, preferences, classes, roomSize, times, classSubject = None, relationMode = False)

    # initialize two arrays to  store results
    # classesInTime: {time: list of classes in that time}
    classesInTime = {t: [] for t in times}
    # professorsInTime: {time: list of professors teaching a class in that time}
    professorsInTime = {t: [] for t in times}
    
    profOfCDict = {}
    for c in classes:
        profOfCDict[c] = professorOfClass[int(c)]

    # reorganize outputs
    roomOfClass = {} # courseID: roomID
    timeOfClass = {} # courseID: timeID
    
    preferencesDict = {}
    for s in students:
        preferencesDict[s] = preferences[int(s)]
    for c in classes:
        assignClassToTime23(c, availableRoomsInTime, professorsInTime, classesInTime, studentsInClass, \
                            profOfCDict, times, overlap, classes, timeOfClass, roomSize, roomOfClass, \
                            classSubject=None, sortedSubjectClassroom=None, overlapsWithTime=None, relation=None, \
                            classLevel=None, classLevelTimeRecord=None)
    
    # calculate optimality
    studentsTakingClass = calculateStudentsInClass(timeOfClass, classes, students, preferencesDict)

    f = open("schedule.txt", "w+")
    f.write("Course" + '\t' + "Room" + '\t' + "Teacher" + '\t' + "Time" + '\t' + "Students" + '\n')
    for i in range(len(classes)):
        c = classes[i]
        f.write(str(c) + '\t' + str(roomOfClass[c]) + '\t' + professorOfClass[c] + '\t' + timeOfClass[c] + '\t' + ' '.join(studentsTakingClass[c]) + '\n')
    
    total = 0
    for key in studentsTakingClass:
        total += len(studentsTakingClass[key])
    opt = total / (len(students) * 4)
    print(opt)


def mainHC(classLevelMode=False, overlapTimeMode = False, relationMode = False, subjectClassroomMode=False):
    """Use parseHC() to get a list of mutually exclusive time slots."""
    classLevel, professorOfClass, courseID, subject, classSubject, times, startTime, endTime, daysOfWeek, classroomID_fromtxt, classroomCap, roomSize, classID, teacherID, classID_teacherID, students, preferences, preferencesDict,sortedSubjectClassroom = parseHC()
    timeTuples = list(zip(times, startTime, endTime, daysOfWeek))
    overlapsWithTime = getOverlappingTimes(timeTuples)
    studentsInClass, overlap, classes, availableRoomsInTime, relation = construct(students, preferences, classID, roomSize, times, classSubject, relationMode = relationMode)
    
    # initialize two arrays to store results
    # classesInTime: {time: list of classes in that time}
    classesInTime = {t: [] for t in times}
    # professorsInTime: {time: list of professors teaching a class in that time}
    professorsInTime = {t: [] for t in times}
    
    profOfCDict = {}
    for c in classes:
        profOfCDict[c] = professorOfClass[int(c)]

    # reorganize outputs
    roomOfClass = {} # courseID: roomID
    timeOfClass = {} # courseID: timeID
    classLevelTimeRecord={(t,s):[] for t in times for s in subject}
    
    print("classLevelMode == True")
    for c in classes:
        assignClassToTime1(c, availableRoomsInTime, professorsInTime, classesInTime, studentsInClass, \
                            profOfCDict, times, overlap, classes, timeOfClass, roomSize, roomOfClass, \
                            classSubject, sortedSubjectClassroom, overlapsWithTime, relation, \
                            classLevel, classLevelTimeRecord, classLevelMode = True, \
                            overlapTimeMode = False, relationMode = False, subjectClassroomMode = False)

    # calculate optimalty
    studentsTakingClass = calculateStudentsInClass(timeOfClass, classes, students, preferencesDict)

    f = open("schedule.txt", "w+")
    f.write("Course" + '\t' + "Room" + '\t' + "Teacher" + '\t' + "Time" + '\t' + "Students" + '\n')

    for c in classes:
        f.write(str(c) + '\t' + str(roomOfClass[c]) + '\t' + profOfCDict[c] + '\t' + timeOfClass[c] + '\t' + ' '.join(studentsTakingClass[c]) + '\n')  
    
    total = 0
    for key in studentsTakingClass:
        total += len(studentsTakingClass[key])
    opt = total / (len(students) * 4)
    print("The optimality is ", opt)
