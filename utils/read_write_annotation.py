""" 
Author:		 Muhammad Tahir Rafique
Date:		 2021-08-03 13:00:09
Description: Provide function to read and write xml file in PASCAL VOC format.
"""
import os
from pascal_voc_writer import Writer
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

# ===============================================
#           READ ANNOTATION FILE
# ===============================================
def read_annotation_file(file_path, remove_space=False):
    """Read a single annotation file and return annotation dictionary.
    Args:
        file_path: string, path to xml file in PASCAL VOC format.
        remove_space: bool, replace space with underscore _ in label name.
    Return:
        anno_dict: dict, containing [detection_classes, detection_boxes, detection_scores, num_detections, file_names]
    """
    # 1. GETTING ROOT INFORMATION
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 2. GETTING VARIFIED INFORMATION
    root_attrib = root.attrib
    verified = root_attrib.get('verified')
    if verified == 'no':
        verified = False
    if verified == 'yes':
        verified = True
    
    # 3. GETTING IMAGE PATH
    image_path = root.find('path').text
    image_dir, image_name = os.path.split(image_path)

    # 4. CHECK FOR WINDOWS PATH
    if image_dir == '':
        split_path = image_path.split('\\')
        image_name = split_path.pop(-1)
        for sp in split_path:
            image_dir = os.path.join(image_dir, sp)


    # 5. GETTING IMAGE SIZE
    height = int(root.find('size').find('height').text)
    width = int(root.find('size').find('width').text)
    depth = int(root.find('size').find('depth').text)
    size = {'height': height, 'width': width, 'depth': depth}

    # 6. COMBINING FILE INFO
    file_info = {
        'verified': verified,
        'image_dir': image_dir,
        'image_name': image_name,
        'size': size
    }

    # 7. GETTING ANNO DICT
    detection_classes = []
    detection_boxes = []
    for member in root.findall('object'):
        # 7.1 GETTING ANNO LABEL
        name = member.find('name').text
        if remove_space:
            name = name.replace(' ', '_')
        detection_classes.append(name)

        # 7.2 GETTING BOUNDING BOX
        bbox = [int(member.find('bndbox').find('xmin').text), int(member.find('bndbox').find('ymin').text), int(member.find('bndbox').find('xmax').text), int(member.find('bndbox').find('ymax').text)]
        detection_boxes.append(bbox)

    num_detections = len(detection_classes)
    anno_dict = {'detection_classes':detection_classes, 'detection_boxes':detection_boxes, 'num_detections':num_detections}
    
    # 8. COMBINING INFORMATION
    det_dict = {'file_info': file_info, 'anno_dict':anno_dict}
    
    return det_dict


# ===============================================
#            WRITING ANNOTATION FILE
# ===============================================
def write_annotation_file_from_dict(det_dict, output_dir, verbos=False):
    """Write annotation dictionary in annotation file. Single file at a time.
    Args:
        det_dict: dictionary, contaion detection information.
        output_dir: string, storing dir.
        verbos: bool, display priting line.
    Return:
        None
    """
    # 1. MAKING OUTPUT DIR
    os.makedirs(output_dir, exist_ok=True)

    # 2. GETTING FILE INFORMATION
    file_info = det_dict['file_info']
    image_name = file_info['image_name']
    image_path = os.path.join(output_dir, image_name)

    # 3. GETTING IMAGE INFORMATION
    height = file_info['size']['height']
    width = file_info['size']['width']
    depth = file_info['size']['depth']

    # 4. WRITIG DATA IN LOOP
    anno_dict = det_dict['anno_dict']
    bbox = anno_dict['detection_boxes']
    name = anno_dict['detection_classes']
    num_detections = anno_dict['num_detections']
    writer = Writer(image_path, width, height, depth)
    for i in range(num_detections):
        xmin = bbox[i][0]
        ymin = bbox[i][1]
        xmax = bbox[i][2]
        ymax = bbox[i][3]
        label = name[i]

        # REMOVING ESCAPE CHAR FOR XML
        for e in ['&', '<', '>']:
            if e in label:
                label = label.replace(e, escape(e))
        writer.addObject(label, xmin, ymin, xmax, ymax)
    
    # 4. WRITING XML FILE
    xml_output_path = os.path.join(output_dir, os.path.splitext(image_name)[0] + '.xml')
    writer.save(xml_output_path)

    # 5. PRINTING VERBOS
    if verbos:
        print('writing: {}'.format(xml_output_path))