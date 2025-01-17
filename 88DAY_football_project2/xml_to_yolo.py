# cvat xml to yolo

import os
import glob
import cv2
from xml.etree.ElementTree import parse

# # xml 1 ~ 5
# def find_xml_file(xml_folder_path) :
#     all_root = []
#     for (path, dir, files) in os.walk(xml_folder_path) :
#         for filename in files :
#             ext = os.path.splitext(filename)[-1]
#             # ext -> .xml
#             if ext == ".xml" :
#                 root = os.path.join(path, filename)
#                 # ./xml_data/test.xml
#                 all_root.append(root)
#             else :
#                 print("no xml files.....")
#                 break

#     return all_root


xml_paths = "./annotations.xml"
# test = glob.glob(os.path.join(xml_folder_path, "*.xml"))

label_dict = {"player":0, "ball":1, "keeper":2, "referee":3}


tree = parse(xml_paths)
root = tree.getroot()
img_metas = root.findall("image")
for img_meta in img_metas :
    # xml image name
    image_name = img_meta.attrib["name"]
    # print(image_name) >> sang1_100.jpg
    image_width = int(img_meta.attrib["width"])
    image_height = int(img_meta.attrib["height"])

    # Box META
    box_metas = img_meta.findall("box")
    for box_meta in box_metas :
        box_label = box_meta.attrib["label"]
        box = [int(float((box_meta.attrib["xtl"]))), int(float((box_meta.attrib["ytl"]))),
                int(float((box_meta.attrib["xbr"]))), int(float((box_meta.attrib["ybr"])))]

        yolo_x = round(((box[0] + box[2])/2)/image_width, 6)
        yolo_y = round(((box[1] + box[3])/2)/image_height, 6)
        yolo_w = round((box[2] - box[0])/image_width, 6)
        yolo_h = round((box[3] - box[1])/image_height, 6)

        print("yolo xywh" , yolo_x, yolo_y, yolo_w, yolo_h)
        image_name_temp = image_name.replace(".jpg", ".txt")

        # txt file save folder
        os.makedirs("./cvat_xml_to_yolo_txt", exist_ok=True)

        # label
        label = label_dict[box_label]

        # txt save
        with open(f"./cvat_xml_to_yolo_txt/{image_name_temp}", 'a') as f :
            f.write(f"{label} {yolo_x} {yolo_y} {yolo_w} {yolo_h} \n")