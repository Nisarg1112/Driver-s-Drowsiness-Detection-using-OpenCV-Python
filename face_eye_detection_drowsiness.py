import cv2
import dlib
from scipy.spatial import distance
from playsound import playsound

import time
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    EAR = (A+B)/(2.0*C)
    return EAR

def lips_aspect_ratio(lips): 
    A = distance.euclidean(lips[4], lips[8])
    B = distance.euclidean(lips[2], lips[10])
    C = distance.euclidean(lips[0], lips[6])

    LAR = (A + B + C) / 3.0
    return LAR

cap = cv2.VideoCapture(0)
hog_face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor(r"C:\Users\Nisarg Trivedi\ML projects\Face Landmark Detection\shape_predictor_68_face_landmarks.dat\shape_predictor_68_face_landmarks.dat")

# Declare another costant to hold the consecutive number of frames to consider for a blink 
CONSECUTIVE_FRAMES = 20 
# Initialize two counters 
BLINK_COUNT = 0 
frame_count = 0
count_sleep = 0

while True:
    # Extract a frame
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = hog_face_detector(gray)
    for face in faces:

        face_landmarks = dlib_facelandmark(gray, face)
        leftEye = []
        rightEye = []

        for n in range(36,42):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            leftEye.append((x,y))
            next_point = n+1
            if n == 41:
                next_point = 36
            x2 = face_landmarks.part(next_point).x
            y2 = face_landmarks.part(next_point).y
            cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)

        for n in range(42,48):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            rightEye.append((x,y))
            next_point = n+1
            if n == 47:
                next_point = 42
            x2 = face_landmarks.part(next_point).x
            y2 = face_landmarks.part(next_point).y
            cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)

        left_ear = eye_aspect_ratio(leftEye)
        right_ear = eye_aspect_ratio(rightEye)

        EAR = (left_ear+right_ear)/2
        EAR = round(EAR,2)
        if EAR<0.26:
            frame_count = frame_count + 1
            if frame_count >= CONSECUTIVE_FRAMES:
                count_sleep += 1
                # Add the frame to the dataset ar a proof of drowsy driving
                cv2.imwrite("dataset/frame_sleep%d.jpg" % count_sleep, frame)
                #playsound(r'C:\Users\Nisarg Trivedi\Downloads\zapsplat_emergency_bell_alarm_fire_or_burglar_ring_002_44042.mp3')
                cv2.putText(frame, "DROWSINESS ALERT!", (270, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                print("Drowsy")
        print(EAR)

    cv2.imshow("Are you Sleepy", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()