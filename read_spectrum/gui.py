from random import randint
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.backends.tkagg as tkagg
import tkinter as Tk
from numpy.polynomial.polynomial import polyval
import serial
import os
import numpy as np
import read_spectrum

delimiter = '\t'
overwrite = 'No'
data = []

try:
    spec = read_spectrum.MicroSpec('COM4')
    spec.set_integration_time(1e-6)
except serial.SerialException:
    exit('Error: el puerto elegido es invalido')

source_active = {'laser': False, 'led': False}

a0 = 3.140535950e2
b1 = 2.683446321
b2 = -1.085274073e-3
b3 = -7.935339442e-6
b4 = 9.280578717e-9
b5 = 6.660903356e-12

coefficients = [a0, b1, b2, b3, b4, b5]

frequency = polyval(np.linspace(1, 288, 288), coefficients)

fig = Figure()

ax = fig.add_subplot(111)
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.grid()

col = [[sg.Button('Leer', size=(10, 2), font='Helvetica 14')],
       [sg.Button('Laser', size=(10, 2), font='Helvetica 14')],
       [sg.Button('Led', size=(10, 2), font='Helvetica 14')],
       [sg.Text('Nombre de archivo', size=(15, 2)), sg.InputText('name', key='filename')],
       [sg.Button('Guardar', size=(10, 2), font='Helvetica 14')]]

layout = [[sg.Text('Mini espectrometro', size=(40, 1), justification='center', font='Helvetica 20')],
          [sg.Canvas(size=(640, 480), key='canvas'), sg.Column(col)]]

# create the window and show it without the plot


window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout)
window.Finalize()  # needed to access the canvas element prior to reading the window

canvas_elem = window.Element('canvas')

graph = FigureCanvasTkAgg(fig, master=canvas_elem.TKCanvas)
canvas = canvas_elem.TKCanvas

while True:

    event, values = window.Read(timeout=20)
    if event == 'Leer':
        ax.cla()
        ax.grid()

        data, tdata = spec.read()
        ax.plot(frequency, data, color='purple')
        graph.draw()
        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = Tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

        canvas.create_image(640 / 2, 480 / 2, image=photo)

        figure_canvas_agg = FigureCanvasAgg(fig)
        figure_canvas_agg.draw()

        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
    elif event in ['Laser', 'Led']:
        if not source_active[event.lower()]:
            spec.start_source(event.lower())
            source_active[event.lower()] = True
        else:
            spec.stop_source(event.lower())
            source_active[event.lower()] = False
    elif event == 'Guardar':
        filename = values['filename']
        if os.path.isfile(filename):
            overwrite = sg.PopupYesNo('El archivo ya existe. Sobreescribir?')
        if (os.path.isfile(filename) and overwrite == 'Yes') or not os.path.isfile(filename):
            try:
                fp = open(filename, 'w')
                if len(data):
                    for idx in range(len(frequency)):
                        fp.write("{f}{d}{s}\n".format(f=frequency[idx], d=delimiter, s=data[idx]))
                else:
                    sg.Popup("Primero hay que realizar una medición")
                fp.close()
            except OSError as e:
                if e.errno == 22:
                    sg.Popup("Nombre de archivo invalido")
                else:
                    sg.Popup("Cancelar", e)
