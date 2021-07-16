# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:10:33 2021

@author: joshb
"""
import os
import glob
import xml.etree.ElementTree as ET
import pandas as pd



xml_list = []

def xml_to_yolo(path, train_file, obj_data, obj_names):
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text, int(root.find('size')[0].text), int(root.find('size')[1].text), member[0].text,
                     int(member[4][0].text), int(member[4][1].text), int(member[4][2].text), int(member[4][3].text))
            xml_list.append(value)
        
    filename = "blank.txt"
    f = open(filename,"w+")
    parse = []
    images = set()
    labels = {}
    labelCount = 0
    f2 = open(train_file,"w+")
    for element in xml_list:
        for entry in element:
            parse.append(entry)
        image_file, image_width, image_height, className, x_min, y_min, x_max, y_max = parse
        
        if className not in labels:
            labels[className] = labelCount
            labelCount += 1
            
        if image_file not in images:
            images.add(image_file)
            training_image_line = "data/obj/" + str(image_file) + "\n"
            f2.write(training_image_line)
            
            f.close()
            parse_jpeg = str(image_file)
            filename = path + "/" + parse_jpeg[0:-5] + ".txt"
            f = open(filename,"w+")
            
        x_center = ((((x_max - x_min) * 1/2) + x_min)/image_width)
        y_center = ((((y_max - y_min) * 1/2) + y_min)/image_height)
        #y_center = ((y_max - y_min) / image_height) * 1/2
        class_width = (x_max - x_min) / image_width
        class_height = (y_max - y_min) / image_height
        
        line = str(labels[className]) + " %.4f %.4f %.4g %.4f \n" % (x_center, y_center, class_width, class_height)
        f.write(line)
        parse.clear()
    f.close()
    f2.close()
    
    # obj.names file
    f3 = open(obj_names, "w+")
    for entry in labels:
        f3.write(entry)
        f3.write("\n")
    f3.close()
    
    #obj.data file
    f4 = open(obj_data, "w+")
    
    f4.write("classes = ")
    f4.write(str(len(labels)))
    f4.write("\n")
    
    f4.write("train  = data/train.txt\nnames = data/obj.names\nbackup = backup/\n")
    f4.close()

srcDirectory = "C:/Users/joshb/work/yolov4/darknet/data/obj"
train_file = "C:/Users/joshb/work/yolov4/darknet/data/train.txt"
obj_names ="C:/Users/joshb/work/yolov4/darknet/data/obj.names"
obj_data = "C:/Users/joshb/work/yolov4/darknet/data/obj.data"
yolov4_data = xml_to_yolo(srcDirectory, train_file, obj_data, obj_names)
#print_yolo_to_text(yolov4_data, filename)

