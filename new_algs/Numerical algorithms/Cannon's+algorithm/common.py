import Cannon


# These functions are not for production,
# just for better test readability
#----
def M1(*data):
    return Cannon.Matrix(1, list(data))
    
def M2(*data):
    return Cannon.Matrix(2, list(data))


def M3(*data):
    return Cannon.Matrix(3, list(data))


def M4(*data):
    return Cannon.Matrix(4, list(data))


def M6(*data):
    return Cannon.Matrix(6, list(data))


def M8(*data):
    return Cannon.Matrix(8, list(data))
#----
