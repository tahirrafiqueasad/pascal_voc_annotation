""" 
Author:		 Muhammad Tahir Rafique
Date:		 2022-11-02 20:55:02
Project:	 Pascal VOC Annotation
Description: Provide function to to draw the bbox on the image.
"""

import os
import glob
import argparse
import cv2
import tqdm

from utils.read_write_annotation import read_annotation_file
from drawing.bbox_on_image import draw_bbox_on_image

class DrawBoundingBox():
    def __init__(self, annotation_dir, output_dir) -> None:
        self.annotation_dir = annotation_dir
        self.output_dir = output_dir
        self.colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]
        self.label_color = {}

    def getAnnotationFileList(self):
        """Getting list of annotation files."""
        return glob.glob(os.path.join(self.annotation_dir, '**', '*.xml'), recursive=True)
    
    def main(self):
        """Main function of the application."""
        # GETTING LIST OF ANNOTATION FILE
        anno_file_list = self.getAnnotationFileList()
        if len(anno_file_list) == 0:
            print('ERROR: No annotation files found.')
        
        # LOOPING THROUGH EACH ANNOTATION
        os.makedirs(self.output_dir, exist_ok=True)
        for anno_file in tqdm.tqdm(anno_file_list):
            # READING ANNOTAITON FILE
            anno_name = os.path.basename(anno_file)
            anno = read_annotation_file(anno_file)

            # READING IMAGE
            try:
                image_name = anno['file_info']['image_name']
                image_path = os.path.join(os.path.dirname(anno_file), image_name)
                image = cv2.imread(image_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            except:
                print(f'ERROR: Image for annotation {anno_name} does not exists.')
                continue

            # LOOPING THROUGH EACH ANNOTATION
            for det_class, det_bbox in zip(anno['anno_dict']['detection_classes'], anno['anno_dict']['detection_boxes']):
                # GETTING SUITABLE COLOR
                color = self.label_color.get(det_class)
                if color is None:
                    color_idx = len(self.label_color.keys()) % len(self.colors)
                    color = self.colors[color_idx]
                    self.label_color[det_class] = color
                
                # DRAWING ON IMAGE
                image = draw_bbox_on_image(image, det_bbox, det_class, color)

            # SAVING IMAGE
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_path = os.path.join(self.output_dir, image_name)
            cv2.imwrite(image_path, image)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Draw the bounding box on the image using annotaton file.')
    parser.add_argument('annotation_dir', type=str, help='annotation directory that contain images and xml files.')
    parser.add_argument('output_dir', type=str, help='output directory in which images are saved.')
    args = parser.parse_args()

    print('Processing...')
    db = DrawBoundingBox(args.annotation_dir, args.output_dir)
    db.main()
    print('Done.')