import Features
import pyodbc
import uuid
import multiprocessing as mp
from joblib import Parallel, delayed


def ExtractFeature(row):    
    instanceFeature = Features.Features(row.Path)

    conn2 = pyodbc.connect("Driver={SQL Server};Server=.\SQLEXPRESS;Trusted_Connection=yes;database=GraphColoringPortfolio")
    cursor2 = conn2.cursor()

    ############################################################################################# Nodes, Edges and Density Features
    #cursor2.execute("SELECT * FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #NumberOfNodes = instanceFeature.NumberOfNodes()
    #NumberOfEdges = instanceFeature.NumberOfEdges()
    #RatioNodesEdges = instanceFeature.RatioNodesEdges()
    #RatioEdgesNodes = instanceFeature.RatioEdgesNodes()
    #Density = instanceFeature.Density()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, numberofnodes, numberofedges, rationodesedges, ratioedgesnodes, density) values (?, ?, ?, ?, ?, ?, ?)",
    #                   str(pk), row.Id, NumberOfNodes, NumberOfEdges, RatioNodesEdges, RatioEdgesNodes, Density)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET numberofnodes=?, numberofedges=?, rationodesedges=?, ratioedgesnodes=?, density=? where GraphID=?",
    #                    NumberOfNodes, NumberOfEdges, RatioNodesEdges, RatioEdgesNodes, Density, existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################## Degree Centrality Features
    #cursor2.execute("SELECT * FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #instanceFeature.ComputeDegree()
    #MinDegree = instanceFeature.MinDegree()
    #MaxDegree = instanceFeature.MaxDegree()
    #MeanDegree = instanceFeature.MeanDegree()
    #StdDegree = instanceFeature.StdDegree()
    #VcDegree = instanceFeature.VcDegree()
    #MedianDegree = instanceFeature.MedianDegree()
    #Q1Degree = instanceFeature.Q1Degree()
    #Q3Degree = instanceFeature.Q3Degree()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, mindegree, maxdegree, meandegree, stddegree, vcdegree, mediandegree, q1degree, q3degree) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #                   str(pk), row.Id, MinDegree, MaxDegree, MeanDegree, StdDegree, VcDegree, MedianDegree, Q1Degree, Q3Degree)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET mindegree=?, maxdegree=?, meandegree=?, stddegree=?, vcdegree=?, mediandegree=?, q1degree=?, q3degree=? where GraphID=?",
    #                    MinDegree, MaxDegree, MeanDegree, StdDegree, VcDegree, MedianDegree, Q1Degree, Q3Degree, existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################## Betweenness Centrality Features
    #cursor2.execute("SELECT * FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #instanceFeature.ComputeBtwnsCentrality()
    #MinBtwnsCentrality = instanceFeature.MinBtwnsCentrality()
    #MaxBtwnsCentrality = instanceFeature.MaxBtwnsCentrality()
    #MeanBtwnsCentrality = instanceFeature.MeanBtwnsCentrality()
    #StdBtwnsCentrality = instanceFeature.StdBtwnsCentrality()
    #VcBtwnsCentrality = instanceFeature.VcBtwnsCentrality()
    #MedianBtwnsCentrality = instanceFeature.MedianBtwnsCentrality()
    #Q1BtwnsCentrality = instanceFeature.Q1BtwnsCentrality()
    #Q3BtwnsCentrality = instanceFeature.Q3BtwnsCentrality()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, minbtwns, maxbtwns, meanbtwns, stdbtwns, vcbtwns, medianbtwns, q1btwns, q3btwns) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #                   str(pk), row.Id, MinBtwnsCentrality, MaxBtwnsCentrality, MeanBtwnsCentrality, StdBtwnsCentrality, VcBtwnsCentrality, MedianBtwnsCentrality, Q1BtwnsCentrality, Q3BtwnsCentrality)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET minbtwns=?, maxbtwns=?, meanbtwns=?, stdbtwns=?, vcbtwns=?, medianbtwns=?, q1btwns=?, q3btwns=? where GraphID=?",
    #                    MinBtwnsCentrality, MaxBtwnsCentrality, MeanBtwnsCentrality, StdBtwnsCentrality, VcBtwnsCentrality, MedianBtwnsCentrality, Q1BtwnsCentrality, Q3BtwnsCentrality, existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################## Closeness Centrality Features
    ##cursor2.execute("SELECT * FROM InstancesFeatures WHERE GraphID=?",row.Id)
    ##existingInstance = cursor2.fetchone()
    ##instanceFeature.ComputeCloseness()
    ##MinCloseness = instanceFeature.MinClosenessCentrality()
    ##MaxCloseness = instanceFeature.MaxClosnessCentrality()
    ##MeanCloseness = instanceFeature.MeanClosenessCentrality()
    ##StdCloseness = instanceFeature.StdClosenessCentrality()
    ##VcCloseness = instanceFeature.VcClosenessCentrality()
    ##MedianCloseness = instanceFeature.MedianClosenessCentrality()
    ##Q1Closeness = instanceFeature.Q1ClosenessCentrality()
    ##Q3Closeness = instanceFeature.Q3ClosenessCentrality()
    ##if (existingInstance==None) :
    ##    pk = uuid.uuid4()
    ##    cursor2.execute("insert into InstancesFeatures(Id, GraphID, mincloseness, maxcloseness, meancloseness, stdcloseness, vccloseness, mediancloseness, q1closeness, q3closeness) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    ##                   str(pk), row.Id, MinCloseness, MaxCloseness, MeanCloseness, StdCloseness, VcCloseness, MedianCloseness, Q1Closeness, Q3Closeness)
    ##else :
    ##    cursor2.execute("UPDATE InstancesFeatures SET mincloseness=?, maxcloseness=?, meancloseness=?, stdcloseness=?, vccloseness=?, mediancloseness=?, q1closeness=?, q3closeness=? where GraphID=?",
    ##                    MinCloseness, MaxCloseness, MeanCloseness, StdCloseness, VcCloseness, MedianCloseness, Q1Closeness, Q3Closeness, existingInstance.GraphID)
    ##conn2.commit()

    ############################################################################################## Eigenvector Centrality Features
    #cursor2.execute("SELECT * FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #instanceFeature.ComputeEgvCentrality()
    #MinEgvCentrality = instanceFeature.MinEgvCentrality()
    #MaxEgvCentrality = instanceFeature.MaxEgvCentrality()
    #MeanEgvCentrality = instanceFeature.MeanEgvCentrality()
    #StdEgvCentrality = instanceFeature.StdEgvCentrality()
    #VcEgvCentrality = instanceFeature.VcEgvCentrality()
    #MedianEgvCentrality = instanceFeature.MedianEgvCentrality()
    #Q1EgvCentrality = instanceFeature.Q1EgvCentrality()
    #Q3EgvCentrality = instanceFeature.Q3EgvCentrality()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, minegvcentrality, maxegvcentrality, meanegvcentrality, stdegvcentrality, vcegvcentrality, medianegvcentrality, q1egvcentrality, q3egvcentrality) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #                   str(pk), row.Id, MinEgvCentrality, MaxEgvCentrality, MeanEgvCentrality, StdEgvCentrality, VcEgvCentrality, MedianEgvCentrality, Q1EgvCentrality, Q3EgvCentrality)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET minegvcentrality=?, maxegvcentrality=?, meanegvcentrality=?, stdegvcentrality=?, vcegvcentrality=?, medianegvcentrality=?, q1egvcentrality=?, q3egvcentrality=? where GraphID=?",
    #                    MinEgvCentrality, MaxEgvCentrality, MeanEgvCentrality, StdEgvCentrality, VcEgvCentrality, MedianEgvCentrality, Q1EgvCentrality, Q3EgvCentrality, existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################## Eccentricity Features
    #cursor2.execute("SELECT * FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #instanceFeature.ComputeEccentricity()
    #MinEccentricity = instanceFeature.MinEccentricity()
    #MaxEccentricity = instanceFeature.MaxEccentricity()
    #MeanEccentricity = instanceFeature.MeanEccentricity()
    #StdEccentricity = instanceFeature.StdEccentricity()
    #VcEccentricity = instanceFeature.VcEccentricity()
    #MedianEccentricity = instanceFeature.MedianEccentricity()
    #Q1Eccentricity = instanceFeature.Q1Eccentricity()
    #Q3Eccentricity = instanceFeature.Q3Eccentricity()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, mineccentricity, maxeccentricity, meaneccentricity, stdeccentricity, vceccentricity, medianeccentricity, q1eccentricity, q3eccentricity) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #                   str(pk), row.Id, MinEccentricity, MaxEccentricity, MeanEccentricity, StdEccentricity, VcEccentricity, MedianEccentricity, Q1Eccentricity, Q3Eccentricity)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET mineccentricity=?, maxeccentricity=?, meaneccentricity=?, stdeccentricity=?, vceccentricity=?, medianeccentricity=?, q1eccentricity=?, q3eccentricity=? where GraphID=?",
    #                    MinEccentricity, MaxEccentricity, MeanEccentricity, StdEccentricity, VcEccentricity, MedianEccentricity, Q1Eccentricity, Q3Eccentricity, existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################# Clustering Features
    #cursor2.execute("SELECT GraphID FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #instanceFeature.ComputeClustering()
    #MinClustering = instanceFeature.MinClustering()
    #MaxClustering = instanceFeature.MaxClustering()
    #MeanClustering = instanceFeature.MeanClustering()
    #StdClustering = instanceFeature.StdClustering()
    #VcClustering = instanceFeature.VcClustering()
    #MedianClustering = instanceFeature.MedianClustering()
    #Q1Clustering = instanceFeature.Q1Clustering()
    #Q3Clustering = instanceFeature.Q3Clustering()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, minlocalclustering, maxlocalclustering, meanlocalclustering, stdlocalclustering, vclocalclustering, medianlocalclustering, q1clustering, q3clustering) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #                   str(pk), row.Id, MinClustering, MaxClustering, MeanClustering, StdClustering, VcClustering, MedianClustering, Q1Clustering, Q3Clustering)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET minlocalclustering=?, maxlocalclustering=?, meanlocalclustering=?, stdlocalclustering=?, vclocalclustering=?, medianlocalclustering=?, q1clustering=?, q3clustering=? where GraphID=?",
    #                    MinClustering, MaxClustering, MeanClustering, StdClustering, VcClustering, MedianClustering, Q1Clustering, Q3Clustering, existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################# Weighted Clustering Features
    #instanceFeature.ComputeWeightedClustering()
    #MinWeightedClustering = instanceFeature.MinWeightedClustering()
    #MaxWeightedClustering = instanceFeature.MaxWeightedClustering()
    #MeanWeightedClustering = instanceFeature.MeanWeightedClustering()
    #StdWeightedClustering = instanceFeature.StdWeightedClustering()
    #VcWeightedClustering = instanceFeature.VcWeightedClustering()
    #MedianWeightedClustering = instanceFeature.MedianWeightedClustering()
    #Q1WClustering = instanceFeature.Q1WeightedClustering()
    #Q3WClustering = instanceFeature.Q3WeightedClustering()
    #cursor2.execute("SELECT GraphID FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, minlocalwclustering, maxlocalwclustering, meanlocalwclustering, stdlocalwclustering, vclocalwclustering, medianlocalwclustering, q1wclustering, q3wclustering) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #                   str(pk), row.Id, MinWeightedClustering, MaxWeightedClustering, MeanWeightedClustering, StdWeightedClustering, VcWeightedClustering, MedianWeightedClustering, Q1WClustering, Q3WClustering)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET minlocalwclustering=?, maxlocalwclustering=?, meanlocalwclustering=?, stdlocalwclustering=?, vclocalwclustering=?, medianwclustering=?, q1wclustering=?, q3wclustering=? where GraphID=?",
    #                    MinWeightedClustering, MaxWeightedClustering, MeanWeightedClustering, StdWeightedClustering, VcWeightedClustering, MedianWeightedClustering, Q1WClustering, Q3WClustering, existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################# Adjacency Matrix Features
    #instanceFeature.ComputeAdjacencyMatrixEigenvalues()
    #Index = instanceFeature.Index()
    #SecondLargestAdjEgv = instanceFeature.SecondLargestAdjEgv()
    #SecondSmallestAdjEgv = instanceFeature.SecondSmallestAdjEgv()
    #SmallestAdjEgv = instanceFeature.SmallestAdjEgv()
    #MeanSpectrum = instanceFeature.MeanSpectrum()
    #StdSpectrum = instanceFeature.StdSpectrum()
    #Energy = instanceFeature.Energy()
    #GapLargestAndSecondLargestAdjEgv = instanceFeature.GapLargestAndSecondLargestAdjEgv()
    #cursor2.execute("SELECT GraphID FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()

    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, adjindex, seclargestadjegv, secsmallestadjegv, smallestadjegv, meanspectrum, stdspectrum, energy, gaplargestand2ndlargestadj) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #                   str(pk), row.Id, Index, SecondLargestAdjEgv, SecondSmallestAdjEgv, SmallestAdjEgv, MeanSpectrum, StdSpectrum, Energy, GapLargestAndSecondLargestAdjEgv)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET adjindex=?, seclargestadjegv=?, secsmallestadjegv=?, smallestadjegv=?, meanspectrum=?, stdspectrum=?, energy=?, gaplargestand2ndlargestadj=? where GraphID=?",
    #                    Index, SecondLargestAdjEgv, SecondSmallestAdjEgv, SmallestAdjEgv, MeanSpectrum, StdSpectrum, Energy, GapLargestAndSecondLargestAdjEgv, existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################## Laplacian Matrix Features
    #instanceFeature.ComputeLaplacianMatrixEigenvalues()
    #LaplacianIndex = instanceFeature.LaplacianIndex()
    #SecondLargestLapEgv = instanceFeature.SecondLargestLapEgv()
    #SecondSmallestNZLapEgv = instanceFeature.SecondSmallestNZLapEgv()
    #SmallestNZLapEgv = instanceFeature.SmallestNZLapEgv()
    #AlgebraicConnectivity = instanceFeature.AlgebraicConnectivity()
    #SmallestLapEgv = instanceFeature.SmallestLapEgv()
    #GapLargestAndSmallestNZLapEgv = instanceFeature.GapLargestAndSmallestNZLapEgv()
    #cursor2.execute("SELECT GraphID FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, laplacianindex, seclargestlapegv, secondsmallestnzlapegv, smallestnzlapegv, algconnectivity, smallestlapegv, gaplargestandsmallestnzlap) values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #                   str(pk), row.Id, LaplacianIndex, SecondLargestLapEgv, SecondSmallestNZLapEgv, SmallestNZLapEgv, AlgebraicConnectivity, SmallestLapEgv, GapLargestAndSmallestNZLapEgv)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET laplacianindex=?, seclargestlapegv=?, secondsmallestnzlapegv=?, smallestnzlapegv=?, algconnectivity=?, smallestlapegv=?, gaplargestandsmallestnzlap=? where GraphID=?",
    #                    LaplacianIndex, SecondLargestLapEgv, SecondSmallestNZLapEgv, SmallestNZLapEgv, AlgebraicConnectivity, SmallestLapEgv, GapLargestAndSmallestNZLapEgv,  existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################### Wiener Index Feature
    #WienerIndex = instanceFeature.WienerIndex()
    #cursor2.execute("SELECT GraphID FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, wienerindex) values (?, ?, ?)",
    #                   str(pk), row.Id, WienerIndex)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET wienerindex=? where GraphID=?",
    #                    WienerIndex, existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################## Average Path Length Feature
    AveragePathLength = instanceFeature.AveragePathLength()
    cursor2.execute("SELECT GraphID FROM InstancesFeatures WHERE GraphID=?",row.Id)
    existingInstance = cursor2.fetchone()
    if (existingInstance==None) :
        pk = uuid.uuid4()
        cursor2.execute("insert into InstancesFeatures(Id, GraphID, avgpathlength) values (?, ?, ?)",
                       str(pk), row.Id, AveragePathLength)
    else :
        cursor2.execute("UPDATE InstancesFeatures SET avgpathlength=? where GraphID=?",
                        AveragePathLength, existingInstance.GraphID)
    conn2.commit()

    ############################################################################################# Degeneracy Feature
    #Degeneracy = instanceFeature.Degeneracy()
    #cursor2.execute("SELECT GraphID FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, degeneracy) values (?, ?, ?)",
    #                   str(pk), row.Id, Degeneracy)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET degeneracy=? where GraphID=?",
    #                    Degeneracy, existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################## Girth Feature
    #Girth = instanceFeature.Girth()
    #cursor2.execute("SELECT GraphID FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, girth) values (?, ?, ?)",
    #                   str(pk), row.Id, Girth)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET girth=? where GraphID=?",
    #                    Girth, existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################## Connected Components, Rank and CoRank Features
    #ConnectedComponents = instanceFeature.ConnectedComponents()
    #Rank = instanceFeature.Rank()
    #CoRank = instanceFeature.CoRank()
    #cursor2.execute("SELECT GraphID FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, connectedcomponents, rank, corank) values (?, ?, ?, ?, ?)",
    #                   str(pk), row.Id, ConnectedComponents, Rank, CoRank)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET connectedcomponents=?, rank=?, corank=? where GraphID=?",
    #                    ConnectedComponents, Rank, CoRank, existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################## Maximal Clique Size
    ##MaxCliqueSize = instanceFeature.MaxCliqueSize()
    ##cursor2.execute("SELECT GraphID FROM InstancesFeatures WHERE GraphID=?",row.Id)
    ##existingInstance = cursor2.fetchone()
    ##if (existingInstance==None) :
    ##    pk = uuid.uuid4()
    ##    cursor2.execute("insert into InstancesFeatures(Id, GraphID, maxcliquesize) values (?, ?, ?)",
    ##                   str(pk), row.Id, MaxCliqueSize)
    ##    conn2.commit()
    ##else :
    ##    cursor2.execute("UPDATE InstancesFeatures SET maxcliquesize=? where GraphID=?",
    ##                    MaxCliqueSize, existingInstance.GraphID)
    ##    conn2.commit()

    ############################################################################################# Szeged Index Feature
    #SzegedIndex = instanceFeature.SzegedIndex()
    #cursor2.execute("SELECT GraphID FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, szegedindex) values (?, ?, ?)",
    #                   str(pk), row.Id, SzegedIndex)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET szegedindex=? where GraphID=?",
    #                    SzegedIndex, existingInstance.GraphID)
    #conn2.commit()

    ############################################################################################## Spectral Bipartivity (Beta) Feature
    #Beta = instanceFeature.Beta()
    #cursor2.execute("SELECT GraphID FROM InstancesFeatures WHERE GraphID=?",row.Id)
    #existingInstance = cursor2.fetchone()
    #if (existingInstance==None) :
    #    pk = uuid.uuid4()
    #    cursor2.execute("insert into InstancesFeatures(Id, GraphID, beta) values (?, ?, ?)",
    #                   str(pk), row.Id, Beta)
    #else :
    #    cursor2.execute("UPDATE InstancesFeatures SET beta=? where GraphID=?",
    #                    Beta, existingInstance.GraphID)
    #conn2.commit()

    #del instanceFeature
    #conn2.close()

    print(row.Name," processed.")

if __name__=='__main__':
    conn1 = pyodbc.connect("Driver={SQL Server};Server=.\SQLEXPRESS;Trusted_Connection=yes;database=GraphColoringPortfolio")
    cursor1 = conn1.cursor()

    #num_cores = multiprocessing.cpu_count()
    num_cores = 7

    results = Parallel(n_jobs=num_cores, verbose=50)(delayed(ExtractFeature)(row) for row in cursor1.execute("SELECT GraphInstances.Id, Path, Name FROM GraphInstances, InstancesFeatures where GraphInstances.Id=InstancesFeatures.GraphID and avgpathlength is null Order By Name"))

    conn1.close()