import os, glob, serial, time, sys
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

if __name__ == "__main__":

    if len(sys.argv) != 2:
        exit('cantidad de argumentos invalida')

    delimiter='\t'
    filename = sys.argv[1]

    DATASET_NAME = "OPTOELECTRONICA 2019"
    mpl.rcParams["savefig.directory"] = os.path.dirname(__file__)

    spec = MicroSpec('/dev/ttyACM0')
    icc = spec.set_integration_time(1)
    time.sleep(1)   # si no se espera, el programa nunca le escribe al arduino y no anda
    sdata, tdata = spec.read()

    frequency = linspace(340,850, len(sdata))
    plot(frequency, sdata)
    title(DATASET_NAME)
    show()

    with open(filename, 'w') as fp:
        for idx in range(len(frequency)):
            fp.write("{f}{d}{s}\n".format(f=frequency[idx], d=delimiter, s=sdata[idx]))
