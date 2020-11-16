try:
    import networkx as nx
    import numpy as np
    import igraph as ig
    import mathchem as mc
    from decimal import *

    class Features(object):

        def __init__(self, graphFilePath):
            self.graphFilePathDimacs = graphFilePath
            self.graphFilePath = graphFilePath+'.edl'
            self.G=nx.read_edgelist(graphFilePath+'.edl', nodetype=int)
            self.MAXDECIMAL = float('99999999999999999.9999999999')

    ## Nodes and Edges Features ###############################################################
        def NumberOfNodes(self) :
            return nx.number_of_nodes(self.G)

        def NumberOfEdges(self) :
            return nx.number_of_edges(self.G)

        def RatioNodesEdges(self) :
            return float(nx.number_of_nodes(self.G))/nx.number_of_edges(self.G)

        def RatioEdgesNodes(self) :
            return float(nx.number_of_edges(self.G))/nx.number_of_nodes(self.G)

        def Density(self) :
            return nx.density(self.G)

    ### Degree Features ###############################################################
    
        def ComputeDegree(self):
            self.degreeList = np.array(nx.degree(self.G).values())

        def MinDegree(self) :
            return min(self.degreeList)

        def MaxDegree(self) :
            return max(self.degreeList)

        def MeanDegree(self) :
            return np.mean(self.degreeList)

        def StdDegree(self) :
            return np.std(self.degreeList)

        def VcDegree(self) :
            if (self.MeanDegree()!=0):
                return self.StdDegree()/self.MeanDegree()
            else:
                return self.MAXDECIMAL

        def Q1Degree(self) :
            return np.percentile(self.degreeList,25)

        def MedianDegree(self) :
            return np.median(self.degreeList)

        def Q3Degree(self) :
            return np.percentile(self.degreeList,75)

    ### Betweenness Centrality Features ###############################################################
        def ComputeBtwnsCentrality(self):
            self.btwnsCentralityList = nx.algorithms.betweenness_centrality(self.G).values()
    
        def MinBtwnsCentrality(self) :
            return min(self.btwnsCentralityList)

        def MaxBtwnsCentrality(self) :
            return max(self.btwnsCentralityList)

        def MeanBtwnsCentrality(self) :
            return np.mean(self.btwnsCentralityList)

        def StdBtwnsCentrality(self) :
            return np.std(self.btwnsCentralityList)

        def VcBtwnsCentrality(self) :
            if (self.MeanBtwnsCentrality()!=0):
                return self.StdBtwnsCentrality() / self.MeanBtwnsCentrality()
            else:
                return self.MAXDECIMAL

        def Q1BtwnsCentrality(self) :
            return np.percentile(self.btwnsCentralityList,25)

        def MedianBtwnsCentrality(self) :
            return np.median(self.btwnsCentralityList)

        def Q3BtwnsCentrality(self) :
            return np.percentile(self.btwnsCentralityList,75)

    ### Closeness Centrality Features ###############################################################
        def ComputeCloseness(self):
            self.closenessList = nx.algorithms.closeness_centrality(self.G).values()
        
        def MinClosenessCentrality(self) :
            return min(self.closenessList)

        def MaxClosnessCentrality(self) :
            return max(self.closenessList)

        def MeanClosenessCentrality(self) :
            return np.mean(self.closenessList)

        def StdClosenessCentrality(self) :
            return np.std(self.closenessList)

        def VcClosenessCentrality(self) :
            if (self.MeanClosenessCentrality()!=0):
                return self.StdClosenessCentrality()/self.MeanClosenessCentrality()
            else:
                return self.MAXDECIMAL

        def Q1ClosenessCentrality(self) :
            return np.percentile(self.closenessList,25)

        def MedianClosenessCentrality(self) :
            return np.median(self.closenessList)

        def Q3ClosenessCentrality(self) :
            return np.percentile(self.closenessList,75)

    ### Eigenvector Centrality Features ###############################################################
        def ComputeEgvCentrality(self):
            self.egvCentralityList = nx.algorithms.eigenvector_centrality_numpy(self.G).values()
    
        def MinEgvCentrality(self) :
            return min(self.egvCentralityList)

        def MaxEgvCentrality(self) :
            return max(self.egvCentralityList)

        def MeanEgvCentrality(self) :
            return np.mean(self.egvCentralityList)

        def StdEgvCentrality(self) :
            return np.std(self.egvCentralityList)

        def VcEgvCentrality(self) :
            if (self.MeanEgvCentrality()!=0):
                return self.StdEgvCentrality()/self.MeanEgvCentrality()
            else:
                return self.MAXDECIMAL

        def Q1EgvCentrality(self) :
            return np.percentile(self.egvCentralityList,25)

        def MedianEgvCentrality(self) :
            return np.median(self.egvCentralityList)

        def Q3EgvCentrality(self) :
            return np.percentile(self.egvCentralityList,75)

    ### Eccentricity Features ###############################################################
        def ComputeEccentricity(self):
            self.eccentricityList = nx.algorithms.eccentricity(self.G).values()
    
        def MinEccentricity(self) :
            return min(self.eccentricityList)

        def MaxEccentricity(self) :
            return max(self.eccentricityList)

        def MeanEccentricity(self) :
            return np.mean(self.eccentricityList)

        def StdEccentricity(self) :
            return np.std(self.eccentricityList)

        def VcEccentricity(self) :
            if (self.MeanEccentricity()!=0):
                return self.StdEccentricity()/self.MeanEccentricity()
            else:
                return self.MAXDECIMAL

        def Q1Eccentricity(self) :
            return np.percentile(self.eccentricityList, 25)

        def MedianEccentricity(self) :
            return np.median(self.eccentricityList)

        def Q3Eccentricity(self) :
            return np.percentile(self.eccentricityList, 75)

    ### Local Clustering Features ###############################################################
        def ComputeClustering(self):
            self.ClusteringList = np.array(nx.clustering(self.G).values())
    
        def MinClustering(self) :
            return min(self.ClusteringList)

        def MaxClustering(self) :
            return max(self.ClusteringList)

        def MeanClustering(self) :
            return np.mean(self.ClusteringList)

        def StdClustering(self) :
            return np.std(self.ClusteringList)

        def VcClustering(self) :
            if (self.MeanClustering()!=0):
                return self.StdClustering()/self.MeanClustering()
            else:
                return self.MAXDECIMAL

        def Q1Clustering(self) :
            return np.percentile(self.ClusteringList, 25)

        def MedianClustering(self) :
            return np.median(self.ClusteringList)

        def Q3Clustering(self) :
            return np.percentile(self.ClusteringList, 75)

    ### Weighted Local Clustering Features ###############################################################
        def ComputeWeightedClustering(self):
            self.WeightedClusteringList = self.ClusteringList * self.degreeList
    
        def MinWeightedClustering(self) :
            return min(self.WeightedClusteringList)

        def MaxWeightedClustering(self) :
            return max(self.WeightedClusteringList)

        def MeanWeightedClustering(self) :
            return np.mean(self.WeightedClusteringList)

        def StdWeightedClustering(self) :
            return np.std(self.WeightedClusteringList)

        def VcWeightedClustering(self) :
            if (self.MeanWeightedClustering()!=0):
                return self.StdWeightedClustering()/self.MeanWeightedClustering()
            else:
                return self.MAXDECIMAL

        def Q1WeightedClustering(self) :
            return np.percentile(self.WeightedClusteringList, 25)

        def MedianWeightedClustering(self) :
            return np.median(self.WeightedClusteringList)

        def Q3WeightedClustering(self) :
            return np.percentile(self.WeightedClusteringList, 75)

    ### Adjacency Matrix Features ###############################################################
        def ComputeAdjacencyMatrixEigenvalues(self):
            self.adjacencySpectrum =  np.array(nx.adjacency_spectrum(self.G)).real
            self.adjacencySpectrum.sort()
            
        def Index(self):
            return self.adjacencySpectrum[self.adjacencySpectrum.size-1]

        def SecondLargestAdjEgv(self):
            return self.adjacencySpectrum[self.adjacencySpectrum.size-2]

        def SecondSmallestAdjEgv(self):
            return self.adjacencySpectrum[1]

        def SmallestAdjEgv(self):
            return self.adjacencySpectrum[0]

        def MeanSpectrum(self):
            return np.mean(self.adjacencySpectrum)

        def StdSpectrum(self):
            return np.std(self.adjacencySpectrum)

        def VcSpectrum(self):
            if (self.MeanSpectrum()!=0):
                return self.StdSpectrum()/self.MeanSpectrum()
            else:
                return self.MAXDECIMAL

        def Energy(self):
            return np.sum(np.absolute(self.adjacencySpectrum))

        def GapLargestAndSecondLargestAdjEgv(self):
            return self.Index()-self.SecondLargestAdjEgv()

    ### Laplacian Matrix Features ###############################################################
        def ComputeLaplacianMatrixEigenvalues(self):
            self.laplacianSpectrum =  np.around(np.array(nx.laplacian_spectrum(self.G)),decimals=4)
            self.laplacianSpectrum.sort()

        def LaplacianIndex(self):
            return self.laplacianSpectrum[self.laplacianSpectrum.size-1]

        def SecondLargestLapEgv(self):
            return self.laplacianSpectrum[self.laplacianSpectrum.size-2]

        def SmallestLapEgv(self):
            return self.laplacianSpectrum[0]

        def SmallestNZLapEgv(self):
            self.index = 0
            while (self.laplacianSpectrum[self.index]==0):
                self.index = self.index+1
            return self.laplacianSpectrum[self.index]

        def SecondSmallestNZLapEgv(self):
            self.index = 0
            while (self.laplacianSpectrum[self.index]==0):
                self.index = self.index+1
            return self.laplacianSpectrum[self.index+1]

        def AlgebraicConnectivity(self):
            return nx.linalg.algebraicconnectivity.algebraic_connectivity(self.G)

        def GapLargestAndSmallestNZLapEgv(self):
            return self.LaplacianIndex()-self.SmallestNZLapEgv()

    ### Wiener Index ###############################################################
        def WienerIndex(self):
            m = mc.Mol()
            m.read_edgelist(self.G.edges())
            return m.wiener_index()

    ### Szeged Index ###############################################################
        def SzegedIndex(self):
            m = mc.Mol()
            m.read_edgelist(self.G.edges())
            return m.szeged_index()

    ### Spectral Bipartivity (Beta) ###############################################################
        def Beta(self):
            G_MAT=nx.to_numpy_matrix(self.G) # Convert NX network to adjacency matrix 
            ei,ev=np.linalg.eig(G_MAT)   # Calculate eigenvalues 
            SC_even=0       # Sum of the contributions from even closed walks in G 
            SC_all=0        # Sum of the contributions of all closed walks in G 
            for j in range(0,self.G.number_of_nodes()): 
                SC_even=SC_even+np.cosh(ei[j].real) 
                SC_all=SC_all+np.e**(ei[j].real) 
            # Proportion of even closed walks over all closed walks 
            #print SC_even
            #print SC_all
            if (SC_all!=0 and SC_all!=float('Inf')):
                B=SC_even/SC_all
            else:
                B=0
            return B 


    ### Avg Path Length ###############################################################
        def AveragePathLength(self):
            return nx.average_shortest_path_length(self.G)

    ### Degeneracy ###############################################################
        def Degeneracy(self):
            return max(nx.core_number(self.G).values())

    ### Girth ###############################################################
        def Girth(self):
            self.IG = ig.Graph.Read_Edgelist(self.graphFilePath)
            return self.IG.girth()

    ### Connected Components, Rank and Co-Rank ###############################################################
        def ConnectedComponents(self):
            return nx.number_connected_components(self.G)
    
        def Rank(self):
            return nx.number_of_nodes(self.G) - nx.number_connected_components(self.G)

        def CoRank(self):
            return nx.number_of_edges(self.G) - nx.number_of_nodes(self.G)+nx.number_connected_components(self.G)

    ### Size of Largest Maximal Clique ###############################################################
        def MaxCliqueSize(self):
            return nx.node_clique_number(self.G).values().pop()
except:
    raise