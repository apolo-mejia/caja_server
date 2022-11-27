import sqlite3

connection = sqlite3.connect('database.db')

with open('data_init/schema_task.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO tasks (name,id_machine,id_part,id_maintenance,id_template,c_task,c_measure,units,d_start,d_end,d_allow,t_interval,hf_start,hf_end,s_val,g_val,y_val,o_val,r_val,s_fields,description,avatar,help) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ('Norma 10816-Velocidad',1,1,2,1,1,100,'mm/s','2022-11-11','2030-11-11',124,60,'06:15:00','18:45:00',0.03,1.4,2.8,4.5,5,'{"Group":["2","Medium-size machines"],"Rated-Power":["15","300"], "base":"rigid","type":"Motores, 160mm < H < 300mm"}','Norma ISO 10816 - Evaluacion de vibraciones en maquinas con medidas tomadas en partes no rotativas. \n Parte 3: Maquinas Industriales con Potencia nominal superior a 15kW y velocidades nominales entre 120 y 15000 RPM,"medidas in situ."','ISO101816_vel_g2_rigid.png','La Norma ISO 10816 Mechanical Vibration - Measurement and evaluation of machine vibration')
           )
connection.commit()
connection.close()
