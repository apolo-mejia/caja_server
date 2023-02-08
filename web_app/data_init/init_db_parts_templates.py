import sqlite3

connection = sqlite3.connect('database.db')

with open('data_init/schema_part_template.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

#cur.execute("INSERT INTO parts_templates (name, type, users, avatar, description) VALUES (?,?,?,?,?)",
#    ('Motor_AC', 'global', 'local', 'motor.png', 'Motor completo, use esta parte para motores AC en los cuales solo va instalar un sensor.')
#    )
cur.execute("INSERT INTO parts_templates (name,type,users,categories,brand,model,m_serial,avatar,s_fields,description) VALUES (?,?,?,?,?,?,?,?,?,?)",
   ('Brida', 'global', 'local','["basic","movil"]','Cualquiera','Cualquiera','Cualquiera', 'brida.png','{"tipo":["pinonada","AD"],"acople":["plastico","AD"]}','Brida de acople: use esta parte a la salida del motor con un eje o cuando o dos ejes se acoplen.')
   )
#cur.execute("INSERT INTO parts_templates (name, type, users, avatar, description) VALUES (?,?,?,?,?)",
#   ('Apoyo', 'global', 'local', 'apoyo.png', 'Apoyo para rodamiento: use esta parte para chumaceras o soportes que alojan rodamientos.')
#   )
#cur.execute("INSERT INTO parts_templates (name, type, users, avatar, description) VALUES (?,?,?,?,?)",
#   ('Eje', 'global', 'local', 'eje.png', 'Eje: Use esta parte para respresentar ejes o masas rotativas.')
#   )
#cur.execute("INSERT INTO parts_templates (name, type, users, avatar, description) VALUES (?,?,?,?,?)",
#   ('Ventilador', 'global', 'local', 'ventilador.png', 'Ventilador de aspas: use esta parte para represntar ventiladores de aspas.')
#   )

connection.commit()
connection.close()
