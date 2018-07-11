import os
import math
import numpy as np
import cv2

FRAMES_OUTPUT_DIR = '../output_frames'

def drawLine(image_path, first_point, second_point, save):
    img  = cv2.imread(image_path, cv2.IMREAD_COLOR)
    cv2.line(img, (first_point[0], first_point[1]), (second_point[0], second_point[1]), (255,0,0), 3)

    image_path_splited = image_path.split('/')
    output_file_name = 'output ' + image_path_splited [len(image_path_splited) - 1]

    if(save):
        if not os.path.isdir(FRAMES_OUTPUT_DIR):
            os.makedirs(FRAMES_OUTPUT_DIR)
        cv2.imwrite(FRAMES_OUTPUT_DIR +  '/' + output_file_name,img)
    else:
        cv2.imshow(output_file_name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()