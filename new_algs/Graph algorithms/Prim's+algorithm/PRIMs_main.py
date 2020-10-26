## PRIMs_main.py
## Main function to test MST implementation using PRIM's algorithm.

from PRIMs_MST import Graph;        ## Import Graph class, which has PRIM's MST feature.

def main ():

    ## Initialize graph with undirected edges (and weights).
    g = Graph(n_vertices = 5);
    
    g.add_edge([0, 1, 2]);  g.add_edge([0, 3, 6]);     
    g.add_edge([1, 2, 3]);  g.add_edge([1, 3, 8]);  g.add_edge([1, 4, 5]);  
    g.add_edge([2, 4, 7]); 
    g.add_edge([3, 4, 9]); 

    
    print('GRAPH: ', g.edges);

    MST = g.PRIMs_MST();

    print("Prim\'s MST: ", MST);    ## [[0,1,2], [1,2,3],[1,4,5],[0,3,6]]; in any order.

    return 0;

if __name__ == '__main__':
    main();
    