# Homework 1 Image Filtering Stencil Code
# Based on previous and current work
# by James Hays for CSCI 1430 @ Brown and
# CS 4495/6476 @ Georgia Tech
import numpy as np
from numpy import pi, exp, sqrt
from skimage import io, img_as_ubyte, img_as_float32
from skimage.transform import rescale

def my_imfilter(image, kernel):
    """
    Your function should meet the requirements laid out on the homework webpage.
    Apply a filter (using kernel) to an image. Return the filtered image. To
    achieve acceptable runtimes, you MUST use numpy multiplication and summation
    when applying the kernel.
    Inputs
    - image: numpy nd-array of dim (m,n) or (m, n, c)
    - kernel: numpy nd-array of dim (k, l)
    Returns
    - filtered_image: numpy nd-array of dim of equal 2D size (m,n) or 3D size (m, n, c)
    Errors if:
    - filter/kernel has any even dimension -> raise an Exception with a suitable error message.
    """
    filtered_image = np.zeros(image.shape)
    np.flipud(kernel)
    np.fliplr(kernel)
    height, width = kernel.shape
    if width%2==0 or height%2==0:
        raise Exception('The dimensions of the filter must be odd.')
    
    if image.ndim == 2:
        m,n = image.shape
        pad_image = np.pad(image, ((height//2,height//2), (width//2,width//2)))
        for j in range(0,n):
            for i in range(0,m):
                img_square = pad_image[i:i+height,j:j+width]
                product = img_square * kernel
                filtered_image[i,j] = np.sum(product)
    else:
        m,n,c = image.shape
        pad_image = np.pad(image, ((height//2, height//2), (width//2, width//2),(0,0)))
        for k in range(0,c):
            for j in range(0,n):
                for i in range(0,m):
                    img_square = pad_image[i:i+height,j:j+width,k]
                    product = img_square * kernel
                    filtered_image[i,j,k] = np.sum(product)

    return filtered_image

"""
EXTRA CREDIT placeholder function
"""

def my_imfilter_fft(image, kernel):
    """
    Your function should meet the requirements laid out in the extra credit section on
    the homework webpage. Apply a filter (using kernel) to an image. Return the filtered image.
    Inputs
    - image: numpy nd-array of dim (m,n) or (m, n, c)
    - kernel: numpy nd-array of dim (k, l)
    Returns
    - filtered_image: numpy nd-array of dim of equal 2D size (m,n) or 3D size (m, n, c)
    Errors if:
    - filter/kernel has any even dimension -> raise an Exception with a suitable error message.
    """
    filtered_image = np.zeros(image.shape)

    ##################
    # Your code here #
    print('my_imfilter_fft function in student.py is not implemented')
    ##################

    return filtered_image


def gen_hybrid_image(image1, image2, cutoff_frequency):
    """
     Inputs:
     - image1 -> The image from which to take the low frequencies.
     - image2 -> The image from which to take the high frequencies.
     - cutoff_frequency -> The standard deviation, in pixels, of the Gaussian
                           blur that will remove high frequencies.

     Task:
     - Use my_imfilter to create 'low_frequencies' and 'high_frequencies'.
     - Combine them to create 'hybrid_image'.
    """

    assert image1.shape[0] == image2.shape[0]
    assert image1.shape[1] == image2.shape[1]
    assert image1.shape[2] == image2.shape[2]

    # Steps:
    # (1) Remove the high frequencies from image1 by blurring it. The amount of
    #     blur that works best will vary with different image pairs
    # generate a 1x(2k+1) gaussian kernel with mean=0 and sigma = s, see https://stackoverflow.com/questions/17190649/how-to-obtain-a-gaussian-filter-in-python
    s, k = cutoff_frequency, cutoff_frequency*2
    probs = np.asarray([exp(-z*z/(2*s*s))/sqrt(2*pi*s*s) for z in range(-k,k+1)], dtype=np.float32)
    kernel = np.outer(probs, probs)

    low_frequencies = my_imfilter(image1,kernel)

    # (2) Remove the low frequencies from image2. The easiest way to do this is to
    #     subtract a blurred version of image2 from the original version of image2.
    #     This will give you an image centered at zero with negative values.
    blurred2 = my_imfilter(image2,kernel)
    high_frequencies = image2 - blurred2

    # (3) Combine the high frequencies and low frequencies, and make sure the hybrid image values are within the range 0.0 to 1.0
    # Your code here
    hybrid_image = np.clip(low_frequencies+high_frequencies, -1, 1)

    return low_frequencies, high_frequencies, hybrid_image
