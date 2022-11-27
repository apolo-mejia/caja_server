import sqlite3

connection = sqlite3.connect('database.db')

with open('data_init/schema_part.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO parts (name, id_machine, id_maintenance, type, users, template, c_task, brand, model, m_serial, i_serial, a_status, picture, avatar, description, s_fields) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    ('Motor AC', 1, 2, 'Motor AC(completo)','default', 1, 1000000, 'c', 'c', 'c', 'c', 1, 'src', 'motor_fl.png', 'Parte de Prueba','{"base":["rigida","na"],"f_variator":["escalar","na"]}')
    )

connection.commit()
connection.close()
