import logging
import sys

logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

# to read input file
# process
# to write output file
class ReadandWrite:
    def __init__(self):
        super().__init__();
        self.initdirect();

    def initdirect(self):
        self.car_path = sys.argv[1];
        self.road_path = sys.argv[2];
        self.cross_path = sys.argv[3];
        self.answer_path = sys.argv[4];

    def readCar(self):
        #print("test: car_path: %s" %(self.car_path));

        self.car_list = [];
        with open(self.car_path,'r') as carinfo:
            next(carinfo);
            for line in carinfo.readlines():
                templist = [];
                for obj in line.split("(")[1].split(")")[0].split(", "):
                    numobj = int(obj);
                    templist.append(numobj);
                #print(templist);
                self.car_list.append(templist);
            #print(self.car_list);

        carinfo.close();

        return self.car_list;

    def readCross(self):
        #print("test: cross_path: %s" %(self.cross_path));

        self.cross_list = [];
        with open(self.cross_path,'r') as crossinfo:
            next(crossinfo);
            for line in crossinfo.readlines():
                templist = [];
                for obj in line.split("(")[1].split(")")[0].split(", "):
                    numobj = int(obj);
                    templist.append(numobj);
                #print(templist);
                self.cross_list.append(templist);
            #print(self.cross_list);

        crossinfo.close();

        return self.cross_list;

    def readRoad(self):
        #print("test: road_path: %s" %(self.road_path));

        self.road_list = [];
        with open(self.road_path,'r') as roadinfo:
            next(roadinfo);
            for line in roadinfo.readlines():
                templist = [];
                for obj in line.split("(")[1].split(")")[0].split(", "):
                    numobj = int(obj);
                    templist.append(numobj);
                #print(templist);
                self.road_list.append(templist);
            #print(self.road_list);

        roadinfo.close();

        return self.road_list;

    def writeAnswer(self,solutions):
        #print("test: answer_path: %s" %(self.answer_path));

        with open(self.answer_path,'w') as answer:
            answer.truncate();
            txthead = "#(carId,StartTime,RoadId...)\n";
            answer.write(txthead);
            for car in solutions:
                tempstr = "(";
                for obj in car:
                    strobj = str(obj);
                    tempstr = tempstr + strobj;
                    if car.index(obj) != len(car)-1:
                        tempstr = tempstr + ",";
                tempstr = tempstr + ")";
                #print(tempstr);
                answer.write(tempstr+'\n');

        answer.close();   


# process
roadentermax = 1.0;
roadenterdiff = 0.6;
carentermax = 0.5;
carenterdiff = 0.8;
crosswait = 0.7;

# process
class Car:
    def __init__(self,carinfo):
        super().__init__();
        self.initcar(carinfo);

    def initcar(self,carinfo):
        self.id = carinfo[0];
        self.departure = carinfo[1];
        self.destination = carinfo[2];
        self.maxv = carinfo[3];
        self.plant = carinfo[4];

        self.shortroute = [];
        self.departtime = 1;
        self.usetime = 0;
        self.route = [];
        self.routenodes = [];
        self.currentroad = 0;
        self.departed = False;
        
        self.crossnum = 0;
        self.straightnum = 0;
        self.leftnum = 0;
        self.rightnum = 0;
        self.crosspriority = 0;

        self.busyrates = [];

    def caltimeschedule(self,time,roadlist,nodelist,fsrinstance):
        roadnum = len(self.route);
        self.crossnum = roadnum - 1;
        self.timeschedule = [[] for i in range(roadnum)];
        #print(self.route);
        self.busyrates = [];
        currenttime = time;
        for road in self.route:
            roadindex = self.route.index(road);
            rstart = self.routenodes[roadindex];
            rend = self.routenodes[roadindex+1];

            self.timeschedule[roadindex].append(rstart);
            self.timeschedule[roadindex].append(currenttime);
            self.timeschedule[roadindex].append(rend);

            roadinsindex = fsrinstance.roadid_list.index(road);

            roadinstance = roadlist[roadinsindex];
            limitspeed = roadinstance.limitv;
            if self.maxv >= limitspeed:
                self.usetime = self.usetime + roadinstance.mintime;
                currenttime = currenttime + roadinstance.mintime;
                usettime = roadinstance.mintime;
            else:
                usettime = int(roadinstance.lengthr/self.maxv) + 1;
                self.usetime = self.usetime + usettime;
                currenttime = currenttime + usettime;

            forbackflag = 0;
            startnodeid = roadinstance.originc;
            endnodeid = roadinstance.endc;
            if (rstart == startnodeid)and(rend == endnodeid):
                forbackflag = 0;
            elif (rstart == endnodeid)and(rend == startnodeid):
                forbackflag = 1;

            thisbusyrate = roadinstance.getbusyrate(currenttime,forbackflag);
            self.busyrates.append(thisbusyrate);

            leavewait = self.leavewaittime(currenttime,roadinstance,forbackflag);
            currenttime = currenttime + leavewait;
            waittingtime = 0;
            if roadindex+1 < len(self.route):
                nextroadid = self.route[roadindex+1];
                waittingtime = self.enterwaittime(currenttime,nextroadid,roadlist,rend,roadinstance,forbackflag,fsrinstance) + leavewait;
                lnodeindex = fsrinstance.crossid_list.index(rend);
                leavingnode = nodelist[lnodeindex];
                nodebusyrate = leavingnode.calcrossbusyrate(currenttime,roadlist,fsrinstance);
                if nodebusyrate > crosswait:
                    waittingtime = waittingtime + 1;

                if roadindex >= 0:
                    crossroadsinfo = leavingnode.roadssequence;
                    enteringindex = crossroadsinfo.index(road);
                    nextroadindex = crossroadsinfo.index(nextroadid);
                    #print("road %d to road %d at node %d"%(road,nextroadid,rend));
                    if (abs(enteringindex-nextroadindex) == 2):
                        #print("Just Go Straight");
                        waittingtime = waittingtime + 0;
                        #waittingtime = 1;
                        self.straightnum = self.straightnum + 1;
                    elif (enteringindex-nextroadindex == -1)or(enteringindex-nextroadindex == 3):
                        waittingtime = waittingtime + self.leftwaittime(currenttime,nextroadindex,roadlist,leavingnode,fsrinstance);
                        #waittingtime = waittingtime + 1;
                        #waittingtime = 2;
                        self.leftnum = self.leftnum + 1;
                    elif (enteringindex-nextroadindex == 1)or(enteringindex-nextroadindex == -3):
                        waittingtime = waittingtime + self.rightwaittime(currenttime,nextroadindex,roadlist,leavingnode,fsrinstance);
                        #waittingtime = waittingtime + 2;
                        #waittingtime = 3;
                        self.rightnum = self.rightnum + 1;
            currenttime = currenttime + waittingtime;
            occupytime = usettime + waittingtime;

            if self.crossnum != 0:
                self.crosspriority = self.straightnum*100/self.crossnum + self.leftnum*10/self.crossnum + self.rightnum/self.crossnum;
            else:
                self.crosspriority = 100;

            self.timeschedule[roadindex].append(currenttime);
            self.timeschedule[roadindex].append(road);
            self.timeschedule[roadindex].append(occupytime);
            self.timeschedule[roadindex].append(forbackflag);

        return(self.timeschedule);

    def enterwaittime(self,time,nextroadid,roadlist,node,troad,forbackflagt,fsrinstance):
        basictime = 0;
        nextroadindex = fsrinstance.roadid_list.index(nextroadid);
        nextroad = roadlist[nextroadindex];
        if nextroad.originc == node:
            forbackflagn = 0;
        elif nextroad.endc == node:
            forbackflagn = 1;

        if time > len(nextroad.busyrate[forbackflagn]):
            basictime = 0;
            return basictime;
        else:
            nextmintime = int(nextroad.lengthr/min(self.maxv,nextroad.limitv))+1;
            nextbusyrate = nextroad.busyrate[forbackflagn][time-1];
            nextdiffcars = nextroad.diffcarnum[forbackflagn][time-1];
        #     nextcars = len(nextroad.schedule[forbackflagn][time-1]);

        #     if time > len(troad.schedule[forbackflagt]):
        #         basictime = 0;
        #     else:
        #         thiscars = len(troad.schedule[forbackflagt][time-1]);
        #         leftcars = thiscars - nextcars/3;
        #         if leftcars < 0:
        #             basictime = 0;
        #         else:
        #             runtime = nextroad.lengthr/min(nextroad.limitv,self.maxv);
        #             basictime = runtime*leftcars/troad.maxcapacity;
        #             if basictime < 1:
        #                 basictime = 0;
        #             else:
        #                 basictime = int(basictime) + 1;
            # left = nextmintime*(1-nextbusyrate);
            # if left < 1:
            #    basictime = 1;
            # else:
            #    basictime = 0;
            #    return basictime;

            if nextbusyrate <= carentermax:
                basictime = 0;
            elif nextbusyrate > carenterdiff:
                basictime = 1;
            elif nextdiffcars < 0:
                basictime = 0;
            else:
                basictime = 1;

            return basictime;

    def leftwaittime(self,time,nextdir,roadlist,atnode,fsrinstance):
        node = atnode;
        straight = 0;
        if nextdir == 1:
            straight = node.south;
        elif nextdir == 2:
            straight = node.west;
        elif nextdir == 3:
            straight = node.north;
        elif nextdir == 4:
            straight = node.east;
        
        if straight == -1:
            lefttime = 0;
            #print("left turning waiting: no straight road");
            return lefttime;
        else:
            sroadindex = fsrinstance.roadid_list.index(straight);
            straightroad = roadlist[sroadindex];
            if straightroad.endc == atnode.id:
                forbackflag = 0;
                #print("left turning waiting: forward straight road");
            elif straightroad.originc == atnode.id:
                forbackflag = 1;
                #print("left turning waiting: backward straight road");
            
            if time > len(straightroad.busyrate[forbackflag]):
                lefttime = 0;
                #print("left turning waitting: straight road no car yet");
                return lefttime;
            else:
                straightbusy = straightroad.busyrate[forbackflag][time-1];
                straightruntime = straightroad.mintime;
                lefttime = round(straightruntime*straightbusy);

                # if straightroad.busyrate[forbackflag][time-1] == 0:
                #     lefttime = 0;
                #     #print("left turning waitting: straight road busyrate is 0");
                # else:
                #     lefttime = 1;
                #     #print("left turning waitting: cars in straight road");

                return lefttime;

    def rightwaittime(self,time,nextdir,roadlist,atnode,fsrinstance):
        node = atnode;
        straight = 0;
        left = 0;
        straighttime = 1;
        lefttime = 1;
        righttime = 0;
        if nextdir == 1:
            straight = node.south;
            left = node.west;
        elif nextdir == 2:
            straight = node.west;
            left = node.north;
        elif nextdir == 3:
            straight = node.north;
            left = node.east;
        elif nextdir == 4:
            straight = node.east;
            left = node.south;

        if straight == -1:
            straighttime = 0;
            #print("right turning waiting: no straight road");
        else:
            sroadindex = fsrinstance.roadid_list.index(straight);
            straightroad = roadlist[sroadindex];
            if straightroad.endc == atnode.id:
                forbackflags = 0;
                #print("right turning waiting: forward straight road");
            elif straightroad.originc == atnode.id:
                forbackflags = 1;
                #print("right turning waiting: backward straight road");
            
            if time > len(straightroad.busyrate[forbackflags]):
                straighttime = 0;
                #print("right turning waiting: straight road no car yet");
            else:
                straightbusy = straightroad.busyrate[forbackflags][time-1];
                straightruntime = straightroad.mintime;
                straighttime = round(straightruntime*straightbusy);

                # if straightroad.busyrate[forbackflags][time-1] == 0:
                #     straighttime = 0;
                #     #print("right turning waiting: straight road busy rate is 0");
                # else:
                #     straighttime = 1;
                #     #print("right turning waiting: cars in straight road");

        if left == -1:
            lefttime = 0;
            #print("right turning waiting: no left road");
        else:
            lroadindex = fsrinstance.roadid_list.index(left);
            leftroad = roadlist[lroadindex];
            if leftroad.endc == atnode.id:
                forbackflagl = 0;
                #print("right turning waiting: forward left road");
            elif leftroad.originc == atnode.id:
                forbackflagl = 1;
                #print("right turning waiting: backward left road");
            
            if time > len(leftroad.busyrate[forbackflagl]):
                lefttime = 0;
                #print("right turning waiting: left road no car yet");
            else:
                leftbusy = leftroad.busyrate[forbackflagl][time-1];
                leftruntime = leftroad.mintime;
                lefttime = round(leftbusy*leftruntime);

                # if leftroad.busyrate[forbackflagl][time-1] == 0:
                #     lefttime = 0;
                #     #print("right turning waiting: left road busy rate is 0");
                # else:
                #     lefttime = 1;
                #     #print("right turning waiting: cars in left road");

        righttime = straighttime + lefttime;
        #print("right waitting time: %d"%(righttime));
        return righttime;

    def leavewaittime(self,time,road,forbackflag):
        leavetime = 0;
        if time > len(road.busyrate[forbackflag]):
            leavetime = 0;
        else:
            myserial = len(road.schedule[forbackflag][time-1]);
            waitingrate = myserial/road.maxcapacity;
            runtime = road.lengthr/min(road.limitv,self.maxv);
            leavetime = runtime*waitingrate;
            leavetime = round(leavetime);
            #if road.busyrate[forbackflag][time-1] > 0.5:
            #    leavetime = 1;
            #else:
            #    leavetime = 0;

        return leavetime;

    def occupyroad(self,roadlist,fsrinstance):
        for obj in self.timeschedule:
            enteringnodeid = obj[0];
            entertime = obj[1];
            leavingnodeid = obj[2];
            leavetime = obj[3];
            roadid = obj[4];
            runtime = obj[5];
            forbackflag = obj[6];

            roadinsindex = fsrinstance.roadid_list.index(roadid);
            roadinstance = roadlist[roadinsindex];
            roadinstance.enterroad(self.id,entertime,leavetime,forbackflag);

    def depart(self,time,roadlist,fsrinstance):
        self.departtime = time;
        self.occupyroad(roadlist,fsrinstance);

    def departflag(self,time,roadlist,nodelist,fsrinstance):
        departflag = True;
        self.caltimeschedule(time,roadlist,nodelist,fsrinstance)
        #print(len(self.timeschedule)-len(self.route));
        for obj in self.timeschedule:
            entertime = obj[1];
            leavetime = obj[3];
            roadid = obj[4];
            forbackflag = obj[6];

            roadinsindex = fsrinstance.roadid_list.index(roadid);
            roadinstance = roadlist[roadinsindex];
            departflag = departflag and roadinstance.enterflag(entertime,leavetime,forbackflag);
            #print("car.departflag: %s"%(departflag));
            if departflag == False:
                return False;
                break;

        return departflag;

    def calredirpara(self):
        maxbusyrate = max(self.busyrates);
        maxbusyroad = self.route[self.busyrates.index(maxbusyrate)];
        fromnode = self.routenodes[self.busyrates.index(maxbusyrate)];
        tonode = self.routenodes[self.busyrates.index(maxbusyrate)+1];
        minbusyrate = min(self.busyrates);
        minbusyroad = self.route[self.busyrates.index(minbusyrate)];
        avgbusyrate = sum(self.busyrates)/len(self.busyrates);
        if maxbusyrate > 0.1:
            avgrate = avgbusyrate/maxbusyrate;
        else:
            avgrate = 1;

        secondmax = sorted(self.busyrates, reverse = True)[1];
        difftosec = maxbusyrate-secondmax;


        #print(self.busyrates);
        #print("max: %f, at road: %d, min: %f, at road: %d, average: %f, difftomin: %f, difftoavg: %f"%(maxbusyrate,maxbusyroad,minbusyrate,minbusyroad,avgbusyrate,maxbusyrate-minbusyrate,maxbusyrate-avgbusyrate));

        return [maxbusyrate,maxbusyroad,fromnode,tonode,maxbusyrate-minbusyrate,avgrate,difftosec];

    def redirection(self,fsrinstance,time,roadlist,nodelist):
        oldschedule = self.caltimeschedule(time,roadlist,nodelist,fsrinstance);
        [maxbusyrate,maxbusyroad,fromnode,tonode,difftomin,avgrate,difftosec] = self.calredirpara();
        flag = (maxbusyrate>0.75)and(difftomin>0.5)and(avgrate<0.3)and(difftosec>maxbusyrate/2);
        if flag:
            #print("car id: %d, max road: %d, at index: %d, redirecting from: %d, and next: %d"%(self.id,maxbusyroad,self.route.index(maxbusyroad),fromnode,tonode));
            endnode = self.destination;
            tempmatrix = fsrinstance.nodeMatrix;

            fromnindex = fsrinstance.crossid_list.index(fromnode);
            tonindex = fsrinstance.crossid_list.index(tonode);

            tempmatrix[fromnindex][tonindex] = [0,0];
            #print(fsrinstance.nodeMatrix[fromnode-1][tonode-1]);
            #print(tempmatrix[fromnode-1][tonode-1]);
            [replaceroute,replacenodes] = fsrinstance.findredirection(fromnode,endnode,tempmatrix);
            newroute = [];
            for i in range(self.route.index(maxbusyroad)):
                newroute.append(self.route[i]);
            for road in replaceroute:
                newroute.append(road);

            oldroute = self.route;
            self.route = newroute;

            newroutenodes = [];
            for i in range(self.routenodes.index(fromnode)):
                newroutenodes.append(self.routenodes[i]);
            for node in replacenodes:
                newroutenodes.append(node);

            [newroute_c,newroutenodes_c] = self.turnningbackcheck(newroute,newroutenodes);

            oldroutenodes = self.routenodes;
            self.routenodes = newroutenodes;

            newschedule = self.caltimeschedule(time,roadlist,nodelist,fsrinstance);
            [maxbusyrate_new,maxbusyroad_new,fromnode_new,tonode_new,difftomin_new,avgrate_new,difftosec_new] = self.calredirpara();

            #print("max busyrate reduced: %s, diff to min reduced: %s, average rate rised: %s"%(maxbusyrate_new<maxbusyrate,difftomin_new<difftomin,avgrate_new>avgrate));

            if (maxbusyrate_new < maxbusyrate)and(difftomin_new<difftomin)and(avgrate_new>avgrate)and(difftosec_new<difftosec):
                #print("Redirection accepted!!!!!");
                self.route = newroute_c;
                self.routenodes = newroutenodes_c;
            else:
                self.route = oldroute;
                self.routenodes = oldroutenodes;
                self.timeschedule = oldschedule;
                #self.caltimeschedule(time,roadlist,nodelist);
                #print("Redirection unacceptable");

    def turnningbackcheck(self,newroute,newroutenodes):
        i = 0;
        newroute_c = newroute;
        newroutenodes_c = newroutenodes;
        while i < len(newroute)-1:
            if newroute_c[i] == newroute_c[i+1]:
                del newroute_c[i];
                del newroute_c[i];
                del newroutenodes_c[i];
                del newroutenodes_c[i];
                i = i - 1;
            else:
                i = i + 1;
        
        return [newroute_c,newroutenodes_c];


class Cross:
    def __init__(self,crossinfo):
        super().__init__();
        self.initcross(crossinfo);

    def initcross(self,crossinfo):
        self.id = crossinfo[0];
        self.north = crossinfo[1];
        self.east = crossinfo[2];
        self.south = crossinfo[3];
        self.west = crossinfo[4];
        self.roadssequence = crossinfo;

        self.lastnode = 0;
        self.nextnodes = [];
        self.roadsnum = 0;

        self.nextnodesforredir = [];

    def calcrossbusyrate(self,time,roadlist,fsrinstance):
        if self.north != -1:
            nroadindex = fsrinstance.roadid_list.index(self.north);
            northroad = roadlist[nroadindex];
            if time <= len(northroad.busyrate[0]):
                northbusyfor = northroad.busyrate[0][time-1];
            else:
                northbusyfor = 0;

            if time <= len(northroad.busyrate[1]):
                northbusyback = northroad.busyrate[1][time-1];
            else:
                northbusyback = 0;

            northbusy = (northbusyfor + northbusyback)/2;
            self.roadsnum = self.roadsnum + 1;
        else:
            northbusy = 0;

        if self.east != -1:    
            eroadindex = fsrinstance.roadid_list.index(self.east);
            eastroad = roadlist[eroadindex];
            if time <= len(eastroad.busyrate[0]):
                eastbusyfor = eastroad.busyrate[0][time-1];
            else:
                eastbusyfor = 0;

            if time <= len(eastroad.busyrate[1]):
                eastbusyback = eastroad.busyrate[1][time-1];
            else:
                eastbusyback = 0;

            eastbusy = (eastbusyfor + eastbusyback)/2;
            self.roadsnum = self.roadsnum + 1;
        else:
            eastbusy = 0;

        if self.south != -1:
            sroadindex = fsrinstance.roadid_list.index(self.south);
            southroad = roadlist[sroadindex];
            if time <= len(southroad.busyrate[0]):
                southbusyfor = southroad.busyrate[0][time-1];
            else:
                southbusyfor = 0;

            if time <= len(southroad.busyrate[1]):
                southbusyback = southroad.busyrate[1][time-1];
            else:
                southbusyback = 0;

            southbusy = (southbusyfor + southbusyback)/2;
            self.roadsnum = self.roadsnum + 1;
        else:
            southbusy = 0;

        if self.west != -1:
            wroadindex = fsrinstance.roadid_list.index(self.west);
            westroad = roadlist[wroadindex];
            if time <= len(westroad.busyrate[0]):
                westbusyfor = westroad.busyrate[0][time-1];
            else:
                westbusyfor = 0;

            if time <= len(westroad.busyrate[1]):
                westbusyback = westroad.busyrate[1][time-1];
            else:
                westbusyback = 0;

            westbusy = (westbusyfor + westbusyback)/2;
            self.roadsnum = self.roadsnum + 1;
        else:
            westbusy = 0;

        if self.roadsnum != 0:
            crossbusy = (northbusy + eastbusy + southbusy + westbusy)/self.roadsnum;
        else:
            crossbusy = 0;

        return crossbusy;


class Road:
    def __init__(self,roadinfo):
        super().__init__();
        self.initroad(roadinfo);

    def initroad(self,roadinfo):
        self.id = roadinfo[0];
        self.lengthr = roadinfo[1];
        self.limitv = roadinfo[2];
        self.lanenum = roadinfo[3];
        self.originc = roadinfo[4];
        self.endc = roadinfo[5];
        self.ifbiway = roadinfo[6];

        self.mintime = int(roadinfo[1]/roadinfo[2]);
        self.maxcapacity = self.lanenum*self.lengthr;
        self.busyrate = [[],[]];
        self.diffcarnum = [[],[]];
        self.schedule = [[],[]];

    def enterroad(self,carid,entertime,leavetime,forbackflag):
        currenttimelen = len(self.schedule[forbackflag]);
        while currenttimelen < leavetime:
            self.schedule[forbackflag].append([]);
            self.busyrate[forbackflag].append(0);
            self.diffcarnum[forbackflag].append(0);
        
        for time in range(entertime,leavetime):
            self.schedule[forbackflag][time-1].append(carid);
            currentcarnum = len(self.schedule[forbackflag][time-1]);
            self.busyrate[forbackflag][time-1] = currentcarnum/self.maxcapacity;

        return self.busyrate;

    def caldiffcars(self,forbackflag):
        for i in range(len(self.busyrate[forbackflag])):
            if i == 0:
                self.diffcarnum[forbackflag][i] = len(self.schedule[forbackflag][i]);
            elif i > 0:
                lastcarnum = len(self.schedule[forbackflag][i-1]);
                currentcarnum = len(self.schedule[forbackflag][i]);
                self.diffcarnum[forbackflag][i] = currentcarnum - lastcarnum;

        return self.diffcarnum;

    def enterflag(self,entertime,leavetime,forbackflag):
        currenttimelen = len(self.schedule[forbackflag]);
        while currenttimelen < leavetime:
            self.schedule[forbackflag].append([]);
            self.busyrate[forbackflag].append(0);
            self.diffcarnum[forbackflag].append(0);
            currenttimelen = len(self.schedule[forbackflag]);

        self.caldiffcars(forbackflag);
        thisflags = [];
        runtime = entertime-leavetime;
        for time in range(entertime,leavetime):
            #print("entertime: %d"%(entertime));
            #print("leavetime: %d"%(leavetime));
            #print("time: %d"%(time));
            #print("forbackflag: %d"%(forbackflag));
            currentcars = self.schedule[forbackflag][time-1];
            currentbusyrate = self.busyrate[forbackflag][time-1];
            thisflags.append(currentbusyrate);

        enterdiff = self.diffcarnum[forbackflag][entertime-1];

        if max(thisflags) > roadentermax:
            flag = False;
        elif max(thisflags) < roadenterdiff:
            flag = True;
        elif enterdiff < 0:
            flag = True;
        else:
            flag = False;

        return flag;

    def getbusyrate(self,time,forbackflag):
        busyrate = 0;
        if time > len(self.busyrate[forbackflag]):
            busyrate = 0;
        else:
            busyrate = self.busyrate[forbackflag][time-1];

        return busyrate;


class FindSRoute:
    def __init__(self,cars,crosses,roads):
        super().__init__();
        self.initmap(cars,crosses,roads);

    def initmap(self,cars,crosses,roads):
        self.cars_list = [];
        self.cross_list = [];
        self.roads_list = [];

        self.crossid_list = [];
        self.roadid_list = [];

        for carinfo in cars:
            tempcar = Car(carinfo);
            self.cars_list.append(tempcar);

        for crossinfo in crosses:
            tempcross = Cross(crossinfo);
            self.crossid_list.append(tempcross.id);
            self.cross_list.append(tempcross);

        for roadinfo in roads:
            temproad = Road(roadinfo);
            self.roadid_list.append(temproad.id);
            self.roads_list.append(temproad);

        self.nodesnum = len(crosses);
        self.nodeMatrix = [[[0,0] for i in range(self.nodesnum)] for j in range(self.nodesnum)];

        for road in self.roads_list:
            temproadid = road.id;
            temporigin = road.originc;
            tempend = road.endc;
            templength = road.lengthr;
            tempmintime = road.mintime;
            tempbiway = road.ifbiway;
            startnodeindex = self.crossid_list.index(temporigin);
            endnodeindex = self.crossid_list.index(tempend);
            self.nodeMatrix[startnodeindex][endnodeindex][0] = tempmintime;
            self.nodeMatrix[startnodeindex][endnodeindex][1] = temproadid;
            if tempbiway == 1:
                self.nodeMatrix[endnodeindex][startnodeindex][0] = tempmintime;
                self.nodeMatrix[endnodeindex][startnodeindex][1] = temproadid;

        #print(self.nodeMatrix);

    def findnearnode(self):
        for node in self.cross_list:
            rownum = self.crossid_list.index(node.id);
            for nextn in self.nodeMatrix[rownum]:
                if nextn[0] != 0:
                    nearindex = self.nodeMatrix[rownum].index(nextn);
                    nearid = self.cross_list[nearindex].id;
                    nearmintime = nextn[0];
                    nearroadid = nextn[1];
                    nearinfo = [nearid,nearmintime,nearroadid];
                    node.nextnodes.append(nearinfo);

            #print(node.id);
            #print(node.nextnodes);

    def findrouteMatrix(self):
        self.routeMrtix = [[[] for i in range(len(self.cross_list))] for i in range(len(self.cross_list))];
        self.noderouteMatrix = [[[] for i in range(len(self.cross_list))] for i in range(len(self.cross_list))];
        for nodestart in self.cross_list:
            rownum = self.crossid_list.index(nodestart.id);
            for nodeend in self.cross_list:
                columnum = self.crossid_list.index(nodeend.id);

                self.cross_list[rownum].lastnode = 0;
                currentnode = self.cross_list[rownum];
                opennode = [];
                closenode = [];
                opennode.append(currentnode);
                while(len(opennode) != 0):
                    currentnode = opennode.pop(0);
                    if currentnode.id != nodeend.id:
                        # if currentnode.id < nodestart.id:
                        #     cnodeindex = self.crossid_list.index(currentnode.id);
                        #     restroute = self.noderouteMatrix[cnodeindex][columnum];
                        #     for nodeid in restroute:
                        #         if restroute.index(nodeid) != 0:
                        #             nodeinsindex = self.crossid_list.index(nodeid);
                        #             nodeinstance = self.cross_list[nodeinsindex];
                        #             nodeinstance.lastnode = currentnode.id;
                        #             currentnode = nodeinstance;

                        #     break;

                        for obj in currentnode.nextnodes:
                            nextnindex = self.crossid_list.index(obj[0]);
                            nextn = self.cross_list[nextnindex];
                            closedflag = nextn.id;
                            if closedflag not in closenode:
                                nextn.lastnode = currentnode.id;
                                opennode.append(nextn);
                        closenode.append(currentnode.id);
                    elif currentnode.id == nodeend.id:
                        break;

                nodelist = [];
                nodelist.append(currentnode);
                while currentnode.lastnode != 0:
                    lastnodeindex = self.crossid_list.index(currentnode.lastnode);
                    lastn = self.cross_list[lastnodeindex];
                    nodelist.append(lastn);
                    currentnode = lastn;
                nodelist.reverse();

                nodeidlist = [];
                for node in nodelist:
                    nodeidlist.append(node.id);
                self.noderouteMatrix[rownum][columnum] = nodeidlist;

                for node in nodelist:
                    nextindex = nodelist.index(node) + 1;
                    if nextindex < len(nodelist):
                        nextid = nodelist[nextindex].id;
                        for obj in node.nextnodes:
                            if obj[0] == nextid:
                                thisroad = obj[2];
                                self.routeMrtix[rownum][columnum].append(thisroad);

                print([rownum,columnum]);
                print(self.routeMrtix[rownum][columnum]);

        print("Find all route Done!");
        #print(self.routeMrtix);

    def findroutebylist(self,car):
        startp = car.departure;
        endp = car.destination;

        startindex = self.crossid_list.index(startp);
        endindex = self.crossid_list.index(endp);

        car.shortroute = self.routeMrtix[startindex][endindex];
        #print(car.shortroute);
        car.route = car.shortroute;
        car.routenodes = self.noderouteMatrix[startindex][endindex];
        return car.shortroute;

    def findoneroute(self,car):
        startp = car.departure;
        endp = car.destination;
        #print("start: %s; destination: %s" %(startp,endp));

        startindex = self.crossid_list.index(startp);
        endindex = self.crossid_list.index(endp);

        self.cross_list[startindex].lastnode = 0;
        currentnode = self.cross_list[startindex];
        opennode = [];
        closenode = [];
        opennode.append(currentnode);
        #i = 0;
        while(len(opennode) != 0):
            currentnode = opennode.pop(0);
            if currentnode.id != endp:
                for obj in currentnode.nextnodes:
                    nextnindex = self.crossid_list.index(obj[0]);
                    nextn = self.cross_list[nextnindex];
                    closedflag = nextn.id;
                    if closedflag not in closenode:
                        nextn.lastnode = currentnode.id;
                        opennode.append(nextn);
                closenode.append(currentnode.id);
            elif currentnode.id == endp:
                break;

        nodelist = [];
        nodelist.append(currentnode);
        while currentnode.lastnode != 0:
            lastnodeindex = self.crossid_list.index(currentnode.lastnode);
            lastn = self.cross_list[lastnodeindex];
            nodelist.append(lastn);
            currentnode = lastn;
        nodelist.reverse();
        
        nodeidlist = [];
        for node in nodelist:
            nodeidlist.append(node.id);
        #print(nodeidlist);

        for node in nodelist:
            nextindex = nodelist.index(node) + 1;
            if nextindex < len(nodelist):
                nextid = nodelist[nextindex].id;
                for obj in node.nextnodes:
                    if obj[0] == nextid:
                        thisroad = obj[2];
                        car.shortroute.append(thisroad);

        #print(car.shortroute);
        car.route = car.shortroute;
        car.routenodes = nodeidlist;
        return car.shortroute;

    def findnearnodefordirection(self,tempMatrix):
        for node in self.cross_list:
            rownum = self.crossid_list.index(node.id);
            node.nextnodesforredir = [];
            for nextn in tempMatrix[rownum]:
                if nextn[0] != 0:
                    nearindex = tempMatrix[rownum].index(nextn);
                    nearid = self.cross_list[nearindex].id;
                    nearmintime = nextn[0];
                    nearroadid = nextn[1];
                    nearinfo = [nearid,nearmintime,nearroadid];
                    node.nextnodesforredir.append(nearinfo);
    
    def findredirection(self,fromnode,tonode,tempMatrix):
        startp = fromnode;
        endp = tonode;
        redirectedroute = [];
        redirectednodes = [];
        #print("start: %s; destination: %s" %(startp,endp));

        self.findnearnodefordirection(tempMatrix);

        startindex = self.crossid_list.index(startp);
        endindex = self.crossid_list.index(endp);

        self.cross_list[startindex].lastnode = 0;
        currentnode = self.cross_list[startindex];
        opennode = [];
        closenode = [];
        opennode.append(currentnode);
        #i = 0;
        while(len(opennode) != 0):
            currentnode = opennode.pop(0);
            if currentnode.id != endp:
                for obj in currentnode.nextnodesforredir:
                    nextnindex = self.crossid_list.index(obj[0]);
                    nextn = self.cross_list[nextnindex];
                    closedflag = nextn.id;
                    if closedflag not in closenode:
                        nextn.lastnode = currentnode.id;
                        opennode.append(nextn);
                closenode.append(currentnode.id);
            elif currentnode.id == endp:
                break;

        nodelist = [];
        nodelist.append(currentnode);
        while currentnode.lastnode != 0:
            lastnindex = self.crossid_list.index(currentnode.lastnode);
            lastn = self.cross_list[lastnindex];
            nodelist.append(lastn);
            currentnode = lastn;
        nodelist.reverse();
        
        nodeidlist = [];
        for node in nodelist:
            nodeidlist.append(node.id);
        #print(nodeidlist);

        for node in nodelist:
            nextindex = nodelist.index(node) + 1;
            if nextindex < len(nodelist):
                nextid = nodelist[nextindex].id;
                for obj in node.nextnodesforredir:
                    if obj[0] == nextid:
                        thisroad = obj[2];
                        redirectedroute.append(thisroad);

        #print(car.shortroute);
        return [redirectedroute,nodeidlist];

    def findall(self):
        if len(self.cars_list) < self.nodesnum*self.nodesnum:
            for car in self.cars_list:
                car.shortroute = self.findoneroute(car);
        else:
            self.findrouteMatrix();
            for car in self.cars_list:
                car.shortroute = self.findroutebylist(car);

        print("Find all Done!");

    def outputinfo(self):
        return [self.cars_list,self.roads_list,self.cross_list];


class IterateDispatch:
    def __init__(self,carlist,crosslist,roadlist,fsrinstance):
        super().__init__();
        self.inititerrate(carlist,crosslist,roadlist,fsrinstance);

    def inititerrate(self,carlist,crosslist,roadlist,fsrinstance):
        self.currenttime = 1;
        self.departednum = 0;
        self.car_list = carlist;
        self.cross_list = crosslist;
        self.road_list = roadlist;
        self.totalcarnum = len(self.car_list);
        self.departedlist = [];

        connectMatrix = fsrinstance.nodeMatrix;

        self.car_list = sorted(self.car_list, key = lambda car: (-car.maxv, -car.crossnum, -car.crosspriority));

        self.carwaitinglist = self.car_list;
        while len(self.carwaitinglist) > 0:
            cari = 0;
            failed = 0;
            while cari < len(self.carwaitinglist):
                thiscar = self.carwaitinglist[cari];
                if self.currenttime >= thiscar.plant:
                    #thiscar.redirection(fsrinstance,self.currenttime,self.road_list,self.cross_list);
                    thisflag = thiscar.departflag(self.currenttime,self.road_list,self.cross_list,fsrinstance);
                    #print(thisflag);
                    if thisflag:
                        thiscar.depart(self.currenttime,self.road_list,fsrinstance);
                        self.departedlist.append(thiscar);
                        self.carwaitinglist.remove(thiscar);
                        self.departednum = self.departednum + 1;
                        thiscar.departed = True;
                        #print("current departed: %d, at time: %d, car: %d" %(self.departednum,self.currenttime,thiscar.id));
                    else:
                        cari = cari + 1;
                        failed = failed + 1;
                        #print("current chacking car: %d, of total car: %d, and departed: %d, time: %d" %(cari,self.totalcarnum,self.departednum,self.currenttime));

                    if failed >= 100:
                        cari = 0;
                        failed = 0;
                        self.currenttime = self.currenttime + 1;

                else:
                    cari = cari + 1;

            self.currenttime = self.currenttime + 1;
            #print("current time: %d" %(self.currenttime));

    def outputanswer(self):
        self.car_list = sorted(self.departedlist, key = lambda car: car.id, reverse = False);
        self.answer = [];
        for car in self.car_list:
            oneanswer = [];
            oneanswer.append(car.id);
            oneanswer.append(car.departtime);
            for road in car.shortroute:
                oneanswer.append(road);
            self.answer.append(oneanswer);

        return self.answer;
                    

# to write output file


def Start():
    readwrite = ReadandWrite();
    cars = readwrite.readCar();
    crosses = readwrite.readCross();
    roads = readwrite.readRoad();
    #testanswer = [[1001, 1, 501, 502, 503, 516, 506, 505, 518, 508, 509, 524],[1002, 1, 513, 504, 518, 508, 509, 524],[1003, 2, 513, 517, 507, 508, 509, 524]];
    #readwrite.writeAnswer(testanswer);
    findsroute = FindSRoute(cars,crosses,roads);
    findsroute.findnearnode();
    #findsroute.findrouteMatrix();
    #testcar = findsroute.cars_list[0];
    #testroute1 = findsroute.findoneroute(testcar);
    #testroute2 = findsroute.findroutebylist(testcar);
    #print(testcar.caltimeschedule(findsroute.roads_list,findsroute.cross_list));
    findsroute.findall();
    [processedcars,processedroads,processednodes] = findsroute.outputinfo();
    #print(processedcars[1].timeschedule);
    IDtruth = IterateDispatch(processedcars,processednodes,processedroads,findsroute);
    answer = IDtruth.outputanswer();
    readwrite.writeAnswer(answer);



if __name__ == "__main__":
    Start()
    main()