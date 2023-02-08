import sqlite3
import datetime as dt
import shutil

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

# get machine parts
def get_machine_parts(id_machine):
    conn = get_db_connection()
    m_parts = conn.execute('SELECT * FROM parts WHERE id_machine=? ORDER BY ordinal ASC',(id_machine,)).fetchall()
    conn.close()
    return m_parts

# get part data
def get_part(id_part):
    conn = get_db_connection()
    part = conn.execute('SELECT * FROM parts WHERE id=?',(id_part,)).fetchone()
    conn.close()
    return part

# get task data
def get_task(id_task):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id=?', (id_task,)).fetchone()
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
    result = conn.execute('INSERT INTO machines(name,id_process,id_maintenance,users,kw_nom,rpm_nom,avatarf,a_status) VALUES(?,?,?,?,?,?,?,?)',
             (datos['name'],1,1,'local',float(datos['kw_nom']),float(datos['rpm_nom']),datos['avatarf'],6)
             )
    conn.commit()
    machine = conn.execute('SELECT * FROM machines WHERE name=?',(datos['name'],)).fetchone()
    conn.close()
    file = "journal/machines/machine_"+str(machine['id'])
    f = open(file,"a")
    f.write(str(dt.datetime.now())+"-> Maquina con nombre: "+machine['name']+" ha si creada. Asocida de al proceso " + str(machine['id_process']) + ".")
    f.write("\n")
    f.write(str(dt.datetime.now())+"-> Potencia: "+str(machine['kw_nom'])+" kW. Velocidad de Giro:" + str(machine['rpm_nom']) + " RPM. Avatar: "+ machine['avatarf'] + ".")
    f.write("\n")
    f.close()
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

# Updates ---- update a part 
# update a table tegister with as many clos as need to be affected
# pointer is a tuple by now : table and id register to be afected
# data is a dicionary with keys as a column to be afected
def update_table_register(pointer,data):
    conn = get_db_connection()
    last_it = 0
    text = 'UPDATE '+ pointer[0]+' SET '
    for key,value in data.items():
        last_it = last_it + 1
        if last_it < len(data):
            text += key +' = '+ str(value) + ','
        else:
            text += key +' = '+ str(value)
    text +=' WHERE id=' + str(pointer[1])
    conn.execute(text)
    conn.commit()
    conn.close()
    return text