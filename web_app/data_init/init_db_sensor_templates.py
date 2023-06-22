import sqlite3

connection = sqlite3.connect('database.db')

with open('data_init/schema_sensor_template.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO sensor_templates (model, capacities, picture, avatar, description, s_fields) VALUES (?,?,?,?,?,?)",
   ('Marcial', '["temp", "acc", "mag", "gir"]', 'no-picture.png','motion-sensor.png','Sensor de vibraciones','{"tipo":"genérico"}')
)

connection.commit()
connection.close()
