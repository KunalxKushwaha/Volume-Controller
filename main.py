
import cv2
import numpy as np
from math import hypot
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Webcam setup
cap = cv2.VideoCapture(0)

# Mediapipe hands setup
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

# Pycaw volume control setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]

# Variables for smoothing
vol = 0
volBar = 400
volPer = 0
smoothness = 5

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        for id, lm in enumerate(handLms.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        # Thumb tip = id 4, Index tip = id 8
        if len(lmList) >= 9:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            length = hypot(x2 - x1, y2 - y1)

            # Convert length to volume level
            vol = np.interp(length, [15, 200], [volMin, volMax])
            volBar = np.interp(length, [15, 200], [400, 150])
            volPer = np.interp(length, [15, 200], [0, 100])

            # Smooth volume and set
            vol = smoothness * round(vol / smoothness)
            volume.SetMasterVolumeLevel(np.clip(vol, volMin, volMax), None)

            # Drawing circles and line between fingers
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (200, 0, 200), 3)
            cv2.circle(img, (cx, cy), 12, (0, 255, 0), cv2.FILLED)

    # Draw stylish volume bar background
    cv2.rectangle(img, (50, 150), (85, 400), (50, 50, 50), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (100, 255, 100), cv2.FILLED)

    # Draw percentage box
    cv2.rectangle(img, (40, 420), (120, 460), (50, 50, 50), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Title
    cv2.putText(img, "Volume Controller", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 200, 0), 2)

    cv2.imshow("Hand Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
