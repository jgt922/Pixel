import os, glob, json
import serial

port = glob.glob("/dev/ttyACM*")[-1]
ser = serial.Serial(port, baudrate=115200)

from pylab import *
from matplotlib import pyplot as plt                            #pyplot es una libreria de graficas como la de matlab plot

#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)
fig, ax1 = plt.subplots()
ax1.margins()                                                   # margen de contorno
plt.ion()                                                       # mantener interaccion con la ventana

fig.canvas.draw()

l1, = ax1.plot(arange(288),[0]*288)                             # se crea una tupla o lista de tamaño 288

ax1.set_xlim(300,900)
ax1.set_ylim(0,2**10)
plt.show()

while True:
    try:
        line = ser.readline()                                   # lee una linea de stream del puerto serial
        data = json.loads(line.decode('utf8'))                  # decodifica en formato utf8
        spec = array(data)                                      # mete los datos en un array
        print(spec)                                             # imprime el array de datos

        pix = arange(1,289)

        A_0 = 3.088195936e+2; B_1 = 2.714595744; B_2 = -1.476579277e-3; B_3 = -4.130205383e-6; B_4 = -5.430814222e-9; B_5 = 2.592402617e-11

        nm = A_0 + B_1 * pix + B_2 * pix**2 + B_3 * pix**3 + B_4 * pix**4 + B_5 * pix**5

        xlabel('Wavelength(nm)')
        ylabel('adu')

        l1.set_xdata(nm)
        l1.set_ydata(spec)
        ax1.draw_artist(l1)
        fig.canvas.draw()
        fig.canvas.flush_events()
    except ValueError:
        pass
