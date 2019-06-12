import sys, os
from matplotlib import pyplot as plt
from numpy.polynomial.polynomial import polyval
import numpy as np

f = []
d = []

if len(sys.argv) != 2:
    exit('cantidad de argumentos invalida')

delimiter='\t'
filename = sys.argv[1]

if not os.path.isfile(filename):
	exit('el archivo indicado no existe')

with open(filename, 'r') as fp:
    for line in fp:
        f.append(float(line.split(delimiter)[0]))
        d.append(float(line.split(delimiter)[1]))

# coefficients
a0 = 3.140535950e2
b1 = 2.683446321
b2 = -1.085274073e-3
b3 = -7.935339442e-6
b4 = 9.280578717e-9
b5 = 6.660903356e-12

coefficients = [a0, b1, b2, b3, b4, b5]

f = polyval(np.linspace(1, 288, 288), coefficients)

plt.plot(f, d)
plt.show()
