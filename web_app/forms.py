from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField, SelectField, TextAreaField, BooleanField, FileField, TimeField
from wtforms.validators import DataRequired, MacAddress
from flask_wtf.file import FileField

# Aqui vamos con las listas
class mano_list(FlaskForm):
    soportes = SelectField('Marcas de Soportes', choices=[('soportes','Llevar lista'),('fag','FAG'),('ina','INA'),('skf','SKF'),
        ('snr','SNR'),('ntn','NTN'),('koy','KOYO'),('nsk','NSK'),('smt','SEALMASTER'),('lbt','LINK BELT'),('oth','Other..')])
    motores = SelectField('Marcas de Motores', choices=[('motores','Levar lista'),('weg','WEG'),('sms','SIEMENS'),('wth','Westinghouse')])
    rodamientos = SelectField('Marcas de Rodamientos', choices=[('rodamientos','Llevar lista'),('fag','FAG'),('ina','INA'),('skf','SKF'),
        ('snr','SNR'),('ntn','NTN'),('koy','KOYO'),('nsk','NSK'),('smt','SEALMASTER'),('lbt','LINK BELT'),('oth','Other..')])
class dim_list(FlaskForm):
    dimensiones = SelectField('Dimensión', choices=[('ad','Adimencional'), ('power','Potencia'),('volts','Voltaje'),
        ('current','Corriente'),('angle','Ángulo'),('force','Fuerza'),('torque','Torque'),('imon','Momento de Inercia'),
        ('percent','Porcentaje'),('length','Distancia'),('speed','Velocidad'),('acc','Aceleración'),('mass','Masa'),
        ('freq','Frecuencia'),('time','Tiempo')])
    unidades = SelectField('Únidades', choices=[('none','Ninguna'),('kV','Kilo-Vatios [kV]'),('N','Newton [N]'),('m','Metros [m]'),
        ('mps','MetrosxSegundo [m/s]'),('rpm','Revoluciones Por Minuto'),('mpss','Metros / Segundos2  [m/s²]'),('kg','Kilogramo'),('Hz','Hertz'),
        ('V','Voltage'),('A','Amperios'),('deg','Grados Decimales'),('percent','Porcentaje [%]'),('N.m','Newton x metro [N.m]'),
        ('Kg.m.m','Kilogramo x metro² [k.m²]')])
# Aqui donde se onfigura la caja
class ssid_form(FlaskForm):
    ssid = StringField('SSID',validators=[DataRequired()])
    pass_word = StringField('PassKey', validators=[DataRequired()])
    submit = SubmitField('Registrar...')

class erase_network(FlaskForm):
    ssid = StringField('SSID', validators=[DataRequired()])
    id_net = StringField('Net_id', validators=[DataRequired()])
    submit = SubmitField('Olviar Red...')

# Clase para las pruebas de toma con el sensor
class start_measure(FlaskForm):
    sensor_mac = StringField('MAC_sensor', validators=[DataRequired()])
    submit = SubmitField('Iniciar la toma')

# Creacion/Edicion de maquinas
class create_machine(FlaskForm):
    name = StringField('Nombre de la máquina', validators=[DataRequired('El campo: "Nombre de la máquina" es obligatorio para crear la máquina como entidad')])
    rpm_nom = DecimalField('Velocidad Giro [RPM]')
    kw_nom = DecimalField('Potencia nominal ', validators=[DataRequired('El campo: "Potencia Nominal" es obligatorio para crear la máquina como entidad')])
    id_process = SelectField('Proceso asociado', choices=[(0,"N/A")])
    id_maintenance = SelectField('Plan de Mantenimiento', choices=[(0,"N/A")])
    users = SelectField('Usuarios Autorizados', choices=[('admin','Administradores'),('sudo','Super Usuarios'),('oper','Operadores'),('repo','Repoteros')])
    brand = StringField('Marca')
    model = StringField('Modelo')
    m_serial = StringField('Serial de Fabrica')
    i_serial =StringField('Serial Interno')
    i_nom = DecimalField('Corriente Nominal')
    v_nom = DecimalField('Voltaje Nominal')
    n_phases = SelectField('Numero de fases',choices=[(1,"1"),(2,"2"),(3,"3")])
    n_poles = SelectField('Numero de polos', choices=[(0,"N/A"),(2,"2"),(4,"4"),(6,"6"),(8,"8")])
    f_nom = SelectField('Frecuencia', choices=[(1,"50/60"),(50,"50"),(60,"60")])
    nema_class = SelectField('Clase Nema', choices=[("1","1"),("2","2"),("3","3"),("3R","3R"),("3S","3S"),("3X","3X"),("3RX","3RX"),("3SX","3SX"),("4","4"),("4X","4X"),("5","5"),("6","6"),("6P","6P"),("7","7"),("8","8"),("9","9"),("10","10"),("11","11"),("12","12"),("12k","12K"),("13","13")])
    ip_grade = StringField('Grado IP')
    housing = StringField('Housing')
    avatarf = StringField('Avatar')
    picture = StringField('Foto')
    description = TextAreaField('Descripción de la máquina')
    journal = TextAreaField('Mensaje al crear en Journal')
    submit = SubmitField('Crear maquina...')

# Creation of parts templates
class create_part_template_f(FlaskForm):
    name = StringField('Nombre del template', validators=[DataRequired('Elnombre del template es obligatorio')])
    type = SelectField('Tipo del plantilla', choices=[('global','Global'),('unica','única')])
    users = SelectField('Usuarios autorizados', choices=[('local','Local'), ('sudo','Super Usuarios'), ('adm','administradores'),('oper','operadores')])
    basic = BooleanField('Básicas')
    movil = BooleanField('Móviles')
    fixed = BooleanField('Fijas') 
    # Optional reference values
    mano_list = SelectField('marcas', choices=[('no_marca','Sin marca'), ('mano_soporte','Marcas de Soporte'),
        ('mano_rodamiento', 'Marcas de Rodamiento'),('mano_motor','Marcas de Motores')])
    brand = StringField('Marca o Manofacturero')
    model = StringField('Modelo o Referencia')
    m_serial = StringField('Serial de Fábrica')
    # Description
#    picture = StringField('Foto por defecto del a parte'),
    description = TextAreaField('Descripción de la parte')
    # Specific fields
    s_fields = TextAreaField('Datos especificos de la parte')
    submit_p_t =SubmitField('Adicionar template...')

# Upload an  Part avatar 
class upload_part_avatar(FlaskForm):
    avatar_name = StringField('Nombre', validators=[DataRequired('El Avatar es necesario')])
    avatar_up = FileField('Avatar o ícono')
    submit_avatar = SubmitField('Cargar la imagen')
# create a JSON field
class create_s_field(FlaskForm):
    s_key = StringField('Key_word', validators=[DataRequired()])
    s_name = StringField('Nombre  campo', validators=[DataRequired()])
    s_dim = dim_list.dimensiones
    s_units = StringField('unidades')
    s_units2 = dim_list.unidades
    s_type = SelectField('Tipo dato', choices=[('int','Entero'),('float','Decimal'),('Texto','Texto'),('select','Selección'),('bolean','Boleano'),('mano_list','Lista Marcas')])
    s_value_def = StringField('Valor default')
    s_important = BooleanField('Importante!')
    s_description = StringField('Descripción')

# Creacion/ Edicion de partes desde la creacion de machine_ec
class create_part(FlaskForm):
    name = StringField('Nombre de parte', validators=[DataRequired('El campo: "Nombre de parte" es obligatorio para adicionar la parte a esta maquina.')])
    ordinal = SelectField('Ordinal', choices=[(99,'auto'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10')])
    avatarp = StringField('avatar', validators=[DataRequired('El campo avatar es obligatorio')])
    machine_id = IntegerField('id_maquina', validators=[DataRequired('El campo id_maquina es obligatorio')])
    submit = SubmitField('Adicionar parte...')

# Creacion/ Edicion de partes desde la creacion de machine_ec2
class create_part2(FlaskForm):
    namep = StringField('Nombre de parte', validators=[DataRequired('El campo: "Nombre de parte" es obligatorio para adicionar la parte a esta maquina.')])
    ordinal = SelectField('Ordinal', choices=[(99,'auto'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10')])
    template_id = IntegerField('avatar', validators=[DataRequired('El campo avatar es obligatorio')])
    machine_idp = IntegerField('id_maquina', validators=[DataRequired('El campo id_maquina es obligatorio')])
    submit = SubmitField('Adicionar parte...')

# Creación / Edición de los campos especificos, el JSON
class update_part_json(FlaskForm):
    part_id = IntegerField('id de la parte a editar', validators=[DataRequired('Es necesario qu parte editar')])
    json_pack = TextAreaField('json_part', validators=[DataRequired('El valor es necesario validación')])
    submit_json = SubmitField('Actualizar parte...')

# Create update field/fields of a table. work together with update_table_register query
class update_field_tablereg(FlaskForm):
    table = StringField('Tabla a ser afectada', validators = [DataRequired('Tabla es Necesario')])
    id = IntegerField('Id o posicion a ser afectada', validators =[DataRequired('La posición a afectar es necesaria')])
    submit = SubmitField('Finalizar')

# Matricular un sensor a una parte de una máquina
class enrroll_sensor(FlaskForm):
    mac2e = StringField('MAC del sensor')
    model = StringField('Nombre del sensor')
    capacities = StringField('Capacidades')
    alias = StringField('Nombre Interno')
    part_id = IntegerField('id de la parte a editar', validators=[DataRequired('Es necesario que parte editar')])
    avatars = StringField('avatar')
    picture = StringField('Foto')
    description = TextAreaField('Descripción')
    s_fields = TextAreaField('Campos especiales') 
    submit = SubmitField('Matricular Sensor')

# Hacer una broadCast para encontrar un sensor
class send_sensor_req(FlaskForm):
    mac_address = StringField('MAC a llamar', validators=[MacAddress('Eso no es una MAC')])
    requirement = SelectField('Requerimiento', choices=[('meas8','meas8 - algo debe hacer'),('meas9','meas9 - Hacer Broadcast'),('meas10','meas10 - Traer datos sensor')])
    extra_int = IntegerField('Campo Extra')
    submitqr = SubmitField('Solicitar...')

# Recibir una cadena JSON stringfy
class send_JSONpack(FlaskForm):
    pack = TextAreaField('Jsonpack', validators=[DataRequired('Es necesario el paquete')])
    submitpk = SubmitField('Enviar')

# Clase para subie archivos
class upload_file(FlaskForm):
    documento = FileField('Selecionar archivo')
    submitdoc = SubmitField('Cargar...')

# Clase que maneja los campos de las tasks
class task_data(FlaskForm):
    t_int_h = SelectField('horas', choices=[(0,"00h"),(1,"01h"),(2,"02h"),(3,"03h"),(4,"04h"),(5,"05h"),(6,"06h"),(7,"07h"),(8,"08h"),(9,"09h"),(10,"10h"),(11,"11h")])
    t_int_m = SelectField('minutos', choices=[(0,"00'"),(15,"15'"),(30,"30'"),(45,"45'")])
    monday = BooleanField('Lunes')
    tuesday = BooleanField('Martes')
    wednesday = BooleanField('Miercoles')
    thursday = BooleanField('Jueves')
    friday = BooleanField('Viernes')
    saturday = BooleanField('Sabado')
    sunday = BooleanField('Domingo')
    d_allow = IntegerField('d_allow')
    hf_start_h = SelectField('Horas', choices=[(0,"00h"),(1,"01h"),(2,"02h"),(3,"03h"),(4,"04h"),(5,"05h"),(6,"06h"),(7,"07h"),(8,"08h"),(9,"09h"),(10,"10h"),(11,"11h"),(12,"12h"),(13,"13h"),(14,"14h"),(15,"15h"),(16,"16h"),(17,"17h"),(18,"18h"),(19,"19h"),(20,"20h"),(21,"21h"),(22,"22h"),(23,"23h")])
    hf_start_m = SelectField('minutos', choices=[(0,"00'"),(15,"15'"),(30,"30'"),(45,"45'")])
    hf_end_h = SelectField('Horas', choices=[(0,"00h"),(1,"01h"),(2,"02h"),(3,"03h"),(4,"04h"),(5,"05h"),(6,"06h"),(7,"07h"),(8,"08h"),(9,"09h"),(10,"10h"),(11,"11h"),(12,"12h"),(13,"13h"),(14,"14h"),(15,"15h"),(16,"16h"),(17,"17h"),(18,"18h"),(19,"19h"),(20,"20h"),(21,"21h"),(22,"22h"),(23,"23h")])
    hf_end_m = SelectField('minutos', choices=[(0,"00'"),(15,"15'"),(30,"30'"),(45,"45'")])
    submitint = SubmitField('Cargar Intervalo...')