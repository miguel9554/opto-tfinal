import os, glob, serial, time
from pylab import *


class MicroSpec(object):
    def __init__(self, port):
        self._ser = serial.Serial(port,baudrate=115200, timeout=1)
    def set_integration_time(self, seconds):
        cmd = "SPEC.INTEG %0.6f\n" % seconds
        self._ser.write(cmd.encode('utf8'))
    def read(self):
        self._ser.write(b"SPEC.READ?\n")
        
        sdata = self._ser.readline()
        sdata = array([int(p) for p in sdata.split(b",")])
        self._ser.write(b"SPEC.TIMING?\n")
        tdata = self._ser.readline()
        tdata = array([int(p) for p in tdata.split(b",")])
        return (sdata, tdata)
    def led_start(self):
        self._ser.write(b"LED.START\n")
    def led_stop(self):
        self._ser.write(b"LED.STOP\n")
    def laser_start(self):
        self._ser.write(b"LASER.START\n")
    def laser_stop(self):
        self._ser.write(b"LASER.STOP\n")


if __name__ == "__main__":

    spec = MicroSpec('COM3')
    print('inicializando...')
    time.sleep(1)   # esperamos a que se inicialize
    icc = spec.set_integration_time(1e-6)
    spec.laser_start()
    time.sleep(2)   # le damos tiempo a la luz
    print('midiendo...')
    sdata, tdata = spec.read()
    time.sleep(1)
    spec.laser_stop()

    print(sdata)
    frequency = linspace(340,850, len(sdata))
    plot(frequency, sdata)
    show()
