# GENERADOR DE FUNCIONES PARA EL SCHEDULE
import datetime as dt

def gen_week_block(task):
# Comencemos por mostrar el estado actual semana
    #task = get_task(id_task)
    now = dt.datetime.today().replace(second=0, microsecond=0)
# Obtenemos el inicio y final de la semana desde la fecha de sistema
    s_week = now - dt.timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute)
    e_week = s_week + dt.timedelta(days=6, hours=23, minutes=59, seconds=59)
# Generemos el primer bloque de horas que va desde start_week hasta ese domingo
    s_iso = str(s_week.year)+'-'+s_week.strftime('%m')+'-'+s_week.strftime('%d')+' '+task['hf_start']
    e_iso = str(e_week.year)+'-'+e_week.strftime('%m')+'-'+e_week.strftime('%d')+' '+task['hf_end']
    first_take = dt.datetime.fromisoformat(s_iso)
    last_take = dt.datetime.fromisoformat(e_iso)
# Generemos el numero de rows
    n_row = last_take.hour - first_take.hour + 1
# Generemos entonces la primera row (cabecera)
    block = []
    block.append(['Hora',0,1,2,3,4,5,6])
    for i in range(1,8):
        block[0][i]= (s_week + dt.timedelta(days=i-1)).strftime("%A, %d")
# Se debe generar una row para el primer espacio muerto de tiempo
    d_time1 = s_week.strftime('%H:%M')+' - '+(first_take - dt.timedelta(minutes=first_take.minute)).strftime('%H:%M')
    block.append([d_time1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
# Generemos primero la primera colunma y el numero de rows
    for i in range(n_row):
        time = (first_take + dt.timedelta(hours=i, minutes=-first_take.minute)).strftime('%H:%M - ')+(first_take+ dt.timedelta(hours=i)).strftime('%H:59')
        block.append([time,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])
# Aqui tenemos un ciclo que recorre todas las posiciones, filter allow days
# entonces creemos los  rows validas una lista
    interval = task['t_interval'] # este valor viene desde la base de datos en minutos
    win = ((last_take.hour+1) - first_take.hour)*60 - (first_take.minute +( 60 - last_take.minute))
    a_win = ((last_take.hour+1) - first_take.hour)*60
# colocar un if para cunado el gap es 0
    s_gap = first_take.minute / 15
    r_allow = []
    p = interval / 15
    for i in range(n_row*4):
        if  i < s_gap:
            r_allow.append(0)
        elif i > (win / 15):
            r_allow.append(0)
        elif (i%p == 0):
            r_allow.append(1)
        elif i == s_gap or i == (win / 15):
            r_allow.append(1)
        else:
            r_allow.append(0)

# Recorrido por todas los slots
    for j in range(2,n_row+2):
        ini = (j-2)*4
        end = ini+4
        t_allow = r_allow[ini:end]
#        print (str(ini)+'--'+str(end))
#        print (r_allow[ini:end])

        for i in range(28):
            if i+1 < 5 :
                if (task['d_allow'] & 64 == 64) and (t_allow[i] & 1):
                    block[j][i+1]=1
                else:
                    block[j][i+1]=0
            elif i+1 < 9 :
                if (task['d_allow'] & 32 == 32) and (t_allow[i-4] & 1):
                    block[j][i+1]=1
                else:
                    block[j][i+1]=0
            elif i+1 < 13 :
                if (task['d_allow'] & 16 == 16) and (t_allow[i-8] & 1):
                    block[j][i+1]=1
                else:
                    block[j][i+1]=0
            elif i+1 < 17 :
                if (task['d_allow'] & 8 == 8) and (t_allow[i-12] & 1):
                    block[j][i+1]=1
                else:
                    block[j][i+1]=0
            elif i+1 < 21 :
                if (task['d_allow'] & 4 == 4) and (t_allow[i-16] & 1):
                    block[j][i+1]=1
                else:
                    block[j][i+1]=0
            elif i+1 < 25 :
                if (task['d_allow'] & 2 == 2) and (t_allow[i-20] & 1):
                    block[j][i+1]=1
                else:
                    block[j][i+1]=0
            elif i+1 < 29 :
                if (task['d_allow'] & 1 == 1) and (t_allow[i-24] & 1):
                    block[j][i+1]=1
                else:
                    block[j][i+1]=0
            else:
                block[j][i+1]=0

# Generemos el tiempo muerto al final del dia
    d_time2 = (first_take + dt.timedelta(hours=n_row, minutes=-first_take.minute)).strftime('%H:%M')+' - '+(s_week + dt.timedelta(hours=23, minutes=59)).strftime('%H:%M')
    block.append([d_time2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

# Generemos la particion hora minuto del intervalo de tomas
    h_interval = int(interval / 60)
    m_interval = (interval / 15) % 4
    #m_interval = (interval) % 4
# Generemos una ultima entrada a la lista bock con datos necsarios
    block.append({'n_rows':len(block),'r_allow':r_allow, 'win': win,'n_meas':win/interval, 'a_win':a_win,'s_week':s_week.strftime('%d - %m- %Y'),
                  'e_week':e_week.strftime('%d - %m- %Y'),'week':now.strftime('%W'),'h_interval':h_interval,'m_interval':m_interval*15 })
    print (first_take)
    for x in range (n_row+3):
        print (block[x])
    return block
#print (block[1])
#print (block[2])
