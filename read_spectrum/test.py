import serial, time

port = serial.Serial('COM3',baudrate=115200, timeout=1)
if not port.is_open:
	print('no se abrio el puerto')
if not port.writable():
	print('no se puede escribir el puerto')
if not port.readable():
	print('no se puede leer el puerto')
print("in waiting: {d}".format(d=port.in_waiting))
while port.in_waiting:
	s = port.readline()
	print(s)
print('afuera del while')
print('esperando...')
time.sleep(0.5)
print('escribiendo')
port.write(b"SPEC.READ?\r\n")
while True:
	s = port.readline()
	print(s)