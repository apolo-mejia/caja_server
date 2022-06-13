import socket
import subprocess
import csv

# fn ping que devuelve existe el host y tien coneccion
def ping(host,port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host, port)
        s.connect(server_address)
    except OSError as error:
        return False
    else:
        s.close()
        return True

def get_saved_nets():
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
    print('Generando archivos de ')

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
    return 0

def erase_network_fn(id):
    print(id)
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


# devuelve un dicionario a un archivo cvs
# keys -> primera linea
def get_dict(file):
#def add_wifi(file):
    dict = {}
    keys = []
    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        keys = next(csvreader)
        for row in csvreader:
            pass
        args = row
        i=0
        for key in keys:
            dict[key]=args[i]
            i = i+1
    return dict

# Devuelve una lista de diccionarias a un archivo CVS
def get_dicts(file):
    list =[]
    keys=[]
    rows=[]
    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        keys=next(csvreader)
        rows.append(row)
        for row in rows:
            dic={}
            i=0
            for key in keys:
                dic[key]=row[i]
                i = i+1
            list.append(dic)
    return list


#def write_flag(flag,state):
#    f=open('/home/pi/servicio/flags/'+flag, 'w')
#    if state == 'ON':
#        f.write('1')
#    else:
#        f.write('0')
#    f.close()
