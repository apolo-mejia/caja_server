import os
import time
import netifaces
import socket
import subprocess
from classes import *
import RPi.GPIO as GPIO

#hardware set up
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN)
# Funciones de prueba antes de llevar a functions.py
def Evento(channel):
# Generador consulta de las interfaces que estan guardadas en
# /etc/wap_suplicant/wpa_supplicant.conf
    argument = ['touch','file2']
    p = subprocess.run(argument, capture_output=True)
    argument = ['wpa_cli','-i','wlan0','list_networks']
    p = subprocess.run(argument, capture_output=True, text=True)
#    print(p.stderr)
#    print(p.returncode)
#    print(p.stdout)
#   Generacion del archivo de texto con la consulta
    f = open('/var/www/html/web_app/myfile.txt', 'w')
    f.write(p.stdout)
    f.close()
#   Generacion de un archivo tipo csv
    fr = open('/var/www/html/web_app/myfile.txt', 'r')
    fw = open('/var/www/html/web_app/cvsfile.txt', 'w')
    fw.close()
    b=0
    for x in fr:
        fw = open('/var/www/html/web_app/cvsfile.txt','a')
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

# INTERRUPCIONES
GPIO.add_event_detect(21, GPIO.RISING, bouncetime=2500, callback=Evento)

# my lista/objetos de diccionario de interfaces.
WIFI=wlan(NIC='wlan0', name='WIFI', description='Conexion WIFI')
LAN0=lan_server(NIC='eth0', name='LAN_0', description='Actua como servidor DHCP')
VPN=vpn(NIC='tun0', name='iris02', description='conexion  a servidor central')
#VPN.get_ip()
#VPN.get_node()


#interfaces = [
#        {'name':'Local' , 'interface':'lo'},
#        {'name':'Ethernet0' , 'interface':'eth0'},
#        {'name':'Ethernet1','interface':'eth1'},
#        {'name':'WIFI', 'interface':'wlan0'},
#        {'name':'VPN','interface':'tun0'}
#        ]

# Creamos una lista con las interfaces activas
# INTERFACES = netifaces.interfaces()
# Ya se hizo una clase de cada objeto[interface]

# Revision si se tienen una coneccion a internet

#print(ping('8.8.8.8',53))
#scan_host_eth0()

#print(INTERFACES)
#print(interfaces)
#print(VPN.ip_addr)
#print(WIFI.SSID)
while True:
    print('entrando a un cliclo infinito, presionar Ctrl+C por ahora')
    WIFI.display_state()
    time.sleep(5)
    LAN0.display_state()
    time.sleep(5)
    VPN.display_state()
    time.sleep(5)
GPIO.cleanup()
