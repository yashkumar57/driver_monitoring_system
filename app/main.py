import cv2 as c
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import math
import winsound
from datetime import datetime
from yolo_detection import detect_people
from tracking import create_trackers
from alerts import save_screenshot
from database import log_alert
from detection import analyze_face
from detection import EAR_THRESHOLD, MAR_THRESHOLD

# preparing mediapipe........
base_options = python.BaseOptions(model_asset_path="face_landmarker.task")
options = vision.FaceLandmarkerOptions(base_options=base_options,num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)
FRAME_LIMIT = 15
person_states = {}
cap = c.VideoCapture(0, c.CAP_DSHOW)
yolo_per_frame = 10
frame_counter = 0
next_id = 0
trackers = {}

while True:
    start = c.getTickCount()
    current_time = datetime.now().strftime("%H:%M:%S") #time for ss and fps
    ret, frame = cap.read()
    if not ret:
        break
    frame = c.flip(frame, 1)
    height, width = frame.shape[:2]
    # yolo
    if frame_counter % yolo_per_frame == 0:
        trackers.clear()
        filtered_boxes = detect_people(frame)
        trackers = create_trackers(frame, filtered_boxes)
    # updating trackers
    for obj_id, tracker in trackers.items():
        if obj_id not in person_states:
            person_states[obj_id] = {"counter": 0,"alert_sent": False,"yawn_counter": 0,"yawn_alert_sent": False}
            state = person_states[obj_id]
        success, box = tracker.update(frame)
        if not success:
            continue
        x, y, w, h = map(int, box)
        # face box
        x = max(0, x)
        y = max(0, y)
        w = min(w, width - x)
        h = min(h, height - y)
        if w <= 0 or h <= 0:
            continue
        c.rectangle(frame,(x, y),(x + w, y + h),(0, 255, 0),2)
        c.putText(frame,f"ID: {obj_id}",(x, y - 10),c.FONT_HERSHEY_SIMPLEX,0.7,(0, 255, 0),2)
        # cropped face for mediapipe
        face = frame[y:y + h, x:x + w]
        if face is None or face.size == 0:
            continue
        # mediapipe
        rgb = c.cvtColor(face, c.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = detector.detect(mp_image)
        # landmarks
        if result.face_landmarks:
            landmarks = result.face_landmarks[0]
            ear , mar , left_eye , right_eye , mouth = analyze_face(landmarks , w , h) 
            # drawing L
            for point in left_eye:
                px , py = point
                c.circle(frame, (x+ px, y + py), 2, (0,0,255), -1)
            # drawing R
            for point in right_eye:
                px , py = point
                c.circle(frame, (x+ px, y + py), 2, (0,0,255), -1)
            # drawing mouth landmarks
            for point in mouth:
                px , py = point
                c.circle(frame, (x+ px, y + py), 2, (255,0,255), -1)
            if ear == 0 or mar == 0:
                continue
            # ear n mar display
            c.putText(frame,f"EAR: {ear:.2f}",(x, y - 40),c.FONT_HERSHEY_SIMPLEX,0.7,(255, 0, 0),2)
            c.putText(frame,f"MAR: {mar:.2f}",(x, y - 70),c.FONT_HERSHEY_SIMPLEX,0.7,(0, 255, 255), 2)
            status = "NORMAL"
            #drowsy!!!
            if ear < EAR_THRESHOLD:
                state["counter"] += 1
            else:
                state["counter"] = 0
                state["alert_sent"] = False
            if state["counter"] > FRAME_LIMIT:
                status = "DROWSY"
                c.putText(frame,"DROWSY!",(width//2 -120, 80),c.FONT_HERSHEY_SIMPLEX,1.5,(0, 0, 255),3)
                winsound.Beep(1000, 300)   
                if not state["alert_sent"]: #saving ss 1 time in db
                    screenshot_path = save_screenshot(frame)
                    log_alert(current_time, status, screenshot_path)
                    state["alert_sent"] = True
            # Yawn Detect n display
            if mar > MAR_THRESHOLD:
                state["yawn_counter"] += 1
            else:
                state["yawn_counter"] = 0
                state["yawn_alert_sent"] = False
            if state["yawn_counter"] > FRAME_LIMIT:
                status = "YAWNING"
                c.putText(frame,"YAWNING!",(width//2 - 120, 140),c.FONT_HERSHEY_SIMPLEX,1.2,(0, 255, 255),3)
                if not state["yawn_alert_sent"]:
                    screenshot_path = save_screenshot(frame)
                    log_alert(current_time, status, screenshot_path)
                    state["yawn_alert_sent"] = True
            c.putText(frame,f"STATUS: {status}",(20, 30),c.FONT_HERSHEY_SIMPLEX,0.9,(0, 255, 0),2)
    # FPS calc
    fps = c.getTickFrequency() / (c.getTickCount() - start)
    c.putText(frame,f"FPS: {int(fps)}",(20 , 50),c.FONT_HERSHEY_SIMPLEX, 0.8,(255, 255, 0),2)
    #time and display
    c.putText(frame, current_time,(520, 20), c.FONT_HERSHEY_SIMPLEX, 0.7 , (255,255,0), 2)
    c.imshow("Driver Drowsiness Monitor", frame)
    frame_counter += 1

    if c.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
c.destroyAllWindows()