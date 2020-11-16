#ASMath.py
from __future__ import division
import math
import ASDrawing
from numpy import matrix
from numpy import linalg
import settings


def distancePoints2D(point0, point1):
	return math.sqrt( abs(point0[0] - point1[0])**2 + abs(point0[1] - point1[1])**2)


def distancePoints3D(point0, point1):
	return math.sqrt( abs(point0[0] - point1[0])**2 + abs(point0[1] - point1[1])**2 + abs(point0[2] - point1[2])**2  )

def divide(x, y):
	if y == 0:
		return 0
	return x/y


#####################################################
# de Boor Algorithm
#####################################################
def splineBasis(u, order, index, knots):
	if order == 0:
		if u >= knots[index] and u <= knots[index+1]:
			return 1
		return 0
	else:
		t0 = 0
		denom0 = knots[index+order] - knots[index]
		if denom0 != 0:
			t0 = float(u - knots[index])/denom0

		t1 = 0
		denom1 = knots[index+order+1] - knots[index+1]
		if denom1 != 0:
			t1 = float(knots[index+order+1] - u)/denom1

		return t0*splineBasis(u, order-1, index, knots) + t1*splineBasis(u, order-1, index+1, knots)

def deBoor_generatePoint_4D(k, u, points, knots):
	result = [0, 0, 0, 0]
	for i in range(len(points)):
		basis = splineBasis(u, k, i, knots)
		result = [x + y for x, y in zip(result, [basis*x for x in points[i]])]
	return result
    
#####################################################
# Elevation and Knot Generation Functions
#####################################################
def elevate3Dto4D(points, weights): ## Should be working
	elevatedPoints = []
	for i in range(0, len(points)):
		weight = weights[i]
		elevatedPoints.append([weight*points[i][0], weight*points[i][1], weight*points[i][2], weight])
	return elevatedPoints

def project4Dto3D(point): ## Should be working
	return [divide(point[0],point[3]), divide(point[1],point[3]), divide(point[2],point[3])]

def generateKnots(points, k):
	knots = []
	for i in range(len(points)-k+1):
		knots.append(i/(len(points)-k))
	for i in range(k):
		knots.append(knots[-1])
		knots.insert(0, knots[0])
	# print(knots)
	return knots


#####################################################
# NURB Algorithm
#####################################################
def nurb_4D(k, u, points, weights, knots):
	elevatedPoints = elevate3Dto4D(points, weights)
	elevatedPoint = deBoor_generatePoint_4D(k, u, elevatedPoints, knots)
	delevatedPoint, weight = [project4Dto3D(elevatedPoint), elevatedPoint[3]]
	return [delevatedPoint, weight]


#####################################################
# Surface Functions
#####################################################
def surface(uK, vK, u, v, points, weights, uKnots, vKnots):
	n = len(points) # Number of rows
	m = len(points[0]) # Number of columns
	nPoints = []
	nWeights = []
	for i in range(n):
		point, weight = nurb_4D(uK, u, points[i], weights[i], uKnots)
		nPoints.append(point)
		nWeights.append(weight)
	return nurb_4D(vK, v, nPoints, nWeights, vKnots)[0]

def allSurfacePoints(uK, vK, points, weights, uKnots, vKnots):
	n = settings.vRes
	m = settings.uRes
	result = []
	for i in range(n+1):
		resultRow = []
		for j in range(m+1):
			u = float(i)/n
			v = float(j)/m
			resultRow.append(surface(uK, vK, u, v, points, weights, uKnots, vKnots))
		result.append(resultRow)
	return result


def nurbsSurface(uK, vK, uKnots, vKnots, points, weights):
	result = allSurfacePoints(uK, vK, points, weights, uKnots, vKnots)
	# for row in result:
	# 	print(row)
	return result
