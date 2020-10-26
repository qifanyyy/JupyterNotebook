import scipy.ndimage as nd
from pyrp import RP
import sys

DEMO_PARAMS = './rp.npy'


def demo(path='./test_images/000013.jpg'):
     # Load image
    img = nd.imread(path)

    # Instantiate rp wrapper class
    rp = RP()

    # Load demo parameters
    rp.loadParamsFromNumpy(DEMO_PARAMS)

    # Get the boxes
    boxes = rp.getProposals(img)

    # Remove duplicates
    boxes = rp.removeDuplicates(boxes)

    return boxes

if __name__ == '__main__':

    image_path = ""
    save_path = ""

    try:
        if len(sys.argv) > 1:
            for arg in sys.argv[1:]:
                arg2 = arg.split("=")
                if arg2[0] == "image":
                    image_path = arg2[1]
                elif arg2[0] == "savefile":
                    save_path = arg2[1]

        if image_path is not "":
            boxes = demo(image_path)
        else:
            boxes = demo()

        if save_path is not "":
            if save_path.split(".")[-1] == "npy":
                import numpy as np
                np.save(save_path, boxes)
            elif save_path.split(".")[-1] == "mat":
                import scipy.io as scio
                print save_path
                scio.savemat(save_path, {'boxes': boxes})
        else:
            print boxes

    except Exception as e:
        print e.message
        print "Usage:"
        print "python demo.py [image=image_path] [savefile=(save_file.npy | save_file.mat)]"
