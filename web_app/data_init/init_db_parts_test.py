import sqlite3

connection = sqlite3.connect('database.db')

with open('data_init/schema_part.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO parts (name, id_machine, ordinal, id_maintenance, type, users, template, c_task, brand, model, m_serial, i_serial, a_status, picture, avatar, description, s_fields) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    ('Motor AC',1,1,2,'Motor AC(completo)','default',1,1,'c','c','c','c',1,'src','motor.png','Motor de Prueba','{"base":["rigida","AD"],"f_variator":["escalar","AD"],"Numero de apoyos":["1","AD"]}')
    )
cur.execute("INSERT INTO parts (name, id_machine, ordinal, id_maintenance, type, users, template, c_task, brand, model, m_serial, i_serial, a_status, picture, avatar, description, s_fields) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    ('Acople/Brida',1,2,2,'Bida Ventada','default',1,1,'c','c','c','c',4,'src','brida.png','Brida de Prueba','{"tipo":["pinonada","AD"],"acople":["plastico","AD"]}')
    )
cur.execute("INSERT INTO parts (name, id_machine, ordinal, id_maintenance, type, users, template, c_task, brand, model, m_serial, i_serial, a_status, picture, avatar, description, s_fields) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    ('Rodamiento',1,3,2,'Rodamiento Izquierdo','default',1,1,'c','c','c','c',1, 'src','rodamiento.png','Rodamiento Junto al la brida','{"marca":["FAG","GER"],"chumacera":["sencilla","AD"]}')
    )
cur.execute("INSERT INTO parts (name, id_machine, ordinal, id_maintenance, type, users, template, c_task, brand, model, m_serial, i_serial, a_status, picture, avatar, description, s_fields) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    ('Eje',1,4,2,'Eje Diametro 12.5mm','default',1,1,'c','c','c','c',2,'src','eje.png','Brida de Prueba','{"largo":["1","m"],"material":["Fe","AD"]}')
    )
cur.execute("INSERT INTO parts (name, id_machine, ordinal, id_maintenance, type, users, template, c_task, brand, model, m_serial, i_serial, a_status, picture, avatar, description, s_fields) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    ('Rodamiento',1,5,2,'Rodamiento Izquierdo','default',1,1,'c','c','c','c',2,'src','rodamiento.png','Rodamiento Junto al la brida','{"marca":["FAG","GER"],"chumacera":["sencilla","AD"]}')
    )
cur.execute("INSERT INTO parts (name, id_machine, ordinal, id_maintenance, type, users, template, c_task, brand, model, m_serial, i_serial, a_status, picture, avatar, description, s_fields) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    ('Ventilador',1,6,2,'Ventilador','default',1,1,'c','c','c','c',3,'src','ventilador.png','Ventilador de Prueba','{"tipo":["aereo","AD"],"material":["plastico","Poliuretileno"]}')
    )


connection.commit()
connection.close()
