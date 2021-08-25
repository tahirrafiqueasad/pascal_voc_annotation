""" 
Author:		 Muhammad Tahir Rafique
Date:		 2021-08-24 17:03:42
Description: Provide function remove and replace label in det dict.
"""
import copy
import numpy as np

# ===============================================
#       REMOVE LABELS FROM DET DICT
# ===============================================
def remove_labels_from_det_dict(det_dict, label_list):
    """Remove labels from det dict and return modified det dict."""
    # 1. MAKING A COPY OF DET DICT
    new_det_dict = copy.deepcopy(det_dict)

    # 2. LOOPING THROUGH EACH ELEMENT TO FIND LABELS TO BE REMOVED
    anno_dict = new_det_dict['anno_dict']
    location = []
    for i in range(anno_dict['num_detections']):
        # 2.1 GETTING CURRENT LABEL AND BOX
        current_label = anno_dict['detection_classes'][i]

        # 2.2 IF CURRENT LABEL IS NOT NEEDED TO MODIFIED
        if current_label not in label_list:
            location.append(i)

    # 3. UPDATING DET DICT
    for k in list(anno_dict.keys()):
        if type(anno_dict[k]) == list:
            new_det_dict['anno_dict'][k] = list(np.array(anno_dict[k])[location])

    # 4. UPDATING NUM DETECTION
    new_det_dict['anno_dict']['num_detections'] = len(new_det_dict['anno_dict']['detection_classes'])
    
    return new_det_dict



# ===============================================
#           MODIFIED LABELS IN DET DICT
# ===============================================
def modify_labels_in_det_dict(det_dict, modified_label_dict):
    """Modified label in det dict according to modified label dict."""
    # 1. MAKING COPY OF DET DICT
    new_det_dict = copy.deepcopy(det_dict)

    # 2. LOOPING THROUGH EACH ELEMENT OF ANNO DICT
    anno_dict = new_det_dict['anno_dict']
    for i in range(anno_dict['num_detections']):
        # 2.1 GETTING CURRENT LABEL
        current_label = anno_dict['detection_classes'][i]

        # 2.2 GETTING MODIFIED LABEL
        modified_label = modified_label_dict.get(current_label)

        # 2.3 CHECK FOR REMOVAL FOR LABEL
        if (modified_label is None) or (current_label is None):
            continue

        # 2.4 UPDATING LIST
        new_det_dict['anno_dict']['detection_classes'][i] = modified_label
    
    return new_det_dict