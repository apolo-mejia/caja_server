from functions import *
import os
import netifaces
from luma.core.interface.serial import i2c
from PIL import ImageFont, ImageDraw
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import sh1106

serial = i2c(port=1, address=0x3C)
device = sh1106(serial_interface=None, width=128, height=64, rotate=0)
font=ImageFont.truetype(font="/home/pi/sistema0.2/fonts/Arial.ttf",size=9)


class vpn:
    def __init__(self,NIC, name, description):
        self.NIC = NIC
        self.name = name
        self.description = description
        self.node = ""
        self.ip_addr = ""
        self.get_ip()
        self.get_node()

    def get_node(self):
        if ping('10.0.0.1',655) == True:
            self.node = socket.getfqdn("10.0.0.1")
#            print("Esta conectado a la vpn")
        else:
            self.node = "No conectado"
#            print("no esta conectado")
        return True

    def get_ip(self):
        try:
            addr = netifaces.ifaddresses(self.NIC)[netifaces.AF_INET]
            self.ip_addr =addr[0]['addr']
            return self.ip_addr
        except KeyError:
            self.ip_addr = "None"
            return self.ip_addr

    def display_state(self):
        with canvas(device) as draw:
            draw.rounded_rectangle(device.bounding_box, radius=5 , outline='white', fill='black')
            draw.ellipse([(3,3),(19,19)], fill="white")
            draw.polygon([(11,11),(4,19),(18,19)], fill="black")
            draw.ellipse([(5,5),(17,17)], fill="black")
            draw.ellipse([(8,7),(14,13)],fill="white")
            draw.polygon([(11,11),(8,18),(14,18)], fill="white")
            draw.text((24, 2), "INTERFACE", font=font, fill="white")
            draw.text((24, 12), "VPN", font=font, fill="white")
            draw.text((4, 22), "Conn a: "+ self.node + " - Central1 ", font=font, fill="white")
            draw.text((4, 32), "IP : "+ self.ip_addr, font=font,  fill="white")
            draw.text((4, 42), "Registrado", font=font, fill="white")

class wlan:
    def __init__(self,NIC, name, description):
        self.NIC = NIC
        self.name = name
        self.description = description
        self.int_con = False
        self.check_internet_conn()
        self.SSID = "None"
        self.get_SSID()
        self.ip_addr = "None"
        self.get_ip()

    def check_internet_conn(self):
        self.int_con = ping('8.8.8.8',53)
        return self.int_con

    def get_SSID(self):
        ssid = os.popen('iwgetid -r').read()
        self.SSID = ssid[:-1]
        return self.SSID

    def get_ip(self):
        try:
            addr = netifaces.ifaddresses(self.NIC)[netifaces.AF_INET]
            self.ip_addr =addr[0]['addr']
            return self.ip_addr
        except KeyError:
            self.ip_addr = "None"
            return self.ip_addr

    def update(self):
        self.check_internet_conn()
        self.get_SSID()
        self.get_ip()
        return 0

    def display_state(self):
        with canvas(device) as draw:
            draw.rounded_rectangle(device.bounding_box, radius=5, outline="white", fill="black")
            draw.ellipse([(9,16),(13,19)], fill="white")
            draw.arc([(6,12),(16,20)],205,335,fill="white", width=1)
            draw.arc([(3,9),(19,20)],205, 335, fill="white", width=1)
            draw.arc([(0,6),(22,20)],210, 330, fill="white", width=1)
            draw.text((24, 2), "INTERFACE", font=font, fill="white")
            draw.text((24, 12), self.name, font=font, fill="white")
            draw.text((4, 22), "Conn a: "+ self.SSID, font=font, fill="white")
            draw.text((4, 32), "IP asignada: "+str(self.ip_addr), font=font,  fill="white")
            if self.int_con == True:
                draw.text((4, 42), "Acceso a Internet", font=font, fill="white")
            else:
                draw.text((4, 42), "Sin Acceso a Internet", font=font, fill="white")

    def display_conf_state(self):
        with canvas(device) as draw:
            draw.rounded_rectangle(device.bounding_box, radius=5, outline="white", fill="black")
            draw.ellipse([(9,16),(13,19)], fill="white")
            draw.arc([(6,12),(16,20)],205,335,fill="white", width=1)
            draw.arc([(3,9),(19,20)],205, 335, fill="white", width=1)
            draw.arc([(0,6),(22,20)],210, 330, fill="white", width=1)
            draw.text((24, 2), "INTERFACE", font=font, fill="white")
            draw.text((24, 12), self.name, font=font, fill="white")
            draw.text((4, 32), "CONFIGURANDO..." , font=font, fill="white")

class lan_server:
    def __init__(self, NIC, name, description):
        self.NIC = NIC
        self.name = name
        self.description = description
        self.hosts = []
        self.scan_interface()

    def scan_interface(self):
        for i in range (101,105):
            ip_scan = "192.168.39."+str(i)
            if ping(ip_scan,80) == True:
               self.hosts.append({'ip':ip_scan, 'name': socket.getfqdn(ip_scan)})
               #print('En la direccion '+ ip_scan + 'esta ' + socket.getfqdn(ip_scan))
            else:
               self.hosts.append({'ip':ip_scan, 'name': 'None'})
               #print('En la direccion ' + ip_scan +'No hay nada')
        return self.hosts

    def display_state(self):
        with canvas(device) as draw:
            draw.rounded_rectangle(device.bounding_box, radius=5 , outline="white", fill="black")
#    draw.rectangle((2,2,20,20), outline="white", fill="black")
            draw.line([(3,18),(19,18)], fill="white", width=2)
            draw.line([(11,18),(11,58)], fill="white", width=2)
            draw.line([(3,4),(3,18)], fill="white", width=2)
            draw.line([(19,4),(19,18)], fill="white", width=2)
            draw.line([(7,6),(7,15)], fill="white", width=1)
            draw.line([(10,6),(10,15)], fill="white", width=1)
            draw.line([(13,6),(13,15)], fill="white", width=1)
            draw.line([(16,6),(16,15)], fill="white", width=1)
            draw.text((24, 2), "INTERFACE", font=font, fill="white")
            draw.text((24, 12),self.name, font=font, fill="white")

            ly_pos = 28
            ty_pos = 22
            for i in range (4):
                if self.hosts[i]['name'] == 'None':
                    draw.line([(11, ly_pos),(18,ly_pos)], fill="white", width=1)
                    draw.text((20, ty_pos), 'X - Nada conectado', font=font, fill="white")
                else:
                    draw.line([(11, ly_pos),(18,ly_pos)], fill="white", width=1)
                    draw.text((20, ty_pos), self.hosts[i]['ip'] +'-'+ self.hosts[i]['name'] , font=font, fill="white")
                ly_pos = ly_pos + 10
                ty_pos = ty_pos + 10

