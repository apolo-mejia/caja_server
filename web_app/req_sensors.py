import serial
from time import sleep
import json
import datetime as dt


def take_measure(esp32):
    esp32.write(b'meas4')
    rawString = str(esp32.readline())
    sleep(10)
    return 0

def create_document(esp32):
# Establecer el nombre del archivo toma
    toma = str(dt.datetime.now()).replace(' ','_')
    filename = "/home/pi/caja_server/servicio/medidas/stest/"+toma+".txt"
    file2send = toma+".txt"
# Creemos el archivo donde vamos a escribir
    f = open(filename, "w")
    f.write("X,Y,Z")
    f.close()
    return filename, file2send

def get_data_len(esp32):
# Importa un JSON con el numero de mustras y la duración, ya hecha la toma
    esp32.write(b'meas5')
    rawString = str(esp32.readline())
    newString = rawString[2:-5]
    pack = json.loads(newString)
#    esp32.close()
    return pack["duration"], pack["samples"]

def get_data_points(tmuestra, file2write,esp32):
# Importa todos los puntos de la toma y los guarda en el archivo aquel
    i = 0
    esp32.write(b'meas6')
    sleep(1)
    f = open(file2write, "a")
    while i < tmuestra:
        pack = json.loads(str(esp32.readline())[2:-5])
#        newString = rawString[2:-5]
#        print(pack, end="")
#        print("---" + str(i))
        f.write("\n")
        f.write(str(pack["X"])+","+str(pack["Y"])+","+str(pack["Z"]))
        i = i+1
    f.close()
    return i

#esp32 = serial.Serial('/dev/ttyUSB0', 115200, timeout=None)
#sleep(1)
#take_measure()
#file = create_document()
#duration,samples = get_data_len()
#raw = get_data_points(samples, file)
#print(str(duration) + "---" + str(samples))
#print("las iteraciones" + str(raw))
#print("Las tomas" + str(samples))
#esp32.close()
