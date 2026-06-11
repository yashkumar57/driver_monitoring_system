import cv2 as c
def create_trackers(frame, boxes):
    trackers = {}
    next_id = 1
    for box in boxes:
        x, y, w, h = box
        tracker = c.TrackerCSRT_create()
        tracker.init(frame, (x, y, w, h))
        trackers[next_id] = tracker
        next_id += 1
    return trackers