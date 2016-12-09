#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import time
import glob
import sys
from sys import argv
import re
import operator

CONTENTS_CONFIG = '''{
  "images" : [
    {
      "idiom" : "universal",
      "scale" : "1x"
    },
    {
      "idiom" : "universal",
      "filename" : "2xpng",
      "scale" : "2x"
    },
    {
      "idiom" : "universal",
      "filename" : "3xpng",
      "scale" : "3x"
    }
  ],
  "info" : {
    "version" : 1,
    "author" : "xcode"
  }
}'''

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

def make_imageset(name, image_dir, output_dir):
    global CONTENTS_CONFIG
    config_json = CONTENTS_CONFIG
    # print "name:%s, image_dir:%s, output_dir:%s" % (name, image_dir, output_dir)
    source_path = image_dir + "/" + name
    imageset_path = output_dir + "/" + name +".imageset"
    image_names = [
        name + "@2x.png",
        name + "@3x.png"
    ]
    clear_folder(imageset_path)
    # print "source_path:%s \n imageset_path:%s \n %s" % (source_path, imageset_path, image_names)
    for name_temp in image_names:
        image_temp_path = image_dir + "/" + name_temp
        if os.path.isfile(image_temp_path) == False:
            print_color_string("未找到: " + image_temp_path, "red")
        else:
            cmd = "cp " + image_temp_path + " " + imageset_path
            # print cmd
            os.system(cmd)
    json = config_json.replace("2xpng", name + "@2x.png")
    json = json.replace("3xpng", name + "@3x.png")
    f = file(imageset_path + "/Contents.json", "w")
    f.write(json)
    f.close()

def ergodic_and_generate():
    global CURRENT_DIR_PATH
    global OUTPUT_DIR_NAME
    #获取脚本所在目录
    current_dir_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
    output_dir = current_dir_path + "/" + OUTPUT_DIR_NAME
    clear_folder(output_dir)
    images_dir = current_dir_path + "/" + IMAGES_DIR_NAME
    list_dirs = os.walk(images_dir)
    # print_color_string(images_dir, "lred")
    index = 0
    for root, dirs, files in list_dirs:
        index = index + 1
        # print_color_string("level %s, root:%s" % (index, root), "red")
        relatvie_path = output_dir + root.replace(images_dir, "")
        # print "relative: %s" % (relatvie_path)
        for d in dirs:
            sub_dir = relatvie_path + "/" + d
            clear_folder(sub_dir)
            # print "FOLDER:", os.path.join(root, d), ", sub:", sub_dir
        # print "-------------------------"
        image_names = set()
        for f in files:
            # print "FILE:", os.path.join(root, f)
            partions = f.partition("@")
            if len(partions) != 3 or len(partions[1]) == 0 or len(partions[2]) == 0:
                continue
            image_names.add(partions[0])
        # print "image_names : %s" % (image_names)
        for name in image_names:
            make_imageset(name, root, relatvie_path)
    print_color_string("Done~", "lred")

def clear_folder(output_dir):
    if output_dir != ".":
        cmd = "rm -rf " + output_dir + " ; mkdir " + output_dir
        os.system(cmd)

if __name__ == '__main__':
    if (len(argv) < 1):
        print "Usage: imageset.py"
        exit(0)
    ergodic_and_generate()
