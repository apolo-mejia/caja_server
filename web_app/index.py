from flask import Flask, render_template, url_for, request, redirect
from functions import *
from forms import *
import time

app = Flask(__name__)
app.config['SECRET_KEY']='MySEcuRiTY71315404kEyI2'

@app.route('/')
def net_conf():
    return render_template('net_conf.html')

@app.route('/wifi_conf')
def wifi_conf():
    write_flag('wifi_saved','ON',[]) # bandera requiere las redes guadadas
    time.sleep(1) # Por ahora vamos a esperar, pero la idea es hacer una clase de semaphore()
    nets = wifi_scan() # genera una lista de diccionarios, con las redes disponibles al rededor
    listed_nets=get_dicts('/home/pi/servicio/redes/wifi/cvsfile.txt')
#    print(listed_nets)
    nets=get_wifi_description(nets)
    netc={}
    netc['ssid']='Ninguna'
    for net in listed_nets:  # se adicionan las propiedades de id, saved y True
        for net_w in nets:
            if net_w['ssid'] == net['ssid']:
                net_w['saved'] = True
                net_w['id'] = net['network_id']
        if net['flags'] == '[CURRENT]':
            netc = net

    return render_template('wifi_conf.html',nets=nets,listed_nets=listed_nets,netc=netc)

@app.route('/<string:id>/ssid_conf', methods=('GET','POST'))
def ssid_conf(id):
    nets = wifi_scan() # vuelve a scanear las redes mmm?
    listed_nets=get_dicts('/home/pi/servicio/redes/wifi/cvsfile.txt')
    nets=get_wifi_description(nets)
#    print(listed_nets)
    netc={}
    for net in listed_nets:
        print(net['network_id'])
        for net_w in nets:
            if net_w['ssid'] == net['ssid']:
                net_w['saved'] = True
                net_w['id'] = net['network_id']

    for net_w  in nets:
        if net_w['ssid'] == id:
            netc = net_w
            print('match')

    form = ssid_form()
    if form.validate_on_submit():
        result = request.form
        print(result['ssid'])
        print('y la contrasena es : ' + result['pass_word'])
        write_flag('wifi_add','ON',[result['ssid'], result['pass_word']])
        time.sleep(5)
        return redirect(url_for('wifi_conf'))
    form0 = erase_network()
    if form0.validate_on_submit():
        result0 = request.form
# Aqui voy cambiando la invokacion de esta a la marka flaga
#        erase_network_fn(result0['id_net'])
        write_flag('wifi_erase','ON',[result0['id_net']])
        time.sleep(5)
        return redirect(url_for('wifi_conf'))
    return render_template('ssid_conf.html', net = netc, form = form, form0 = form0)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True)
