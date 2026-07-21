import serial

ser = serial.Serial("COM8", 115200)

def read_joystick():
    line = ser.readline().decode("utf-8").strip()
    x, y, button = map(int, line.split(","))
    return x, y, button

