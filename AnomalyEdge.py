import numpy as np
import heapq
from skimage import morphology
from skimage.measure import regionprops, label
from scipy import ndimage as ndi
from skimage.segmentation import watershed

def find_edge_of_anomaly(image, labeled_hyst, class_image):
    gradient = np.gradient(image)
    horizGradientMagn = np.sqrt(gradient[0]**2 + gradient[1]**2)
    correctedAnomalies = np.zeros(image.shape, dtype=np.uint8)
    binary_image = (image > 0).astype(np.uint8)
    footprint = morphology.disk(1)
    
    for region in regionprops(labeled_hyst):
        starty, startx, stopy, stopx = region.bbox
        binary_image_region = binary_image[starty:stopy, startx:stopx] * region.image
        labeled_image_region = label(binary_image_region, connectivity=2, background=0)
        distance = ndi.distance_transform_edt(labeled_image_region == 0)
        labeled_image_region_connected = watershed(distance, labeled_image_region) * region.image
        horizGradientMagn_region = horizGradientMagn[starty:stopy, startx:stopx] * region.image
        
        for subregion in regionprops(labeled_image_region_connected):
            correctedAnomaliesSubregion = np.zeros(image.shape, dtype=np.uint8)
            starty1, startx1, stopy1, stopx1 = subregion.bbox
            horizGradientMagn_subregion = horizGradientMagn_region[starty1:stopy1, startx1:stopx1] * subregion.image
            horizGradientMagn_vector = horizGradientMagn_subregion.flatten()
            perim = int(subregion.perimeter)
            highest_values = heapq.nlargest(perim, horizGradientMagn_vector)
            
            binary_matrix = np.isin(horizGradientMagn_subregion, highest_values).astype(np.uint8)
            image_subregion = image[starty + starty1: starty + stopy1, startx + startx1: startx + stopx1]
            maxima = image_subregion[binary_matrix == 1]
            threshold = np.mean(maxima)
            image_subregion_above_threshold = (image_subregion > threshold).astype(bool)
            
            if np.mean(image_subregion[image_subregion_above_threshold]) > 0:
                correctedAnomaliesSubregion[starty + starty1: starty + stopy1, startx + startx1: startx + stopx1] = (
                    morphology.closing(image_subregion_above_threshold, footprint) * subregion.image
                )
                correctedAnomalies += correctedAnomaliesSubregion
    
    correctedAnomalies[correctedAnomalies > 1] = 1
    corrected_class_image = class_image * correctedAnomalies
    return corrected_class_image