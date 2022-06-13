import logging
import os
import time
import netifaces
import socket
import subprocess
from classes import *
from functions import *
import RPi.GPIO as GPIO
from PIL import ImageFont, ImageDraw, Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

def inicio():
    #Hardware SET UP
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21,GPIO.IN)

    # Interruptions
    GPIO.add_event_detect(21, GPIO.RISING, bouncetime=2500, callback=Evento)

#  CALL BACK  FUNCTIONS !!!HERE FOR NOW!!!
def Evento(chanel):
# Generador consulta de las interfaces que estan guardadas en
# /etc/wap_suplicant/wpa_supplicant.conf
    argument = ['wpa_cli','-i','wlan0','list_networks']
    p = subprocess.run(argument, capture_output=True, text=True)
#    print(p.stderr)
#   Generacion del archivo de texto con la consulta
    f = open('/home/pi/servicio/redes/wifi/myfile.txt', 'w')
    f.write(p.stdout)
    f.close()
#   Generacion de un archivo tipo csv
    fr = open('/home/pi/servicio/redes/wifi/myfile.txt', 'r')
    fw = open('/home/pi/servicio/redes/wifi/cvsfile.txt', 'w')
    fw.close()
    b=0
    for x in fr:
        fw = open('/home/pi/servicio/redes/wifi/cvsfile.txt','a')
        str = x
        if b == 0:
            str2pass = str.replace(' / ', ',')
            str2pass = str2pass.replace(' ', '_')
            b=b+1
        else:
            str2pass = str.replace('\t',',')
        fw.write(str2pass)
        fw.close()
    fr.close()
    print('Se ha ingresado al evento')
    #time.sleep(2)
    print('Ahora vamos a salir de este evento ...')

# Keeps track of hom many times main() has run
RUN=0
logger = logging.getLogger(f"main.{__name__}")
# Iniciamos los objetos GOLBALES Aqui
WIFI=wlan(NIC='wlan0', name='WIFI', description='Conexion WIFI')
LAN0=lan_server(NIC='eth0', name='LAN_0', description='Actua como servidor DHCP')
VPN=vpn(NIC='tun0', name='iris02', description='conexion  a servidor central')
# Inicio del manejador de evento de banderas
class MyEventHandler(FileSystemEventHandler):
#    def on_modified(self, event):
#        print(event.src_path, '-- modificado.')
    def on_modified(self, event):
#        print(event)
        flag = Path(event.src_path).name
        if flag == 'wifi_saved':
            print('entremos a wifi_saved')
            get_saved_nets()
        elif flag == 'wifi_add':
            dict = get_dict('/home/pi/servicio/flags/wifi_add')
            add_network(dict['ssid'],dict['password'])
            time.sleep(1)
#            print(dict['ssid'])
        elif flag == 'wifi_erase':
            dict = get_dict('/home/pi/servicio/flags/wifi_erase')
            print(dict)
            erase_network_fn(dict['id_net'])
        else:
            print('!no se reconoce la bandera')

# Inicio del observador
observer = Observer()
observer.schedule(MyEventHandler(), '/home/pi/servicio/flags', recursive=False)
observer.start()

def main():
    """
        This is an example of code you want to run on every iteration
        You can, and probably should move this to its own Python module

        This sample code intentionally crashes once in a while to show what
        happens when your code raises an exception
    """

    # Increment run counter
    # Let it's run for testing purposes
    global RUN, WIFI,LAN0, VPN
    RUN += 1
    observer.join(1)
    print('entrando a un cliclo infinito, presionar Ctrl+C por ahora')
    WIFI.update()
    WIFI.display_state()
    time.sleep(5)
    LAN0.display_state()
    time.sleep(5)
    VPN.display_state()
    time.sleep(5)

    # If the number of times we've run is a multiple of 3, crash!
    # if RUN % 3 == 0:
    #    raise Exception("Something failed!")
    #else:
    #    logger.info("Running our code")
