# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 19:04:04 2021

@author: Admin
"""
import os
import json
import cv2
from contouring_semantic_segmentation import*

# ignore the background since we do not want to contour the background!
# This assumes that it is jpeg
class_dictionary = {'concrete':1, 'steel':2, 'metal decking':3}

output_textfile_destination = "output.txt"


def make_ohev_list(one_hot_encoded_vector_dir):
    ohev_list_array = []
    for image_name in os.listdir(one_hot_encoded_vector_dir):
        ohev_list_array.append(image_name)
    return ohev_list_array

ohev_directory = './ohev/'
image_dir = './masks/'

ohev_list_array = make_ohev_list(ohev_directory)
complete_contours = {}

# expects a jpeg for the image file-type, but could easily be modified for a png
for image_name in ohev_list_array: 
    ohev_file_name = ohev_directory + image_name
    image_file_name = image_dir + image_name.split('.')[-2]+'.png'
    for class_name in class_dictionary:
        complete_class_contours = contour_class(ohev_file_name, image_file_name, image_name, class_dictionary[class_name], class_name)
        if complete_class_contours == None:
            print(class_name + ': not present on image')
        else:
            complete_contours[class_name] = complete_class_contours
    # ------------------------------------------------------------------------   
    # TODO:
    # CONVERT complete_contours TO JSON
    # ------------------------------------------------------------------------
    #print(complete_contours)
    def keypoints_to_text(destination, keypoints, img):
        #width, height = image.shape[0:2]
        #condense_array_to_oneline = str(keypoints).replace('\n', '').replace(" ", "").replace("'", "").replace("array", "").replace("(", "").replace(")", "")                                
        VERSION_NUMBER = "4.5.6"

        with open(destination, 'w') as f:

            f.write("version:4.5.6\n")
            f.write("shapes:\n")
            for index in keypoints:
                pars = keypoints[index]

                for i in range(len(pars)):
                    f.write("label:")
                    f.write(index)
                    f.write("\n")
                    f.write("points:")
                    for entry in pars[i]:
                        for x,y in entry:
                            f.write("[")
                            f.write(str(x))
                            f.write(",")
                            f.write(str(y))
                            f.write("]")
                    f.write("\n")

                    f.write("group_id:null\n")
                    f.write("shape_type:polygon\n")
                    f.write("flags:{}\n")

            f.write("imagePath:")
            f.write(image_file_name)
            f.write("\n")
            f.write("imageData:")
            f.write("none\n")
            width,height,channels = img.shape
            f.write("imageHeight:")
            f.write(str(height))
            f.write("\n")
            f.write("imageWidth:")
            f.write(str(width))
            f.write("\n")
            f.close()
            
    def text_to_json(destination, text_file):
        dictionary = {}
        shape_dict = {}
        
        with open(text_file) as tr:
            for line in tr:
                key,data = line.strip().split(":",1)
                print(key, " = ", data)
                if key == "version":
                    dictionary[key] = data
                elif key == "shapes":
                    dictionary.setdefault("shapes",[])
                elif key == "points":
                    ## TODO fix points to be int instead of string
                    #data = data.replace("[", "").replace("]", "")
                    points_list = data.replace("[","").split("]")
                    points_list.pop()
                    points = []
                    for item in points_list:
                        x,y = item.split(",")
                        points.append([float(x),float(y)])
                    shape_dict[key] = points
                elif key == "flags":
                    shape_dict[key] = data
                    dictionary["shapes"].append(shape_dict)
                    shape_dict = {}
                elif key == "imagePath":
                    dictionary[key] = data
                elif key == "imageData":
                    dictionary[key] = data
                elif key == "imageHeight":
                    dictionary[key] = int(data)
                elif key == "imageWidth":
                    dictionary[key] = int(data)
                else:
                    shape_dict[key] = data
                
            out_file = open(destination, "w") 
            json.dump(dictionary, out_file, indent = 4, sort_keys = False) 
            out_file.close() 
        
    
    img = cv2.imread(image_file_name)
    keypoints_to_text(output_textfile_destination, complete_contours, img)
    text_to_json("out.json", "output.txt")
    
        
    