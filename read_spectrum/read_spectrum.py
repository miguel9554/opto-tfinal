import serial
import matplotlib.pyplot as plt

with serial.Serial('COM4', 115200, timeout=1) as ser:
	while True:
		line = str(ser.readline())   # read a '\n' terminated line
		# print(line.split(',')[:len(line.split(','))-1])
		try:
			ints = [int(j) for j in line.split(',')[1:len(line.split(','))-1]]
			print(ints)
			if ints:
				plt.clf()
				plt.plot(ints)
				plt.show(block=False)
				plt.pause(0.05)
		except Exception:
			print('a')