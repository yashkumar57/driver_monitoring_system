import math

# indices on mesh
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [78, 308, 13, 14]
EAR_THRESHOLD = 0.22
MAR_THRESHOLD = 0.60
# ear n mar func
def EAR(eye):
    A = math.dist(eye[1], eye[5])
    B = math.dist(eye[2], eye[4])
    C = math.dist(eye[0], eye[3])
    if C == 0:
      return 0	
    return (A + B) / (2.0 * C)

def MAR(mouth):
    A = math.dist(mouth[2], mouth[3])
    C = math.dist(mouth[0], mouth[1])
    if C == 0:
      return 0
    return A / C
#calc aspect ration
def analyze_face(landmarks, w, h):
    left_eye = []
    right_eye = []
    mouth = []
    # L
    for idx in LEFT_EYE:
        lx = int(landmarks[idx].x * w)
        ly = int(landmarks[idx].y * h)
        left_eye.append((lx, ly))
    # R
    for idx in RIGHT_EYE:
        rx = int(landmarks[idx].x * w)
        ry = int(landmarks[idx].y * h)
        right_eye.append((rx, ry))
    # mouth landmarks
    for idx in MOUTH:
        mx = int(landmarks[idx].x * w)
        my = int(landmarks[idx].y * h)
        mouth.append((mx, my))
    # ear , mar values
    ear = (EAR(left_eye) + EAR(right_eye)) / 2.0
    mar = MAR(mouth)
    return ear , mar , left_eye , right_eye , mouth