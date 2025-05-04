import numpy as np
import rank_max_opening as rmo 
from skimage.transform import hough_line, hough_line_peaks

def orthogonality_map(image, labeled_hyst_watershed, length, width, slice, rank, nrofdim):
    
    # Convert map with labeled objects (after watershed) to binary map
    if nrofdim == 2:
        binary_image = labeled_hyst_watershed > 0
    else:
        binary_image = labeled_hyst_watershed[slice,:,:] > 0

    # Apply hough transform and calculate the median of the resulting angles
    tested_angles = np.linspace(-np.pi/2, np.pi/2, 360, endpoint=False)
    h, theta, d = hough_line(binary_image, theta=tested_angles)
    _, angles, _ = hough_line_peaks(h, theta, d)
    medianAngle = np.median(angles) * 180 / np.pi

    if nrofdim == 2:
        orthogonalityMap = orthogonality_map_2(image, length, width, medianAngle, rank)    
    else:
        orthogonalityMap = np.zeros(image.shape[:3])
        for k in range(image.shape[0]):
            image_slice = image[k,:,:]
            orthogonality_slice = orthogonality_map_2(image_slice, length, width, medianAngle, rank)
            orthogonalityMap[k,:,:] = orthogonality_slice

    return orthogonalityMap

def orthogonality_map_2(image, length, width, medianAngle, rank):
    
    # Detect structures along perpendicular dominant orientations
    sigma = 3
    rankmaxopening1 = rmo.rank_max_opening(image, length, width, medianAngle, sigma, rank)

    # Calculate rank max opening with structuring element at an angle of the dominant orientations + 45 degrees
    rankmaxopening2 = rmo.rank_max_opening(image, length, width, medianAngle + 45, sigma, rank)

    # Divide the two images
    orthogonalityMap = rankmaxopening1 / rankmaxopening2

    return orthogonalityMap