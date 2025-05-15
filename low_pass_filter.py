import numpy as np
import vigra
from scipy import ndimage as ndi

def LPF(classnumber,classname,classlayer,sigma,truncate):

    #https://stackoverflow.com/questions/18697532/gaussian-filtering-a-image-with-nan-in-python/36307291#36307291
    def gaussfilter(U):    
        LPF = ndi.gaussian_filter(U, sigma=sigma)
        W = 0*U.copy() + 1
        W[U == 0] = 0
        WFloat = W.astype('float64')
        WLPF = ndi.gaussian_filter(WFloat, sigma=sigma, truncate=truncate)
        Filtered = LPF/WLPF
        Filtered[U == 0] = 0
        return Filtered
    
    depth_indices = np.arange(classlayer.shape[0])[:, None, None]
    classlayer_depth = np.where(classlayer == classnumber, depth_indices, 0).astype(np.uint8)

    # Flatten spatial dimensions for easier processing
    reshaped = classlayer_depth.reshape(classlayer.shape[0], -1)
    nonzero_mask = reshaped != 0

    # Compute top and bottom using masked min/max
    classlayer_top = np.where(nonzero_mask.any(axis=0), np.min(np.where(nonzero_mask, reshaped, np.inf), axis=0), 0)
    classlayer_bottom = np.where(nonzero_mask.any(axis=0), np.max(reshaped, axis=0), 0)

    # Reshape to 2D images; convert to uint8
    classlayer_top_reshaped = (classlayer_top.reshape(classlayer.shape[1:3])).astype(np.uint8)
    classlayer_bottom_reshaped = (classlayer_bottom.reshape(classlayer.shape[1:3])).astype(np.uint8)

    # Apply low-pass filter
    classlayer_top_LPF = gaussfilter(classlayer_top_reshaped)
    classlayer_bottom_LPF = gaussfilter(classlayer_bottom_reshaped)

    classlayer_LPF = np.zeros(classlayer.shape[:3], dtype=np.uint8)

    # Convert top and bottom to uint8
    top = classlayer_top_LPF.astype(np.uint8)
    bottom = classlayer_bottom_LPF.astype(np.uint8)

    # Create a 3D array of depth indices
    depth = np.arange(classlayer.shape[0])[:, None, None]

    # Create a mask where depth is between top and bottom
    mask = (depth >= top[None, :, :]) & (depth < bottom[None, :, :]) & (top[None, :, :] > 0) & (bottom[None, :, :] > 0)

    # Assign classnumber where the mask is True
    classlayer_LPF[mask] = classnumber

    return classlayer_LPF