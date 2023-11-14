"""Utilities to improve whole-brain regions segmentation."""
import numpy as np
from skimage.measure import label
from skimage.segmentation import find_boundaries


def extract_continuous_region(image):
    """Extract continuous region from image."""
    image = np.where(image > 0, 1, 0)
    return label(image)


def get_boundaries(image_regions):
    """Obtain boundaries from image regions."""
    boundaries = np.zeros_like(image_regions)
    label_values = np.unique(image_regions)
    for i in label_values:
        if i == 0:
            continue
        boundary = find_boundaries(image_regions == i)
        boundaries += np.where(boundary > 0, i, 0)
    return boundaries


def remove_boundaries_from_segmentation(image_segmentation, image_labels=None):
    """Remove boundaries from segmentation."""
    if image_labels is None:
        image_regions = extract_continuous_region(image_segmentation)
    else:
        image_regions = image_labels
    boundaries = get_boundaries(image_regions)

    seg_in = np.where(image_regions > 0, image_segmentation, 0)
    seg_no_boundaries = np.where(boundaries > 0, 0, seg_in)
    return seg_no_boundaries, seg_in, boundaries, image_regions