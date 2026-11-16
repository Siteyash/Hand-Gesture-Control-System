
import cv2
import mediapipe as mp
import serial
import time
import os

# =====================================
# PROJECT 05: HAND GESTURE CONTROL
# =====================================

# Arduino configuration
ARDUINO_PORT = "COM4"
BAUD_RATE = 9600

# MediaPipe model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "hand_landmarker.task")

# Connect Arduino
try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print("Arduino connected on", ARDUINO_PORT)

except serial.SerialException as error:
    print("Arduino connection failed:", error)
    raise SystemExit

# MediaPipe Tasks setup
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)

# Finger counting
def count_fingers(landmarks, handedness):

    count = 0

    # Thumb detection
    if handedness == "Right":
        if landmarks[4].x < landmarks[3].x:
            count += 1
    else:
        if landmarks[4].x > landmarks[3].x:
            count += 1

    # Four fingers
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]

    for tip, pip in zip(tips, pips):
        if landmarks[tip].y < landmarks[pip].y:
            count += 1

    return count


# Gesture labels
gesture_names = {
    0: "CLOSED FIST - ALL OFF",
    1: "RED LED ON",
    2: "GREEN LED ON",
    3: "BLUE LED ON",
    4: "ALL LEDs ON",
    5: "SERVO + BUZZER ON"
}

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Webcam not detected!")
    arduino.write(b'0')
    arduino.close()
    raise SystemExit

last_timestamp = -1
last_command = None

print("\nHAND GESTURE CONTROL STARTED")
print("Show your hand to control Arduino.")
print("Press Q to exit.\n")

try:
    with HandLandmarker.create_from_options(options) as detector:

        while True:

            success, frame = cap.read()

            if not success:
                print("Camera frame unavailable!")
                break

            frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb
            )

            timestamp = max(
                int(time.monotonic() * 1000),
                last_timestamp + 1
            )
            last_timestamp = timestamp

            results = detector.detect_for_video(mp_image, timestamp)

            if results.hand_landmarks:

                landmarks = results.hand_landmarks[0]
                handedness = results.handedness[0][0].category_name

                finger_count = count_fingers(landmarks, handedness)

                # Send only changed commands
                command = str(finger_count)

                if command != last_command:
                    arduino.write(command.encode())
                    last_command = command
                    print("Gesture:", finger_count,
                          "-", gesture_names[finger_count])

                height, width, _ = frame.shape

                # Draw connections
                for connection in mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS:

                    start = landmarks[connection.start]
                    end = landmarks[connection.end]

                    x1, y1 = int(start.x * width), int(start.y * height)
                    x2, y2 = int(end.x * width), int(end.y * height)

                    cv2.line(
                        frame, (x1, y1), (x2, y2),
                        (0, 255, 0), 2
                    )

                # Draw landmarks
                for point in landmarks:
                    x = int(point.x * width)
                    y = int(point.y * height)
                    cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

                cv2.putText(
                    frame,
                    f"FINGERS: {finger_count}",
                    (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (0, 255, 0),
                    3
                )

                cv2.putText(
                    frame,
                    gesture_names[finger_count],
                    (20, 110),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255, 255, 0),
                    2
                )

            else:

                # No hand: turn all outputs off
                if last_command != '0':
                    arduino.write(b'0')
                    last_command = '0'

                cv2.putText(
                    frame,
                    "NO HAND DETECTED",
                    (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2
                )

            cv2.imshow("PROJECT 05 - HAND GESTURE CONTROL", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:
    # Safe shutdown
    try:
        arduino.write(b'0')
        arduino.close()
    except serial.SerialException:
        pass

    cap.release()
    cv2.destroyAllWindows()

    print("System stopped safely.")
