from enum import Enum
from random import randint

class Colors(Enum):
	RED = 0
	GREEN = 1
	BLUE = 2
	YELLOW = 3
	BLACK = 4
	PURPLE = 5
	WHITE = 6

colors = [
	Colors.RED, 
	Colors.GREEN,
	Colors.BLUE,
	Colors.YELLOW,
	Colors.BLACK,
	Colors.PURPLE,
	Colors.WHITE,
]

def getRandomColor(colorNums):
	return colors[randint(0, colorNums-1)]

plotColorsDict = {
	Colors.RED: "red",
	Colors.GREEN: "green",
	Colors.BLUE: "blue",
	Colors.YELLOW: "yellow",
	Colors.BLACK: "black",
	Colors.PURPLE: "purple",
	Colors.WHITE: "white"
}
