class Student:
    def __init__(self, first_name="No name", last_name="No name",
                 rating="0.0", height=0.0):
        self.first_name = first_name
        self.last_name = last_name
        self.rating = rating
        self.height = height

    def __str__(self):
        return self.first_name + " " + self.last_name + "(rating=" + str(
            self.rating) + " height=" + str(self.height)

