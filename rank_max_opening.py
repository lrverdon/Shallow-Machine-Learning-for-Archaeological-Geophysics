import numpy as np
import skimage.morphology as morph
import skimage.transform as transf
import vigra
from scipy import signal

def rank_max_opening(image, length, width, orientation, sigma, rankperc):
    k = round((length * width) * rankperc/100)
    orient90 = orientation + 90
    rank = (length * width) - k + 1

    image = vigra.filters.gaussianSmoothing(image, sigma)

    rect = morph.rectangle(length,width)
    rectrot1 = transf.rotate(rect,orientation,resize=True)
    strel1 = rectrot1 > 0
    rectrot2 = transf.rotate(rect,orient90,resize=True)
    strel2 = rectrot2 > 0
    if strel1.shape[0] % 2 == 0:
        strel1 = strel1[0:strel1.shape[0]-1,:]
    if strel1.shape[1] % 2 == 0:
        strel1 = strel1[:,0:strel1.shape[1]-1]
    if strel2.shape[0] % 2 == 0:
        strel2 = strel2[0:strel2.shape[0]-1,:]
    if strel2.shape[1] % 2 == 0:
        strel2 = strel2[:,0:strel2.shape[1]-1]

    B1 = signal.order_filter(image,strel1,rank)
    deltaB1 = morph.dilation(B1,strel1)
    gammaBk1 = np.minimum(image,deltaB1)

    B2 = signal.order_filter(image,strel2,rank)
    deltaB2 = morph.dilation(B2,strel2)
    gammaBk2 = np.minimum(image,deltaB2)

    img = np.maximum(gammaBk1,gammaBk2)

    return img