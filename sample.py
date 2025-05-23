# #code for voume inc and decrease
# import cv2
# import numpy as np
# from math import hypot
# import mediapipe as mp
# from ctypes import cast, POINTER, c_float
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# cap = cv2.VideoCapture(0)

# mpHands = mp.solutions.hands
# hands = mpHands.Hands()
# mpDraw = mp.solutions.drawing_utils


# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(
#     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))

# volMin, volMax = volume.GetVolumeRange()[:2]

# while True: 
#     success, img = cap.read()
#     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(imgRGB)

#     lmList = []
#     if results.multi_hand_landmarks:
#         for handLms in results.multi_hand_landmarks:
           
#             for id, lm in enumerate(handLms.landmark):
#                 h, w, c = img.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#                 lmList.append([id, cx, cy])
#                 mpDraw.draw_landmarks(img, handLms,mpHands.HAND_CONNECTIONS)
#                 if id == 4:
#                     cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

#             if len(lmList) != 0:
#                 x1, y1 = lmList[4][1], lmList[4][2]
#                 x2, y2 = lmList[8][1], lmList[8][2]
#                 cv2.circle(img, (x1, y1), 4, (255, 0, 0), cv2.FILLED)
#                 cv2.circle(img, (x2, y2), 4, (255, 0, 0), cv2.FILLED)
#                 cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
#                 length = hypot(x2 - x1, y2 - y1)
#                 # Hand range 50 - 300
#                 # Volume range -63.5 - 0.0
#                 vol = np.interp(length, [15, 220], [volMin, volMax])
#                 print(vol, length)
#                 volume.SetMasterVolumeLevel(vol, None)

#             mpDraw.draw_landmarks(img, handLms,
#                                    mpHands.HAND_CONNECTIONS)

#     cv2.imshow("Image", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
