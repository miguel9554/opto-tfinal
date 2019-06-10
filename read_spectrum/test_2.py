import serial, io

ser = serial.Serial('COM3', 115200, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

sio.write(u"SPEC.READ?\n")
sio.flush()
while True:
	s = sio.readline()
	print(s)