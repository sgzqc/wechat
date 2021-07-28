import matplotlib.pyplot as plt
import numpy as np
import imageio
from _utils import *


def DCT2D(x):
    '''
    Discrete space cosine transform
    x: Input matrix
    '''
    N1, N2 = x.shape
    X = np.zeros((N1, N2))
    n1, n2 = np.mgrid[0:N1, 0:N2]
    for w1 in range(N1):
        for w2 in range(N2):
            l1 = (2/N1)**0.5 if w1 else (1/N1)**0.5
            l2 = (2/N2)**0.5 if w2 else (1/N2)**0.5
            cos1 = np.cos(np.pi*w1*(2*n1 + 1)/(2*N1))
            cos2 = np.cos(np.pi*w2*(2*n2 + 1)/(2*N2))
            X[w1, w2] = l1*l2*np.sum(x*cos1*cos2)
    return X


def iDCT2D(X, shift=True):
    '''
    Inverse discrete space cosine transform
    X: Input spectrum matrix
    '''
    N1, N2 = X.shape
    x = np.zeros((N1, N2))
    k1, k2 = np.mgrid[0:N1, 0:N2]
    l1 = np.ones((N1, N2))*(2/N1)**0.5
    l2 = np.ones((N1, N2))*(2/N2)**0.5
    l1[0] = (1/N1)**0.5; l2[:,0] = (1/N2)**0.5
    for n1 in range(N1):
        for n2 in range(N2):
            cos1 = np.cos(np.pi*k1*(2*n1 + 1)/(2*N1))
            cos2 = np.cos(np.pi*k2*(2*n2 + 1)/(2*N2))
            x[n1, n2] = np.sum(l1*l2*X*cos1*cos2)
    return x


if __name__ == "__main__":
    image = imageio.imread('./sample/cameraman.png')
    s = 4
    image = image[::s, ::s] / 255
    N1, N2 = image.shape
    histogram(image, interval=[0, 1])

    IMAGE = DCT2D(image)
    xX = np.array([image, np.log10(1 + abs(IMAGE))])
    panel(xX, [2, 1], text_color='green',
          texts=['Input image', 'DCT Spectrum'])

    image_ = iDCT2D(IMAGE)
    Xx_ = np.array([np.log10(1 + abs(IMAGE)), image_])
    panel(Xx_, [2, 1], text_color='green',
          texts=['DCT Spectrum', 'Reconstructed image'])

    u, v = np.mgrid[0:N1, 0:N2] / max(N1, N2)
    r = (u ** 2 + v ** 2) ** 0.5
    theta = np.arctan2(v, u)
    H = np.exp(-3 * r ** 2) * (np.cos(4 * 2 * theta) / 2 + 1 / 2)
    image__ = iDCT2D(H * IMAGE)
    Hx__ = np.array([H, abs(image__ * 0.5 + 0.5)])
    panel(Hx__, (2, 1), text_color='green',
          texts=['Filter', 'Filtered image'])

