# -*- coding: utf-8 -*-
import serial
import time
import argparse
from matplotlib import pyplot as plt
from numpy.polynomial.polynomial import polyval
import numpy as np


class MicroSpec(object):
    def __init__(self, port):
        self._ser = serial.Serial(port, baudrate=115200, timeout=1)
        time.sleep(1)  # esperamos a que se inicialize

    def set_integration_time(self, seconds):
        cmd = "SPEC.INTEG %0.6f\n" % seconds
        self._ser.write(cmd.encode('utf8'))

    def read(self):
        self._ser.write(b"SPEC.READ?\n")
        sdata = self._ser.readline()
        sdata = np.array([int(p) for p in sdata.split(b",")])
        self._ser.write(b"SPEC.TIMING?\n")
        tdata = self._ser.readline()
        tdata = np.array([int(p) for p in tdata.split(b",")])
        return sdata, tdata

    def start_source(self, source):
        self._ser.write("{source}.START\n".format(source=source.upper()).encode('utf-8'))

    def stop_source(self, source):
        self._ser.write("{source}.STOP\n".format(source=source.upper()).encode('utf-8'))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='Nombre del archivo de salida')
    parser.add_argument('source', type=str.lower, choices=['laser', 'led', 'ext'], help='Fuente a utilizar. Laser, led o ext para una fuente externa')
    args = parser.parse_args()
    
    delimiter = '\t'
    filename = args.filename
    source = args.source

    try:
        spec = MicroSpec('COM4')
    except serial.SerialException:
        exit('Error: el puerto elegido es invalido')

    spec.set_integration_time(1e-6)
    if source != 'ext':
        spec.start_source(source)
        time.sleep(2)   # le damos tiempo a la luz
    print('midiendo...')
    sdata, tdata = spec.read()
    time.sleep(1)

    if source != 'ext':
        spec.stop_source(source)

    # coefficients
    a0 = 3.140535950e2
    b1 = 2.683446321
    b2 = -1.085274073e-3
    b3 = -7.935339442e-6
    b4 = 9.280578717e-9
    b5 = 6.660903356e-12

    coefficients = [a0, b1, b2, b3, b4, b5]

    frequency = polyval(np.linspace(1, 288, 288), coefficients)

    plt.plot(frequency, sdata)
    plt.show()

    with open(filename, 'w') as fp:
        for idx in range(len(frequency)):
            fp.write("{f}{d}{s}\n".format(f=frequency[idx], d=delimiter, s=sdata[idx]))
