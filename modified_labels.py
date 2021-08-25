""" 
Author:		 Muhammad Tahir Rafique
Date:		 2021-08-24 18:00:02
Description: Provide function to modified labels in xml files.
"""
import os
import glob
import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count
import concurrent.futures
import argparse

from includes.read_write_xml import read_annotation_file, write_annotation_file_from_dict
from includes.label import remove_labels_from_det_dict, modify_labels_in_det_dict


# -----------------------------------------------
#               GET MODIFIED DICT
# -----------------------------------------------
def _get_modified_label_dict_from_csv(modeified_label_csv_file_path):
    # 1. READING FILE
    df = pd.read_csv(modeified_label_csv_file_path, dtype=str)

    # 2. GETTING LABELS
    label = list(df['Label'])

    # 3. GETTING MODIFIED LABELS
    mod_label = list(df['Modified_Label'])
    modified_label = {}
    for l, m in zip(label, mod_label):
        if type(m) is not str:
            if np.isnan(m):
                modified_label[l] = None
                continue
        modified_label[l] = m

    return modified_label


# ===============================================
#               MODIFIED ANNO LABELS
# ===============================================
def modify_annotation_labels(xml_dir, output_dir, modeified_label_csv_file_path):
    """modifiy annotations labes to provided dictionary.
    Args:
        xml_dir: string, directory containing annotation files.
        output_dir: string, directory to which modeified annotaions are saved.
        modeified_label_csv_file_path: str, path to updated csv file.
    """
    # 1. GETTING MODIFIED LABEL DICT
    label_dict = _get_modified_label_dict_from_csv(modeified_label_csv_file_path)

    # 2. GETTING MODIFIED AND REMOVABLE LABELS
    removed_labels, modified_labels = [], {}
    for k, v in label_dict.items():
        if v is None:
            removed_labels.append(k)
        else:
            modified_labels[k] = v

    # 3. GETTING LIST OF ALL XML FILES
    xml_files = glob.glob(os.path.join(xml_dir, '*.xml'))

    # 4. READING ALL XML FILES
    args = [(f,) for f in xml_files]
    with Pool(cpu_count()) as pool:
        dit_dict_list = pool.starmap(read_annotation_file, args)

    # 5. REMOVING UNWANTED LABELS
    args = [(dit_dict, removed_labels) for dit_dict in dit_dict_list]
    with Pool(cpu_count()) as pool:
        dit_dict_list = pool.starmap(remove_labels_from_det_dict, args)

    # 6. MODIFIED ALL LABELS
    args = [(dit_dict, modified_labels) for dit_dict in dit_dict_list]
    with Pool(cpu_count()) as pool:
        dit_dict_list = pool.starmap(modify_labels_in_det_dict, args)

    # 7. WRITING FILES
    output_dir_list = [output_dir]*len(dit_dict_list)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(write_annotation_file_from_dict, dit_dict_list, output_dir_list)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Modified the labels in csv file generated by annotation counter.')

    parser.add_argument(
        'xml_dir', 
        type=str, 
        help='path to xml dir.'
        )

    parser.add_argument(
        'output_dir', 
        type=str, 
        help='path to output dir.'
        )

    parser.add_argument(
        'modeified_label_csv_file_path', 
        type=str, 
        help='csv file path generated by annotation counter and modified by user.', 
        default='count_file.csv'
        )

    args = parser.parse_args()

    modify_annotation_labels(args.xml_dir, args.output_dir, args.modeified_label_csv_file_path)
