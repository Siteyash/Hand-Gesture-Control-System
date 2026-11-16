
import serial
import time

try:
    arduino = serial.Serial("COM4", 9600, timeout=2)

    print("Connecting to Arduino...")
    time.sleep(2)

    print("Arduino connected!")

    while True:
        command = input("Enter 1 (ON), 0 (OFF), Q (QUIT): ")

        if command == "1":
            arduino.write(b'1')
            print("ON command sent")

        elif command == "0":
            arduino.write(b'0')
            print("OFF command sent")

        elif command.lower() == "q":
            break

        else:
            print("Invalid command")

    arduino.close()

except serial.SerialException as error:
    print("Serial Error:", error)
