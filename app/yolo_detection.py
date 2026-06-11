import cv2 as c
import numpy as np

# preparing yolooo....
net = c.dnn.readNet("yolo/yolov3.weights", "yolo/yolov3.cfg")
with open("yolo/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

def detect_people(frame):
    height, width = frame.shape[:2]
    blob = c.dnn.blobFromImage(frame, 1 / 255.0,(416,416),swapRB=True,crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    boxes = []
    confidences = []
    for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                if classes[class_id] != "person":
                    continue
                confidence = scores[class_id]
                if confidence > 0.5:
                    cx = int(detection[0] * width)
                    cy = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(cx - w / 2)
                    y = int(cy - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
    indices = c.dnn.NMSBoxes(boxes,confidences,0.5,0.4)
    filtered_boxes = []
    if len(indices) > 0:
        for i in indices:
            i = int(i)
            filtered_boxes.append(boxes[i])
    return filtered_boxes