import sqlite3
import datetime as dt

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
    m_parts = conn.execute('SELECT * FROM parts WHERE id_machine=?',(id_machine,)).fetchall()
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
