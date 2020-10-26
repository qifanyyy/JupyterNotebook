# Created by Marcin Wilk - BSD License

from dijkstra import dijkstra,dijkstra_all
from graph import graph,graph_shapes
from time import time
from psim import PSim
import random 

def dijkstra_p(g,source,p):
    """
    PYsim parallel implementation of dijkstra's algorithm
    Result: One source shourtest paths to all nodes
    Implementation parallelizes finding minimums and 
    updating the results (inner loop is parallelized)
    Uses the method of collecting of intermediate minimums and 
    broadcasting of newly found path to all processes
    """
    # Initialize communicator
    comm=PSim(p)
    myRank=comm.rank
    chunkSize=len(g)/p

    # Scatter the graph by partitioning it one dimensionally, 
    # along with known distances to source, and remaining node information
    myGraphChunk = comm.one2all_scatter(0,g)
    localResultView=comm.one2all_scatter(0,g[source])
    localRemainView= comm.one2all_scatter(0,g[source])

    # Each process will iterate q times, where q is number of nodes in graph
    for q in range(len(g)):
        # Get shortest path to locally un-visited nodes 
        lowestLocalDist=min(localRemainView)
        lowestLocalDistIdx=localRemainView.index(lowestLocalDist)

        # Collect the lowest distances and node indexes from all processes
        gatheredCandidatesDist=comm.all2one_collect(0,lowestLocalDist)
        gatheredCandidatesIdxs=comm.all2one_collect(0,lowestLocalDistIdx+myRank*chunkSize)
        
        processWithLowestDist=-1
        addedNodeIdx=-1
        lowestOverallDistance=-1

        # One 'main' process finds the global minimum
        if myRank==0:
            lowestOverallDistance=min(gatheredCandidatesDist)
            processWithLowestDist=gatheredCandidatesDist.index(lowestOverallDistance)
            addedNodeIdx=gatheredCandidatesIdxs[processWithLowestDist]

        # 'Main' process broadcasts the finding to all processes
        receivedBroadcast = \
            comm.one2all_broadcast(0,\
            (processWithLowestDist,addedNodeIdx,lowestOverallDistance,))
        
        # If this process is responsible for the newly found shortest path,
        # then mark this node as visited.
        if myRank==receivedBroadcast[0]:
            indexToUpdate=receivedBroadcast[1]-myRank*chunkSize
            localRemainView[indexToUpdate]=''

        # Each process loop over all connections to this last visited node
        # that they have the visibility to.
        for iter in range(len(localResultView)):
            potentialNewDistance = \
                    myGraphChunk[iter][receivedBroadcast[1]]+receivedBroadcast[2]
            # If the distances through this node are less than what we know
            if potentialNewDistance < localResultView[iter]:
                # Update the local portion of the result list and 
                # remaining nodes list
                localResultView[iter]=potentialNewDistance
                localRemainView[iter]=potentialNewDistance

    # Reduce the final result to a single list and return it
    reassembled=comm.all2one_reduce(0,localResultView)
    if myRank==0:
        return reassembled
    else:
        return []

if __name__=="__main__":
    # Unit test, compared against the linear version of the algorithm
    p=32
    g=graph(256,max_edge=10000,shape=graph_shapes.FULL).matrix

    i=random.randint(0,len(g)-1)
    time1=time()
    expected=dijkstra(g,i)
    time2=time()
    print "Linear execution time: ",time2-time1," seconds."
    timeA=time()
    result=dijkstra_p(g,i,p)
    if(result!=[]):
        timeB=time()    
        assert(expected==result)
        print "Parallel execution time: ",timeB-timeA," seconds."
