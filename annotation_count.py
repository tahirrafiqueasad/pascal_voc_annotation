""" 
Author:		 Muhammad Tahir Rafique
Date:		 2021-08-03 15:58:59
Description: Provide function to count annotations in PASCAL VOC format.
"""
import os
import glob
import pandas as pd
from multiprocessing import Pool, cpu_count
import argparse

from includes.read_write_xml import read_annotation_file
from includes.annotation_count import annotation_count_from_det_dict


# ===============================================
#         WRITING ANNOTATION COUNT FILE
# ===============================================
def write_annotaion_count(annotation_dir, csv_file_path, arrange):
    """read annotaion files and return count dictionary.
    Args:
        annotation_dir: string, path to annotation files directory.
    """
    # 1. GETTING LIST OF ANNOTATION FILES
    anno_files = glob.glob(os.path.join(annotation_dir, '*.xml'))

    # 2. READING ALL FILE
    arguments = [(args,) for args in anno_files]
    with Pool(cpu_count()) as pool:
        det_dict_list = pool.starmap(read_annotation_file, arguments)

    # 3. FINDING COUNT
    arguments = [(args,) for args in det_dict_list]
    with Pool(cpu_count()) as pool:
        count_list = pool.starmap(annotation_count_from_det_dict, arguments)

    # 4. COMBINING COUNT
    count = {}
    for fc in count_list:
        for k, v in fc.items():
            old_count = count.get(k)
            if old_count is None:
                count[k] = v
                continue
            count[k] += v

    # 5. GETTING DATAFRAME
    label, value, mod_label = [], [], []
    for k, v in count.items():
        label.append(k)
        value.append(v)
        mod_label.append('')
    df = pd.DataFrame({'Label':label, 'Count':value, 'Modified_Label': mod_label})
    if arrange:
        df.sort_values('Count', ascending=False, inplace=True)
    
    # 6. SAVING FILE
    output_dir = os.path.split(csv_file_path)[0]
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(csv_file_path, index=False)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Counting label in pascal voc format xml files.')
    parser.add_argument(
        'xml_dir', 
        type=str, 
        help='path to xml dir.'
        )

    parser.add_argument(
        'csv_file_path', 
        type=str, 
        help='csv file path to which count is stored.', 
        default='count_file.csv'
        )

    parser.add_argument(
        '--arrange', 
        help='Arrange labels in csv file', 
        default=False,
        required=False,
        action='store_true'
        )
    args = parser.parse_args()
    write_annotaion_count(args.xml_dir, args.csv_file_path, args.arrange)