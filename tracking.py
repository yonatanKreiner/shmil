import cv2
import sys
import draw_line
import numpy

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

def drawRoute(route, frame):
    for i in range(len(route) - 1):
        cv2.line(frame, (route[i][0], route[i][1]), (route[i+1][0], route[i+1][1]), (255,0,0), 3) 

VIDEO_PATH = '/home/yonatan/Desktop/pictures/stab.mp4'

tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
tracker_type = tracker_types[2]

# set up boxs
boxs = [(120, 117, 10, 20), (45, 640, 20, 10), (410,410,20,20)]
trackers = getTrackers(tracker_type)
cars_count = len(boxs)
routes = [[] for i in range(cars_count)]

video = cv2.VideoCapture(VIDEO_PATH)
if not video.isOpened():
    print("Could not open video")
    sys.exit()

ok, prev_frame = video.read()
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
            pass
            #drawRoute(routes[i], frame)

    cv2.imshow("Tracking", thresh)

    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

    prev_frame = frame
    #cv2.waitKey()