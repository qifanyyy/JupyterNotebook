from graph import Graph

def main():
	g = Graph(path="test/three_triangle.dot")
	print(g)
	g.startRunning(1000, 0.4)
	g.runColoring()
	g.showColoringStats()

if __name__ == "__main__":
    main()