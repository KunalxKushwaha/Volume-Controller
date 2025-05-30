# Hey Hey Hey!!!!!!! 

<h3>So this baaically controls the volume on your Desktop or System through their Speakers or Bluetooth Connected Devices.</h3><br>
The Volume Controller project utilizes computer vision and gesture recognition to adjust the system's audio volume without the need for physical interaction with keyboard keys or mouse clicks. This is achieved by tracking hand movements and gestures using a webcam feed, analyzing them with the help of OpenCV and Mediapipe, and mapping the distance between fingers to volume levels using pycaw.<br>

How It Works:
1. Capture real-time video from the webcam.
2. Use Mediapipe to detect hand landmarks.
3. Measure the Euclidean distance between the thumb tip and index finger tip.
4. Map the measured distance to the system's volume range using interpolation. 
5. Update the system volume using pycaw.
6. Display volume level and gesture overlay on the video feed for user feedback.

Author - Kunal Kushwaha
