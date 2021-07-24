import matplotlib.pyplot as plt
import numpy as np
import imageio
from _utils import *


def DFT2D(x, shift=True):
    '''
    Discrete space fourier transform
    x: Input matrix
    '''
    pi2 = 2*np.pi
    N1, N2 = x.shape
    X = np.zeros((N1, N2), dtype=np.complex64)
    n1, n2 = np.mgrid[0:N1, 0:N2]

    for w1 in range(N1):
        for w2 in range(N2):
            j2pi = np.zeros((N1, N2), dtype=np.complex64)
            j2pi.imag = pi2*(w1*n1/N1 + w2*n2/N2)
            X[w1, w2] = np.sum(x*np.exp(-j2pi))
    if shift:
        X = np.roll(X, N1//2, axis=0)
        X = np.roll(X, N2//2, axis=1)
    return X


def iDFT2D(X, shift=True):
    '''
    Inverse discrete space fourier transform
    X: Complex matrix
    '''
    pi2 = 2*np.pi
    N1, N2 = X.shape
    x = np.zeros((N1, N2))
    k1, k2 = np.mgrid[0:N1, 0:N2]
    if shift:
        X = np.roll(X, -N1//2, axis=0)
        X = np.roll(X, -N2//2, axis=1)
    for n1 in range(N1):
        for n2 in range(N2):
            j2pi = np.zeros((N1, N2), dtype=np.complex64)
            j2pi.imag = pi2*(n1*k1/N1 + n2*k2/N2)
            x[n1, n2] = abs(np.sum(X*np.exp(j2pi)))
    return 1/(N1*N2)*x


if __name__ == "__main__":
    image = imageio.imread('./sample/cameraman.png')
    s = 4
    image = image[::s, ::s] / 255
    N1, N2 = image.shape
    IMAGE = DFT2D(image)
    xX = np.array([image, np.log10(1 + abs(IMAGE))])
    panel(xX, [2, 1], text_color='green',
          texts=['Input image', 'Spectrum'])


    image_ = iDFT2D(IMAGE)
    Xx_ = np.array([np.log10(1 + abs(IMAGE)), image_])
    panel(Xx_, [2, 1], text_color='green',
          texts=['Spectrum', 'Reconstructed image'])

