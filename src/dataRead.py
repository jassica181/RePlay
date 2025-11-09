# for reading the data into the game
# make sure you have pyserial installed using sudo pip3 install pyserial
import time

import serial
import serial.tools.list_ports


def findPort():
    ports = serial.tools.list_ports.comports()
    print(ports)
    for port in ports:
        print(port.name)
        if "Arduino" in port.name:
            device = port.device
            return device
    print("No device found")
    return None


def readData():
    port = findPort()
    if not port:
        print("please connect arduino")
        return False
    try:
        ser = serial.Serial(port, 115200, timeout=0)
        print("attempting to connect device")
        time.sleep(2)
        print("connected")
        ser.open()  # open the port to listen
    except Exception as e:
        print(e)


def readEmg(arduino):
    try:
        line = arduino.readline().decode("utf-8").strip()
        return int(line)
    except Exception as e:
        print(e)
    return None
