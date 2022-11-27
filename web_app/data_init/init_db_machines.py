import sqlite3

connection = sqlite3.connect('database.db')

with open('data_init/schema_machine.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
   "INSERT INTO machines (name, id_process, id_maintenance, users, brand, model, m_serial, i_serial, kw_nom, rpm_nom, i_nom, v_nom, n_phases, n_poles, f_nom, nema_class, ip_class, housing, a_status, picture, avatar, description) VALUES ('Maquina1', 1, 1, 'default', 'c', 'c', 'c', 'c', 1, 1800, 1, 220, 3, 1, 60, 2, 11, 1, 1, 'src', 'src', 'Maquina de Prueba')"
           )

connection.commit()
connection.close()
