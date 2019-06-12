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
    def start_source(self, source):
        self._ser.write("{source}.START\n".format(source=source.upper()).encode('utf-8'))
    def stop_source(self, source):
        self._ser.write("{source}.STOP\n".format(source=source.upper()).encode('utf-8'))


if __name__ == "__main__":

    if len(sys.argv) not in [2,3]:
        exit('cantidad de argumentos invalida')

    delimiter='\t'
    filename = sys.argv[1]
    ext_source = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2].lower() in ['laser','led'] else None
    spec = MicroSpec('/dev/ttyACM0')
    print('inicializando...')
    time.sleep(1)   # esperamos a que se inicialize
    icc = spec.set_integration_time(1e-6)
    if ext_source:
        spec.start_source(ext_source)
        time.sleep(2)   # le damos tiempo a la luz
    print('midiendo...')
    sdata, tdata = spec.read()
    time.sleep(1)
    if ext_source:
        spec.stop_source(ext_source)

    frequency = linspace(340,850, len(sdata))
    plot(frequency, sdata)
    show()

    with open(filename, 'w') as fp:
        for idx in range(len(frequency)):
            fp.write("{f}{d}{s}\n".format(f=frequency[idx], d=delimiter, s=sdata[idx]))
