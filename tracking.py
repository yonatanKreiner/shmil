import cv2
import sys
from random import randint

#bbox = cv2.selectROI(frame, False)

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

VIDEO_PATH = 'videos/DJI_0002.MP4'

tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
tracker_type = tracker_types[2]

# set up boxs
boxs = [(125, 120, 10, 20), (45, 640, 20, 10), (410,415,20,10), (1075,240,10,20), (300,320,10,20), (843,465,10,20),
        (840,487,20,15), (820,475,15,15), (935,505,20,10), (978,515,20,10), (1055,520,15,15), (1020,550,10,15)]

trackers = getTrackers(tracker_type)
cars_count = len(boxs)
colors = [(randint(0, 255),randint(0,255),randint(0, 255)) for i in range(cars_count)]
routes = [[] for i in range(cars_count)]

#video
video = cv2.VideoCapture(VIDEO_PATH)
if not video.isOpened():
    print("Could not open video")
    sys.exit()

ok, frame = video.read()
prev_frame = frame

if not ok:
    print('Cannot read video file')
    sys.exit()

oks = [trackers[i].init(frame, boxs[i]) for i in range(cars_count)]

while True:
    ok, frame = video.read()
    if not ok:
        break
     
    timer = cv2.getTickCount()

    for i in range(cars_count):
        oks[i], boxs[i] = trackers[i].update(frame)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    for i in range(cars_count):
        if oks[i]:
            bbox = boxs[i]
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            #cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            routes[i].append(p1)
        else :
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        if (len(routes[i]) > 0):
            drawRoute(routes[i], frame, colors[i])

    cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
 
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

    cv2.imshow("Tracking", frame)

    k = cv2.waitKey(1) & 0xff
    if k == 27 : break