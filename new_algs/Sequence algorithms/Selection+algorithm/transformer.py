import numpy as np
import cv2 as cv
import random

"""
@author: Jia Geng
@email: jxg570@miami.edu

Dev Log
10/15   Current version only support grayscale
10/16   17 Transformers implemented
10/17   Changed the input/param format requirements: input & param all must be float
10/18   Implemented a super class for better reporting the params
10/18   Added height param. But the random threshold is still only bounded by width
10/24   Fixed an error cause by the census transformation which will crop the border of the image. Pad image by 1. 
10/24   Used 1e-8 instead of 0 as the lower bound for normalization and log transformation for stability
11/1    Refactored some methods. Added a decode method that make the params compatible for json
"""


class Transformer:

    def __init__(self, width, height):
        """
        Basic element for init a transformer
        :param width:
        """
        self.width = width
        self.height = height
        self.code = -1
        self.params = []

    def mutate(self, r=0.0005):
        """
        Dummy super class method
        :param r:
        :return:
        """
        pass

    def rep(self):
        """
        Return the description of the transformer
        :return: description
        """

        rep = [self.code, self.params]
        return rep

    def decode_params(self):
        """
        Decode the param for the transformers
        :return: decoded params
        """
        return self.params

    @staticmethod
    def get_tfm(img_width, img_height, gene):
        """
        Get a tfm
        :param img_width: img width
        :param img_height: img height
        :param gene: gene code: -1 means random
        :return:
        """

        if gene == -1:
            gene = random.randrange(1, 18)

        if gene == 1:
            x = AdaptiveThreshold(width=img_width, height=img_height)
        elif gene == 2:
            x = CannyEdge(width=img_width, height=img_height)
        elif gene == 3:
            x = CensusTransformation(width=img_width, height=img_height)
        elif gene == 4:
            x = CLAHistogram(width=img_width, height=img_height)
        elif gene == 5:
            x = HistogramEqualization(width=img_width, height=img_height)
        elif gene == 6:
            x = DistanceTransformation(width=img_width, height=img_height)
        elif gene == 7:
            x = Dilate(width=img_width, height=img_height)
        elif gene == 8:
            x = Erode(width=img_width, height=img_height)
        elif gene == 9:
            x = DifferenceGaussian(width=img_width, height=img_height)
        elif gene == 10:
            x = GaussianBlur(width=img_width, height=img_height)
        elif gene == 11:
            x = Gradient(width=img_width, height=img_height)
        elif gene == 12:
            x = HarrisCorner(width=img_width, height=img_height)
        elif gene == 13:
            x = IntegralTransformation(width=img_width, height=img_height)
        elif gene == 14:
            x = LaplacianEdge(width=img_width, height=img_height)
        elif gene == 15:
            x = Log(width=img_width, height=img_height)
        elif gene == 16:
            x = MediumBlur(width=img_width, height=img_height)
        elif gene == 17:
            x = SquareRoot(width=img_width, height=img_height)
        elif gene == 18:
            x = Gabor(width=img_width, height=img_height)
        else:
            raise Exception("Invalid Gene Number {}".format(gene))

        return x


class AdaptiveThreshold(Transformer):
    """
    Transformer AdaptiveThreshold
    """

    def __init__(self, width, height):
        """
        Constructor, initialize params randomly
        :param width: image size
        :param height: image height
        """
        Transformer.__init__(self, width, height)
        self.code = 1
        x, y, z = np.random.choice(2, 1), np.random.choice(2, 1), np.random.choice(2, 1)
        adaptive_approach = 1 if x == 1 else 2
        thresh_mode = 1 if y == 1 else 2
        block_size = random.randrange(3, width + 1, 2)
        self.params = [adaptive_approach, thresh_mode, block_size]
        self.c = 0

    def mutate(self, r=0.0005):
        """
        If mutate, regenerate the parameter
        :param r: mutate rate
        :return: void
        """

        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[0] = 1 if np.random.choice(2, 1) == 0 else 2
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[1] = 1 if np.random.choice(2, 1) == 0 else 2
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[2] = random.randrange(3, self.width + 1, 2)

    def transform(self, img: np.ndarray):
        """
        Process the img
        :param img:
        :return: masked img in float format
        """
        if img.dtype == np.float:
            img_8u = (img * 255).astype(np.uint8)
        else:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        decoded_params = self.decode_params()

        mask = cv.adaptiveThreshold(img_8u, 255, decoded_params[0], decoded_params[1], decoded_params[2], self.c)
        return img * (mask == 255)

    def decode_params(self):
        """
        Decode the params
        :return: decoded params
        """
        decoded = [None, None, None]

        if self.params[0] == 1:
            decoded[0] = cv.ADAPTIVE_THRESH_MEAN_C
        elif self.params[0] == 2:
            decoded[0] = cv.ADAPTIVE_THRESH_GAUSSIAN_C
        else:
            raise Exception("Param 0 code should be {} or {} but was {}".format(1, 2, self.params[0]))

        if self.params[1] == 1:
            decoded[1] = cv.THRESH_BINARY
        elif self.params[1] == 2:
            decoded[1] = cv.THRESH_BINARY_INV
        else:
            raise Exception("Param 1 code should be {} or {} but was {}".format(1, 2, self.params[1]))

        decoded[2] = self.params[2]

        return decoded


class CannyEdge(Transformer):
    """
    Transformer CannyEdge
    """

    def __init__(self, width, height):
        """
        Constructor init random params
        """

        Transformer.__init__(self, width, height)
        self.code = 2
        theta = random.uniform(0.3, 0.9)
        self.params = [theta]

    def mutate(self, r=0.0005):
        """
        Mutate
        :param r: mutate rate
        :return: void
        """
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[0] = random.uniform(0.3, 0.9)

    def transform(self, img):
        """
        Process image
        :param img: input img
        :return: Edged Image
        """

        if img.dtype == np.float:
            img_8u = (img * 255).astype(np.uint8)
        else:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        thresh, _ = cv.threshold(img_8u, thresh=0, maxval=255, type=(cv.THRESH_BINARY + cv.THRESH_OTSU))
        mask = cv.Canny(img_8u, threshold1=int(thresh * 0.1), threshold2=int(thresh * self.params[0]))
        return img * (mask == 255)


class CensusTransformation(Transformer):
    """
    Census Transformation 3x3 patch
    """

    def __init__(self, width, height):
        """
        Constructor
        :param width: image width
        """

        Transformer.__init__(self, width, height)
        self.code = 3

    def transform(self, img: np.ndarray):
        """
        Census transformation.
        Encode each pixel according to pixel's rank
        :param img: input image
        :return: census transformed image
        """

        if img.dtype != np.float:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        img = cv.copyMakeBorder(img, 1, 1, 1, 1, cv.BORDER_CONSTANT, None, 0)

        w, h = self.width + 2, self.height + 2

        # Initialize param array
        census = np.zeros((h - 2, w - 2), dtype=np.uint8)

        # centre pixels, which are offset by (1, 1)
        cp = img[1:h - 1, 1:w - 1]

        # offsets of non-central pixels
        offsets = [(u, v) for v in range(3) for u in range(3) if not u == 1 == v]

        # Do the pixel comparisons (encode the neighborhood compare into)
        for u, v in offsets:
            census = (census << 1) | (img[v:v + h - 2, u:u + w - 2] >= cp)

        return (census / 255).astype(np.float)


class CLAHistogram(Transformer):
    """
    Contrast Limited Adaptive Histogram Equalization.
    Enhance the contrast of an image.
    """

    def __init__(self, width, height):
        """
        Constructor
        Random clip limit and tile size
        :param width: image size
        """

        Transformer.__init__(self, width, height)
        self.code = 4
        clip_limit = np.random.uniform(10, 40)
        tile_size = random.randrange(3, width + 1)
        self.params = [clip_limit, tile_size]

    def mutate(self, r=0.0005):
        """
        Mutate
        :param r: mutate rate
        :return:
        """

        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[0] = np.random.uniform(10, 40)
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[1] = random.randrange(3, self.width + 1)

    def transform(self, img: np.ndarray):
        """
        Process the image
        :param img: image to be processed
        :return:
        """

        if img.dtype == np.float:
            img_8u = (img * 255).astype(np.uint8)
        else:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        clahe = cv.createCLAHE(clipLimit=self.params[0], tileGridSize=(self.params[1], self.params[1]))
        img = clahe.apply(img_8u, None)

        return (img / 255).astype(np.float)


class HistogramEqualization(Transformer):
    """
    Histogram Equalization to enhance the contrast of the image
    """

    def __init__(self, width, height):
        Transformer.__init__(self, width, height)
        self.code = 5

    @staticmethod
    def transform(img: np.ndarray):
        if img.dtype == np.float:
            img_8u = (img * 255).astype(np.uint8)
        else:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))
        img = cv.equalizeHist(img_8u, None)
        return (img / 255).astype(np.float)


class DistanceTransformation(Transformer):
    """
    Distance Transform.
    Threshold image into binary image then compute the distance of each pixel's distance to the closest null pixel
    """

    def __init__(self, width, height):
        """
        Constructor. Random distance method and kernel size.
        :param width:
        """

        Transformer.__init__(self, width, height)
        self.code = 6
        dist = 1 if random.randrange(2) == 0 else 2
        k_size = 3 if random.randrange(2) == 0 else 5
        self.params = [dist, k_size]

    def mutate(self, r=0.0005):
        """
        Mutate
        :param r: mutate rate
        :return: void
        """

        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[0] = 1 if random.randrange(2) == 0 else 2
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[1] = 3 if random.randrange(2) == 0 else 5

    def transform(self, img):
        """
        Process image: auto-threshold to binary image, then apply distance transform plus normalization
        :param img: input image
        :return: distance transformed image
        """

        if img.dtype == np.float:
            img_8u = (img * 255).astype(np.uint8)
        else:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        # algorithm decide threshold
        _, img = cv.threshold(img_8u, 0, 1.0, cv.THRESH_BINARY | cv.THRESH_OTSU)

        # the dist image will be normalized and convert to uint8

        decoded = self.decode_params()
        img = cv.distanceTransform(img, decoded[0], decoded[1], dstType=cv.CV_64F)

        # normalization
        img = cv.normalize(img, None, 1e-8, 1.0, cv.NORM_MINMAX, cv.CV_64F)
        return img

    def decode_params(self):
        """
        Decode the param
        :return: decoded param
        """
        decoded = [None, None]
        if self.params[0] == 1:
            decoded[0] = cv.DIST_L1
        elif self.params[0] == 2:
            decoded[0] = cv.DIST_L2
        else:
            raise Exception("Param 0 code should be {} or {} but was {}".format(1, 2, self.params[0]))

        decoded[1] = self.params[1]

        return decoded


class Dilate(Transformer):
    """
    Dilate the image.
    """

    def __init__(self, width, height):
        """
        Constructor
        One random param -> iteration. More iteration -> more dilated
        :param width: image width
        """

        Transformer.__init__(self, width, height)
        self.code = 7
        num_iter = random.randrange(1, 9)  # more iterations -> more dilated
        self.params = [num_iter]

    def mutate(self, r=0.0005):
        """
        Mutate
        :param r: mutate rate
        :return: void
        """

        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[0] = random.randrange(1, 9)

    def transform(self, img):
        """
        Process image
        :param img: input image
        :return: dilated image
        """

        if img.dtype != np.float:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        img = cv.dilate(img, kernel=(3, 3), iterations=self.params[0])  # use default kernel size the 8 neighbors
        return img


class Erode(Transformer):
    """
    Erode the image.
    One random param -> iteration. More iteration -> more eroded
    """

    def __init__(self, width, height):
        """
        Constructor
        :param width: image width
        """

        Transformer.__init__(self, width, height)
        self.code = 8
        num_iter = random.randrange(1, 9)  # more iterations -> more eroded
        self.params = [num_iter]

    def mutate(self, r=0.0005):
        """
        Mutate
        :param r: mutate rate
        :return: void
        """

        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[0] = random.randrange(1, 9)

    def transform(self, img):
        """
        Process image
        :param img: input image
        :return: dilated image
        """

        if img.dtype != np.float:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        img = cv.erode(img, kernel=(3, 3), iterations=self.params[0])  # use default kernel size the 8 neighbors
        return img


class DifferenceGaussian(Transformer):

    def __init__(self, width, height):
        """
        Constructor.
        Two random param: sigma value and the aspect ratio between two sigmas
        The rule is that the kernel size need to be 3 * sigma while smaller than the patch size
        :param width: image width
        :param height: image height
        """

        Transformer.__init__(self, width, height)
        self.code = 9

        sigma_a = random.uniform(1, 3)  # smaller sigma
        self.ratio = random.uniform(1, 5)  # ratio between smaller sigma and the larger sigma
        sigma_b = sigma_a * self.ratio
        a, b = 3 * sigma_a, 3 * sigma_b
        a, b = int(np.ceil(a) // 2 * 2 + 1), int(np.ceil(b) // 2 * 2 + 1)  # round to nearest odd
        t = self.width if self.width % 2 == 1 else self.width - 1
        a, b = min(a, t), min(b, t)  # kernel size can not be larger than the width also odd
        k_size_a = a
        k_size_b = b

        self.params = [sigma_a, k_size_a, sigma_b, k_size_b]

    def mutate(self, r=0.0005):
        """
        Mutate
        :param r: mutate rate
        :return: void
        """

        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[0] = random.uniform(1, 3)
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.ratio = random.uniform(1, 5)
        self.params[2] = self.params[0] * self.ratio
        a, b = 3 * self.params[0], 3 * self.params[2]
        a, b = int(np.ceil(a) // 2 * 2 + 1), int(np.ceil(b) // 2 * 2 + 1)
        t = self.width if self.width % 2 == 1 else self.width - 1
        a, b = min(a, t), min(b, t)  # kernel size can not be larger than the width also odd
        self.params[1] = a
        self.params[3] = b

    def transform(self, img):
        """
        Process the image.
        Take the difference between two gaussian
        :param img: input image
        :return: difference of gaussian
        """

        if img.dtype != np.float:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))
        img_a = cv.GaussianBlur(img, ksize=(self.params[1], self.params[1]), sigmaX=self.params[0])
        img_b = cv.GaussianBlur(img, ksize=(self.params[3], self.params[3]), sigmaX=self.params[2])
        img = cv.normalize(img_b - img_a, None, 1e-8, 1.0, cv.NORM_MINMAX, cv.CV_64F)
        return img


class GaussianBlur(Transformer):
    """
    Gaussian Blur
    """

    def __init__(self, width, height):
        """
        Constructor
        One random param: sigma
        The kernel size is three times of the sigma
        The kernel size should not be larger than the patch
        :param width: image width
        :param height: image height
        """
        Transformer.__init__(self, width, height)
        self.code = 10
        sigma = random.uniform(1, min(width / 3, 5))
        a = sigma * 3
        k_size = int(np.ceil(a) // 2 * 2 + 1)
        self.params = [sigma, k_size]

    def mutate(self, r=0.0005):
        """
        Mutate
        :param r: mutate rate
        :return: void
        """

        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[0] = random.uniform(1, min(self.width / 3, 5))
            a = self.params[0] * 3
            self.params[1] = int(np.ceil(a) // 2 * 2 + 1)

    def transform(self, img):
        """
        Process the image
        :param img: input image
        :return: blurred image
        """

        if img.dtype != np.float:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        img = cv.GaussianBlur(img, ksize=(self.params[1], self.params[1]), sigmaX=self.params[0])
        return img


class Gradient(Transformer):
    """
    Gradient filters
    """

    def __init__(self, width, height):
        """
        Constructor.
        One random param decide which gradient filter to use
        :param width: image width
        :param height: image height
        """

        Transformer.__init__(self, width, height)
        self.code = 11
        kernel = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]
        self.params = [kernel]
        g = random.randrange(4)
        if g == 0:
            self.prewitt()
        elif g == 1:
            self.sobel()
        elif g == 2:
            self.kirsch()
        elif g == 3:
            self.scharr()
        else:
            raise Exception("Random Number out of scope {}".format(g))

    def prewitt(self):
        """
        Prewitt filter
        :return: void
        """
        if random.randrange(2) == 0:
            self.params[0] = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]
        else:
            self.params[0] = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]

    def sobel(self):
        """
        Sobel filter
        :return: void
        """
        if random.randrange(2) == 0:
            self.params[0] = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
        else:
            self.params[0] = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]

    def kirsch(self):
        """
        Kirsch filter
        :return: void
        """
        x = random.randrange(8)
        if x == 0:
            self.params[0] = [[5, 5, 5], [-3, 0, -3], [-3, -3, -3]]
        elif x == 1:
            self.params[0] = [[5, 5, -3], [5, 0, -3], [-3, -3, -3]]
        elif x == 2:
            self.params[0] = [[5, -3, -3], [5, 0, -3], [5, -3, -3]]
        elif x == 3:
            self.params[0] = [[-3, -3, -3], [5, 0, -3], [5, 5, -3]]
        elif x == 4:
            self.params[0] = [[-3, -3, -3], [-3, 0, -3], [5, 5, 5]]
        elif x == 5:
            self.params[0] = [[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]]
        elif x == 6:
            self.params[0] = [[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]]
        else:
            self.params[0] = [[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]]

    def scharr(self):
        """
        Scharr filter
        :return: void
        """
        if random.randrange(2) == 0:
            self.params[0] = [[3, 10, 3], [0, 0, 0], [-3, -10, -3]]
        else:
            self.params[0] = [[3, 0, -3], [10, 0, -10], [3, 0, -3]]

    def mutate(self, r=0.0005):
        """
        Mutate
        :param r:
        :return:
        """
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            g = random.randrange(4)
            if g == 0:
                self.prewitt()
            elif g == 1:
                self.sobel()
            elif g == 2:
                self.kirsch()
            elif g == 3:
                self.scharr()
            else:
                raise Exception("Random number out of scope {}".format(g))

    def transform(self, img):
        """
        Process image
        :param img: input image
        :return: normalized gradient image
        """

        if img.dtype != np.float:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))
        decoded_param = self.decode_params()
        img = cv.filter2D(img, -1, kernel=decoded_param)
        img = cv.normalize(img, None, 1e-8, 1.0, cv.NORM_MINMAX, cv.CV_64F)
        return img

    def decode_params(self):
        """
        Decode the params
        :return: decoded params
        """

        decoded = np.asarray(self.params[0])
        return decoded


class HarrisCorner(Transformer):
    """
    Harris Corner
    """

    def __init__(self, width, height):
        """
        Constructor
        Three random param: block size, kernel size, k
        :param width: image width
        :param height: image height
        """
        Transformer.__init__(self, width, height)
        self.code = 12
        block_size = random.randrange(2, width + 1)
        k_size_upper = min(width // 2 * 2 + 1, 31)
        k_size = random.randrange(3, k_size_upper + 1, step=2)
        k = random.uniform(0.01, 0.09)
        self.params = [block_size, k_size, k]

    def mutate(self, r=0.0005):
        """
        Mutate
        :param r: mutate rate
        :return:
        """
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[0] = random.randrange(2, self.width + 1)
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            k_size_upper = min(self.width // 2 * 2 + 1, 31)
            self.params[1] = random.randrange(3, k_size_upper + 1, step=2)
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[2] = random.uniform(0.01, 0.09)

    def transform(self, img):
        """
        Process image
        :param img: input image
        :return: harris corner, normalized
        """

        if img.dtype != np.float:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        img = cv.cornerHarris(img.astype(np.float32), blockSize=self.params[0], ksize=self.params[1], k=self.params[2])
        img = cv.normalize(img, None, 1e-8, 1.0, cv.NORM_MINMAX, cv.CV_64F)
        return img


class IntegralTransformation(Transformer):
    """
    Image Integral
    """

    def __init__(self, width, height):
        """
        Constructor
        :param width: image width
        :param height: image height
        """

        Transformer.__init__(self, width, height)
        self.code = 13

    @staticmethod
    def transform(img):
        """
        Process image
        :param img: input image
        :return: normalized integral
        """

        if img.dtype != np.float:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        img = cv.normalize(cv.integral(img), None, 1e-8, 1.0, cv.NORM_MINMAX, cv.CV_64F)[1:, 1:]
        return img


class LaplacianEdge(Transformer):
    """
    Laplacian Filter
    """

    def __init__(self, width, height):
        """
        Constructor
        :param width: image width
        :param height: image height
        """

        Transformer.__init__(self, width, height)
        self.code = 14
        k_size = random.randrange(3, min(self.width + 1, 31), step=2)
        self.params = [k_size]

    def mutate(self, r=0.0005):
        """
        Mutate
        :param r: mutate rate
        :return: void
        """

        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[0] = random.randrange(3, min(self.width + 1, 31), step=2)

    def transform(self, img):
        """
        Process image
        :param img: input image
        :return: normalized laplacian edges
        """

        if img.dtype != np.float:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        img = cv.normalize(cv.Laplacian(img, ddepth=-1, ksize=self.params[0]), None, 1e-8, 1.0, cv.NORM_MINMAX,
                           cv.CV_64F)
        return img


class Log(Transformer):
    """
    Logarithm Transformation
    """

    def __init__(self, width, height):
        """
        Constructor
        :param width: image width
        :param height: image height
        """

        Transformer.__init__(self, width, height)
        self.code = 15

    @staticmethod
    def transform(img):
        """
        Process image with logarithm transformer to enhance contrast
        p = c * log(1 + img)
        :param img: input image
        :return:
        """

        if img.dtype == np.float:
            img_8u = (img * 255).astype(np.uint8)
        else:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        contrast = 255 / (np.log(img_8u.max() + 1 + 1e-8))  # in case divide by 0
        img = contrast * np.log(1 + 1e-8 + img_8u.astype(np.float))
        img = cv.normalize(img, None, 1e-8, 1.0, cv.NORM_MINMAX, cv.CV_64F)
        return img


class MediumBlur(Transformer):
    """
    Medium Blur
    """

    def __init__(self, width, height):
        """
        Constructor
        :param width: image width
        :param height: image height
        """

        Transformer.__init__(self, width, height)
        self.code = 16
        k = random.randrange(3, min(width + 1, 15), step=2)
        self.params = [k]

    def mutate(self, r=0.0005):
        """
        Mutate
        :param r: mutate rate
        :return: void
        """
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[0] = random.randrange(3, min(self.width + 1, 15), step=2)

    def transform(self, img):
        """
        Processing Data
        :param img: input image
        :return: smoothed image
        """

        if img.dtype != np.float:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        if self.params[0] <= 5:
            img = img.astype(np.float32)
            img = cv.medianBlur(img, ksize=self.params[0])
            img = img.astype(np.float)
        else:
            img_8u = (img * 255).astype(np.uint8)
            img = (cv.medianBlur(img_8u, ksize=self.params[0]) / 255).astype(np.float)
        return img


class SquareRoot(Transformer):
    """
    Square root for Gamma modification
    """

    def __init__(self, width, height):
        """
        Constructor
        :param width: image width
        :param height: image height
        """

        Transformer.__init__(self, width, height)
        self.code = 17

    @staticmethod
    def transform(img):
        """
        Must be performed on float points [0, 1] so that it have meaningful effect.
        Increase the contrast
        :param img:
        :return:
        """
        if img.dtype != np.float:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        # make sure there are no funny number
        img[img < 0] = 1e-8

        return np.sqrt(img)


class Gabor(Transformer):
    """
    Gabor filter
    """

    def __init__(self, width, height):
        """
        Constructor
        4 random params
        - sigma: sigma of the gaussian
        - theta: orientation
        - lambd: wavelength
        - gamma: aspect ratio = 1 means circle, otherwise oval
        :param width: image width
        """
        Transformer.__init__(self, width, height)
        sigma = random.uniform(1, min(width / 3, 5))
        ksize = int(3 * sigma)
        theta = np.pi * random.uniform(0, 1)
        lambd = random.randrange(3, width // 2)
        if random.randrange(2) == 1:
            gamma = random.uniform(0, 1)
        else:
            gamma = 1
        self.params = [ksize, sigma, theta, lambd, gamma]
        self.code = 18

    def mutate(self, r=0.0005):
        """
        Mutate
        :param r: mutate rate
        :return: void
        """
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[1] = random.uniform(1, min(self.width // 3, 5))
            self.params[0] = int(3 * self.params[0])
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[2] = np.pi * random.uniform(0, 1)
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            self.params[3] = random.randrange(3, self.width // 2)
        if np.random.choice(2, 1, p=[1 - r, r]) == 1:
            if random.randrange(2) == 1:
                self.params[4] = random.uniform(0, 1)
            else:
                self.params[4] = 1

    def transform(self, img):
        """
        Must be performed on float points [0, 1] so that it have meaningful effect.
        Increase the contrast
        :param img: input image
        :return:
        """

        # check input
        if img.dtype != np.float:
            raise Exception("Input should be {} but was {}".format(np.float, img.dtype))

        # apply kernel
        kernel = cv.getGaborKernel(ksize=(self.params[0], self.params[0]), sigma=self.params[1], theta=self.params[
                2], lambd=self.params[3], gamma=self.params[4], psi=0, ktype=cv.CV_64F)
        img = cv.filter2D(img, -1, kernel=kernel)

        img = cv.normalize(img, None, 1e-8, 1.0, cv.NORM_MINMAX, cv.CV_64F)
        return img

#
# class HoughCircle(Transformer):
#     """
#     Hough circles
#     """
#     def __init__(self, width, height):
#         """
#         Constructor
#         4 random param
#         - min_dist_ratio decide minDist
#         - theta: decide the param1 param2
#         - min_r_ratio/max_r_ratio: decide the min/max radius
#         :param width: subpatch width
#         :param height: subpatch height
#         """
#         Transformer.__init__(self, width=width, height=height)
#         min_dist_ratio = random.uniform(0, 0.2)
#         theta = random.uniform(0.3, 0.9)
#         min_r_ratio = random.uniform(0, 0.3)
#         max_r_ratio = random.uniform(0.3, 0.9)
#         self.params = [min_dist_ratio, theta, min_r_ratio, max_r_ratio]
#         self.code = 19
#
#     def mutate(self, r=0.0005):
#         """
#         Mutate
#         :param r: mutate rate
#         :return: void
#         """
#         if np.random.choice(2, 1, p=[1 - r, r]) == 1:
#             self.params[0] = random.uniform(0, 1)
#         if np.random.choice(2, 1, p=[1 - r, r]) == 1:
#             self.params[1] = random.uniform(0.3, 0.9)
#         if np.random.choice(2, 1, p=[1 - r, r]) == 1:
#             self.params[2] = random.uniform(0, 0.3)
#         if np.random.choice(2, 1, p=[1 - r, r]) == 1:
#             self.params[3] = random.uniform(0.3, 0.9)
#
#     def transform(self, img):
#
#         # check input
#         if img.dtype != np.float:
#             raise Exception("Input should be {} but was {}".format(np.float, img.dtype))
#
#         img_8u = (img * 255).astype(np.uint8)
#         thresh, _ = cv.threshold(img_8u, thresh=0, maxval=255, type=(cv.THRESH_BINARY + cv.THRESH_OTSU))
#         thresh = max(1, thresh)
#         min_dist = max(3, int(self.params[0] * max(self.width, self.height)))
#         param1, param2 = thresh * 0.1, thresh * self.params[1]
#         print(param1, param2)
#         min_r = max(3, int(self.params[2] * min(self.width, self.height)))
#         max_r = max(3, int(self.params[3] * min(self.width, self.height)) + 1)
#         circles = cv.HoughCircles(image=img_8u, method=cv.HOUGH_GRADIENT, dp=1, minDist=min_dist, param1=param1,
#                                   param2=param2, minRadius=min_r, maxRadius=max_r)
