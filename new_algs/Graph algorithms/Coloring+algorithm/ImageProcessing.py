import cv2
import numpy as np


class IP:

    def __init__(self, img_dir):
        self.img_dir = img_dir
        self.src_img = cv2.imread(cv2.samples.findFile(img_dir))
        gray_img = cv2.cvtColor(self.src_img, cv2.COLOR_RGB2GRAY)
        bw = cv2.threshold(gray_img, 10, 255, cv2.THRESH_BINARY)[1]
        self.bw = cv2.bitwise_not(bw)
        self.num_labels, self.labels = cv2.connectedComponents(self.bw)
        self.init_colors = {1: [255, 161, 0],
                            2: [161, 0, 255],
                            3: [0, 255, 161],
                            4: [0, 235, 255],
                            5: [128, 128, 128],
                            6: [0, 0, 0]}
        print("Done!")

    def adjacency_matrix(self):
        height = self.src_img.shape[0]
        width = self.src_img.shape[1]

        matrix = [[0 for col in range(self.num_labels - 2)] for row in range(self.num_labels - 2)]

        for i in range(height):
            last = 1
            c = 0
            for j in range(width):
                if self.labels[i, j] == 0:
                    c = c + 1
                    continue
                if self.labels[i, j] == last:
                    c = 0
                    continue
                if c > 5:
                    last = self.labels[i, j]
                    c = 0
                    continue
                label_index = self.labels[i, j] - 2
                last_index = last - 2
                c = 0
                if last_index != -1 and label_index != -1 and matrix[last_index][label_index] != 1:
                    matrix[last_index][label_index] = 1
                    matrix[label_index][last_index] = 1
                last = self.labels[i, j]

        for i in range(width):
            last = 1
            c = 0
            for j in range(height):
                if self.labels[j, i] == 0:
                    c = c + 1
                    continue
                if self.labels[j, i] == last:
                    c = 0
                    continue
                if c > 5:
                    last = self.labels[j, i]
                    c = 0
                    continue
                label_index = self.labels[j, i] - 2
                last_index = last - 2
                c = 0
                if last_index != -1 and label_index != -1 and matrix[last_index][label_index] != 1:
                    matrix[last_index][label_index] = 1
                    matrix[label_index][last_index] = 1
                last = self.labels[j, i]

        print("Done!")
        print(matrix.__len__(), " Regions")
        return matrix

    def show(self, colors):
        cv2.imshow('Binary Image', self.src_img)
        cv2.waitKey()

        colors.insert(0, 5)
        colors.insert(0, 6)
        colored = np.array([[self.init_colors[colors[j]] for j in i] for i in self.labels], dtype=np.uint8)

        cv2.imshow('Colored Image', colored)
        cv2.waitKey()

        label_hue = np.uint8(179 * self.labels / np.max(self.labels))
        blank_ch = 255 * np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
        labeled_img[label_hue == 0] = 0

        cv2.imshow("Component Labeling", cv2.cvtColor(labeled_img, cv2.COLOR_BGR2RGB))
        cv2.waitKey()
