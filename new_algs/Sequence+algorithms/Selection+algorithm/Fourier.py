import cv2
import numpy

MIN_DESCRIPTOR = 10
TRAINING_SIZE = 2

def reconstruct(descriptors, degree):
    """ reconstruct(descriptors, degree) attempts to reconstruct the image
    using the first [degree] descriptors of descriptors"""
    # truncate the long list of descriptors to certain length
    descriptor_in_use = truncate_descriptor(descriptors, degree)
    contour_reconstruct = numpy.fft.ifft(descriptor_in_use)
    contour_reconstruct = numpy.array(
        [contour_reconstruct.real, contour_reconstruct.imag])
    contour_reconstruct = numpy.transpose(contour_reconstruct)
    contour_reconstruct = numpy.expand_dims(contour_reconstruct, axis=1)
    if contour_reconstruct.min() < 0:
        contour_reconstruct -= contour_reconstruct.min()
    contour_reconstruct *= 800 / contour_reconstruct.max()
    contour_reconstruct = contour_reconstruct.astype(numpy.int32, copy=False)
    black = numpy.zeros((800, 800), numpy.uint8)
    cv2.drawContours(black, contour_reconstruct, -1, 255, thickness=5)
    return descriptor_in_use

def truncate_descriptor(descriptors, degree):
    descriptors = numpy.fft.fftshift(descriptors)
    center_index = len(descriptors) / 2
    descriptors = descriptors[
        center_index - degree / 2:center_index + degree / 2]
    descriptors = numpy.fft.ifftshift(descriptors)
    return descriptors


def findDescriptor(img):
    contour = []
    _, contour, hierarchy = cv2.findContours(
        img,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE,
        contour)
    contour_array = contour[0][:, 0, :]
    contour_complex = numpy.empty(contour_array.shape[:-1], dtype=complex)
    contour_complex.real = contour_array[:, 0]
    contour_complex.imag = contour_array[:, 1]
    fourier_result = numpy.fft.fft(contour_complex)
    return fourier_result

def sample_generater(sample1):
    response = numpy.array([0, 1])
    response = numpy.tile(response, TRAINING_SIZE / 2)
    response = response.astype(numpy.float32)
    training_set = numpy.empty(
        [TRAINING_SIZE, MIN_DESCRIPTOR], dtype=numpy.float32)
    for i in range(0, TRAINING_SIZE - 1, 2):
        descriptors_sample1 = findDescriptor(sample1)
        descriptors_sample1 = truncate_descriptor(
            descriptors_sample1,
            MIN_DESCRIPTOR)

    return training_set, response

def getFourier(img):

    _, img = cv2.threshold(sample1, 127, 255, cv2.THRESH_BINARY_INV)
    fourier_result = findDescriptor(sample1)
    contour_reconstruct = reconstruct(fourier_result, MIN_DESCRIPTOR)

    return contour_reconstruct

