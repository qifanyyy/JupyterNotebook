import math

class TSPFile:
    name = ''
    file_type = ''
    comment = ''
    dimension = 0 
    edge_weight_type = ''
    node_coord_section = ['']
    adjacency_matrix = [0]
    node_count = [0]
    x_coord = [0]
    y_coord = [0]
    def __init__(self):
        self.name = ''
        self.file_type = ''
        self.comment = ''
        self.dimension = 0 
        self.edge_weight_type = ''
        self.node_coord_section = []
    def fill_props(self, param, value):
        value = value.rstrip().lstrip()
        param = param.rstrip().lstrip()
        if 'NAME' == param:
            self.name = value
        elif 'TYPE' == param:
            self.file_type = value
        elif 'COMMENT' == param:
            self.comment = value
        elif 'DIMENSION' == param:
            self.dimension = int(value)
        elif 'EDGE_WEIGHT_TYPE' == param:
            self.edge_weight_type = value
        elif 'NODE_COORD_SECTION' == param:
            self.instantiate_adjacency_matrix()
        else:
            param = param.lstrip().rstrip()
            self.node_coord_section.append(param)

    def instantiate_adjacency_matrix(self):
        self.adjacency_matrix = self.adjacency_matrix * self.dimension
        self.node_count = self.node_count * self.dimension
        self.x_coord = self.x_coord * self.dimension
        self.y_coord = self.y_coord * self.dimension
        for i in range(self.dimension):
            self.adjacency_matrix[i] = [0] * self.dimension
    
    def compute_adjacency_matrix(self):
        for i in range(self.dimension):
            [self.node_count[i], self.x_coord[i], self.y_coord[i]] = self.node_coord_section[i].split()
            self.node_count[i] = int(self.node_count[i])
            self.x_coord[i] = round(float(self.x_coord[i]), 1)
            self.y_coord[i] = round(float(self.y_coord[i]), 1)
        if 'EUC_2D' in self.edge_weight_type:
            self.compute_euclidean()
        else:
            self.compute_pseudo_euclidean()

    def compute_euclidean(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if i == j:
                    self.adjacency_matrix[i][j] = 0
                else:
                    xd = self.x_coord[i] - self.x_coord[j]
                    yd = self.y_coord[i] - self.y_coord[j]
                    dij = math.sqrt((xd*xd) + (yd*yd))
                    self.adjacency_matrix[i][j] = round(dij)

    def compute_pseudo_euclidean(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if i == j:
                    self.adjacency_matrix[i][j] = 0
                else:
                    xd = self.x_coord[i] - self.x_coord[j]
                    yd = self.y_coord[i] - self.y_coord[j]
                    rij = math.sqrt(((xd*xd) + (yd*yd))/10)
                    tij = round(rij)
                    if tij < rij:
                        self.adjacency_matrix[i][j] = round((tij + 1), 1)
                    else:
                        self.adjacency_matrix[i][j] = round(tij, 1)
