# -*- coding: utf-8 -*-

from scipy.spatial import Delaunay
import numpy as np
import matplotlib.pyplot as plt

import fiona
import shapely.geometry as geometry

from math import atan2
from copy import deepcopy

def add_edge(edges, i, j, only_outer = True):
    """
    Add a line between the i-th and j-th points,
    if not in the list already
    """
    if (i, j) in edges or (j, i) in edges:
        # already added
        assert (j, i) in edges, "Can't go twice over same directed edge right?"
        if only_outer:
            # if both neighboring triangles are in shape, it's not a boundary edge
            edges.remove((j, i))
        return
    edges.add((i, j))

def alpha_shape(points, alpha, only_outer = True):
    """
    Compute the alpha shape (concave hull) of a set of points.
    :param points: np.array of shape (n,2) points.
    :param alpha: alpha value.
    :param only_outer: boolean value to specify if we keep only the outer border
    or also inner edges.
    :return: set of (i,j) pairs representing edges of the alpha-shape. (i,j) are
    the indices in the points array.
    """
    assert points.shape[0] > 3, "Need at least four points"

    tri = Delaunay(points)
    edges = set()
    # Loop over triangles:
    # ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.vertices:
        pa = points[ia]
        pb = points[ib]
        pc = points[ic]
        # Computing radius of triangle circumcircle
        # www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle
        a = np.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
        b = np.sqrt((pb[0] - pc[0]) ** 2 + (pb[1] - pc[1]) ** 2)
        c = np.sqrt((pc[0] - pa[0]) ** 2 + (pc[1] - pa[1]) ** 2)
        s = (a + b + c) / 2.0
        
        area = np.sqrt(s * (s - a) * (s - b) * (s - c))
        
        circum_r = a * b * c / (4.0 * area)
                
        if circum_r < alpha:
            add_edge(edges, ia, ib, only_outer)
            add_edge(edges, ib, ic, only_outer)
            add_edge(edges, ic, ia, only_outer)
        
        else:
            print(area)
        
    return edges, tri

def get_child(edge_list, mother):
    for i, j in edge_list:
        if i == mother:
            return j

def sortList(edge_list, mother, sort = []):
    edges = deepcopy(edge_list)
    if edges:
        child = get_child(edges, mother)
        
        # This is a hack due to the Delaunay triangulation in Sci-Py. The 
        # triangulation can create constrained Delaunay triangles resulting
        # in very small areas which will, when the area check for alpha_shape
        # is invoked, return a large circumference. Filtering these out will
        # require another implementation of Delaunay triangulation or a
        # defined minimum for the area of the triangle. As long as the mother
        # node used to initiate this function is contained on the circumference
        # of the concave-hull then the method will work just fine.
        try:
            assert child != None, "Child is None in ({}, {})".format(mother, child) 
            edges.remove((mother, child))
            sort.append([mother, child])
            sortList(edges, child)
        
        except AssertionError as e:
            print(e)
    
    else:
        print('Edge list is empty')
    
    return sort
    

def create_wkt(points, sorted_edge_list):
    for i in range(len(sorted_edge_list)):
        if i == 0:
            polygon = 'POLYGON(({} {}'.format(points[sorted_edge_list[i][0]][0], points[sorted_edge_list[i][0]][1])
        
        elif i > 0 and i < len(sorted_edge_list) - 1:
            polygon += ',{} {}'.format(points[sorted_edge_list[i][0]][0], points[sorted_edge_list[i][0]][1])
            
        else:
            polygon += ',{} {}))'.format(points[sorted_edge_list[i][1]][0], points[sorted_edge_list[i][1]][1])    
    
    return polygon

def create_point_set(input_shapefile):
    shapefile = fiona.open(input_shapefile)
    
    points = [geometry.shape(point['geometry'])
              for point in shapefile]
    
    x = np.array([p.coords.xy[0][0] for p in points])
    y = np.array([p.coords.xy[1][0] for p in points])
    
    return np.vstack((x,y)).T
    
if __name__ == '__main__':
    """
    input_shapefile = r'C:\Temp\Klar\interp_data\dgu_data_to_interp.shp'
    shapefile = fiona.open(input_shapefile)
    points = [geometry.shape(point['geometry'])
              for point in shapefile]
    
    x = np.array([p.coords.xy[0][0] for p in points])
    y = np.array([p.coords.xy[1][0] for p in points])
    
    points = np.vstack((x,y)).T
    """
    points = create_point_set('C:\\Temp\\Klar\\result_dvr90\\interp_points_dvr90.shp')
    
    edges, tri = alpha_shape(points, alpha=3000, only_outer=True)
    
    sort = sortList(edges, 0)
    
    wkt = create_wkt(points, sort)
    
    # Plotting the output
    plt.figure()
    plt.axis('equal')
    plt.triplot(points[:,0], points[:,1], tri.simplices)
    plt.plot(points[:, 0], points[:, 1], '.')
    for i, j in edges:
        plt.plot(points[[i, j], 0], points[[i, j], 1], 'r')
    plt.show()