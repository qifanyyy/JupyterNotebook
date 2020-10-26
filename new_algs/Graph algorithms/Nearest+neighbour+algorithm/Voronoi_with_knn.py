import numpy as np
from sklearn import neighbors
from PIL import Image, ImageDraw

colors = np.array([[180, 0, 0], [0, 150, 200], [10, 150, 45], [100,100,100], [24,24,24], [0,255,0], [0,0,255], [100,100,200], [75,0,27]])
seeds = np.array([[50, 50], [150, 350], [400, 150],[256, 256],[300,200],[60,200], [29,69], [450, 55], [250,40]])
n_neighbors = 1
dim = 512

def main():
	
	clf = neighbors.KNeighborsClassifier(n_neighbors, weights='uniform',algorithm='auto')
	clf.fit(seeds, colors)


	plot_colors = np.zeros((dim,dim,3), 'uint8')
	plot_coordinates = np.zeros((dim*dim,2))
	
	#The first while loop is a transformation of the data into a format that the classifier will accept
	#The second reverts back to an RGB array tha PIL will understand

	i = 0
	j = 0
	count = 0
	while i < 512:
		while j < 512:
			plot_coordinates[count] = [i, j]
			count += 1
			j += 1
		j = 0
		i += 1

	#Predicted colors for each pixel
	y = clf.predict(plot_coordinates)
	
	i = 0
	j = 0
	count = 0
	while i < 512:
		while j < 512:
			plot_colors[i][j] = y[count]
			count += 1
			j += 1
		j = 0
		i += 1

	r = 2
	img = Image.fromarray(plot_colors)
	draw = ImageDraw.Draw(img)
	for p in seeds:
		draw.ellipse([p[1] - r, p[0] - r, p[1] + r, p[0] + r], fill=(255,255,255))
	img.show()
	img.save('myPlot_with_nearest_neighbors.jpeg')
	

if __name__ == '__main__':
	main()