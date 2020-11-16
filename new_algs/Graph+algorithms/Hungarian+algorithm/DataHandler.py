# -*- coding: utf-8 -*-
#coding:utf8

import threading;
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import ttk;
from openpyxl import load_workbook
from colorutils import Color
import random
import math


# -------------------------------File Names

periodCount = 4;
gradeMultipliers = [None]*20
slotMultipliers = [[50,0.001]]*4

allStudents = []
allActivities = []

class Student:
    name = "Stu"
    grade = 9
    choices = []
    assigned = []
    myFrame : Frame = None
    myButtons : Button = []

    class Act:
        name = "Act"
        isForced = False;

        def __init__ (self, name, isForced):
            self.name = name
            self.isForced = isForced

    def __init__ (self, name, grade):
        self.name = name
        self.grade = grade

class Activity:
    name = "Act"
    period = 0
    assigned = []
    assignedCount = 0;
    myFrame : Frame = None
    stuNameParentFrame : Frame = None;
    stuNameFrame : Frame = None;

    def __init__ (self, name, period):
        self.name = name
        self.period = period;
        self.assigned = [];


def SetUp (_UIAddStudent, _UIAddActivity, _stuSearchVar, _actSearchVar, _HideStudent, _HideActivity, _ShowStudent, _ShowActivity, _stuCountVar, _actCountVar, _statsVar):
    global UIAddStudent, UIAddActivity, stuSearchVar, actSearchVar, HideStudent, HideActivity, ShowStudent, ShowActivity, stuCountVar, actCountVar, statsVar;
    UIAddStudent = _UIAddStudent;
    UIAddActivity = _UIAddActivity;
    stuSearchVar = _stuSearchVar;
    actSearchVar = _actSearchVar;
    HideStudent = _HideStudent;
    HideActivity = _HideActivity;
    ShowStudent = _ShowStudent;
    ShowActivity = _ShowActivity;
    stuCountVar = _stuCountVar;
    actCountVar = _actCountVar;
    statsVar = _statsVar;


# -------------------------------Debug Methods
vowels = ["A","E","I","O","U"]
consonants = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "X", "Z", "W", "Y"]

activities = []
def AddStudents():

    if(len(activities) == 0):
        for n in range(18):
            actName = ""
            for syllable in range(random.randint(5,7)):
                syl = consonants[random.randint(0,len(consonants)-1)] + vowels[random.randint(0,len(vowels)-1)]
                actName += syl;

            activities.append(actName.capitalize())

    stuCount = 220
    for n in range(stuCount):
        stuName = ""
        for syllable in range (random.randint (3, 5)):
            syl = consonants[random.randint (0, len (consonants)-1)] + vowels[random.randint (0, len (vowels)-1)]
            stuName += syl;

        stu = Student(name=stuName.capitalize(), grade = 9 + int(n/stuCount*4))
        stu.choices = []
        for n in range (periodCount):
            stu.choices.append ([]);

        for period in range(periodCount):
            listIndex = []
            for n in range (len(activities)):
                listIndex.append (n);
            random.shuffle (listIndex);
            for cho in range(10):
                stu.choices[period].append(Student.Act(name = activities[listIndex[cho]], isForced = False))

        AddStudent(stu)

        stu.assigned = [None] * periodCount

    UpdateButtonColors()
    return

def AddActivities():
    return

# -------------------------------Adder Methods
def AddStudent (stu : Student):
    allStudents.append(stu)
    UIAddStudent (stu)
    SortStudents();
    StuSearchBarUpdate();

    p = 0
    for period in stu.choices:
        for act in period:
            isThereDuplicate = False
            for existingAct in allActivities:
                #print(str(existingAct.period) + " - " + str(p) + " -*- " + existingAct.name + " - " + act.name)
                if(existingAct.period == p and existingAct.name == act.name):
                    isThereDuplicate = True;
                    break;
            if(not isThereDuplicate):
                AddActivity (Activity (name = act.name, period = p))
        p += 1;

    p = 0
    choiceVals = ""
    for period in stu.choices:
        for act in period:
            isForcedVal = 0;
            if (act.isForced): isForcedVal = 1;
            choiceVals += str (p) + ", " + act.name + ", " + str (isForcedVal) + ";  "
        p += 1;

    p = 0
    assignedVals = ""
    for act in stu.assigned:
        if act != None:
            isForcedVal = 0;
            if (act.isForced): isForcedVal = 1;
            assignedVals += str (p) + ", " + act.name + ", " + str (isForcedVal) + ";  "
            p += 1

    print ("Added student " + str(stu.grade) + " - " + stu.name + " - " + choiceVals + " - " + assignedVals);

def AddActivity (act : Activity):
    allActivities.append(act)
    UIAddActivity (act)
    SortActivities();
    ActSearchBarUpdate();

    assignedVals = ""
    for act in act.assigned:
        if act != None:
            isForcedVal = 0;
            if (act.isForced): isForcedVal = 1;
            assignedVals += act.name + ", " + str (isForcedVal) + ";  "


    print ("Added Activity " + str (act.period) + " - " + act.name + " - " + assignedVals);

# -------------------------------Sorter Methods
def SortStudents ():
    #quick and dirty bubble sort; O(n^2) can't stop us baby
    for i in range(0,len(allStudents)-1):
        swapped = False;
        for j in range(0,len(allStudents)-i-1):
            if(allStudents[j].grade < allStudents[j+1].grade or #sort them based on grade
                    (allStudents[j].grade == allStudents[j+1].grade and allStudents[j].name.lower() > allStudents[j+1].name.lower())): #and for the same grades sort on name
                temp = allStudents[j];
                allStudents[j] = allStudents[j+1]
                allStudents[j + 1] = temp
                swapped = True;
        if not swapped:
            break;

def SortActivities ():
    #quick and dirty bubble sort; O(n^2) can't stop us baby
    for i in range(0,len(allActivities)-1):
        swapped = False;
        for j in range(0,len(allActivities)-i-1):
            if(allActivities[j].period > allActivities[j+1].period or #sort them based on grade
                    (allActivities[j].period == allActivities[j+1].period and allActivities[j].name.lower() > allActivities[j+1].name.lower())): #and for the same grades sort on name
                temp = allActivities[j];
                allActivities[j] = allActivities[j+1]
                allActivities[j + 1] = temp
                swapped = True;
        if not swapped:
            break;

# -------------------------------Search Bar Methods
def StuSearchBarUpdate (*args):
    SearchStudents(stuSearchVar.get());

def SearchStudents (searchString : str):
    stuCount = 0;
    for stu in allStudents:
        HideStudent(stu)
        if(len(searchString)>0):
            if(stu.name[0:len(searchString)].lower() == searchString.lower()):
                ShowStudent (stu)
                stuCount+=1
            elif(str(stu.grade) == searchString):
                ShowStudent (stu)
                stuCount += 1
        else:
            ShowStudent (stu)
            stuCount+=1

    stuCountVar.set("Total Students: " + str(len(allStudents)) + "    Currently Visible: " + str(stuCount))

def ActSearchBarUpdate (*args):
    SearchActivities(actSearchVar.get());

def SearchActivities (searchString : str):
    actCount = 0;
    for act in allActivities:
        HideActivity(act)
        if(len(searchString)>0):
            if(act.name[0:len(searchString)].lower() == searchString.lower()):
                ShowActivity (act)
                actCount+=1
            elif(str(act.period) == searchString):
                ShowActivity (act)
                actCount += 1
        else:
            ShowActivity (act)
            actCount+=1

    actCountVar.set("Total Activities: " + str(len(allActivities)) + "    Currently Visible: " + str(actCount))


# -------------------------------Helper methods
def GetActivityWithName (period, actName):
    myAct: Activity = None;
    for act in allActivities:
        if (act.period == period) and act.name == actName:
            myAct = act;
            break;
    return myAct;
#Button colors:
#def color = "#f0f0f0"
#blue = #80ffd9
#green = #93ff80
#yellow = #fffd80
#orange =  ##ffaa80
#red = #ff8080
def AssignStudentToActivity (stu : Student, period, index, boolShouldUpdateButtonColors, actName):
    if(stu == None): #the hungarian algorithm have to assign dummy students
        print("Assigning dummy student")
        return;

    isForced = False;
    try:
        actName = stu.choices[period][index].name;
        isForced = stu.choices[period][index].isForced;
    except:
        #do nothing
        kek = 5;

    #if this student is already assigned to an activity for this period
    if (stu.assigned[period] != None):
        if (stu.assigned[period].name == actName): #if the same activity
            print(stu.name + " is already assigned to " + actName)
            if (boolShouldUpdateButtonColors):
                UpdateButtonColors();
            return;
        else: #if a different one, unassign first
            UnAssignStudentFromActivity (stu, period, GetActivityWithName (period, stu.assigned[period].name))

    myAct: Activity = GetActivityWithName (period, actName);

    stu.assigned[period] = Student.Act(name = actName, isForced = isForced)

    isAssigned = False;
    for n in range(len(myAct.assigned)):
        if (myAct.assigned[n] == None): #assign the student to the first empty slot
            myAct.assigned[n] = stu;
            isAssigned = True
            break;
    if not isAssigned: #if no slot is available add new slot
        myAct.assigned.append(stu);

    myAct.assignedCount += 1;

    print(stu.name + " is assigned to " + str(period) + " - " + actName + " >> assignedCount = " + str(myAct.assignedCount))
    if(boolShouldUpdateButtonColors):
        UpdateButtonColors();


def UnAssignStudentFromActivity (stu : Student, period, act : Activity):
    act.assigned.remove(stu);
    act.assignedCount -= 1;
    print (stu.name + " is unassigned from " + str (period) + " - " + act.name)

def UpdateButtonColors ():
    print("Updating button colors")
    for stu in allStudents:
        for period in range(len(stu.myButtons)):
            for index in range(len(stu.myButtons[period])):
                actName = stu.choices[period][index].name;
                myAct: Activity = None;
                for act in allActivities:
                    if (act.period == period) and act.name == actName:
                        myAct = act;
                        break;

                myColor = "#ff8080";  # red

                if (myAct.assignedCount < slotMultipliers[0][0]):
                    myColor = "#80ffd9"  # blue
                elif (myAct.assignedCount < slotMultipliers[1][0]):
                    myColor = "#93ff80"  # green
                elif (myAct.assignedCount < slotMultipliers[2][0]):
                    myColor = "#fffd80"  # yellow

                isAssigned = False;
                #print(stu.name + " - " + str(period) + " - " + str(periodCount) + " - " + str(len(stu.assigned)))
                if (stu.assigned[period] != None):
                    if (myAct.name == stu.assigned[period].name):
                        isAssigned = True;

                isForced = stu.choices[period][index].isForced;

                fontStatus = "arial 9"
                if(isAssigned):
                    fontStatus += " bold"
                if (isForced):
                    fontStatus += " italic"

                stu.myButtons[period][index].config (background = myColor, font = fontStatus);


def UpdateActivityAssignmentsUI ():
    print("Updating Activity Students")
    stuMaxChoice = len(allStudents[0].choices[0])
    for act in allActivities:
        act.stuNameFrame.destroy()
        act.stuNameFrame = Frame(act.stuNameParentFrame)
        act.stuNameFrame.pack();

        count = 0;
        n = 0;

        for stu in act.assigned:
            choiceIndex = 0;
            for acts in stu.choices[act.period]:
                if(acts.name == act.name):
                    break;
                choiceIndex += 1;

            print("For act " + act.name + " with " + str(act.assignedCount) + " - " + str(len(act.assigned)) + " assigned, adding " + stu.name +  " - " + str(choiceIndex));
            myC = Color(hsv=(((stuMaxChoice-choiceIndex)/stuMaxChoice) * 120,1,1));
            Label (act.stuNameFrame, text = str(stu.grade) + " - " + stu.name, relief = GROOVE, width = 15, bg = myC.hex).grid (column = n%11, row = math.floor(n/11), ipadx = 3, ipady = 3, padx=3, pady=3);
            count += 1;
            n += 1;

            if (count == slotMultipliers[0][0]):
                Frame(act.stuNameFrame, width=8, height=15, relief=GROOVE, bg = "#80ffd9").grid (column = n%11, row = math.floor(n/11), sticky=N+S)# blue
                n += 1;
            elif (count == slotMultipliers[1][0]):
                Frame(act.stuNameFrame, width=8, height=15, relief=GROOVE, bg = "#93ff80").grid (column = n%11, row = math.floor(n/11), sticky=N+S)# green
                n += 1;
            elif (count == slotMultipliers[2][0]):
                Frame(act.stuNameFrame, width=8, height=15, relief=GROOVE, bg = "#fffd80").grid (column = n%11, row = math.floor(n/11), sticky=N+S)# yellow
                n += 1;

        if (count > slotMultipliers[2][0]):
            Frame (act.stuNameFrame, width = 8, height=15, relief = GROOVE, bg = "#ff8080").grid (column = n%11, row = math.floor(n/11), sticky=N+S)  # red
            n += 1;


# -------------------------------Main Method
MaxSlotCount = 30
def AssignStudents ():
    print("Brace Yourselves. Hungarian Algorithm is incoming") #helpful message

    totalChoiceCount = 0
    totalStuCount = 0
    worstChoice = 0;
    for period in range (periodCount):
        acts = []
        for act in allActivities:
            if(act.period == period):
                acts.append(act);

        costMatrix = [];

        #populate the cost matrix
        n = 0
        for stu in allStudents:
            costMatrix.append([])
            for act in acts:
                for actSlot in range (MaxSlotCount):
                    costMatrix[n].append(CostSlot(stu, act, CalculateCost(stu, act, actSlot, period)))
            n += 1;

        #add dummy low value slots
        totalActSlotCount = len(acts) * MaxSlotCount;

        #if we got more activity slots than students, add empty slots that will have no value
        if(n < totalActSlotCount):
            for i in range (n,totalActSlotCount):
                costMatrix.append ([])
                for act in acts:
                    for actSlot in range (MaxSlotCount):
                        costMatrix[i].append (CostSlot (None, act, 0))
        #there is no way in my current sittuation to have more students than activity slots... so i wont be coding that


        length = totalActSlotCount;
        #the hungarian algorithm works to minimize the cost, but we need to maximize it, so subtract everything from the max cost
        theMaxCost = 0

        for r in range(length):
            for c in range(length):
                theMaxCost = max(theMaxCost, costMatrix[r][c].cost);

        DebugDrawMatrix(costMatrix, length, "Before inversion");
        for rows in costMatrix:
            for slots in rows:
                slots.cost = theMaxCost - slots.cost;

        print("Cost Matrix is set up. There are " + str(totalActSlotCount) + " slots to fill.")
        DebugDrawMatrix(costMatrix, length, "After inversion");
        #SETTING UP IS COMPLETE! now the actual algorithm
        #find the least value in each row and subtract
        for r in range(length):
            minVal = theMaxCost;
            for c in range(length):
                minVal = min(minVal, costMatrix[r][c].cost);
            for c in range(length):
                costMatrix[r][c].cost -= minVal;
        DebugDrawMatrix (costMatrix, length, "After normalizing rows");

        #find the least value in each column and subtract
        for c in range(length):
            minVal = theMaxCost;
            for r in range(length):
                minVal = min(minVal, costMatrix[r][c].cost);
            for r in range(length):
                costMatrix[r][c].cost -= minVal;
        DebugDrawMatrix (costMatrix, length, "After normalizing columns");

        lineCount = 0;
        # repeat until finished
        while (lineCount < length):
            DebugDrawMatrix (costMatrix, length, "Repeat algorithm");

            #mark all zeroes using the min number of lines
            lineCount = 0;
            for r in range(length):
                for c in range(length):
                    costMatrix[r][c].assigned = False #clear the markings

            columnZeroCount = [0]*length
            maxColumnZeroCount = 0;
            for c in range(length):
                for r in range(length):
                    if costMatrix[r][c].cost == 0:
                        columnZeroCount[c] += 1;
                maxColumnZeroCount = max(maxColumnZeroCount, columnZeroCount[c]);

            crossedColumns = [False]*length
            nonAssignedRows = [];
            #"assign" as many tasks as possible
            for r in range(length):
                isAss = False
                minZeroCountColumn = -1;
                minZeroCount = maxColumnZeroCount
                for c in range(length):
                    if costMatrix[r][c].cost == 0 and crossedColumns[c] == False:
                        if columnZeroCount[c] <= minZeroCount:
                            minZeroCountColumn = c;
                            minZeroCount = columnZeroCount[c];

                if minZeroCountColumn != -1:
                    crossedColumns[minZeroCountColumn] = True
                    costMatrix[r][minZeroCountColumn].assigned = True
                    isAss = True
                if not isAss:
                    nonAssignedRows.append(r);

            rMarks = [False] * length;
            cMarks = [False] * length;

            #do the complicated wikipedia step 3 drawing marking stuff
            #Mark all rows having no assignments
            for unAssRow in nonAssignedRows:
                rMarks[unAssRow] = True;
                DebugDrawMatrix (costMatrix, length, "Marking row without ass " + str(unAssRow), rMarks, cMarks)
                #Mark all columns having zeros in newly marked rows
                MarkColumnWithZeroes(costMatrix, cMarks, rMarks, unAssRow, length) #--------------------------------------RECURSIVE MARKING METHOD

            DebugDrawMatrix(costMatrix, length, "Marked Places", rMarks,cMarks)
            # draw lines through marked columns and UNmarked rows
            for c in range (length):
                if cMarks[c]:
                    for _r in range (length):
                        costMatrix[_r][c].markCount += 1;
                    lineCount += 1;
                    DebugDrawMatrix (costMatrix, length, "Draw vertical " + str (c), rMarks,cMarks)


            for r in range(length):
                if not rMarks[r]:
                    for _c in range (length):
                        costMatrix[r][_c].markCount += 1;
                    lineCount += 1;
                    DebugDrawMatrix (costMatrix, length, "Draw horizontal " + str (r), rMarks,cMarks)



            DebugDrawMatrix (costMatrix, length, "Draw lines " + str(lineCount));
            #check if there are enough lines
            if(lineCount >= length):
                break;

            #broaden the zeroes

            #find the minimum unmarked spot
            minUnmarked = theMaxCost;
            for r in range (length):
                for c in range (length):
                    if costMatrix[r][c].markCount <= 0:
                        minUnmarked = min (minUnmarked, costMatrix[r][c].cost);
            print("Minimum unmarked: " + str(minUnmarked))
            #subtract min unmarked from al unmarked
            for r in range (length):
                for c in range (length):
                    if costMatrix[r][c].markCount <= 0:
                        costMatrix[r][c].cost -= minUnmarked;

            #add minunmarked to all double marked
            for r in range (length):
                for c in range (length):
                    if costMatrix[r][c].markCount >= 2:
                        costMatrix[r][c].cost += minUnmarked;

            #clean the markings
            for r in range (length):
                for c in range (length):
                    costMatrix[r][c].markCount = 0;
            #repeat the same process until we got enough lines

        #assign students to activities

        #clean markings
        for r in range (length):
            for c in range (length):
                costMatrix[r][c].markCount = 0;

        assignedCount = 0
        #assign students until there are none left

        # find row zero count
        rCount = []
        for r in range (length):
            zeroCount = 0;
            for c in range (length):
                if (costMatrix[r][c].cost == 0 and costMatrix[r][c].markCount <= 0):
                    zeroCount += 1;
            if zeroCount == 0:
                zeroCount = 100000;
            rCount.append (zeroCount);

        while (assignedCount < length):
            DebugDrawMatrix (costMatrix, length, "Assign Student #" + str(assignedCount));

            #assign student with the least amount of zero and marked used spots
            rIndex = rCount.index(min(rCount))
            cIndex = 0;
            for c in range(length):
                cIndex = c;
                if(costMatrix[rIndex][c].cost == 0 and costMatrix[rIndex][c].markCount <= 0):
                    break;

            myStu = costMatrix[rIndex][cIndex].stu
            myAct = costMatrix[rIndex][cIndex].act

            choiceIndex = 0;

            if(myStu != None):
                for _act in myStu.choices[period]:
                    if _act.name == myAct.name:
                        break;
                    choiceIndex += 1;
                totalChoiceCount += choiceIndex + 1;
                totalStuCount += 1;
                worstChoice = max(worstChoice, choiceIndex);

            AssignStudentToActivity(myStu, period, choiceIndex, False, myAct.name)
            assignedCount += 1;

            #mark the column and the row
            for c in range(length):
                costMatrix[rIndex][c].markCount += 1;

            rCount[rIndex] = 100000
            for r in range(length):
                if costMatrix[r][cIndex] == 0 and  costMatrix[r][cIndex].markCount <= 0:
                    rCount[r] -= 1;
                if(rCount[r] <= 0):
                    rCount[r] = 100000
                costMatrix[r][cIndex].markCount += 1;
        #repeat for the other periods and pray that we are done with the algorithm
    UpdateButtonColors();

    CalculateAverages();

    #update activity student placements
    UpdateActivityAssignmentsUI();

    print("ASSIGNMENTS DONE");

def CalculateAverages():

    totalChoiceCount = 0
    worst = 0
    for stu in allStudents:
        for period in range(periodCount):
            choiceIndex = 0;
            for _act in stu.choices[period]:
                if not stu.assigned[period] == None:
                    if _act.name == stu.assigned[period].name:
                        break;
                choiceIndex += 1;
            totalChoiceCount += choiceIndex + 1;
            worst = max (worst, choiceIndex);

    stuStats =  "Average Choice: " + "{0:.2f}".format ((totalChoiceCount/4.0) / len(allStudents)) + "     Worst Choice: " + str (worst + 1)

    # calculate average fill
    total = 0;
    least = 100;
    maxim = 0;
    for act in allActivities:
        total += act.assignedCount;
        least = min (least, act.assignedCount)
        maxim = max (maxim, act.assignedCount)

    actStats = "Average Fill: " + "{0:.2f}".format (total / len (allActivities)) + "     Least Fill: " + str (least) + "     Max Fill: " + str (maxim)

    statsVar.set(stuStats + "      " + actStats)

def MarkColumnWithZeroes (costMatrix, cMarks, rMarks, row, length):
    # Mark all columns having zeros in newly marked rows
    for c in range (length):
        if costMatrix[row][c].cost == 0 and not cMarks[c]:
            cMarks[c] = True;
            DebugDrawMatrix (costMatrix, length, "Marking column with zero " + str(c), rMarks, cMarks)
            MarkRowWithAssignment(costMatrix, cMarks, rMarks, c, length)


def MarkRowWithAssignment (costMatrix, cMarks, rMarks, column, length):
    # Mark all rows having assignments in newly marked columns
    for r in range (length):
        if costMatrix[r][column].assigned and rMarks[r] == False:
            rMarks[r] = True;
            DebugDrawMatrix (costMatrix, length, "Marking row with assignment " + str(r), rMarks, cMarks)
            # mark all columns having zeros in newly marked rows
            MarkColumnWithZeroes (costMatrix, cMarks, rMarks, r, length)


class CostSlot:
    stu : Student;
    act : Activity;
    cost = 0;
    markCount = 0;
    assigned = False;

    def __init__ (self, _stu, _act, _cost):
        self.stu = _stu;
        self.act = _act;
        self.cost = _cost;

def CalculateCost (stu : Student, act : Activity, actSlot, period):
    cost = 0;

    if stu == None:
        return 0;

    choiceIndex = 0;
    forcedMult = 1;
    for choice in stu.choices[period]:
        if choice.name == act.name:
            if(choice.isForced):
                forcedMult = 1000;
            break;
        choiceIndex += 1;

    choiceMult = pow(2,-choiceIndex)
    if(choiceIndex > len(stu.choices[period])):
        choiceMult = 0;

    slotMult = slotMultipliers[3][1];

    if (actSlot < slotMultipliers[0][0]):
        slotMult = slotMultipliers[0][1];
    elif (actSlot < slotMultipliers[1][0]):
        slotMult = slotMultipliers[1][1];
    elif (actSlot < slotMultipliers[2][0]):
        slotMult = slotMultipliers[2][1];


    cost = gradeMultipliers[stu.grade] * slotMult * choiceMult * forcedMult;

    return cost;


def DebugDrawMatrix (_costMatrix, _length, message, _rMarks = [], _cMarks = []):
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
    print("DebugDrawing >> " + message)
    return

    columnNames = ""

    for c in range(_length):
        columnNames += _costMatrix[0][c].act.name + " - ";
    print(columnNames)

    topMarks = "   "
    if (len (_cMarks) >= _length):
        for b in _cMarks:
            if b:
                topMarks += "    *     -"
            else:
                topMarks += "          -"
        print(topMarks)

    for r in range(_length):
        row = ""
        if(_costMatrix[r][0].stu != None):
            row += _costMatrix[r][0].stu.name[0]
        else:
            row += "D"
        row += " > "
        for c in range(_length):
            middleThing = " - "
            marks = ""
            marks += "*" * _costMatrix[r][c].markCount;
            if(_costMatrix[r][c].assigned):
                marks += "~"
            else:
                marks += " "
            marks += " " * (2 - _costMatrix[r][c].markCount);
            row += "{: >5d}".format(int(_costMatrix[r][c].cost)) + marks + middleThing
        if (len(_rMarks) > r):
            if(_rMarks[r]):
                print(row + "*")
            else:
                print(row)
        else:
            print(row)


    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")