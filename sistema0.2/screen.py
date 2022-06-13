import time
from luma.core.interface.serial import i2c
from PIL import ImageFont, ImageDraw, Image
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import sh1106
# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = sh1106(serial_interface=None, width=128, height=64, rotate=0)

#font=ImageFont.truetype(font="/usr/share/fonts/truetype/freefont/FreeMono.ttf",size=9)
font=ImageFont.truetype(font='/home/pi/sistema0.2/fonts/arial.ttf',size=9)
#font=ImageFont.load_default()
#font=ImageFont.(font='FreeMono.ttf', size=9)
def wlan0_screen():
    with canvas(device) as draw:
        draw.rounded_rectangle(device.bounding_box, radius=5 , outline="white", fill="black")
        draw.ellipse([(9,16),(13,19)], fill="white")
        draw.arc([(6,12),(16,20)],205,335,fill="white", width=1)
        draw.arc([(3,9),(19,20)],205, 335, fill="white", width=1)
        draw.arc([(0,6),(22,20)],210, 330, fill="white", width =1)
        draw.text((24, 2), "INTERFACE", font=font, fill="white")
        draw.text((24, 12), "WIFI", font=font, fill="white")
        draw.text((4, 22), "Conn a: ", font=font, fill="white")
        draw.text((52, 22),"GIRALDO", font=font,fill="white")
        draw.text((4, 32), "IP: 192.168.0.38", font=font,  fill="white")
        draw.text((4, 42), "Acceso a Internet", font=font, fill="white")

print(device.bounding_box)

def eth0_screen():
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
#    draw.line([(18,6),(18,15)], fill="white", width=1)
        draw.text((24, 2), "INTERFACE", font=font, fill="white")
        draw.text((24, 12),"Ethernet", font=font, fill="white")
        draw.line([(11,28),(18,28)], fill="white", width=1)
        draw.text((20, 22), "Sensor1:192.168.39.101 ", font=font, fill="white")
        draw.line([(11,38),(18,38)], fill="white", width=1)
        draw.text((20, 32), "Host :  HIPARCO ",font=font, fill="white")
        draw.line([(11,48),(18,48)], fill="white", width=1)
        draw.text((20, 42), "Host:192.168.39.101 ", font=font, fill="white")
        draw.line([(11,58),(18,58)], fill="white", width=1)
        draw.text((20, 52), "Host :  HIPARCO ", font=font, fill="white")

def vpn_screen():
    with canvas(device) as draw:
        draw.rounded_rectangle(device.bounding_box, radius=5 , outline="white", fill="black")
#        draw.rectangle((2,2,20,20), outline="white", fill="black")
        draw.ellipse([(3,3),(19,19)], fill="white")
        draw.polygon([(11,11),(4,19),(18,19)], fill="black")
        draw.ellipse([(5,5),(17,17)], fill="black")
        draw.ellipse([(8,7),(14,13)],fill="white")
        draw.polygon([(11,11),(8,18),(14,18)], fill="white")
        draw.text((24, 2), "INTERFACE", font=font, fill="white")
        draw.text((24, 12), "VPN", font=font, fill="white")
        draw.text((4, 22), "Conn a: Central1 ", font=font, fill="white")
        draw.text((4, 32), "IP: 10.0.0.10", font=font,  fill="white")
        draw.text((4, 42), "Registrado", font=font, fill="white")




#wlan0_screen()
#time.sleep(5)
vpn_screen()
time.sleep(5)
