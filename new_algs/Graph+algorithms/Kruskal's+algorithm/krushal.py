
import random

class Maze(object):
    """
    An n-dimensional array generated using Krushal's algorithm.

    >>> m = Maze(2, 2)
    >>> m.generate()
    >>> for wall in m.walls:
    ...     draw(wall)
    """

    def __init__(self, size, dimensions):
        """
        Initialize a square n-dimensional maze.
        """
        self.size = size
        self.dimensions = dimensions

        self.walls = set()
        self.removed_walls = set()

        self.cells = {}

        self.start = [0] * dimensions
        self.end = [size - 1] * dimensions


    def mkcells(self, dimensions):
        """
        A generator that yields all of the cells in the maze.
        """
        if dimensions > 0:
            # generate all values in the lower dimension
            pts = self.mkcells(dimensions - 1)
            # prepent the current dimension's values to each lower value
            for pt in pts:
                for i in xrange(self.size):
                    yield [i] + pt 
        else:
            yield []


    def mkwalls(self):
        """
        A generator that yields all walls in the maze, for later removal by the
        generate() method.
        """
        cell_list = self.mkcells(self.dimensions)
        cell_list = list(cell_list)
        random.shuffle(cell_list)
        for c in cell_list:
            cell = Cell(self, *c)
            for wall in cell.get_walls():
                yield wall

    def get_passages(self, cell):
        """
        For a generated maze, get all cells that connect to this one.
        """
        return filter(lambda w: cell in w, self.removed_walls)


    def generate(self):
        """
        Run the maze generation.
        """
        # FIXME: must the wall list be pre-egeneated?
        wall_list = list(self.mkwalls())
        random.shuffle(wall_list)
        for wall in wall_list:
            if wall.removed or wall.cell_a.set.intersection(wall.cell_b.set):
                pass
            else:
                wall.delete()

        # Now randomly delete a bunch more walls, just to make things easier
        # in higher dimensions
        #for wall in list(self.walls):
        #    if random.random() < .5:
        #        wall = Wall(self, *wall)
        #        wall.delete()


    def in_bounds(self, coords):
        """
        Check to see if a set of coordinates is within the bounds of the maze.
        """
        if len(coords) == self.dimensions and \
           min(coords) > -1 and max(coords) < self.size:
            return True
        return False


class Wall(object):

    def __repr__(self):
        return "<Wall %s %s>" % (repr(self.cell_a.coords), repr(self.cell_b.coords))


    def __init__(self, maze, a, b):
        self.maze = maze
        self.coords = Wall.normalize(a, b)
        if self.removed:
            pass
        else:
            self.maze.walls.add(self.coords)
        self.cell_a = Cell(self.maze, *a)
        self.cell_b = Cell(self.maze, *b)


    def delete(self):
        self.maze.walls.remove(self.coords)
        self.maze.removed_walls.add(self.coords)
        # and merge cell sets here
        set_ = self.cell_a.set | self.cell_b.set
        # make sure all members of the set are updated
        for pt in set_:
            self.maze.cells[pt] = set_


    @property
    def removed(self):
        return self.coords in self.maze.removed_walls


    @staticmethod
    def normalize(pta, ptb):
        return tuple(sorted((tuple(pta), tuple(ptb))))


class Cell(object):

    def __repr__(self):
        return "<Cell %s>" % repr(self.coords)


    def __init__(self, maze, *coords):
        self.maze = maze
        self.coords = tuple(coords)


    @property
    def set(self):
        if self.coords in self.maze.cells:
            pass
        else:
            s = set()
            s.add(self.coords)
            self.maze.cells[self.coords] = s
        return self.maze.cells[self.coords]


    @set.setter
    def set(self, value):
        self.maze.cells[self.coords] = value


    def get_walls(self, check_removed=True):
        for idx, v in enumerate(self.coords):
            pt = list(self.coords)
            for m in (1, -1):
                if v + m < self.maze.size and v + m > -1:
                    pt[idx] = v + m
                    wall = Wall(self.maze, self.coords, pt)
                    if wall.removed and check_removed:
                        pass
                    else:
                        yield wall
