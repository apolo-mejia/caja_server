import sqlite3

connection = sqlite3.connect('database.db')

with open('data_init/schema_sensor.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

#cur.execute("INSERT INTO sensors (part_id, model, alias, mac, capacities, picture, avatar, description, s_fields) VALUES (?,?,?,?,?,?,?,?,?)",
#   (1,'Marcial000', 'Sensor Test', '00:00:00:00:00:00','["temp", "acc", "mag", "gir"]','no-picture.png','motion-sensor.png','Sensor de prueba no exite!!','{"tipo":"genérico"}')
#)

connection.commit()
connection.close()
