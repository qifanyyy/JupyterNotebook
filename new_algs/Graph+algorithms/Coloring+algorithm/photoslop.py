import numpy as np, scipy.ndimage as ndi
import matplotlib.pyplot as plt
import os, sys


def analog_filter(images, smallest, show):
    floyd = [[-1, -1, 3],
             [5, 3, 7]]
    flatt = [[22, 10, 22],
             [10, 22, 10]]
    conv1 = ndi.convolve(images[smallest][:, :, 0], np.array(floyd)) / 16
    conv2 = ndi.convolve(images[smallest][:, :, 1], np.array(floyd)) / 16
    conv3 = ndi.convolve(images[smallest][:, :, 2], np.array(floyd)) / 16
    dith1 = images[smallest][:, :, 0] - conv1
    dith2 = images[smallest][:, :, 1] - conv2
    dith3 = images[smallest][:, :, 2] - conv3
    avg = (dith1 / 3 + dith2 / 3 + dith3 / 3) * 2.2
    test = ndi.convolve(dith1, np.array(flatt) / 16)
    if show:
        plt.imshow(avg + test, 'gray')
        plt.title(smallest)
        plt.show()


def load_test_images(image_library):
    images = {}
    pic_names = os.listdir(image_library)
    sizes = {}
    for name in pic_names:
        pic_path = '/media/tylersdurden/CoopersDB/Images/Astronomical/' + str(name)
        images[name] = plt.imread(pic_path)
        sizes[images[name].shape[1] * images[name].shape[0]] = name
    return images, sizes, pic_names


def main():
    images, sizes, pic_names = load_test_images('/media/tylersdurden/CoopersDB/Images/Astronomical/')

    ''' Calling this thing the analog filter '''
    if 'test' and 'show' in sys.argv:
        for pic_name in sizes.values():
            analog_filter(images, pic_name, True)
    elif '-test' in sys.argv:
        for pic_name in pic_names:
            analog_filter(images, pic_name, False)
        smallest = sizes[np.array(sizes.keys()).min()]

    test = images[pic_names.pop()]

    c0 = np.array(test[:,:,0])
    c1 = np.array(test[:,:,1])
    c2 = test[:,:,2]

    plt.imshow((ndi.median_filter(c0,2)), 'gray')
    plt.show()


if __name__ == '__main__':
    main()
