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
prev_frame = frame

if not ok:
    print('Cannot read video file')
    sys.exit()

oks = [trackers[i].init(prev_frame, boxs[i]) for i in range(cars_count)]

while True:
    ok, frame = video.read()
    ok, frame2 = video.read()
    ok, frame3 = video.read()
    ok, frame4 = video.read()
    if not ok:
        break

    for i in range(cars_count):
        oks[i], boxs[i] = trackers[i].update(frame)

    delta = cv2.absdiff(frame, prev_frame)
    kernel = numpy.ones((5, 5), numpy.uint8)
    kernel[2][2] = -24
    masked = cv2.dilate(delta, kernel, iterations = 1)
    thresh = cv2.threshold(masked, 100, 255, cv2.THRESH_BINARY)[1]

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

    cv2.imshow("Tracking", thresh)

    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

    prev_frame = frame
    #cv2.waitKey()