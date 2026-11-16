# 🖐️ Hand Gesture Controlled Hardware System Using Computer Vision & Arduino

An AI-driven Human-Computer Interaction (HCI) and Embedded Systems project that controls Arduino-connected actuators (LEDs, Buzzer, Servo Motor) in real time using webcam-based hand gesture recognition powered by **OpenCV** and **Google MediaPipe Tasks**.

---

## 📌 Project Overview

This project bridges computer vision and embedded electronics. A camera feed captures the user's hand, tracks 21 3D landmarks in real time using Google MediaPipe Tasks (`hand_landmarker.task`), and calculates the number of raised fingers. 

Based on the finger count (0 to 5), the Python application transmits serial commands over USB to an **Arduino Uno**, triggering specific hardware responses including individual LEDs, all LEDs combined, and an automated servo-and-buzzer alert mechanism.

---

## ✨ Key Features

- **Real-Time Hand Tracking:** Employs Google MediaPipe Vision Tasks for ultra-fast, robust 21-point 3D hand landmark detection.
- **Accurate Finger Counting:** Implements handedness-aware thumb orientation logic and vertical tip-to-PIP comparison for high-precision finger counting.
- **Serial Hardware Interfacing:** Low-latency USB serial communication (9600 baud) between Python and Arduino Uno.
- **Fail-Safe Mechanism:** Automatically resets all hardware outputs (`allOff()`) when no hand is detected in the frame or on program termination.
- **Visual On-Screen Feedback:** Overlays detected finger count, gesture description, skeletal connections, and landmarks onto the video feed.

---

## 🖐️ Gesture Control Mapping

| Finger Count | Gesture | Hardware Action |
| :---: | :--- | :--- |
| **0** | Closed Fist / No Hand | **All Outputs OFF** (Safe idle state) |
| **1** | One Finger (Index) | **Red LED** ON |
| **2** | Two Fingers (Index + Middle) | **Green LED** ON |
| **3** | Three Fingers (Index + Middle + Ring) | **Blue LED** ON |
| **4** | Four Fingers (All fingers except thumb) | **All LEDs** ON (Red + Green + Blue) |
| **5** | Open Palm (All 5 fingers) | **Servo Motor moves to 90°** + **Buzzer** ON |

---

## 🛠️ Hardware Requirements

| Component | Specification | Quantity |
| :--- | :--- | :---: |
| **Microcontroller** | Arduino Uno R3 / Nano | 1 |
| **Actuator** | Micro Servo Motor (SG90) | 1 |
| **LED 1** | Red LED (5mm) | 1 |
| **LED 2** | Green LED (5mm) | 1 |
| **LED 3** | Blue LED (5mm) | 1 |
| **Audio Alert** | Active Buzzer (5V) | 1 |
| **Resistors** | 220Ω / 330Ω (for LEDs) | 3 |
| **Prototyping** | Breadboard & Jumper Wires | 1 set |
| **PC / Camera** | USB Cable & Webcam | 1 |

---

## 🔌 Circuit & Pin Connections

| Hardware Component | Arduino Uno Pin | Description |
| :--- | :---: | :--- |
| **Red LED (Anode)** | `Pin 3` | In series with 220Ω resistor to GND |
| **Green LED (Anode)** | `Pin 4` | In series with 220Ω resistor to GND |
| **Blue LED (Anode)** | `Pin 5` | In series with 220Ω resistor to GND |
| **Buzzer (+)** | `Pin 8` | Negative terminal to GND |
| **Servo Signal (Orange)** | `Pin 9` | PWM-capable digital pin |
| **Servo Power (Red)** | `5V` | Regulated 5V DC |
| **Servo Ground (Brown)** | `GND` | Common Ground with Arduino |

---

## 📂 Project Structure

```text
Project05_Hand_Gesture_Control/
├── Arduino/
│   └── Hand_Gesture_ComPort/
│       └── Hand_Gesture_ComPort.ino    # Arduino sketch (Actuator controller)
├── Python/
│   ├── main.py                         # OpenCV + MediaPipe hand tracking & serial sender
│   ├── serial_test.py                  # Standalone Arduino serial communication test script
│   └── requirements.txt                # Python dependencies
├── Images/                             # Project photos, circuit diagrams & screenshots
│   └── .gitkeep
├── hand_landmarker.task                # MediaPipe pre-trained hand landmarker model
├── requirements.txt                    # Project root dependencies
├── .gitignore                          # Git ignore rules (.venv, cache, IDE files)
└── README.md                           # Documentation & setup guide
```

---

## 🚀 Setup & Installation

### Step 1: Arduino Setup
1. Open [Arduino IDE](https://www.arduino.cc/en/software).
2. Open `Arduino/Hand_Gesture_ComPort/Hand_Gesture_ComPort.ino`.
3. Connect your Arduino Uno via USB.
4. Select your board (**Tools > Board > Arduino Uno**) and the corresponding COM Port (**Tools > Port**).
5. Click **Upload**.

---

### Step 2: Python Environment Setup
1. Clone or download this repository.
2. Open a terminal in the project root directory.
3. (Recommended) Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate
   ```
4. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

### Step 3: Run the Application
1. In `Python/main.py`, verify that `ARDUINO_PORT` matches your Arduino COM port (e.g., `"COM4"` on Windows or `"/dev/ttyUSB0"` on Linux):
   ```python
   ARDUINO_PORT = "COM4"
   BAUD_RATE = 9600
   ```
2. Run the main tracking script:
   ```bash
   python Python/main.py
   ```
3. Show your hand in front of the webcam and observe the hardware responding according to your finger count!
4. Press **`Q`** in the video window to safely exit and reset all hardware.

---

## 📸 Images & Demonstrations

Place your hardware setup photos, circuit wiring diagrams, and demo screenshots in the [`Images/`](Images/) folder.

---

## 🛡️ Notes & Troubleshooting

- **Access Denied / COM Port Busy:** Close the Arduino IDE Serial Monitor before running `Python/main.py`. Only one program can access the COM port at a time.
- **Lighting Conditions:** Ensure adequate lighting for the camera so MediaPipe can detect hand landmarks reliably.
- **Servo Jitter:** When using multiple LEDs and a servo simultaneously, ensure the 5V power supply from USB provides sufficient current, or use an external 5V power supply with a common ground for the servo.

---

## 📜 License & Credits

Developed by **[Siteyash](https://github.com/Siteyash)**.  
Open-source under the MIT License. Feel free to use and adapt this project for educational and learning purposes!

