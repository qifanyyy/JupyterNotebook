#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 21:17:46 2018

@author: Elizabeth Chan, Tessa Pham, Xinyi Wang

"""

"""
Structure:

1. Parsing the file

    - parseTXT() function parses the demo data file
        return students, preferences, classes, times, professorOfClass, classrooms, sizes
    - parseExcel() function to be added, to parse the excel data

This function incurs cheap costs.

2. Constructing the data

    - construct(students, preferences, classes)
        return studentsInClass, overlap, classes

    After we load the data in by either parseTXT() or parseExcel(), we feed the
    data into this construct function. The construct function takes inputs:
        students, preferences, classes, classrooms, sizesOfClassrooms, times
    and outputs:
        studentsInClass, overlap, classes, availableRoomsInTime

    The complexity of this function is O(k log k)+ O(w), which is the complexity to
    process the data

3. Assign the Classes to times
    assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,professorOfClass,times,overlap,classes)


"""



# parsing excel
import os
import pandas as pd
import xlrd
import copy
import csv
import datetime
import math
import numpy as np

# parsing for demo data
def parseTXT():
    '''
Parses the constraints.txt and pref.txt, return roomSize, students, preferences, classes, times, professorOfClass.
Outputs look like:
    
students, ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
classes, [6, 5, 4, 8, 1, 7, 3, 2]
preferences [[], [7, 4, 2, 8], [2, 3, 4, 1], [4, 6, 5, 3], [3, 1, 7, 2], [5, 1, 3, 4], [7, 8, 2, 3], [5, 1, 2, 8], [2, 6, 8, 7], [2, 1, 3, 7], [3, 6, 4, 2]]
times ['0', '1', '2', '3']
roomSize {'1': 876, '2': 815, '3': 232, '4': 101}
professorOfClass [0, '4', '4', '2', '1', '1', '3', '3', '2']

    '''
    students = []
    preferences = []
    classes = []
    times = []
    professorOfClass = []
    roomSize={}



    # preferences
    DSP1 = open("basic/pref.txt", "r") # opens file with name of "test.txt"
    preferencesInfo = DSP1.read().replace("\t", " ").replace("\n", " ").split(" ")
 
    for i in range(1, int(preferencesInfo[1]) + 1):
       students.append(str(i))

    temp = []
    count = 0
    for i in range (2, len(preferencesInfo)):
        if (count % 5  != 0):
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
            # for j in range(0, int(splitDemoCon[i + 1])):
            for j in range(1, int(splitDemoCon[i + 1]) + 1): # range(1, 15)
                classes.append(j) # classes[0..13] will store 1 - 14, same as students above!

    #rooms
    i=0    
    while splitDemoCon[i]!="Rooms":
        i+=1
    total_number_of_Rooms=int(splitDemoCon[i + 1]) + 1
    count=0
    while count<total_number_of_Rooms-1:
        roomSize[splitDemoCon[i+2]]=int(splitDemoCon[i+3])
        i+=2
        count+=1

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
    ptemp=[[int(u) for u in x] for x in preferences]
    preferences=ptemp
#parse classrooms and sizesOfClassrooms
    

    return roomSize, students, preferences, classes, times, professorOfClass

def parseBMC():

    BMCexcel = pd.read_excel('brynmawr/bmc-data-f17.xls')

    # times = [] has been replaced with following three lists 
    daysOfWeek = BMCexcel["Days 1"]
    startTime = BMCexcel["Srt1 AM/PM"]
    endTime = BMCexcel["End 1 AMPM"]

    classes = BMCexcel["Class Nbr"]

    professorOfClass = BMCexcel["Name"]

    # no list of students for students = []
    # instead use this array that is the number of student capacity 
    studentCap = BMCexcel["Class Cap"]


#    print("\n\ndaysOfWeek \n {}".format(daysOfWeek))
#    print("\n\nstartTime \n {}".format(startTime))
#    print("\n\nendTime \n {}".format(endTime))
#    print("\n\nclasses \n {}".format(classes))
#    print("\n\nprofessorOfClass \n {}".format(professorOfClass))

    f = open("brynmawr_date.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in daysOfWeek:
        f.write("{}\n".format(i))
    f.close()


    f = open("brynmawr_startTime.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in startTime:
        f.write("{}\n".format(i))
    f.close()


    f = open("brynmawr_endTime.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in endTime:
        f.write("{}\n".format(i))
    f.close()

    allTime = zip(daysOfWeek, startTime, endTime)
    f = open("brynmawr_allTimes.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in allTime:
        f.write("{}\n".format(i))
    f.close()
    print(classes)
    
    
    return daysOfWeek, startTime, endTime, classes, professorOfClass

    # data not availble from excel file
    # preferences = [] 




# The next level for constructing the inputs.
def construct(students, preferences, classes, roomSize, times):
    # studentsInClass: a dictionary (key = class, value = list of students in that class)
    studentsInClass = {c: [] for c in range(0, 15)}
    studentsInClass.get(0).append(0)
    # overlap: a 2D matrix (row = all classes, column = all classes, entry at (i, j) = # of students taking both classes i and j)
    overlap = [[0 for c in range(0,15)] for c in range(0, 15)]
    for s, p in zip(students, preferences):
        # for each class c in the preference list of student s
        for c in p:
            # add s to student list of class c
            if studentsInClass[c]==None:
                studentsInClass[c]=[s]
            else:
                studentsInClass[c].append(s)
            # increment the overlaps of class c with each class in the rest of list p
            for other_c in p[(p.index(c) + 1):]:
                # in overlap and any other arrays we construct, all classes are 1 less than their original numbers in the data
                overlap[c][other_c] += 1
                overlap[other_c][c] += 1
    # the idea is: we want to sort the array classes, but we have to get the size from len(studentsInClass.get(c)) for each c in classes
    sizes = [len(studentsInClass.get(c)) for c in classes]
    sortedClasses = [x for _, x in sorted(zip(sizes, classes))]
    classes = sortedClasses

#sort the classroom from small to big, and pair with their size.
#    sortedClassroom=[(y, x) for x, y in sorted(zip(sizesOfClassrooms, classrooms))]
    
    sortedClassroom=[(k, roomSize[k]) for k in sorted(roomSize, key=roomSize.get, reverse=False)]
    
    # availableRoomsInTime: a dictionary (key = time, value = list of tuples (room, size), ranked from smallest to largest)
    availableRoomsInTime = {t: sortedClassroom for t in times}
    return studentsInClass, overlap, classes, availableRoomsInTime


def assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,profOfCDict,times,overlap,classes,timeOfClass,classroomOfClass,subjectClassroomMode=False, sortedSubjectClassroom=None, roomSize=None, classSubject=None):
    min_overlap = float("inf")
    chosen_time = times[0]

    prof = profOfCDict[c]

    for t in times:
        # skip if the professor teaching class c is already teaching another class in this time
        if (len(professorsInTime[t]) != 0) & (prof in professorsInTime[t]):
            continue

# skip if no more available rooms or if number of students in class c is greater 
# than the size of the biggest available room in time t
        if (subjectClassroomMode):
            subject=classSubject[c]
            stop=False
            i=0
            lenClassroom=len(sortedSubjectClassroom[subject]) #so you want it small to big
            while stop is False and i<lenClassroom:
                room=sortedSubjectClassroom[subject][i]
                if len(studentsInClass[c]) <= roomSize[room]:
                    if (room,roomSize[room]) in availableRoomsInTime[t]:
                        stop=True
                        tooSmall=False
                    else:
                        i+=1 #this room is taken, try next one
                else:
                    stop=True
                    tooSmall=True  #it means that even the biggest subject-legit classroom's not big enough               
            if i==lenClassroom or tooSmall==True:
                continue
#i==lenClassroom means that all subject-eligible classrooms are taken at this time
        else: # not in subjectClassroomMode, handle things normally
            if len(availableRoomsInTime[t]) == 0:
                continue
            if len(studentsInClass[c]) > availableRoomsInTime[t][-1][1]:
                continue

        count = 0

        for assigned_c in classesInTime[t]:
            count += overlap[c][assigned_c]

        if count < min_overlap:
            min_overlap = count
            chosen_time = t
    # add class c to the chosen time
    classesInTime[chosen_time].append(c)
    # add the professor teaching class c to the list of professors occupied in the chosen time
    professorsInTime[chosen_time].append(prof)
    timeOfClass[c]=chosen_time
    temp=copy.deepcopy(availableRoomsInTime[chosen_time])
    classroomOfClass[c]=temp.pop()[0]
    # classroomOfClass[c] = availableRoomsInTime[chosen_time].pop()[0]
    availableRoomsInTime[chosen_time]=copy.deepcopy(temp)
    


#this function is for optimality analysis
def calculate_student_in_class(timeOfClass,classes, students,preferencesDict):
    studentsTakingClass={}
    for c in classes:
        studentsTakingClass[c]=[]
    for s in students:
        busyTime=[]
        wishList=preferencesDict[s]
        for i in range(0,4):
            if timeOfClass[wishList[i]] not in busyTime:
                busyTime.append(timeOfClass[wishList[i]])
                studentsTakingClass[wishList[i]].append(s)
            #else, just pass.
    return studentsTakingClass
#need to change to a more complicated algorithm to maximize the overal optimality
# brute force: which class to prioritize to receive the largest # classes out of 4.



def main():
    roomSize, students, preferences, classes, times, professorOfClass = parseTXT()
    studentsInClass, overlap, classes, availableRoomsInTime = construct(students, preferences, classes,roomSize,times)

#Now, initialize two arrays to store the results.
    # classesInTime: a dictionary (key = time, value = list of classes in that time)
    classesInTime = {t: [] for t in times}
    # professorsInTime: a dictionary (key = time, value = list of professors teaching a class in that time)
    professorsInTime = {t: [] for t in times}

    profOfCDict={}
    for c in classes:
        profOfCDict[c]=professorOfClass[int(c)]
        
#below are some reorganization for the outputs
    classroomOfClass={} #courseID: roomID
    timeOfClass={} #courseID: timeID
    for c in classes:
        assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,profOfCDict,times,overlap,classes,timeOfClass,classroomOfClass,subjectClassroomMode=False, sortedSubjectClassroom=None, roomSize=None, classSubject=None)

    preferencesDict={}
    for s in students:
        preferencesDict[s]=preferences[int(s)]

#Now calculate optimality

    studentsTakingClass=calculate_student_in_class(timeOfClass,classes, students,preferencesDict)

    f=open("schedule.txt","w+")
    f.write("Course"+'\t'+"Room"+'\t'+"Teacher"+'\t'+"Time"+'\t'+"Students"+'\n')
    for i in range(len(classes)):
        c=classes[i]
        f.write(str(c)+'\t'+str(classroomOfClass[c])+'\t'+profOfCDict[c]+'\t'+timeOfClass[c]+'\t'+' '.join(studentsTakingClass[c])+'\n')   
    with open("schedule.txt") as f:
        print(f.read())
    
    total=0
    for key in studentsTakingClass:
        total+=len(studentsTakingClass[key])
    opt=total/(len(students)*4)
    print(opt)
"""
# to test bmc data
def mainBMC():
  
 
 
 
 
 <FILL IN ALL DATA NEEDED FROM PARSEBMC() OR SOMETHING LIKE THAT>
    
 
 
 
 
 
#Now, initialize two arrays to store the results.
    # classesInTime: a dictionary (key = time, value = list of classes in that time)
    classesInTime = {t: [] for t in times}
    # professorsInTime: a dictionary (key = time, value = list of professors teaching a class in that time)
    professorsInTime = {t: [] for t in times}

    profOfCDict={}
    for c in classes:
        profOfCDict[c]=professorOfClass[int(c)]
        
#below are some reorganization for the outputs
    classroomOfClass={} #courseID: roomID
    timeOfClass={} #courseID: timeID
    for c in classes:
        assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,profOfCDict,times,overlap,classes,timeOfClass,classroomOfClass,subjectClassroomMode=True, sortedSubjectClassroom, roomSize, classSubject)

    preferencesDict={}
    for s in students:
        preferencesDict[s]=preferences[int(s)]

#Now calculate optimality

    studentsTakingClass=calculate_student_in_class(timeOfClass,classes, students,preferencesDict)

    f=open("schedule.txt","w+")
    f.write("Course"+'\t'+"Room"+'\t'+"Teacher"+'\t'+"Time"+'\t'+"Students"+'\n')
    for i in range(len(classes)):
        c=classes[i]
        f.write(str(c)+'\t'+str(classroomOfClass[c])+'\t'+profOfCDict[c]+'\t'+timeOfClass[c]+'\t'+' '.join(studentsTakingClass[c])+'\n')   
    with open("schedule.txt") as f:
        print(f.read())
    
    total=0
    for key in studentsTakingClass:
        total+=len(studentsTakingClass[key])
    opt=total/(len(students)*4)
    print(opt)
                
    """
    

"""
    print('\n')
    print('\n')
    print("Below are what's returned by parseTXT: "+'\n')
    print("students,", students)
    print("classes,", classes)
    print("preferences", preferences)
    print("times",times)
    print("roomSize",roomSize)
    print("professorOfClass",professorOfClass)
    
    print('\n'+"OtherThings"+'\n')
    
    print("classroomOfClass",classroomOfClass)
    print("profOfCDict",profOfCDict) #{7: '7', 10: '3'}
    print("timeOfClass",timeOfClass)
    print("studentsTakingClass",studentsTakingClass)
    print(students, '\n','\n', preferences,'\n','\n',classes,'\n','\n',times,'\n','\n',professorOfClass)

"""

def parseHC():
    # HCexcel = pandas.read_excel('haverford/haverfordEnrollmentDataS14.csv')

    with open('haverford/haverfordEnrollmentDataS14.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')

        professorOfClass = []
        courseID = []
        subject = []
        for row in readCSV:
            professorOfClass_ = row[11]
            courseID_ = row[1]
            subject_ = row[2]

            professorOfClass.append(professorOfClass_)
            courseID.append(courseID_)
            subject.append(subject_)   
        
        professorOfClass.pop(0)
        courseID.pop(0)
        subject.pop(0)


        dictClasses = {}
        for x in range(len(courseID)):
            dictClasses.update({courseID[x] : subject[x]})

        f = open("haverford_dictClasses.txt","w+")
        # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
        for i in dictClasses:
            f.write("{}\t{}\n".format(i, dictClasses[i]))
        f.close()

        # populating arrays from haverfordConstraints.txt file and haverfordConstraints_withZerios.txt file 

        timeID = []
        for i in range(1,61):
            timeID.append(str(i))
        # print timeID

        HCconstraints = open("haverford/haverfordConstraints.txt", "r")
        constraints = HCconstraints.read().replace("\t", " ").replace("\r", " ").replace("\n", " ").split(" ")

        constraints = list(filter(None, constraints))
        
        justTimes = []
        for i in range(4, 363):
            justTimes.append(constraints[i])
        # print justTimes

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

        timeTupes = list(zip(timeID, startTime, endTime, daysOfWeek))
        # print timeTupes

        f = open("haverford_times.txt","w+")
        # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
        for i in range(len(timeTupes)):
            f.write("{}\t{}\t{}\n".format(startTime[i], endTime[i], daysOfWeek[i]))

        for i in timeTupes: 
            f.write("{}\n".format(i))
        f.close()



        justRooms = []
        for i in range(365, 465):
            justRooms.append(constraints[i])
        # print justRooms

        roomSizeName = []
        roomSizeCap = []
        roomSize = {}
        count = 0 
        for i in range (len(justRooms)):
            if count % 2 == 0:
                roomSizeName.append(justRooms[i])
            count = count + 1; 

        # print roomSizeName

        count = 0
        for i in range (1, len(justRooms)):
            if count % 2 == 0:
                roomSizeCap.append(justRooms[i])
            count = count + 1; 

        # print roomSizeCap

        roomSize = dict(zip(roomSizeName, roomSizeCap))

        f = open("haverford_roomSize.txt","w+")
        # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
        for i in roomSize:
            f.write("{}\t{}\n".format(i, roomSize[i]))
        f.close()

        # HCconstraints.close()

        HCconstraintsEnd = open("haverford/haverfordConstraints_withZeros.txt", "r")
        Endconstraints = HCconstraintsEnd.read().replace("\t", " ").replace("\r", " ").replace("\n", " ").split(" ")


        justClassesAndTeachers = []
        for i in range(564, len(Endconstraints)):
            justClassesAndTeachers.append(Endconstraints[i])
        # print justClassesAndTeachers

        classID = []
        teacherID = []
        classID_teacherID = {}
        count = 0 
        for i in range (len(justClassesAndTeachers)):
            if count % 2 == 0:
                classID.append(justClassesAndTeachers[i])
            count = count + 1; 

        # print classID

        count = 0
        for i in range (1, len(justClassesAndTeachers)):
            if count % 2 == 0:
                teacherID.append(justClassesAndTeachers[i])
            count = count + 1; 

        # print teacherID

        # for i in range(len(classID)):
        #     classID_teacherID.update({classID[i], teacherID[i]})
        
        classID_teacherID = dict(zip(classID, teacherID))

        # print classID_teacherID

        f = open("haverford_classID_teacherID.txt","w+")
        for i in classID_teacherID:
            f.write("{}\t{}\n".format(i, classID_teacherID[i]))
        f.close()

        HCconstraintsEnd.close()

        
        HCstudentprefs = open("haverford/haverfordStudentPrefs.txt", "r")
        studentprefs = HCstudentprefs.read().replace("\t", " ").replace("\r", " ").split('\n')

        studentprefs.pop(0)

        studentNumber = []
        for i in range(len(studentprefs)-1):
            temp = studentprefs[i].split(' ', 1)
            studentNumber.append(temp[0])

        student_pref = []
        for i in range(len(studentNumber)):
            temp = studentprefs[i].split(' ', 1)
            individualPrefs = temp[1].split(" ")
            individualPrefs.pop(-1)
            student_pref.append(individualPrefs)

        studentPreferences = dict(zip(studentNumber, student_pref))


        f = open("haverford_studentPreferences.txt","w+")
        for i in studentNumber:
            f.write("{}\t{}\n".format(i, studentPreferences[i]))
        f.close()

#dictClasses is the classSubject
#        HCclassroom = pd.read_excel('haverford/hc-classroom-data.xlsx')
#        subject = HCclassroom["Subject"]
#        classSubject = {}
#        for x in range(len(classID)):
#            classSubject.update( {classID[x] : subject[x]} )
        HCclassroom = pd.read_excel('haverford/hc-classroom-data.xlsx')
#        f = open("brynmawr_classSubject.txt","w+")
#        for i in classSubject:
#            f.write("{}\t{}\n".format(i, classSubject[i]))
#        f.close()
        
        subject_ = HCclassroom["Subject"]
        classroomID = HCclassroom["Facil ID 1"]
        
        roomAndSubject = {}
        for x in range(len(subject_)):
            roomAndSubject.update( { classroomID[x]: subject_[x] } )
        
        sortedSubjectClassroom = {}
        roomOptions = []
        for x in range(len(subject_)):
            if subject_[x] in sortedSubjectClassroom:
                if classroomID[x] not in sortedSubjectClassroom[subject_[x]] and is_nan(classroomID[x]) == False:
                    toAppend = tuple((classroomID[x], roomSize[classroomID[x]]))
                    sortedSubjectClassroom[subject_[x]].append(toAppend)
            else:
                toAppend = tuple((classroomID[x], roomSize[classroomID[x]]))
                sortedSubjectClassroom.update({subject_[x] : [toAppend]})
        
        sortedSubjectClassroom["SOWK"].pop(0)
        del sortedSubjectClassroom["VILLANOV"]
        # print(sortedSubjectClassroom)
        
        for k in sortedSubjectClassroom:
            print(sortedSubjectClassroom[k].sort(key=lambda tup: tup[1], reverse=True))
        
        f = open("brynmawr_sortedSubjectClassroom.txt","w+")
        for i in sortedSubjectClassroom:
            f.write("{}\t{}\n".format(i, sortedSubjectClassroom[i]))
        f.close()
    
        # overview of all arrays created in this function
        '''
        **see txt files with [college]_[name of data structure].txt for external version of parsed data
        !!following from excel file 
        professorOfClass = [] - list of professors
        courseID = [] - list of courseIDs
        subject = [] - list of subjects
        !!following are from haverfordConstraints file 
        timeID = [] - list of times from 1 - 60
        startTime = [] - list of start times 
        endTime = [] - list of end times 
        daysOfWeek = [] - list of the days the times are scheduled for
        timeTupes = [] - a list of tuples of all this data meshed into one 
        roomSizeName = [] - list of room names 
        roomSizeCap = [] - list of room size capacity 
        roomSize = {} - dictionary of roomSizeName:roomSizeCap
        !!following are parsed from other haverfordfile (haverfordConstraints_withZeros) in which i filled in zeros for when there isn't a corresponding teacherID for a particular classID
        classID = [] - list of classID 
        teacherID = [] - list of teacherID
        classID_teacherID = {} - dictionary of classID:teacherID correspondence 
        !!following are parsed from haverfordStudentPrefs.txt
        studentNumber = [] - list of student ID numbers
        student_pref = [] - list of student preferences 
        studentPreferences = {} - dictionary of studentNumber:student_pref ie a students ID number and their corresponding list of classID preferences
        '''

        print(dictClasses)
        print(roomSize)
        print(sortedSubjectClassroom)
        return professorOfClass, courseID, subject, timeID, startTime, endTime, daysOfWeek, timeTupes, roomSizeName, roomSizeCap, roomSize, classID, teacherID, classID_teacherID, studentNumber, student_pref, studentPreferences, roomSize, sortedSubjectClassroom

def is_nan(x):
    return (x is np.nan or x != x)

if __name__ == "__main__":
    parseHC()
