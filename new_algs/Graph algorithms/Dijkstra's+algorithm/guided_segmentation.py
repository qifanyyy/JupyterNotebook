import cv2
import sys
import math
import numpy as np
import dijkstra

def within_bounds(x, delta_x, y, delta_y, min_x, min_y, max_x, max_y):
    """
    Returns whether the pixel given by (x + delta_x, y + delta_y) is in the bounds of the box specified by (min_x, min_y) and (max_x, max_y).
    """
    return (x + delta_x) >= min_x and (x + delta_x) <= max_x and (y + delta_y) >= min_y and (y + delta_y) <= max_y

def compute_costs(grayscale):
    """
    Computes the costs for each edge in the graph represented by the grayscale input image.

    @param      grayscale           A grayscale input image
    @return     adj_list            A weighted adjacency list representation of the pixel graph represented by the input image
    """
    # Filter high frequency noise out of calculations of the energy matrix. 
    blur = cv2.blur(grayscale,(4,4))     
    # Convolve image with Sobel_x kernel.
    sobelx64f = cv2.Sobel(blur,cv2.CV_64F,1,0,ksize=5)
    abs_sobelx64f = np.absolute(sobelx64f)
    sobelx_8u = np.uint8(abs_sobelx64f)
    # Convolve image with Sobel_y kernel.
    sobely64f = cv2.Sobel(blur,cv2.CV_64F,0,1,ksize=5)
    abs_sobely64f = np.absolute(sobely64f)
    sobely_8u = np.uint8(abs_sobely64f)  
    # Calculate the gradient magnitude as a function of the output of the Sobel filter.  
    gradient = (sobelx_8u ** 2 + sobely_8u ** 2) ** 0.5
    
    laplacian = cv2.Laplacian(blur,cv2.CV_64F)

    max_filter_response = np.amax(gradient)    

    return gradient, laplacian, max_filter_response

    # Initialize the adjacency list representation of the weighted pixel graph.
    # adj_list = {}        

    # # Specify a pixel in the image. Recall that the "x" direction is vertical and "y" direction is horizontal, by convention.
    # for x in xrange(len(grayscale)):
    #     for y in xrange(len(grayscale[0])):
    #         adj_list[(x, y)] = []
    #         # Specify the direction to one of its valid neighbors.
    #         for delta_x in range(-1, 2):
    #             for delta_y in range(-1, 2):
    #                 if (delta_x != 0 or delta_y != 0) and within_bounds(x, delta_x, y, delta_y, len(grayscale), len(grayscale[0])):
    #                     # Cost[neigbhor] = (max - filter_response) * distance_to_neighbor
    #                     cost = (max_filter_response - gradient[x + delta_x][y + delta_y]) / max_filter_response * math.sqrt(delta_x ** 2 + delta_y ** 2)
    #                     val = 1
    #                     if laplacian[x + delta_x][y + delta_y] > 0:
    #                         for i in range(-1, 2):
    #                             for j in range(-1, 2):
    #                                 if within_bounds(x + delta_x, i, y + delta_y, j, len(grayscale), len(grayscale[0])):
    #                                     if laplacian[x + delta_x + i][y + delta_y + j] < 0:
    #                                         val = min((val, abs(laplacian[x + delta_x + i][y + delta_y + j]), abs(laplacian[x + delta_x][y + delta_y])))

    #                     if laplacian[x + delta_x][y + delta_y] < 0:
    #                         for i in range(-1, 2):
    #                             for j in range(-1, 2):
    #                                 if within_bounds(x + delta_x, i, y + delta_y, j, len(grayscale), len(grayscale[0])):
    #                                     if laplacian[x + delta_x + i][y + delta_y + j] > 0:
    #                                         val = min((val, abs(laplacian[x + delta_x + i][y + delta_y + j]), abs(laplacian[x + delta_x][y + delta_y])))
    #                     cost += val
    #                     adj_list[(x, y)].append(((x + delta_x, y + delta_y), cost))
    # return adj_list

def partial_adj_list(min_bounds, max_bounds, gradient, laplacian, max_filter_response):
    adj_list = {}
    for x in xrange(min_bounds[0], max_bounds[0] + 1):
        for y in xrange(min_bounds[1], max_bounds[1] + 1):
            adj_list[(x, y)] = []
            # Specify the direction to one of its valid neighbors.
            for delta_x in range(-1, 2):
                for delta_y in range(-1, 2):
                    if (delta_x != 0 or delta_y != 0) and within_bounds(x, delta_x, y, delta_y, min_bounds[0], min_bounds[1], max_bounds[0], max_bounds[1]):
                        # Cost[neigbhor] = (max - filter_response) * distance_to_neighbor
                        cost = (max_filter_response - gradient[x + delta_x][y + delta_y]) / max_filter_response * math.sqrt(delta_x ** 2 + delta_y ** 2)
                        val = 1
                        if laplacian[x + delta_x][y + delta_y] > 0:
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if within_bounds(x + delta_x, i, y + delta_y, j, min_bounds[0], min_bounds[1], max_bounds[0], max_bounds[1]):
                                        if laplacian[x + delta_x + i][y + delta_y + j] < 0:
                                            val = min((val, abs(laplacian[x + delta_x + i][y + delta_y + j]), abs(laplacian[x + delta_x][y + delta_y])))

                        if laplacian[x + delta_x][y + delta_y] < 0:
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if within_bounds(x + delta_x, i, y + delta_y, j, min_bounds[0], min_bounds[1], max_bounds[0], max_bounds[1]):
                                        if laplacian[x + delta_x + i][y + delta_y + j] > 0:
                                            val = min((val, abs(laplacian[x + delta_x + i][y + delta_y + j]), abs(laplacian[x + delta_x][y + delta_y])))
                        cost += val
                        adj_list[(x, y)].append(((x + delta_x, y + delta_y), cost))
    return adj_list

def main(image_filename, display_bounding_boxes=False):    
    """
    Executes interactive segmentation on an input image using Dijkstra's algorithm.

    @param      image_filename      The path to the input image
    """    
    # Read in the image and convert to grayscale for ease of computation.
    color_image = cv2.imread(image_filename)         
    grayscale = cv2.cvtColor(color_image, cv2.COLOR_RGB2GRAY)
    # Precompute the cost matrix (and by extension, the adjacency list) for the input image.
    gradient, laplacian, max_filter_response = compute_costs(grayscale)
    # Tracks the starting position of the path which the application should draw.
    main.start_point = None
    # mouse callback function
    def draw_path(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(color_image, (x, y), 5, (0, 255, 0), -1)
            if main.start_point is None:
                main.start_point = (y, x)
            else:
                end_point = (y, x)
                min_bounds = (min(main.start_point[0], end_point[0]), min(main.start_point[1], end_point[1]))
                max_bounds = (max(main.start_point[0], end_point[0]), max(main.start_point[1], end_point[1]))
                if display_bounding_boxes is True:
                    top_left = tuple(reversed(min_bounds))
                    bottom_right = tuple(reversed(max_bounds))
                    cv2.rectangle(color_image,top_left,bottom_right,(255,0,0),3)                
                adj_list = partial_adj_list(min_bounds, max_bounds, gradient, laplacian, max_filter_response)
                # Draw pixels from start_point to end_point, in color red.
                dist, parent = dijkstra.shortest_path(adj_list, main.start_point, end_point)
                # Construct the path itself from the parent dictionary.
                path = []
                temp = end_point
                while temp is not None:
                    path.append(temp)
                    temp = parent[temp]
                # Paint all those pixels red.
                for pixel in path:
                    cv2.circle(color_image, (pixel[1], pixel[0]), 1, (0, 0, 255), -1)
                # Get ready for next iteration by refreshing the start_point.
                main.start_point = end_point
        if event == cv2.EVENT_RBUTTONDOWN:
            main.start_point = None
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_path)
    while(1):
        cv2.imshow('image', color_image)
        if cv2.waitKey(20) & 0xFF == 27:
            break        
    cv2.destroyAllWindows()


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2 and len(args) != 3:
        print >>sys.stderr, "Please specify an appropriate set of command-line arguments. Run with -h flag for more details."
        sys.exit(1)
    if args[1] == "-h":
        print "guided_segmentation.py"
        print "Author: Sujay Tadwalkar"
        print
        print "Command Syntax:"
        print "python guided_segmentation.py [options] [flags]"
        print
        print "Options:"
        print "-h".ljust(40), "shows this help message".ljust(50)
        print "<input_filepath>".ljust(40), "input_filepath  is the path (absolute or relative) to the input image".ljust(50)
        print
        print "Flags:"
        print "-b",ljust(40), "displays bounding boxes for all paths to help the user understand the path connections"
        print 
        sys.exit(0)            
    if len(args) == 3 and args[2] == "-b":
        main(args[1], True)
    else:
        main(args[1])