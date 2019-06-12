from pylab import *

f = []
d = []

if len(sys.argv) != 2:
    exit('cantidad de argumentos invalida')

delimiter='\t'
filename = sys.argv[1]

with open(filename, 'r') as fp:
    for line in fp:
        f.append(float(line.split(delimiter)[0]))
        d.append(float(line.split(delimiter)[1]))

plot(f, d)
show()
