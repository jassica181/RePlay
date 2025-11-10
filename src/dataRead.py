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
        if "Arduino" in port.description or "usbmodem" in port.name:
            device = port.device
            return device
    print("No device found")
    return None


def readData():
    port = findPort()
    if not port:
        print("please connect arduino")
        return None
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print("attempting to connect device")
        time.sleep(2)
        ser.reset_input_buffer()
        print("connected")
        return ser
    except Exception as e:
        print(e)


def readEmg(arduino):
    try:
        line = arduino.readline().decode("utf-8").strip().split(",")
        line[0] = int(line[0])
        line[1] = int(line[1])
        return line
    except Exception as e:
        print(e)
    return None


if __name__ == "__main__":
    ser = readData()
    while True:
        value = readEmg(ser)
        print(value)
