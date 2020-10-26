import numpy as np
teamscsv = file("Teams.csv",'r')
tourneycsv = file("TourneyDetailedResults.csv",'r')
seasoncsv = file("RegularSeasonDetailedResults.csv",'r')
bracketID = file("bracketID.csv",'r')
keyToEnum = {}
enumToTeamName = {}

def readbrackets():
    bracketlst = []
    for team in bracketID.readlines():
        bracketlst.append(int(team.strip()))
    return bracketlst

def readteams():
    teams = {}
    lines = teamscsv.readlines()
    enum = 0
    for line in lines[1:]:
        teamid,teamname = line[:-1].split(',')
        teams[int(teamid)] = teamname
        keyToEnum[int(teamid)] = enum
        enumToTeamName[enum] = teamname
        enum+=1
    return teams

#there is a bunch of data, lets just look at score for now
# 0      1     2    3       4     5
#2003,  134 ,1421,  92,    1411,  84,  N,1,32,69,11,29,17,26,14,30,17,12,5,3,22,29,67,12,31,14,31,17,28,16,15,5,0,22
#2003,   10 ,1104,  68,    1328,  62,  N,0,27,58, 3,14,11,18,14,24,13,23,7,1,22,22,53, 2,10,16,22,10,22, 8,18,9,2,20
#season,day, Wteam,Wscore,Lteam,Lscore
season = 2016
def readresults(teams,fromyears,computeval):
    n = len(teams)
    incidencematrix = np.zeros([n,n])-np.eye(n,n)
    #read tourneys
    lines = tourneycsv.readlines()
    for line in lines[1:]:
        vals = line[:-1].split(',')
        year = int(vals[0])
        if year >= fromyears:
            wteam = keyToEnum[int(vals[2])]
            lteam = keyToEnum[int(vals[4])]
            [winval,loseval] = computeval(vals)
            incidencematrix[wteam][lteam] += winval
            incidencematrix[lteam][wteam] += loseval
    #read regular season
    lines = seasoncsv.readlines()
    for line in lines[1:]:
        vals = line[:-1].split(',')
        year = int(vals[0])
        if year >= fromyears:#basic filter
            wteam = keyToEnum[int(vals[2])]
            lteam = keyToEnum[int(vals[4])]
            [winval,loseval] = computeval(vals)
            incidencematrix[wteam][lteam] += winval
            incidencematrix[lteam][wteam] +=  loseval
    return incidencematrix

