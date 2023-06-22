import sqlite3
import datetime as dt
import shutil
import os
import json
from index import app

# Connection query
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# get machine data
def get_machine(id_machine):
    conn = get_db_connection()
    machine = conn.execute('SELECT * FROM machines WHERE id=?',(id_machine,)).fetchone()
    conn.close()
    return machine

# get all parts in dict with just few values
def get_machine_parts_dict_DB(id_machine):
    cols = []
    conncol = sqlite3.connect('database.db')
    cursor = conncol.cursor()
    data=cursor.execute('''SELECT id, name, avatar, a_status FROM parts WHERE id_machine=? ORDER BY ordinal ASC''',(id_machine,))
    for column in data.description:
        cols.append(column[0])
    conncol.commit()
    conncol.close()
    conn = get_db_connection()
    result = conn.execute('SELECT id, name, avatar, a_status FROM parts WHERE id_machine=? ORDER BY ordinal ASC',(id_machine,)).fetchall()
    conn.close()
    salida = []
    for dic in result:
        pre_dict = {}
        for col in cols:
            pre_dict[col]=dic[col]
        salida.append(pre_dict)
    return salida


# get machines dict for the DashBoard
def get_machines_dict():
    cols = []
    conncol = sqlite3.connect('database.db')
    cursor = conncol.cursor()
    data = cursor.execute('''SELECT * FROM machines''')
    for col in data.description:
        cols.append(col[0])
    conncol.commit()
    conncol.close()
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM machines').fetchall()
    conn.close()
    salida = []
    for dic in result:
        pre_dict = {}
        for col in cols:
            pre_dict[col] = dic[col]
        salida.append(pre_dict)
    for sal in salida:
        sal['j_lines'] = []
        text = 'static/data/machine_'+str(sal['id'])+'/journal_'+str(sal['id'])+'.txt'
        journal = os.path.join(app.root_path,text)
        try:
            with open (journal) as file:
                for line in (file.readlines() [-3:]):
                    new_line = line[:19]+line[26:-2]
                    sal['j_lines'].append(new_line)
        except:
            sal['j_lines'].append('No se cncuentra el archivo')
        print(sal['j_lines'])
    for sal in salida:
        sal['parts'] = get_machine_parts_dict_DB(sal['id'])
    
    return salida

# task_template available
def get_task_templates_dict(sensors):
    cols = []
    conncol = sqlite3.connect('database.db')
    cursor = conncol.cursor()
    data=cursor.execute('''SELECT * FROM task_templateS''')
    for column in data.description:
        cols.append(column[0])
    conncol.commit()
    conncol.close()
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM task_templates').fetchall()
    conn.close()
    salida = []

    for dic in result:
        pre_dict = {}
        for col in cols:
            pre_dict[col]=dic[col]
        salida.append(pre_dict)
    for sal in salida:
        sal['capacities'] = json.loads(sal['capacities'])
    salida2 =[]    
    for sal in salida:
        if 'acc' in sal['capacities']:
            salida2.append(sal)
        if 'temp' in sal['capacities'] and sal['site']=='any':
            for sensor in sensors:
                pre_dict = {}
                pre_dict['name1'] = sal['name']
                pre_dict['name2'] = sensor['alias']
                pre_dict['sensor_id'] = sensor['id']
                for key,value in sal.items():
                    if key != 'name':
                        pre_dict[key] = value
                salida2.append(pre_dict)
    return salida2

# get part data
def get_part(id_part):
    conn = get_db_connection()
    part = conn.execute('SELECT * FROM parts WHERE id=?',(id_part,)).fetchone()
    conn.close()
    return part

# get task data as dict
def get_task_dict(id_task):
    cols = []
    conncol = sqlite3.connect('database.db')
    cursor = conncol.cursor()
    cadena = 'SELECT * FROM tasks WHERE id='+str(id_task)
    data = cursor.execute(cadena)
    for col in data.description:
        cols.append(col[0])
    conncol.commit()
    conncol.close()
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM tasks WHERE id=?',(id_task,)).fetchone()
    conn.close()
    salida = {}
    for col in cols:
        salida[col] = result[col]
    return salida

# get task data
def get_task(id_task):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id=?', (id_task,)).fetchone()
    conn.close()
    return task

# get task template data
def get_task_template(id_template):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM task_templates WHERE id=?', (id_template,)).fetchone()
    conn.close()
    return task

# get machine scope tasks
def get_machine_scope_task(id_machine):
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE id_machine=?', (id_machine,)).fetchall()
    for task in tasks:
        print (task['name'])
    return tasks

# get all parts templates by now
def get_parts_templates():
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM parts_templates').fetchall()
    conn.close()
    return result
# get all parts template in a dict
def get_parts_templates_dict():
    cols = []
    conncol = sqlite3.connect('database.db')
    cursor = conncol.cursor()
    data=cursor.execute('''SELECT * FROM parts_templateS''')
    for column in data.description:
        cols.append(column[0])
    conncol.commit()
    conncol.close()
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM parts_templates').fetchall()
    conn.close()
    salida = [] 
    for dic in result:
        pre_dict = {}
        for col in cols:
            pre_dict[col]=dic[col]
        salida.append(pre_dict)
    return salida

# get all machines asociated to a parts in a dict
def get_machine_parts_dict(id_machine):
    cols = []
    conncol = sqlite3.connect('database.db')
    cursor = conncol.cursor()
    data=cursor.execute('''SELECT * FROM parts WHERE id_machine=? ORDER BY ordinal ASC''',(id_machine,))
    for column in data.description:
        cols.append(column[0])
    conncol.commit()
    conncol.close()
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM parts WHERE id_machine=? ORDER BY ordinal ASC',(id_machine,)).fetchall()
    conn.close()
    salida = []
    for dic in result:
        pre_dict = {}
        for col in cols:
            pre_dict[col]=dic[col]
        salida.append(pre_dict)
    return salida

# get machine parts
def get_machine_parts(id_machine):
    conn = get_db_connection()
    m_parts = conn.execute('SELECT * FROM parts WHERE id_machine=? ORDER BY ordinal ASC',(id_machine,)).fetchall()
    conn.close()
    return m_parts

# get part template data from avatar 
def get_part_temp_by_avatar(avatar):
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM parts_templates WHERE avatar=?', (avatar,)).fetchone()
    conn.close()
    return result

# get part template data from id 
def get_part_temp_by_id(id):
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM parts_templates WHERE id=?', (id,)).fetchone()
    conn.close()
    return result

# Create a new machine from basic data entry 
def create_new_machine(datos):
    conn = get_db_connection()
    result = conn.execute('INSERT INTO machines(name,id_process,id_maintenance,users,kw_nom,rpm_nom,avatarf,brand,model,m_serial,i_serial,i_nom,v_nom,n_phases,n_poles,f_nom,nema_class,ip_grade,housing,description,a_status) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (datos['name'],datos['id_process'],datos['id_maintenance'],datos['users'],float(datos['kw_nom']),float(datos['rpm_nom']),datos['avatarf'],datos['brand'],datos['model'],datos['m_serial'],datos['i_serial'],float(datos['i_nom']),float(datos['v_nom']),datos['n_phases'],datos['n_poles'],datos['f_nom'],datos['nema_class'],datos['ip_grade'],datos['housing'],datos['description'],6)
             )
    print(result)
    conn.commit()
    machine = conn.execute('SELECT * FROM machines WHERE name=?',(datos['name'],)).fetchone()
    conn.close()
    dir2created = 'machine_' + str(machine['id'])
    parent = os.path.join(app.root_path,'static/data', dir2created)
    #print(parent)
    mode = 0o777
    os.mkdir(parent, mode)
    os.mkdir(parent+'/avatars/', mode)
    os.mkdir(parent+'/pictures/', mode)
    file = parent + '/journal_' + str(machine['id']) + '.txt'
    f = open(file,"a")
    f.write(str(dt.datetime.now())+"-> Maquina con nombre: "+machine['name']+" ha si creada. Asocida de al proceso " + str(machine['id_process']) + ".")
    f.write("\n")
    f.write(str(dt.datetime.now())+"-> Potencia: "+str(machine['kw_nom'])+" kW. Velocidad de Giro:" + str(machine['rpm_nom']) + " RPM. Avatar: "+ machine['avatarf'] + ".")
    f.write("\n")
    if datos['journal'] != "":
            f.write(str(dt.datetime.now())+"-> "+ datos['journal'])
            f.write("\n")
    f.close()
    update_table_register(('machines',str(machine['id'])),{"journal" : "journal_" + str(machine['id']) + ".txt" })
    source = os.path.join(app.root_path,'static/images/avatars/machines/default',machine['avatarf'])
    dest = os.path.join(app.root_path,'static/data',dir2created,'avatars',machine['avatarf'])
    shutil.copy(source,dest)
    return machine

# Create a new part asociated to a machine wich is been edited
def create_new_part(datos):
    conn = get_db_connection()
    templ = conn.execute('SELECT * FROM parts_templates WHERE avatar=?', (datos['avatarp'],)).fetchone()
    result = conn.execute('INSERT INTO parts(name,id_machine,id_maintenance,type,users,template,c_task,a_status,avatar,ordinal,description,s_fields) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
             (datos['name'],datos['machine_id'],1,'normal','local',templ['id'],8,6,datos['avatarp'],datos['ordinal'],templ['description'],templ['s_fields'])
    )
    conn.commit()
    conn.close()
    source = 'static/images/avatars/parts/default/' + datos['avatarp']
    dest = 'static/images/avatars/parts/local/' + datos['avatarp']
    shutil.copy(source,dest)
    return 0

def create_new_part2(datos):
    conn = get_db_connection()
    templ = conn.execute('SELECT * FROM parts_templates WHERE id=?', (datos['template_id'],)).fetchone()
    print(templ['id'])
    result = conn.execute('INSERT INTO parts(name,id_machine,id_maintenance,type,users,template,c_task,a_status,avatar,ordinal,description,s_fields) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
             (datos['namep'],datos['machine_idp'],1,'normal','admin',templ['id'],8,6,templ['avatar'],datos['ordinal'],templ['description'],templ['s_fields'])
    )
    conn.commit()
    conn.close()
    source = 'static/images/avatars/parts/default/' + templ['avatar']
    dest = 'static/data/machine_'+ str(datos['machine_idp']) + '/avatars/' + templ['avatar']
    shutil.copy(source,dest)
    file = 'static/data/machine_'+ str(datos['machine_idp']) +'/journal_' + str(datos['machine_idp']) + '.txt'
    f = open(file,"a")
    f.write(str(dt.datetime.now())+"-> Se ha agregado parte : "+ datos['namep']+".")
    f.write("\n")
    f.close()
    update_table_register(('machines',str(datos['machine_idp'])),{"a_status " : 7 })
    return 0

# Create a new part template
def create_new_part_template(datos):
    conn = get_db_connection()
    cats = []
    if datos['basic'] == True:
        cats.append('basic')
    if datos['movil'] == True:
        cats.append('movil')
    if datos['fixed'] == True:
        cats.append('fixed')
    todb = "{'cats':"+str(cats)+"}"
    result = conn.execute("INSERT INTO parts_templates (name,type,users,categories,brand,model,m_serial,description,s_fields,avatar) VALUES (?,?,?,?,?,?,?,?,?,?)",
    (datos['name'],datos['type'],datos['users'],todb,datos['brand'],datos['model'],datos['m_serial'],datos['description'],datos['s_fields'],datos['name']+".png")
    )
    part_t = conn.execute('SELECT * FROM parts_templates WHERE name=?',(datos['name'],)).fetchone()
    conn.commit()
    conn.close()
    return part_t

def get_sensor_template(name):
    conn = get_db_connection()
    result = conn.execute("SELECT * FROM sensor_templates WHERE model=?",(name,)).fetchone()
    conn.close()
    return result

def get_sensors():
    conn = get_db_connection()
    result = conn.execute("SELECT * FROM sensors").fetchall()
    conn.close()
    return result

def get_sensors_dict():
    cols = []
    conncol = sqlite3.connect('database.db')
    cursor = conncol.cursor()
    data=cursor.execute('''SELECT * FROM sensors''')
    for column in data.description:
        cols.append(column[0])
    conncol.commit()
    conncol.close()
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM sensors').fetchall()
    conn.close()
    salida = [] 
    for dic in result:
        pre_dict = {}
        for col in cols:
            pre_dict[col]=dic[col]
        salida.append(pre_dict)
    return salida

def get_sensors_machine(id_machine):
    parts = get_machine_parts(id_machine)
    sensors = get_sensors_dict()
    list = []
    for part in parts:
        for sensor in sensors:
            if sensor['part_id'] == part['id']:
                list.append(sensor)
    for li in list:
        li['capacities'] = json.loads(li['capacities'])
    # falta la depuracion de las capacidades cuando se hagan mas sensores. 
    capa = []
    for li in list:
        if 'temp' in li['capacities']:
            capa.append('loca')
    #print(capa)
    return list, capa

def pair_sensor2part(datos, id_m):
    conn = get_db_connection()
    result = conn.execute("INSERT INTO sensors (part_id, model, alias, mac, capacities, picture, avatar, description, s_fields) VALUES (?,?,?,?,?,?,?,?,?)",
    (datos['part_id'],datos['model'],datos['alias'],datos['mac2e'],datos['capacities'],datos['picture'],datos['avatars'],datos['description'], datos['s_fields'])
    )
    parte = conn.execute("SELECT name FROM parts WHERE id=?", (datos['part_id'],)).fetchone()
    conn.commit()
    conn.close()
    source = os.path.join(app.root_path,'static/images/avatars/sensors',datos['avatars'])
    text = 'machine_'+str(id_m)
    dest = os.path.join(app.root_path,'static/data',text,'avatars',datos['avatars'] )
    shutil.copy(source,dest)
    file = 'static/data/machine_'+ str(id_m) +'/journal_' + str(id_m) + '.txt'
    f = open(file,"a")
    f.write(str(dt.datetime.now())+"-> Se ha agregado el sensor : "+ datos['alias']+" a parte "+ parte['name'] +".")
    f.write("\n")
    f.close()
    return result

def generate_tasks(pack):
    tasks = []
    for key,value in pack.items():
        task2send = {}
        if pack[key]['tipo'] == 'onsite':
# para el tipo 'onsite' se deben generar una cada que itere este ciclo
            for x in pack[key]['sel']:
                task2send = {}  
                task2send['site'] = pack[key]['tipo']
                task2send['name'] = key
                task2send['id_machine'] = pack[key]['machine']
                end_t = x[1:].find('_')+1
                task2send['id_template'] = x[1:end_t]
                end_p = x[end_t+1:].find('_')+end_t+1
                task2send['id_part'] = x[end_t+1:end_p]
                task2send['id_sensor'] = x[end_p+1:]
                task2send['d_start'] = dt.date.isoformat(dt.date.today())
                task2send['d_end'] = '2050-09-18'
                task_temp = get_task_template(int(task2send['id_template']))
                task2send['units'] = task_temp['units']
                task2send['d_allow'] = task_temp['d_allow']
                task2send['t_interval'] = task_temp['t_interval']
                task2send['hf_start']='06:15:00'
                task2send['hf_end']='18:45:00'
                task2send['s_val'] = task_temp['s_val']
                task2send['g_val'] = task_temp['g_val']
                task2send['y_val'] = task_temp['y_val']
                task2send['o_val'] = task_temp['o_val']
                task2send['r_val'] = task_temp['r_val']
                task2send['s_fields'] = task_temp['s_fields']
                task2send['description'] =task_temp['description']
                task2send['help'] =task_temp['help']
                task2send['avatar'] =task_temp['avatar']
                tasks.append(task2send)
        elif pack[key]['tipo'] == 'any':
            task2send = {}
            task2send['site'] = pack[key]['tipo']
            task2send['name'] = key
            task2send['id_machine'] = pack[key]['machine']
            end_t = pack[key]['sel'][0][1:].find('_')+1
            task2send['id_template'] = pack[key]['sel'][0][1:end_t]
            end_p = pack[key]['sel'][0][end_t+1:].find('_')+end_t+1
            task2send['id_part'] = pack[key]['sel'][0][end_t+1:end_p]
            end_s = pack[key]['sel'][0][end_p+1:].find('_')+end_p+1
            #task2send['id_sensor'] = pack[key]['sel'][0][end_p+1:end_s]
            task2send['id_sensor'] = pack[key]['sel'][0][end_s+1:]
            task2send['d_start'] = dt.date.isoformat(dt.date.today())
            task2send['d_end'] = '2050-09-18'
            task_temp = get_task_template(int(task2send['id_template']))
            task2send['units'] = task_temp['units']
            task2send['d_allow'] = task_temp['d_allow']
            task2send['t_interval'] = task_temp['t_interval']
            task2send['hf_start']='06:15:00'
            task2send['hf_end']='18:45:00'
            task2send['s_val'] = task_temp['s_val']
            task2send['g_val'] = task_temp['g_val']
            task2send['y_val'] = task_temp['y_val']
            task2send['o_val'] = task_temp['o_val']
            task2send['r_val'] = task_temp['r_val']
            task2send['s_fields'] = task_temp['s_fields']
            task2send['description'] =task_temp['description']
            task2send['help'] =task_temp['help']
            task2send['avatar'] =task_temp['avatar']
            tasks.append(task2send)
    # Aqui vamos a coloar el ingreso de las tareas a las bases de datos
    conn = get_db_connection()
    for task in tasks:
        conn.execute("INSERT INTO tasks (name,id_sensor,id_machine,id_part,id_maintenance,id_template,site,c_task,c_measure,units,d_start,d_end,d_allow,t_interval,hf_start,hf_end,s_val,g_val,y_val,o_val,r_val,s_fields,description,avatar,help) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (task['name'],task['id_sensor'],task['id_machine'],task['id_part'],1,task['id_template'],task['site'],1,100,task['units'],task['d_start'],task['d_end'],124,task['t_interval'],'06:15:00','18:45:00',task['s_val'],task['g_val'],task['y_val'],task['o_val'],task['r_val'],task['s_fields'],task['description'],task['avatar'],task['help'])
           )
        conn.commit()
    conn.close()
    return tasks

# Updates ---- update a part 
# update a table tegister with as many cols as need to be affected
# pointer is a tuple by now : table and id register to be afected
# data is a dicionary with keys as a column to be afected
def update_table_register(pointer,data):
    conn = get_db_connection()
    last_it = 0
    text = 'UPDATE '+ pointer[0]+' SET '
    for key, value in data.items():
        last_it = last_it + 1
        if last_it < len(data):
            text += key +' = "'+ str(value) + '", '
        else:
            text += key +' = "'+ str(value)+ '"'
    text +=' WHERE id=' + str(pointer[1])
    print(text)
    conn.execute(text)
    conn.commit()
    conn.close()
    return text

# write in Jornal
def journal_writer(file, data):
    f = open(file,"a")
    f.write(str(dt.datetime.now())+"-> "+ data['pack']+"-")
    f.write("\n")
    f.close()
    print(data)
    return 0