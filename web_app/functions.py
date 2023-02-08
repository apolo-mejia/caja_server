from wifi import Cell
from flask import url_for
import csv
import subprocess
import time
import os

def wifi_scan():
    nets = []
    for cell in Cell.all('wlan0'):
#        print (cell.ssid)
        if cell.encrypted == True:
            en_type = cell.encryption_type
        else:
            en_type = 'unknow'
        if cell.ssid != '\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            nets.append({ 'ssid':cell.ssid, 'signal':str(cell.signal),
                         'quality':str(cell.quality), 'frequency': str(cell.frequency),
                          'bitrates': cell.bitrates, 'encrypted': cell.encrypted,
                          'chanel': cell.channel, 'address': cell.address,
                          'mode':cell.mode, 'encryption_type': en_type })
#        print (cell.quality)
    return nets

#netws = wifi_scan()
#print (netws)

# funcion que borra los detalles de una red guardada en :
# /etc/wpa_supplicant/wpa_supplicant.conf
# el id que se necesita es el id otorgado en el cvsfile.txt
def erase_network_fn(id):
    print(id)
#    id2add ='\''+id+'\''
    id2add = id
    argument = ['wpa_cli','-i','wlan0','remove_network',id2add]
    print(argument)
    p = subprocess.run(argument, capture_output=True)
    print(p.stdout)
    argument0 = ['wpa_cli','-i','wlan0','save_config']
    p0 = subprocess.run(argument0, capture_output=True)
    print(p0.stdout)
    argument1 = ['wpa_cli','-i','wlan0','reconfigure']
    p1 = subprocess.run(argument1, capture_output=True)
    print(p1.stdout)
    return 0

# Funcion que adiciona los detalles de una red a el wpa_supplicant
def add_network(ssid, password):
    argument = ['wpa_cli','-i','wlan0','add_network']
    p = subprocess.run(argument, capture_output=True)
    print(p.stdout)
    id2add = str(p.stdout)[2:-3]
    print(id2add)
    ssid2add = '"'+ssid+'"'
    print(ssid2add)
    argument0 = ['wpa_cli','-i','wlan0','set_network',id2add,'ssid',ssid2add]
    p0 = subprocess.run(argument0,capture_output=True)
    print(p0)
    password2add = '"'+password+'"'
    argument1 = ['wpa_cli','-i','wlan0','set_network',id2add,'psk',password2add]
    p1 = subprocess.run(argument1,capture_output=True)
    print(p1.stdout)
    argument2 = ['wpa_cli','-i','wlan0','enable_network',id2add]
    p2 = subprocess.run(argument2,capture_output=True)
    print(p2.stdout)
    argument4 = ['wpa_cli','-i','wlan0','save_config']
    p4 = subprocess.run(argument4,capture_output=True)
    print(p4.stdout)
    return id2add

# Generador consulta de las interfaces que estan guardadas en
# /etc/wap_suplicant/wpa_supplicant.conf
def list_networks():
#    argument = ['wpa_cli','-i','wlan0','list_networks']
#    p = subprocess.run(argument, capture_output=True, text=True)
#    print(p.stderr)
#    print(p.returncode)
#    print(p.stdout)
#   Generacion del archivo de texto con la consulta
#    f = open('myfile.txt', 'w')
#    f.write(p.stdout)
#    f.close()
#   Generacion de un archivo tipo csv
#    fr = open('myfile.txt', 'r')
#    fw = open('cvsfile.txt', 'w')
#    fw.close()
#    b=0
#    for x in fr:
#        fw = open('cvsfile.txt','a')
#        str = x
#        if b == 0:
#            str2pass = str.replace(' / ', ',')
#            str2pass = str2pass.replace(' ', '_')
#            b=b+1
#        else:
#            str2pass = str.replace('\t',',')
#        fw.write(str2pass)
#        fw.close()
#    fr.close()
    return 0

# funcion retorna una lista de diccionarios desde un csv file
def get_dicts(file):
    list =[]
    keys=[]
    rows=[]
    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        keys=next(csvreader)
        for row in csvreader:
            rows.append(row)
        for row in rows:
            dic={}
            i=0
            for key in keys:
                dic[key]=row[i]
                i = i+1
            list.append(dic)
    return list

def get_wifi_description(wifi_list):
    for net in wifi_list:
        net['signal_n'] = int(net['signal'])
        if net['signal_n'] > -30:
            net['image'] = url_for('static', filename='images/wifi_4.png')
            net['description'] = 'Excelente: Todas las funcionalidades habilitadas a la vez'
        elif net['signal_n'] >= -67 and net['signal_n'] < -30 :
            net['image'] = url_for('static', filename='images/wifi_3.png')
            net['description'] = 'Muy Buena: Envio de datos, servidor, streaming, video. -- Una funcionalidad a la vez'
        elif net['signal_n'] >= -70 and net['signal_n'] < -67 :
            net['image'] = url_for('static', filename='images/wifi_2.png')
            net['description'] = 'Buena: Envio de datos y servidor - OK, Streaming y Video pueden no funcionar'
        elif net['signal_n'] >= -80 and net['signal_n'] < -70 :
            net['image'] = url_for('static', filename='images/wifi_1.png')
            net['description'] = 'Regular: Envio de datos y servidor - pueden no funcionar, Streaming y Video: deshabilitado'
        else:
            net['image'] = url_for('static', filename='images/wifi.png')
            net['description'] = 'Mala: No se debe usar, Todas las funcionalidades deshabilitadas'
    return wifi_list

# Este fn coloca in '1' en la carpeta de banderas del servicio
def write_flag(flag, state, args):
    string=str(time.time())+','
    if state == 'ON':
       string=string+'1'
    else:
        string=string+'0'
    for arg in args:
        string=string+','
        string=string+arg
    f=open('/home/pi/servicio/flags/'+flag, 'a')
    f.write(string+'\n')
#f.write(arg)
    f.close()


# FUNCIONES PARA LA INTEFACE DEL MONITOREO

# Afiliar todas las partes de una maquina a la misma tarea eg. ISO 10816
def get_machine_task(mask, machine):
    if mask&1 == 1 and 1 == machine :
       overal = 1
       machine = machine
    return  str

# Extrae los documentos por tipo desde un a ruta
def get_files_by_ext(path,ext):
    result = []
    for x in  os.listdir(path): 
        if x.endswith(ext):
           result.append(x)
    return result
