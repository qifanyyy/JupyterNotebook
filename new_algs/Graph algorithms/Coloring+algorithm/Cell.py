class Cell:

    def __init__(self, index, color_num):
        self.index = index
        self.neighbours = []
        self.color = color_num
        self.checked = False

    def set_color(self, num):
        self.color = num

    def set_neighbours(self, n_list):
        self.neighbours = n_list
