import io
from flask import Flask, render_template, url_for, request, redirect, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from functions import *
from forms import *
from medidas_gen import *
from req_sensors import *
from queries import *
from schedule import *
#import time
import json
#import random

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

@app.route('/<int:med>/<string:file2read>/show_measure')
def show_measure(med, file2read):
    print(file2read)
    xg, yg, zg = get_vectors("/home/pi/caja_server/servicio/medidas/stest/"+file2read)
    xr = {}
    yr = {}
    zr = {}
    if med==1:
        # Quitamos el offset
        xp = num_derivate_diff(xg)
        yp = num_derivate_diff(yg)
        zp = num_derivate_diff(zg)
        # Generamos los vectores de RMS
        xr['rms'] = get_rms_simple(xp)
        yr['rms'] = get_rms_simple(yp)
        zr['rms'] = get_rms_simple(zp)
        # Generemos los maximos
        xr['max'] = get_max_absval(xp)
        yr['max'] = get_max_absval(yp)
        zr['max'] = get_max_absval(zp)
        units = '[ mm / s² ]'

    elif med==0:
        # Quitamos el offset
        xp = num_derivate_diff(xg)
        yp = num_derivate_diff(yg)
        zp = num_derivate_diff(zg)
        # Generamos los vectores de velocidad
        xv = antiderivate(xp)
        yv = antiderivate(yp)
        zv = antiderivate(zp)
        # Encontremos los RMS
        xr['rms'] = get_rms_simple(xv)
        yr['rms'] = get_rms_simple(yv)
        zr['rms'] = get_rms_simple(zv)
        # Generemos los maximos
        xr['max'] = get_max_absval(xv)
        yr['max'] = get_max_absval(yv)
        zr['max'] = get_max_absval(zv)
        units = '[ mm / s ]'

    elif med==3:
        # Encontremos los RMS
        xr['rms'] = get_rms_simple(xg)
        yr['rms'] = get_rms_simple(yg)
        zr['rms'] = get_rms_simple(zg)
        # Generemos los maximos
        xr['max'] = get_max_absval(xg)
        yr['max'] = get_max_absval(yg)
        zr['max'] = get_max_absval(zg)
        units = '[ m / s² ]'

    rms={'x':xr, 'y':yr, 'z':zr, 'unit': units}
    return render_template('measure.html', med=med,file2read=file2read, rms=rms)

@app.route('/<int:med>/<string:file2read>/plotx.png')
def plotx_png(med, file2read):
    xg, yg, zg = get_vectors("/home/pi/caja_server/servicio/medidas/stest/"+file2read)
    if med == 1:
        xs = num_derivate_diff(xg)
        t = np.linspace(0,500,len(xs))
        win = 350
        uni = '[ m / s²]'
    elif med ==0:
        xm = num_derivate_diff(xg)
        xs = antiderivate(xm)
        win = 350*2
        t = np.linspace(0,500,len(xg)*2)
        i=0
        while len(xs) < len(t):
            xs.append(xs[i])
            i=i+1
        uni = 'v[ mm / s]'
    elif med == 3:
        xs = xg
        t = np.linspace(0,500,len(xs))
        win = 350
        uni = 'g[ m / s² ]'
    fig = create_figure(t, xs, win, uni)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/<int:med>/<string:file2read>/ploty.png')
def ploty_png(med,file2read):
    xg, yg, zg = get_vectors("/home/pi/caja_server/servicio/medidas/stest/"+file2read)
    if med == 1:
        ys = num_derivate_diff(yg)
        t = np.linspace(0,500,len(ys))
        win = 350
        uni = '[ m / s² ]'
    elif med == 0:
        ym = num_derivate_diff(yg)
        ys = antiderivate(ym)
        win = 350*2
        t = np.linspace(0,500,len(yg)*2)
        i=0
        while len(ys) < len(t):
            ys.append(ys[i])
            i=i+1
        uni = 'v[ mm / s]'
    elif med == 3:
        ys = yg
        t = np.linspace(0,500,len(ys))
        win = 350
        uni = 'g[ m /s² ]'
    fig = create_figure(t, ys, win, uni)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/<int:med>/<string:file2read>/plotz.png')
def plotz_png(med, file2read):
    xg, yg, zg = get_vectors("/home/pi/caja_server/servicio/medidas/stest/"+file2read)
    if med == 1:
        zs = num_derivate_diff(zg)
        t = np.linspace(0,500,len(zs))
        win = 350
        uni = '[ m / s² ]'
    elif med ==0:
        zm = num_derivate_diff(zg)
        zs = antiderivate(zm)
        win = 350*2
        t = np.linspace(0,500,len(zg)*2)
        i=0
        while len(zs) < len(t):
            zs.append(zs[i])
            i=i+1
        uni = 'v[ mm / s]'
    elif med == 3:
        zs = zg
        t = np.linspace(0,500,len(zg))
        win = 350
        uni = 'g[ m /s² ]'
    fig = create_figure(t, zs, win, uni)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure(xs,y,win, uni):
    fig = Figure()
    axis = fig.subplots()
    axis.grid(True)
    maximo = max(y)
    minimo = min(y)
    maxim = max(abs(maximo), abs(minimo))
    ysa = np.array(y)

    if maxim == abs(minimo):
        center = np.where(minimo==ysa)[0]
    else:
        center = np.where(maximo==ysa)[0]

#    if center+int(0.5*win) >= 1721:
    if center+int(0.5*win) >= len(xs):
        center = center-int(0.5*win)-1

    inicio = int(xs[center[0]-int(0.5*win)])
    fin = int(xs[center[0]+int(0.5*win)])

    axis.plot(xs,y,linewidth=0.3)
    axis.axis([inicio,fin,minimo,maximo])
    axis.yaxis.set_label_position("right")
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0)
    axis.set_ylabel(uni)
    return fig

@app.route('/<int:med>/<string:file2read>/plot3d.png')
def plot3d_png(med, file2read):
    xg,yg,zg = get_vectors("/home/pi/caja_server/servicio/medidas/stest/"+file2read)
    if med==1:
        # Quitamos el offset
        xp = num_derivate_diff(xg)
        yp = num_derivate_diff(yg)
        zp = num_derivate_diff(zg)
        # Generamos los vectores de RMS
        xr = get_rms_simple(xp)
        yr = get_rms_simple(yp)
        zr = get_rms_simple(zp)
    elif med==0:
        # Quitamos el offset
        xp = num_derivate_diff(xg)
        yp = num_derivate_diff(yg)
        zp = num_derivate_diff(zg)
        # Generamos los vectores de velocidad
        xv = antiderivate(xp)
        yv = antiderivate(yp)
        zv = antiderivate(zp)
        # Encontremos los RMS
        xr = get_rms_simple(xv)
        yr = get_rms_simple(yv)
        zr = get_rms_simple(zv)
    elif med==3:
        # Encontremos los RMS
        xr = get_rms_simple(xg)
        yr = get_rms_simple(yg)
        zr = get_rms_simple(zg)

    fig=components(xr,yr,zr)
    buf = io.BytesIO()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def components(xr, yr, zr):
    fpy = 1/max(xr,yr,zr)
    rms = np.sqrt(xr**2+yr**2+zr**2)
    xpy = xr*fpy
    ypy = yr*fpy
    zpy = zr*fpy
    print(fpy)
    fig = Figure()

    ax = fig.gca(projection='3d')

    z = [0,0]
    z1 = [0,0]
    z2 = [0,1]
    zm = [0, zpy]

    x = [0,1]
    x1 = [0,0]
    x2 = [0,0]
    xm = [0, xpy]

    y = [0,0]
    y1 = [0,1]
    y2 = [0,0]
    ym = [0, ypy]

    # Ejes
    ax.plot(x, y, z, linewidth=0.3, color='black')
    ax.plot(x1, y1, z1, linewidth=0.3, color='black')
    ax.plot(x1, y2, z2, linewidth=0.3, color='black')
    ax.quiver([0,0,0.9],[0,0.9,0],[0.9,0,0],[0,0,1],[0,1,0],[1,0,0], length=0.1, color='black', linewidth=0.4)
    # Proyeción obre los ejes
    ax.plot([0, xpy],[0, 0],[0, 0], linewidth=1, color='blue')
    ax.quiver([0,0.85*xpy],[0,0],[0,0],[0,xpy],[0,0],[0,0], length=0.15, color='blue')
    ax.plot([0, 0],[0, ypy],[0, 0], linewidth=1, color='blue')
    ax.quiver([0,0],[0,0.85*ypy],[0,0],[0,0],[0,ypy],[0,0], length=0.15, color='blue')
    ax.plot([0, 0],[0, 0],[0, zpy], linewidth=1, color='blue')
    ax.quiver([0,0],[0,0],[0,0.85*zpy],[0,0],[0,0],[0,zpy], length=0.15, color='blue')
    # Vector resultante
    ax.plot(xm, ym, zm, linewidth=1, color='red', label='RMS = '+ str(rms))
    ax.quiver([0,0.85*xpy],[0,0.85*ypy],[0,0.85*zpy],[0,xpy],[0,ypy],[0,zpy], length=0.15, color='red')
    # Proyecciones
    ax.plot([0,0],[0,ypy],[0,zpy], linewidth=0.3, color='black', ls='--')
    ax.plot([0,xpy],[0,0],[0,zpy], linewidth=0.3, color='black', ls='--')
    ax.plot([0,xpy],[0,ypy],[0,0], linewidth=0.3, color='black', ls='--')

    # Vamos con las marcas con los textos
    ax.text(0,0,1, 'Z')
    ax.text(0,1,0, 'Y')
    ax.text(1,0,0, 'X')
    ax.text(0,0,0.3, str(round(zr,5)), zdir='z', fontsize=8 )
    ax.text(0,0.5,0, str(round(yr,5)), zdir='y', fontsize=8 )
    ax.text(0.5,0,0, str(round(xr,5)), zdir='x', fontsize=8 )

    ax.grid(False)
#    ax.legend(loc='lower center')
    ax.set_title('Componetes Normales de la medida')
    ax.axis(False)
    ax.view_init(24,62)
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    return fig

@app.route('/sensor', methods=('GET','POST'))
def sensor():
    form = start_measure()
    if form.validate_on_submit():
        print("se presiona el boton")
        esp = serial.Serial('/dev/ttyUSB0', 115200, timeout=None)
        sleep(1)
        take_measure(esp)
        file, file2send = create_document(esp)
        duration,samples = get_data_len(esp)
        raw = get_data_points(samples, file, esp)
        print(str(duration) + "---" + str(samples))
        print("las iteraciones" + str(raw))
        print("Las tomas" + str(samples))
        esp.close()
        return redirect("/1/"+file2send+"/show_measure")
#        return render_template('net_conf.html')
    return render_template("sensor.html", form = form)

@app.route('/<int:id_m>/machine')
def machine(id_m):
    machined = get_machine(id_m)
    tasksd = get_machine_scope_task(id_m)
    partsd = get_machine_parts(id_m)
    nav_menu = 3
    return render_template("machine.html", machined=machined, partsd=partsd, nav_menu=nav_menu, tasksd=tasksd)

@app.route('/<int:id_p>/part')
def part(id_p):
    partd = get_part(id_p)
    machined = get_machine(partd['id_machine'])
# info tareas asociadas
    drop = get_machine_task(partd['c_task'],machined['id'])
    print (drop)
# info de plantilla
    s_fields = json.loads(partd['s_fields'])
# info menu de navegacion
    nav_menu = 4
    return render_template('part.html', machined=machined, partd=partd, s_fields=s_fields, nav_menu = nav_menu)

@app.route('/<int:id_t>/task')
def task(id_t):
    taskd = get_task(id_t)
    machined = get_machine(taskd['id_machine'])
    partsd = get_machine_parts(id_t)
# info del time-table
    w_block = gen_week_block(id_t)
# info de los items especificos
    s_fields = json.loads(taskd['s_fields'])
    nav_menu = 5
    return render_template("task.html", machined=machined, partsd=partsd, nav_menu=nav_menu, taskd=taskd, w_block=w_block, s_fields=s_fields)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True)
