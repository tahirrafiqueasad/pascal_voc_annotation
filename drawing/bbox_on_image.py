""" 
Author:		 Muhammad Tahir Rafique
Date:		 2022-11-02 21:38:31
Project:	 Pacal VOC annotation
Description: Provide function to draw bounding box on image.
"""

import cv2

def draw_bbox_on_image(image, bbox, label, color):
    xmin, ymin, xmax, ymax = bbox
    image = cv2.rectangle(image, [xmin, ymin], [xmax, ymax], color, 2)
    image = cv2.putText(image, label, [xmin, ymin-5], fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=color, thickness=1)
    return image