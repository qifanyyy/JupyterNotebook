"""
An interactive visualizer for TSP instances if you add `Visualizer.update(solution)`
after improving your solution you will see the new path and its cost.
 
 
>>> points = [(0, 0), (1, 1), (1, 2)]
>>> vis = Visualizer(points)
>>> Visualizer.update([0, 1, 2])
 
 
 
Copyright (C) 2013 Toby Davies
 
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:
 
The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 
"""
 
 
import math
import random
import sys
 
import matplotlib
import matplotlib.pyplot

class Visualiser(object):
    "Matplotlib interactive visualiser for TSP solutions"
 
    X = 0
    Y = 1
    
 
    def __init__(self, points):
        self.points = points
        x, y = self.to_coords(range(len(points)), self.X), self.to_coords(range(len(points)), self.Y)
        matplotlib.pyplot.clf()
        _, self.guess, self.set = matplotlib.pyplot.plot(
            x, y, 's',
            x, y, '-',
            [], [], 's')
        matplotlib.pyplot.ion()
        matplotlib.pyplot.show()
        self.__class__.instance = self
 
    def to_coords(self, solution, idx=X):
        return [self.points[i][idx]
                for i in solution]
 
    @classmethod
    def update(cls, solution=None, neighbourhood=None):
        cls.instance._update(solution=solution, neighbourhood=neighbourhood)
 
    def _update(self, solution=None, neighbourhood=None):
        if solution:
            line = self.guess
            line.set_xdata(self.to_coords(solution + [solution[0]], self.X))
            line.set_ydata(self.to_coords(solution + [solution[0]], self.Y))
            cost = self.tour_cost(solution)
        if cost:
            matplotlib.pyplot.legend(("Nodes", "Current: %s"%cost, "Neighbourhood")).draggable()
        if neighbourhood:
            self.set.set_xdata(self.to_coords(neighbourhood, self.X))
            self.set.set_ydata(self.to_coords(neighbourhood, self.Y))
        matplotlib.pyplot.draw()
 
    def tour_cost(self, tour):
        points = self.points
        return sum(length(points[tour[i]], points[tour[(i+1)%len(tour)]])
                   for i in range(len(tour)))
 
 
def length(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
