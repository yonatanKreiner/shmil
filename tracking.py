import cv2
import sys
import draw_line
import numpy
from random import randint

def getTrackers(trackerType):
    if tracker_type == 'BOOSTING':
        trackers = [cv2.TrackerBoosting_create() for box in boxs]
    if tracker_type == 'MIL':
        trackers = [cv2.TrackerMIL_create() for box in boxs]
    if tracker_type == 'KCF':
        trackers = [cv2.TrackerKCF_create() for box in boxs]
    if tracker_type == 'TLD':
        trackers = [cv2.TrackerTLD_create() for box in boxs]
    if tracker_type == 'MEDIANFLOW':
        trackers = [cv2.TrackerMedianFlow_create() for box in boxs]
    if tracker_type == 'GOTURN':
        trackers = [cv2.TrackerGOTURN_create() for box in boxs]
    return trackers

def drawRoute(route, frame, color):
    for i in range(len(route) - 1):
        cv2.line(frame, (route[i][0], route[i][1]), (route[i+1][0], route[i+1][1]), color, 2) 


VIDEO_PATH = '/home/yonatan/Desktop/pictures/stab.mp4'

tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
tracker_type = tracker_types[2]

boxs = [(125, 120, 10, 20), (45, 640, 20, 10), (410,415,20,10), (1075,240,10,20), (300,320,10,20), (843,465,10,20),
        (840,487,20,15), (820,475,15,15), (935,505,20,10), (978,515,20,10), (1055,520,15,15), (1020,550,10,15)]

trackers = getTrackers(tracker_type)
cars_count = len(boxs)
colors = [(randint(0, 255),randint(0,255),randint(0, 255)) for i in range(cars_count)]
routes = [[] for i in range(cars_count)]

video = cv2.VideoCapture(VIDEO_PATH)
if not video.isOpened():
    print("Could not open video")
    sys.exit()

ok, frame = video.read()
prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

if not ok:
    print('Cannot read video file')
    sys.exit()

oks = [trackers[i].init(prev_frame, boxs[i]) for i in range(cars_count)]
b = [[125,120,0]]
z = numpy.zeros((1080,1920, 3), numpy.uint8)
while True:
    ok, frame = video.read()
    [video.read() for i in range(10)]

    if not ok:
        break

    for i in range(cars_count):
        oks[i], boxs[i] = trackers[i].update(frame)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    delta = cv2.absdiff(gray_frame, prev_frame)
    kernel = numpy.ones((5, 5), numpy.uint8)
    kernel[2][2] = -24
    masked = cv2.dilate(delta, kernel, iterations = 1)
    thresh = cv2.threshold(masked, 100, 255, cv2.THRESH_BINARY)[1]
    #points = cv2.findContours(thresh, cv2.RETR_FLOODFILL, cv2.CHAIN_APPROX_SIMPLE)
    points = cv2.findNonZero(thresh)
    if points is not None:
        for p in points:
            point = p[0]     
            p1 = (point[0], point[1])
            p2 = (p1[0] +1, p1[1] + 1)
            cv2.line(z, p1, p2, (255,0,0), 2)  
            #frame.itemset(tuple(point), 0)

    for i in range(cars_count):
        if oks[i]:
            bbox = boxs[i]
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            routes[i].append(p1)
        # else :
            # cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        if (len(routes[i]) > 0):
            # drawRoute(routes[i], frame, colors[i])
            pass
    
    dst = cv2.addWeighted(frame, 0.7, z, 0.3, 0)
    cv2.imshow("Tracking", dst)

    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

    prev_frame = gray_frame
    #cv2.waitKey()