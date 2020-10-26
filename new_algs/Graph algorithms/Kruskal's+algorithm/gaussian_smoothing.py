from __future__ import division
import cv2
import util
import math
from scipy import spatial
import time
import matlab_file_creator as mfc

DISPLAY_IMG = True
LOCAL_CURVE_THICKNESS = math.sqrt(2)
SMOOTHING_ROUNDS = 20

""" Applies a Gaussian Weighting Function to smooth the given curve
    Locates nearest neighbors using a KD-Tree """
def gaussian_smoothing_function(moving_pixels, p1):

    coords = util.Pixel.pixel2coords(moving_pixels)
    kdtree = spatial.KDTree(coords)
    neighbors = kdtree.query_ball_point([p1.x, p1.y], 10*p1.lsw)
    if len(neighbors) < 2: return

    sum1 = [0, 0]
    sum2 = 0
    for idx_n in neighbors:
        if p1 == moving_pixels[idx_n]: continue
        w = math.exp(-(util.pointDist(p1, moving_pixels[idx_n])/2*p1.lsw**2))
        sum1[0] += w * moving_pixels[idx_n].x
        sum1[1] += w * moving_pixels[idx_n].y
        sum2 += w

    if sum2 == 0: return
    p1.x = sum1[0]/sum2
    p1.y = sum1[1]/sum2


""" Iterates through curves and applies smoothing function """
def smooth_image(f, curves, img, artist, img_name):

    curveImg = util.mapCurvesToImg(curves, img.shape)
    util.display_img(curveImg, "Current Image", DISPLAY_IMG)
    cv2.imwrite("smoothing/%s/%s/%s_Smoothing_%d.jpg" % (artist, img_name, img_name, 0), curveImg)

    """ Iteratively smooth each curve """

    start_time = time.time()
    for i in xrange(SMOOTHING_ROUNDS):
        print("Round %s" % i)
        if i % 5 == 0 and i != 0:
            curveImg = util.mapCurvesToImg_circles(curves, img.shape)
            util.display_img(curveImg, "Post Smoothing %d" % i, DISPLAY_IMG)
            cv2.imwrite("smoothing/%s/%s/%s_Smoothing_%d.jpg" % (artist, img_name, img_name, i), curveImg)
        for curve in curves:
            for point in curve:
                gaussian_smoothing_function(curve, point)
    end_time = time.time()
    f.write('Time spent smoothing (s): %s\n' % (end_time - start_time))

    curveImg = util.mapCurvesToImg_circles(curves, img.shape)
    util.display_img(curveImg, "Post Smoothing %s" % SMOOTHING_ROUNDS, DISPLAY_IMG)

    cv2.imwrite("smoothing/%s/%s/%s_Smoothing_%d.jpg" % (artist, img_name, img_name, 30), curveImg)
    #util.save_curves_matlab("%s_SMOOTH" % img_name, artist, "curves", curves, img.shape)
    mfc.save_matlab_suite("%s_SMOOTH" % img_name, artist, "curves", curves, img.shape)
    util.save_curves("%s_SMOOTH.txt" % img_name, artist, "curves", curves)

""" MAIN CODE """

if __name__ == "__main__":

    #artists = ['foster', 'levesque', 'koudelka', 'vidal', 'fiala','fiala', 'vidal']
    #images = ['test2', 'levesque2', 'koudelka5', 'vidal2','fiala_001', 'fiala_010', 'vidal6']
    artists = ['vidal']
    images = ['vidal6']

    for i in xrange(len(images)):
        artist = artists[i]
        img_name = images[i]

        print("Curve Fitting for %s, %s" % (artist, img_name))

        # Load a color image in grayscale
        img = cv2.imread("samples/%s/%s.jpg" % (artist, img_name), 0)
        util.display_img(img, "Initial Image", DISPLAY_IMG)

        img_name += "_PR_NBHD"

        #img_name += "_LSW"
        util.DW("smoothing/%s/%s" % (artist, img_name))
        util.DW("vectorized/%s" % artist)

        f = open("%s/%s/%s_smoothing.txt" % ("stats", artist, img_name), 'w')

        curves = util.load_curves("%s.txt" % img_name, artist, "curves")

        img_name += "_WHAT"

        mfc.save_matlab_suite("%s_MESSY" % img_name, artist, "curves", curves, img.shape)
        f.write("Number of curves: %d\n" % len(curves))

        smooth_image(f, curves)

        f.close()


