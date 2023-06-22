import sqlite3

connection = sqlite3.connect('database.db')

with open('data_init/schema_task_template.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO task_templates (name,capacities,units,site,d_allow,t_interval,s_val,g_val,y_val,o_val,r_val,s_fields,description,avatar,help) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ('Norma 10816-Velocidad','["acc"]','mm/s','onsite',124,240,0.03,1.4,2.8,4.5,5,'{"Group":["2","Medium-size machines"],"Rated-Power":["15","300"], "base":"rigid","type":"Motores, 160mm < H < 300mm"}','Norma ISO 10816 - Evaluacion de vibraciones en maquinas con medidas tomadas en partes no rotativas. \n Parte 3: Maquinas Industriales con Potencia nominal superior a 15kW y velocidades nominales entre 120 y 15000 RPM,"medidas in situ."','ISO101816_vel_g2_rigid.png','La Norma ISO 10816 Mechanical Vibration - Measurement and evaluation of machine vibration')
           )

cur.execute("INSERT INTO task_templates (name,capacities,units,site,d_allow,t_interval,s_val,g_val,y_val,o_val,r_val,s_fields,description,avatar,help) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ('temperatura','["temp"]','°C','any',124,240,0.03,50,80,100,120,'{"key":"value"}','Temperatura en centigrados','temperature.png','Tempteratura del sensor')
           )
connection.commit()
connection.close()
