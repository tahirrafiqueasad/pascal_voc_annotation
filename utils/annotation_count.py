""" 
Author:		 Muhammad Tahir Rafique
Date:		 2021-08-24 13:56:22
Description: Provide function to findout the annotation count in det dict.
"""
import numpy as np

def annotation_count_from_det_dict(det_dict):
    """Return dict of count"""

    # 1. GETTING UNIQUE CLASSES
    anno_dict = det_dict['anno_dict']
    detection_classes = anno_dict['detection_classes']
    labels, count = np.unique(detection_classes, return_counts=True)

    # 3. MAKING DICT
    count_dict = {k:v for k, v in zip(labels, count)}

    return count_dict