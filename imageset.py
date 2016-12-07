#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import time
import glob
import sys
from sys import argv
import re
import operator

CONTENTS_NAME = "contents.json"
OUTPUT_DIR_NAME = "imagesets"
IMAGES_DIR_NAME = "images"

COLORS  = {
    "blue": "0;34m",
    "green": "0;32m",
    "cyan": "0;36m",
    "red": "0;31m",
    "purple": "0;35m",
    "brown": "0;33m",
    "yellow": "1;33m",
    "lred": "1;31m",
}

def print_color_string(string, color):
    print ("\033[" + COLORS[color])
    print string
    print '\033[0m'

def short_name(name):
    index = name.find("@",0)
    if index > 0 :
        return name[0:index]
    return ""

def make_imageset(name, config_json, image_dir, output_dir):

    source_path = image_dir + "/" + name
    imageset_path = output_dir + "/" + name +".imageset"

    image_names = [
        name + "@2x.png",
        name + "@3x.png"
    ]
    cmd = "mkdir " + imageset_path
    os.system(cmd)

    # print "source_path:%s \n imageset_path:%s \n %s" % (source_path, imageset_path, image_names)

    for name_temp in image_names:
        image_temp_path = image_dir + "/" + name_temp
        if os.path.isfile(image_temp_path) == False:
            print_color_string("未找到" + name_temp, "red")
        cmd = "cp " + image_temp_path + " " + imageset_path
        # print cmd
        os.system(cmd)

    json = config_json.replace("2xpng", name + "@2x.png")
    json = json.replace("3xpng", name + "@3x.png")

    f = file(imageset_path + "/Contents.json", "w")
    f.write(json)
    f.close()

def get_images_name(images_dir):
    images = {}
    if os.path.isdir(images_dir):
        subitems = os.listdir(images_dir)
        for item in subitems:
            sname = short_name(item)
            if len(sname) > 0:
                images[sname] = sname
    return images.keys()

def get_image_config(current_dir_path):
    global CONTENTS_NAME
    path = current_dir_path + "/" + CONTENTS_NAME
    f = file(path)
    image_config = f.read()
    f.close()
    return image_config

def clear_imagesets(output_dir):
    if output_dir != "." :
        cmd = "rm -rf " + output_dir + " ; mkdir " + output_dir
        os.system(cmd)

if __name__ == '__main__':
    if (len(argv) < 1):
        print "Usage: imageset.py"
        exit(0)

    global CURRENT_DIR_PATH
    global OUTPUT_DIR_NAME
    #获取脚本所在目录
    current_dir_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
    print current_dir_path
    #获取脚本运行目录
    print os.getcwd()

    image_config = get_image_config(current_dir_path)
    output_dir = current_dir_path + "/" + OUTPUT_DIR_NAME
    clear_imagesets(output_dir)

    images_dir = current_dir_path + "/" + IMAGES_DIR_NAME
    images = get_images_name(images_dir)

    # print "image_config: %s\noutput_dir:%s\nimages_dir:%s\nimages:%s" % (image_config, output_dir, images_dir, images)

    for name in images:
        make_imageset(name, image_config, images_dir, output_dir)
