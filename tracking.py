import cv2
import sys
import draw_line
import numpy
from random import randint
from track import get_nearest_point


def drawRoute(route, frame, color):
    for i in range(len(route) - 1):
        cv2.line(frame, (route[i][0], route[i][1]), (route[i+1][0], route[i+1][1]), color, 2) 


VIDEO_PATH = '/home/yonatan/Desktop/pictures/stab.mp4'

video = cv2.VideoCapture(VIDEO_PATH)
if not video.isOpened():
    print("Could not open video")
    sys.exit()

ok, frame = video.read()
prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

z = numpy.zeros((1080,1920, 3), numpy.uint8)

while True:
    ok, frame = video.read()
    [video.read() for i in range(10)]        
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    delta = cv2.absdiff(gray_frame, prev_frame)
    kernel = numpy.ones((5, 5), numpy.uint8)
    kernel[2][2] = -24
    masked = cv2.dilate(delta, kernel, iterations = 1)
    thresh = cv2.threshold(masked, 100, 255, cv2.THRESH_BINARY)[1]
    
    points = cv2.findNonZero(thresh)
    if points is not None:
        for p in points:
            point = p[0]     
            p1 = (point[0], point[1])
            p2 = (p1[0] +1, p1[1] + 1)
            cv2.line(z, p1, p2, (255,0,0), 2)
        points.sort(1)
        cars = [points[0]]
        '''for point in points:
            nearest = get_nearest_point(point, points)
            if ()''' 
        #contour, hierarchy = cv2.findContours(z,1,2)
        #print(contour)
    
    dst = cv2.addWeighted(frame, 0.7, z, 0.3, 0)
    cv2.imshow("Tracking", dst)

    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

    prev_frame = gray_frame
    #cv2.waitKey()