import io
from flask import Flask, render_template, url_for, request, redirect, Response, jsonify, make_response
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
from agenda import *
import datetime as dt
import json
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY']='MySEcuRiTY71315404kEyI2'

def sensor():
    """ Function for test purposes. """
    print(str(dt.datetime.now()) + " --  Scheduler is alive!")

app.route('/')
def home():
    nav_menu ={}
    nav_menu['rol'] = 0
    l_maq = get_machines_dict()
    return render_template('home.html', nav_menu=nav_menu, l_maq=l_maq)

@app.route('/red_serv')
def red_serv():
    nav_menu ={}
    nav_menu['rol'] = 0
    return render_template('net_conf.html', nav_menu=nav_menu)

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

@app.route('/<int:id_m>/machine', methods=('GET','POST'))
def machine(id_m):
    nav_menu = {}
    nav_menu['rol'] = 0
    nav_menu['where']  = 3
    machined = get_machine(id_m)
    tasksd = get_machine_scope_task(id_m)
    partsd = get_machine_parts(id_m)
    mq_form = create_machine()
    j_form = send_JSONpack()
    pic_form = upload_file()
    j_lines = get_journal_lines(machined['journal'],'machine',id_m)
    if mq_form.validate_on_submit():
        pointer = ('machines', id_m)
        dict = mq_form.data
        dict.pop('submit',None)
        dict.pop('csrf_token', None)
        file = app.root_path+'/static/data/machine_'+str(id_m)+'/'+machined['journal']
        msg = {}
        msg['pack'] = 'Se han cambiado los valores de la maquina.'
        journal_writer(file, msg)
        update_table_register(pointer,dict)
        return redirect(url_for("machine", id_m = id_m))
    if j_form.validate_on_submit():
        file = app.root_path+'/static/data/machine_'+str(id_m)+'/'+machined['journal']
        journal_writer(file, j_form.data)
        return redirect(url_for("machine", id_m = id_m))

    if pic_form.validate_on_submit():
        f= pic_form.documento.data
        filename = secure_filename(f.filename)
        name2save = app.root_path+"/static/data/machine_"+str(machined['id'])+"/pictures/"+filename
        f.save(name2save)
        file = app.root_path+'/static/data/machine_'+str(id_m)+'/'+machined['journal']
        msg = {}
        msg['pack'] = 'Se a agregado / cambiado la foto de la maquina.'
        journal_writer(file, msg)
        conn = get_db_connection()
        conn.execute('UPDATE machines SET picture = ? WHERE id = ?',(filename, id_m))
        conn.commit()
        conn.close()
        return redirect(url_for("machine", id_m = id_m))

    return render_template("machine.html", machined=machined, partsd=partsd, nav_menu=nav_menu, tasksd=tasksd, 
    mq_form=mq_form, j_lines=j_lines, j_form=j_form, pic_form=pic_form)

@app.route('/machines', methods = ('GET','POST'))
def machine_ec():
    nav_menu={}
    nav_menu['rol']=0
    formp = create_part()
    part_ord = 1
    machined = get_machine(1)
    parts_t = get_parts_templates()
    tasksd = get_machine_scope_task(1)
    parts_ava = []
    for part in parts_t:
        parts_ava.append(part['avatar'][:-4])
    nav_menu['where'] = 3
    path = '/home/pi/caja_server/web_app/static/images/avatars/machines/default'
    m_avatars = get_files_by_ext(path,'.png')
    return render_template("machine_ec.html", machined=machined, nav_menu=nav_menu, tasksd=tasksd, 
            parts_t=parts_t,parts_ava= parts_ava, m_avatars=m_avatars, formp=formp, part_ord=str(part_ord),parts=[])

@app.route('/<int:id_pt>/create_part_template', methods = ('GET','POST'))
def create_part_template(id_pt):
    form = create_part_template_f()
    form3 = create_s_field()
    if id_pt == 1023:
        form_mano = mano_list()
        if form.validate_on_submit():
            part_t = create_new_part_template(form.data)
            return redirect(url_for('create_part_template', id_pt=part_t['id']))
        return render_template('create_p_temp.html', form=form, form3=form3, form_mano=form_mano)
    else:
        form2 = upload_part_avatar()
        part_t = get_part_temp_by_id(id_pt)
        s_fields = json.loads(part_t['s_fields'])
        if form2.validate_on_submit():
            f = form2.avatar_up.data
            filename = secure_filename(f.filename)
            nombre = form2.avatar_name.data
            name2save = app.root_path + "/static/images/avatars/parts/default/"+nombre+".png"
            f.save(name2save)
            return redirect(url_for('create_part_template', id_pt=part_t['id']))
            # render_template("test_page.html",result=form2.data)
        return render_template('edit_part_template.html', form=form, form2=form2, form3=form3, part_t=part_t,s_fields=s_fields)

@app.route('/<int:id_p>/<int:rol>/part', methods = ['GET','POST'])
def part(id_p,rol):
    if rol == 1:
        partd = get_part(id_p)
        machined = get_machine(partd['id_machine'])
# info tareas asociadas
        drop = get_machine_task(partd['c_task'],machined['id'])
        print (drop)
# info de plantilla
        s_fields = json.loads(partd['s_fields'])
# info menu de navegacion
        nav_menu = {'level' : 4, 'rol': rol}
        return render_template('part.html', machined=machined, partd=partd, s_fields=s_fields, nav_menu = nav_menu)
    else:
        partd = get_part(id_p)
        machined = get_machine(partd['id_machine'])
        form = update_part_json()
    # info tareas asociadas
        drop = get_machine_task(partd['c_task'],machined['id'])
        print (drop)
    # info de plantilla
        s_fields = json.loads(partd['s_fields'])
    # info menu de navegacion
        nav_menu = {'level' : 4, 'rol': rol}
        if form.validate_on_submit():
            pointer = ('parts',form.data['part_id'])
            data = {'s_fields': "'"+form.data['json_pack']+"'","a_status":1}
            consulta = update_table_register(pointer, data)
            print(consulta)
            return render_template("test_page.html",result=form.data)
        return render_template('part_ec.html', machined=machined, partd=partd, s_fields=s_fields, nav_menu = nav_menu, form=form)

@app.route('/<int:id_t>/task', methods = ('GET', 'POST'))
def task(id_t):
    nav_menu={}
    nav_menu['rol'] = 0
    nav_menu['where'] = 5
    taskd = get_task(id_t)
    machined = get_machine(taskd['id_machine'])
    partsd = get_machine_parts(id_t)
# info del time-table
# w_block = gen_week_block(id_t)
    w_block = gen_week_block(taskd)
# info de los items especificos
    s_fields = json.loads(taskd['s_fields'])
    start = dt.time.fromisoformat(taskd['hf_start'])
    end = dt.time.fromisoformat(taskd['hf_end'])
    form_tk = task_data(t_int_m=w_block[-1]['m_interval'], t_int_h=w_block[-1]['h_interval'], hf_start_h=start.hour,
        hf_start_m=start.minute, hf_end_h=end.hour, hf_end_m=end.minute)
    if form_tk.validate_on_submit():
        pointer = ('tasks',id_t)
        dict = {}
        if int(form_tk.data['t_int_h']) == 0 and int(form_tk.data['t_int_m']) == 0 :
            dict['t_interval'] = 15
        else:
            dict['t_interval'] = (int(form_tk.data['t_int_h'])*4)*15 + int(form_tk.data['t_int_m'])
        dict['d_allow'] = form_tk.data['d_allow']
        dict['hf_start'] = dt.time(int(form_tk.data['hf_start_h']),int(form_tk.data['hf_start_m'])).strftime('%H:%M:%S')
        dict['hf_end'] = dt.time(int(form_tk.data['hf_end_h']),int(form_tk.data['hf_end_m'])).strftime('%H:%M:%S')
        print(form_tk.data)
        update_table_register(pointer,dict)
        return redirect(url_for("task", id_t=id_t))
    return render_template("task.html", machined=machined, partsd=partsd, nav_menu=nav_menu, taskd=taskd, 
        w_block=w_block, s_fields=s_fields, form_tk = form_tk)

@app.route('/<int:id_m>/machine_ec2', methods = ('GET','POST'))
def machine_ec2(id_m):
    if id_m == 99:
        nav_menu={}
        nav_menu['rol'] = 0
        nav_menu['where'] = 3
        mq_form = create_machine()
        insumos = {}
        insumos['completed'] = 0
        insumos['path'] = '/home/pi/caja_server/web_app/static/images/avatars/machines/default/'
        insumos['path_rel'] = 'images/avatars/machines/default/'
        insumos['path_rel_foto'] ='images/pictures/machines/default/'
        insumos['m_avatars'] = get_files_by_ext(insumos['path'],'.png')
        if mq_form.validate_on_submit():
            machine_new = create_new_machine(mq_form.data)
            id_m = machine_new['id']
            return redirect(url_for("machine_ec2", id_m = id_m))   
        return render_template("machine_ec2.html", nav_menu=nav_menu, mq_form=mq_form, insumos=insumos)
    else:
        machine = get_machine(id_m)
        if machine['a_status'] == 6 or machine['a_status'] == 7:
            parts = get_machine_parts(id_m)
            nav_menu={}
            nav_menu['rol'] = 0
            nav_menu['where'] = 4
            insumos = {}
            insumos['completed'] = 20
            insumos['path'] = 'data/machine_'+str(machine['id'])
            insumos['ord'] = 1
            for part in parts:
                insumos['ord'] = insumos['ord']+1
            parts_temp = get_parts_templates_dict()
            formp = create_part2(ordinal=insumos['ord'])
            formf = update_field_tablereg()
            if formp.validate_on_submit():
                create_new_part2(formp.data)
                return redirect(url_for("machine_ec2", id_m = id_m)) 
            if formf.validate_on_submit():
                update_table_register((formf.data['table'],str(formf.data['id'])),{"a_status " : 8 })
                return redirect(url_for("machine_ec2", id_m=id_m))
            return render_template("machine_ec2p.html",nav_menu=nav_menu, insumos=insumos, machine=machine, parts_temp=parts_temp, 
            formp=formp, formf=formf, parts=parts)
        elif machine['a_status'] == 8 or machine['a_status'] == 9:
            parts = get_machine_parts_dict(id_m)
            forms = enrroll_sensor()
            formsr = send_sensor_req(requirement='meas9')
            nav_menu={}
            nav_menu['rol'] = 0
            nav_menu['where'] = 4
            insumos = {}
            insumos['completed'] = 40
            insumos['path'] = 'data/machine_'+str(machine['id'])
            insumos['text1'] = ''
            sensores = get_sensors()
            formf = update_field_tablereg()
            if formsr.validate_on_submit():
                insumos['text0'] = deal_req(formsr.requirement.data, formsr.mac_address.data)
                print(insumos['text0']['envio'])
                insumos['text1'] = deal_req('meas10',formsr.mac_address.data)
                name = str(insumos['text1']['id'])[0:7]
                insumos['act_part']= formsr.extra_int.data
                sensor_temp = get_sensor_template(name)
                insumos['s_fields'] = sensor_temp['s_fields']
                insumos['capacities'] = sensor_temp['capacities']
                insumos['description'] = sensor_temp['description']
                insumos['avatar'] = sensor_temp['avatar']           
                return render_template("machine_ec2s.html",nav_menu=nav_menu, parts=parts, sensores=sensores, machine=machine, 
                        insumos=insumos, forms=forms, formsr=formsr, formf=formf)
            if forms.validate_on_submit():
                result= pair_sensor2part(forms.data, id_m)
                update_table_register(("machines",str(id_m)),{"a_status " : 9 })
                return redirect(url_for("machine_ec2", id_m=id_m)) 
            if formf.validate_on_submit():
                update_table_register((formf.data['table'],str(formf.data['id'])),{"a_status " : 10 })
                insumos['completed'] = 60
                return redirect(url_for("machine_ec2", id_m=id_m))
            return render_template("machine_ec2s.html",nav_menu=nav_menu, parts=parts, sensores=sensores, machine=machine, insumos=insumos, 
                    forms=forms, formsr=formsr, formf=formf)
        elif machine['a_status'] == 10:
            nav_menu={}
            nav_menu['rol'] = 0
            nav_menu['where'] = 5
            form = send_JSONpack()
            parts = get_machine_parts_dict(id_m)
            sensors, capa = get_sensors_machine(id_m)
            insumos = {}
            parts = get_machine_parts_dict(id_m)
            tasks = get_task_templates_dict(sensors)
            insumos['completed'] = 60
            insumos['path'] = 'data/machine_'+str(machine['id'])
            for part in parts:
                part['sensors'] = []
                part['n_sensors'] = 1
                for sensor in sensors:
                    if part['id'] == sensor['part_id']:
                        part['n_sensors']=part['n_sensors']+1
                        part['sensors'].append({'alias':sensor['alias'], 'sensor_id':sensor['id'], 'avatar':sensor['avatar'],'part_id':part['id']})
                #print(part)
            table = generate_meas__table(machine['name'],parts,sensors,tasks)
            if form.validate_on_submit():
                pack = json.loads(form.data['pack'])
                tareas = generate_tasks(pack)
                print(len(tareas))
                update_table_register(("machines",str(id_m)),{"a_status " : 11 })
                return redirect(url_for("machine_ec2", id_m=id_m))
            return render_template("machine_ec2t.html",nav_menu=nav_menu, parts=parts, tasks=tasks,sensors=sensors, form = form,
                    machine=machine,insumos=insumos, table=table)
        elif machine['a_status'] == 11:
            nav_menu={}
            nav_menu['rol'] = 0
            nav_menu['where'] = 5
            insumos = {}
            insumos['completed'] = 80
            form = send_JSONpack(pack="change")
            if form.validate_on_submit():
                update_table_register(("machines",str(id_m)),{"a_status " : 1 })
                return redirect(url_for("machine", id_m=id_m))
            return render_template("machine_ec2d.html", nav_menu=nav_menu, insumos=insumos, machine=machine, form=form)

@app.route('/formas', methods = ('GET', 'POST'))
def formas():
     formsr = send_sensor_req(requirement='meas9')
     if formsr.validate_on_submit():
         print('forma validada!! ')
         text = deal_req(formsr.requirement.data, formsr.mac_address.data)
         print(text)
         return render_template("test_page.html",result=formsr.data, text=text)
     return render_template("form_helper.html", formsr=formsr)

@app.route("/check_time_table", methods = ["POST"])
def check_time_table():
    req = request.get_json(force=True)
    print(req)
    taskd = get_task_dict(int(req['id_t']))
    if int(req['t_int_h']) == 0 and int(req['t_int_m']) == 0 :
        taskd['t_interval'] = 15
    else:
        taskd['t_interval'] = (int(req['t_int_h'])*4)*15 + int(req['t_int_m'])
    taskd['d_allow'] = int(req['d_allow'])
    taskd['hf_start'] = dt.time(int(req['hf_start_h']),int(req['hf_start_m'])).strftime('%H:%M:%S')
    taskd['hf_end'] = dt.time(int(req['hf_end_h']),int(req['hf_end_m'])).strftime('%H:%M:%S') 
    w_sch = gen_week_block(taskd)
    print(w_sch)
    res = make_response(jsonify(w_sch), 200)
    return res

if __name__ == '__main__':
   app.run(host="0.0.0.0", debug = True)
