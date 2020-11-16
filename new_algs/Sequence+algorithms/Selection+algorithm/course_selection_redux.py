# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 20:13:14 2020

@author: Morgan
"""
import copy
import time


def inputfile (filename):
    """
    I need to sort the class list from the earliest to latest
    To prvent clogging the DFS 
    
    
    """
    classdict = {}
    with open(filename, 'r') as f:
        for line in f: 
            
            try:
                temp = line.replace(',', ' ')
                temp = temp.split()
            
                if len(temp) == 5:
                    time = course(temp[0],int(temp[1]), int(temp[2]), int(temp[3]), int(temp[4]))
                    name = temp[0]
                    if name not in classdict:
                        classdict[name] = [time]
                    else:
                        classdict[name] += [time]
                elif len(temp) == 8:
                    time1 = course(temp[0],int(temp[1]), int(temp[2]), int(temp[3]), int(temp[7]))
                    time2 = course(temp[0],int(temp[4]), int(temp[5]), int(temp[6]), int(temp[7]))
                    name = temp[0]
                    if name not in classdict:
                        classdict[name] = [[time1,time2]]
                    else:
                        classdict[name] += [[time1,time2]]
                elif temp == []:
                    pass
                else:
                    raise ValueError
            except:
                raise Exception("Error in user input!! Please check the format!!")
                
        
    return classdict


class course(object):
    def __init__ (self, name, start, end, weekday, sem):
        """
        
        start or end:  in the form of 1430
        weekday: 0 = Mon, 1 = Tue etc
        sem: 1 or 2
        
        """
        self.start = start
        self.end = end
        self.weekday = weekday
        self.sem = sem
        self.name = name
        
        #realstart or end is in minute form 
        #it is used to aid further caculation
        self.realstart = (start//100)*60 + (start%100)
        self.realend = (end//100)*60 + (end%100)
    
    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end
    
    def get_name(self):
        return self.name
    
    def get_realstart(self):
        return self.realstart
    
    def get_realend(self):
        return self.realend
    
    def get_weekday(self):
        return self.weekday
    
    def get_sem(self):
        return self.sem
    
    def timecrash(self, other):
        """
        This function do not take the semester and weekday into account
        
        
        """
        myrange = range (self.get_realstart(), self.get_realend())
        otherrange = range (other.get_realstart(), other.get_realend())
        
        if self.get_realstart() == other.get_realend() or other.get_realstart() == self.get_realend():
            pass                  
        else:
            if self.get_realend() in  otherrange or self.get_realstart() in  otherrange:
                raise ValueError
            
            if other.get_realend() in  myrange or other.get_realstart() in  myrange:
                raise ValueError
        
    def timediff(self, other):
        """
        This function find the time difference between target and self
        
        return: minute
        """        
        diff1 = self.get_realstart() - other.get_realend()
        diff2 = self.get_realend() - other.get_realstart()
        
        return min(abs(diff1), abs(diff2))
    
    def __str__(self):
        weekdaydict = {0:'Mon',1:'Tue',2:'Wed',3:'Thur',4:'Fri',5:'Sat',6:'Sun'}
        weekday = weekdaydict[self.get_weekday()]
        return str(self.get_name()) +": "+ str(self.get_start()) + " -> " + str(self.get_end()) + " (" + weekday + ") in sem " + str(self.get_sem())
    
    def __len__(self):
        return 1
    

def sort_timelist(OG_list, courseX):
    """
    This function sort the class_list (OG_list) from earliest to latest
    """
    for i in range(len(OG_list)):
        temp = OG_list[i]
        if courseX.get_realend() <= temp.get_realstart():
            return OG_list[:i] + [courseX] + OG_list[i:]
        
    return OG_list + [courseX]

def timelist_diff(OG_list, courseX):
    """
    This function return the time difference of the OG_list and the newly list w/ courseX
       
    return: +ve int or -ve int
    
    """
        
    OG_time = 0
    new_time = 0    
    
    if len(OG_list) >= 2:
        for i in range(len(OG_list)-1):
            OG_time += OG_list[i].timediff(OG_list[i+1])       
        
    
    newlist = sort_timelist(OG_list,courseX)
    
    for i in range(len(newlist)-1):
        new_time += newlist[i].timediff(newlist[i+1])
        
    return new_time - OG_time
    
    
        

def printlist(OG_list):
    text = ''
    for course in OG_list:
        text += (str(course)+ '\n')
    return text
        # print(course)


class timetable(object):
    def __init__(self):
        self.sem1 = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:0}
        self.sem2 = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:0}
        self.history = []
        self.dayoff_sem1 = [0,1,2,3,4,5]
        self.dayoff_sem2 = [0,1,2,3,4,5]

    def get_sem1(self):
        return self.sem1
    
    def get_sem2(self):
        return self.sem2
    
    def get_history(self):
        return self.history
    
    def get_dayoff_sem1(self):
        return self.dayoff_sem1
    
    def get_dayoff_sem2(self):
        return self.dayoff_sem2
        
    def get_lendayoff(self):
        return len(self.dayoff_sem1) + len(self.dayoff_sem2)
        
        
    def add(self,timetable ,courseX, sem):
        
        day = timetable[courseX.get_weekday()]
        history = self.get_history()
        dayofflist1 = self.dayoff_sem1
        dayofflist2 = self.dayoff_sem2
        
        for c in day:              #This check if the courseX timecrash with courses in timetable!!
            courseX.timecrash(c)
            
        timetable[6] += timelist_diff(day,courseX)  #This offset the time difference between lesson
        history += [courseX]                        #This add the courseX into the timetable
        
        
        if not day and sem == 1:                                 #This decrease the dayoff counter
            dayofflist1.remove(courseX.get_weekday())
        elif not day and sem == 2:                                 #This decrease the dayoff counter
            dayofflist2.remove(courseX.get_weekday())
            
        day = sort_timelist(day, courseX)           #This turn the sort that day schdule 
        timetable[courseX.get_weekday()] = day
        
        return timetable
    
    
    
    def addcourse(self,courseX):
        if courseX.get_sem() == 1:
            return self.add(self.get_sem1(), courseX, 1)
        
        elif courseX.get_sem() == 2:
            return self.add(self.get_sem2(), courseX, 2)
    
    def __len__(self):
        return (self.get_sem1()[6] + self.get_sem2()[6])
    
    
    

def printtimetable(timetable):
    """
    This function print out the timetable in a readable formate
    
    """
    text = "-----------------\nLoading... \nSem 1 time table:\n"
    
    sem1 = timetable.get_sem1()
    sem2 = timetable.get_sem2()
    for i in range(6):
        if sem1[i]:
            text += '\n'
            text += str(printlist(sem1[i]))
            
    text += '\n'
    text += ("There are in total %s minute(s) between lessons\n"  %sem1[6])
    
    text += '-----------------\nSem 2 time table: \n'
    
    
    for i in range(6):
        if sem2[i]:
            text += '\n'
            text += str(printlist(sem2[i]))          
    
    
    text += '\n'
    text += ("There are in total %s minute(s) between lessons\n-----------------\n"  %sem2[6])
   
    return text
        
def DFS(graph, classlist, shortest, path = timetable(), dayoff_mode = False):
    """
    This algorithm assume you must select all the class you inputed!!!
    
    
    graph: {class name: [opt1, opt2], etc..}
    classlist: just a list of class name
    shortest: the timetable with the least time diff between lesson
    path: current timetable   
    dayoff_mode: prioritise dayoff
    
    """
    if not classlist:
        return path
    
    for time in graph[classlist[0]]:
        temp = copy.deepcopy(path)
        
        try:   
            if len(time) == 1:
                temp.addcourse(time)
            else:
                for c in time:
                    temp.addcourse(c)                    
            
            if not dayoff_mode or shortest == None or shortest.get_lendayoff() < temp.get_lendayoff():
                newpath = DFS(graph, classlist[1:], shortest, temp)
                
                if newpath != None and (shortest == None or len(shortest) > len(newpath)):
                    shortest = newpath 
                    
        except:
            pass
            #this prevent the timecrashed timetable to go any further!!!
        
    return shortest
            


def couretime(timetable):
    """
    This function can print out the course inputed
    with respect to the time
    
    timetable: custom object
    
    return: a nice string
    
    """
    history = timetable.get_history()
    text = ''
    for c in history:        
        text += (str(c) + '\n')
    return text
     
    
    
def basicsorting(filename):
    """
    This basically called all the functioned used
    
    filename: input.txt
    
    return: a nice print out of the sorted timetable
    
    """
    try:
        graph = inputfile(filename)
        classlist = list(graph.keys())
        timetable = DFS(graph, classlist, None)
        
        
        text = str(printtimetable(timetable))
        text += 'Following is the selected class:\n\n'        
        text += couretime(timetable)
        text += '\n-----------------\n'
        return text
    
    except AttributeError:
        error_text = "The classes is not compatible\nPlease check the input again."
        return error_text
    
    except Exception:
        error_text = "Error in user input!!\nPlease check the format and press the button again."
        return error_text

def dayoffsorting(filename):
    """
    This basically called all the functioned and prioritize day-off
    
    filename: input.txt
    
    return: a nice print out of the sorted timetable
    
    """
    weekdaydict = {0:'Mon',1:'Tue',2:'Wed',3:'Thur',4:'Fri',5:'Sat',6:'Sun'}
    try:
        graph = inputfile(filename)
        classlist = list(graph.keys())
        TT = DFS(graph, classlist, None, timetable(), True)
        
        text = str(printtimetable(TT))
        text += 'Following is the selected class:\n\n'        
        text += couretime(TT)
        text += "\nSo you will get in total " + str(TT.get_lendayoff()) +" day(s) off"
           
            
        if len(TT.get_dayoff_sem1()) != 0:
            text += '\n>> In sem 1: '
            for c in TT.get_dayoff_sem1():            
               
                text += ('(' + weekdaydict[c] + ') ')
            
            
        if len(TT.get_dayoff_sem2()) != 0:
            text += '\n>> In sem 2: '
            for c in TT.get_dayoff_sem2():                            
                text += ('(' + weekdaydict[c] + ') ')
            text += '\n>> Are the off day(s)\n-----------------'
        return text
    
    except AttributeError:
        error_text = "The classes is not compatible\nPlease check the input again.\n"
        return error_text
                
    except Exception:
        error_text = "Error in user input!!\nPlease check the format and press the button again."
        return error_text
    
#-----------------------
#Test case      

# a = course("E1",1100,1230,1,1)

# b = course("CC",1330,1420,1,1)
# c = course("CC",1430,1800,2,1)

# d = course("E2",1700,1800,1,1)
# e = course("E2",1800,1900,1,1)

# f = course("E3",2000,2030,1,1)
# g = course("E3",1430,1700,1,1)

# graph = {"CC":[[c,b]], "E1":[a],"E2":[d,e],"E3":[f,g],"E4":[a]}
# classlist = ['E3',"CC",'E1','E2']

# test = DFS(graph, classlist, None)
# print('-----------------')
# print('Loading...')
# printtimetable(test)
# print('-----------------')
# print('The following is selected course:')
# couretime(test)

#----------------------
#loading animation (No in use)

# while animetimer != 6:
#     anime = "|/—\\"
#     for i in anime:
#         time.sleep(0.1)
#         print('loading ...' + i)
#     animetimer += 1

# 
#---------------------- 
# print(basicsorting('input.txt'))
# print('')
# print('')
# print(dayoffsorting('input.txt'))   
# print('You can now exit this window')
# input()


# graph = inputfile("test.txt")
# classlist = list(graph.keys())
# timetable = DFS(graph, classlist, None)        
# print(timetable)

        
        
        
        
        
        