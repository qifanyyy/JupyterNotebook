#!/usr/bin/python3

# author:Administrator
# contact: SystemEngineer
# datetime:2020/6/8 16:42
# software: PyCharm

"""
Document description:
完成路由算法中的Bellman-Ford算法。
"""

import sys
import time


class DistanceVectorRoutingAlgorithm:
    def __init__(self):
        self.startFilePath = ""
        self.changeFilePath = ""
        self.state = ""

        self.nodeNameList = []
        self.allEdgesList = []
        self.distancesList = []
        self.allWeightTable = []
        self.allNeighborFlagTable = []
        self.outputInfoRecord = []
        self.startConfigInfo = []
        # self.chooseRouteInfo = []

        self.nodesCount = 0
        self.edgesCount = 0

    def readStartFileFromFile(self):
        """
        :param filePath:文件路径。
        :return:
        """
        # sefl.startFilePath
        with open("config0") as f:
            lines = f.readlines()

            for i in range(len(lines)):
                lines[i] = lines[i].strip("\n")

        self.nodesCount = int(lines[0])
        self.nodeNameList = lines[1:1 + int(self.nodesCount)]

        for i in range(len(self.nodeNameList)):
            self.nodeNameList[i] = self.nodeNameList[i].lower()

        self.edgesCount = int(lines[1 + int(self.nodesCount)])
        edgesList = lines[1 + int(self.nodesCount) + 1:]
        # print(nodesCount, edgesCount)
        # 定义所有节点的路由表。
        # 多维列表的初始化真是一个坑。第一种方法会导致修改一个，会改变整个列表的值。
        # allWeightTable = [[[0] * 3] * edgesCount]*nodesCount
        # allEdgesList = [[[0 for i in range(3)]for j in range(edgesCount)]for n in range(nodesCount)]
        self.allWeightTable = [[sys.maxsize for i in range(self.nodesCount)]for j in range(self.nodesCount)]
        # 枚举值，一共三种值。0表示是自己。1表示是直接邻居。2表示是非直接邻居。初始化全部设置为非直接邻居。
        self.allNeighborFlagTable = [[2 for i in range(self.nodesCount)]for j in range(self.nodesCount)]
        # outputInfoRecord = [["" for i in range(nodesCount + 1)]for j in range(4)]
        self.outputInfoRecord = [[""] for j in range(4)]
        self.startConfigInfo = [[sys.maxsize for i in range(self.nodesCount)]for j in range(self.nodesCount)]

        self.outputInfoRecord[0][0] = "#START"
        self.outputInfoRecord[1][0] = "#INITIAL"
        self.outputInfoRecord[2][0] = "#UPDATE"
        self.outputInfoRecord[3][0] = "#FINAL"

        for i in range(self.edgesCount):
            params = edgesList[i].split(" ")
            param0 = self.nodeNameList.index(params[0].lower())
            param1 = self.nodeNameList.index(params[1].lower())
            if params[2] == "inf":
                param2 = sys.maxsize
            else:
                param2 = int(params[2])
            
            self.allWeightTable[param0][param1] = param2
            self.allWeightTable[param1][param0] = param2
            self.allWeightTable[param0][param0] = 0
            self.allWeightTable[param1][param1] = 0

            self.startConfigInfo[param0][param1] = param2
            self.startConfigInfo[param1][param0] = param2
            self.startConfigInfo[param0][param0] = 0
            self.startConfigInfo[param1][param1] = 0

            self.allNeighborFlagTable[param0][param1] = 1
            self.allNeighborFlagTable[param1][param0] = 1
            self.allNeighborFlagTable[param0][param0] = 0
            self.allNeighborFlagTable[param1][param1] = 0

            self.recordOutputInfo("start", 0, param0, param1, param1, param2)


    def recordOutputInfo(self, title, step, source, destination, neighbor, distance):
        """

        :param title:
        :param step:
        :param source:
        :param destination:
        :param neighbor:
        :param distance:
        :return:
        """
        # 对于源节点本身不用显示。
        if source == destination:
            # print("source == destination")
            return 

        title = title.lower()
        sourceString = self.nodeNameList[source]
        destinationString = self.nodeNameList[destination]
        neighborString = self.nodeNameList[neighbor]

        if title == "start":
            self.outputInfoRecord[0].append("t=%d distance from %s to %s via %s is %d"
            %(step, sourceString, destinationString, neighborString, distance))
        elif title == "initial":
            self.outputInfoRecord[1].append("router %s: %s is %d routing through %s"
            %(sourceString, destinationString, distance, neighborString))
        elif title == "update":
            if distance != sys.maxsize:
                # 将距离为inf的隐藏起来，不显示。
                self.outputInfoRecord[2].append("t=%d distance from %s to %s via %s is %d"
                %(step, sourceString, destinationString, neighborString, distance))
        elif title == "final":
            self.outputInfoRecord[3].append("router %s: %s is %d routing through %s"
            %(sourceString, destinationString, distance, neighborString))

        else:
            print(title)
            print("ERROR")


    def BellmanFord(self):
        """

        :return:
        """
        for n in range(self.nodesCount):
            # if n == 0:
            #     print("#" + "initial".upper())
            for m in range(self.nodesCount):
                # time.sleep(0.3)
                if n == m:
                    # 如果是源节点自己，那么该节点的cost为0。
                    self.allWeightTable[n][m] = 0

                # 初始化tempDistanceList缓存路径cost的列表，用于最后的比较。
                # 每个下标对应一个节点，表示源节点到对应下标节点的cost。
                # 理论上可以是全连接网络。也就是每个节点都和所有节点相连。所以初始化tempDistanceList长度为所有节点的数量。
                # tempDistanceList是用于计算时缓存用的，计算之后的结果才填写到allWeightTable里面。
                tempDistanceList = [sys.maxsize for i in range(self.nodesCount)]
                tempRoutingList = [sys.maxsize for i in range(self.nodesCount)]
                neighborTempRecord = -1

                # 将所有路径的cost存放到tempDistanceList中。将对应的距离选择的直接邻居存放到tempRoutingList中。
                for neighborIndex in range(self.nodesCount):
                    # 只选通过直接邻居作为出口来计算的最小路径cost。
                    if self.allNeighborFlagTable[n][neighborIndex] == 1:
                        tempRoutingList[neighborIndex] = neighborIndex
                        tempDistanceList[neighborIndex] = self.allWeightTable[n][neighborIndex] + self.allWeightTable[neighborIndex][m]
                        # if tempDistanceList[neighborIndex] < sys.maxsize:
                        #     recordOutputInfo("start", nodeNameList, 1, n, m, neighborIndex, tempDistanceList[neighborIndex], outputInfoRecord)
                # 如果是自己，那么不用计算，直接是0。
                if n == m:
                    self.allWeightTable[n][m] = 0
                else:
                    # 如果计算的到达直接邻居的所有路径cost的最小值还大于直接邻居直连的cost，那么就用直连的cost。
                    if min(tempDistanceList) > self.startConfigInfo[n][m]:
                        self.allWeightTable[n][m] = self.startConfigInfo[n][m]
                        neighborTempRecord = m
                    else:
                        # 其他情况取最小值。
                        self.allWeightTable[n][m] = min(tempDistanceList)
                        neighborTempRecord = tempRoutingList[tempDistanceList.index(min(tempDistanceList))]
                    # chooseRouteInfo[n][m] = neighborTempRecord
                
                # 进行记录。
                if self.state == "start":
                    self.recordOutputInfo("start", 1, n, m, neighborTempRecord, self.allWeightTable[n][m])
                    self.recordOutputInfo("initial", 0, n, m, neighborTempRecord, self.allWeightTable[n][m])
                if self.state == "change":
                    self.recordOutputInfo("update", n, n, m, neighborTempRecord, self.allWeightTable[n][m])
                    self.recordOutputInfo("final", 0, n, m, neighborTempRecord, self.allWeightTable[n][m])



    def recordWriteToFile(self):
        """

        :return:
        """
        with open("output1", "w") as f:
            for n in range(4):
                for m in range(len(self.outputInfoRecord[n])):
                    # print(outputInfoRecord[n][m])
                    f.write(self.outputInfoRecord[n][m] + "\n")


    def readChangeFileFromFile(self):
        # self.changeFilePath
        with open("changeConfig0") as f:
            lines = f.readlines()

            for i in range(len(lines)):
                lines[i] = lines[i].strip("\n")
        
        modifyCount = int(lines[0])
        modifyList = lines[1:]

        for i in range(modifyCount):
            params = modifyList[i].split(" ")
            # print(params)
            param0 = self.nodeNameList.index(params[0].lower())
            param1 = self.nodeNameList.index(params[1].lower())

            if params[2] == "inf":
                param2 = sys.maxsize
            else:
                param2 = int(params[2])

            # 这里只修改权重，没有新增节点或者删除节点，所以不用修改self.allNeighborFlagTable中的内容。
            self.allWeightTable[param0][param1] = param2
            self.allWeightTable[param1][param0] = param2

            self.startConfigInfo[param0][param1] = param2
            self.startConfigInfo[param1][param0] = param2

            self.recordOutputInfo("update", 0, param0, param1, param1, param2)

        # 如果重新读取路径耗费文件，那么需要将allWeightTable表重置。
        for n in range(self.nodesCount):
            for m in range(self.nodesCount):
                if self.startConfigInfo[n][m] < sys.maxsize:
                    self.allWeightTable[n][m] = self.startConfigInfo[n][m]
            

if __name__ == '__main__':

    dv = DistanceVectorRoutingAlgorithm()

    dv.state = "start"
    dv.startFilePath = ""
    dv.readStartFileFromFile()
    # print(dv.allWeightTable)
    # print(dv.allNeighborFlagTable)

    # 定义所有节点到其他节点的距离。
    # 实际使用时的情况如下：
    # 1. 初始化的矩阵为nodesCount*nodesCount维度。
    # 2. 自己到自己的距离初始化为0，也固定下来。
    # 3. 初始化的值都是最大int值。
    # 4. 首先初始化为当前节点和直接相连的节点的距离。
    # 5. 收到邻居节点更新的信息。
    # 6. 当前节点计算。
    # 7. 变化发出通知，没有变化不通知。
    # 
    
    dv.BellmanFord()
    print(dv.allWeightTable)
    # print(dv.startConfigInfo)
    # print(outputInfoRecord)

    dv.state = "change"
    dv.readChangeFileFromFile()
    dv.BellmanFord()
    # print("----------------")
    print(dv.allWeightTable)
    # print(dv.startConfigInfo)

    # for n in range(dv.nodesCount):
    #     for i in range(dv.nodesCount):
    #         if dv.allNeighborFlagTable[n][i] == True:
    #             dv.recordOutputInfo("final", 0, n, i, i, dv.allWeightTable[n][i])

    dv.recordWriteToFile()
    print("Completed.")

