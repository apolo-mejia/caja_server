from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField, SelectField, TextAreaField, BooleanField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField

# Aqui vamos con las listas
class mano_list(FlaskForm):
    soportes = SelectField('Marcas de Soportes', choices=[('soportes','Llevar lista'),('fag','FAG'),('ina','INA'),('skf','SKF'),
        ('snr','SNR'),('ntn','NTN'),('koy','KOYO'),('nsk','NSK'),('smt','SEALMASTER'),('lbt','LINK BELT'),('oth','Other..')])
    motores = SelectField('Marcas de Motores', choices=[('motores','Levar lista'),('weg','WEG'),('sms','SIEMENS'),('wth','Westinghouse')])
    rodamientos = SelectField('Marcas de Rodamientos', choices=[('rodamientos','Llevar lista'),('fag','FAG'),('ina','INA'),('skf','SKF'),
        ('snr','SNR'),('ntn','NTN'),('koy','KOYO'),('nsk','NSK'),('smt','SEALMASTER'),('lbt','LINK BELT'),('oth','Other..')])
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
    name = StringField('Nombre de la maquina', validators=[DataRequired('El campo: "Nombre de la máquina" es obligatorio para crear la máquina como entidad')])
    rpm_nom = DecimalField('Velocidad Nominal de Giro', validators=[
        DataRequired('El campo: "Velocidad Nominal de Giro" es obligatorio para crear la máquina como entidad')]
        )
    kw_nom = DecimalField('Potencia nominal ', validators=[DataRequired('El campo: "Potencia Nominal" es obligatorio para crear la máquina como entidad')], places=2)
    avatarf = StringField('Avatar')
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
    s_dim = SelectField('Dimensión', choices=[('ad','Adimencional'), ('power','Potencia'),('force','Fuerza'),('length','Distancia'),('speed','Velocidad'),('acc','Aceleración'),('mass','Masa')])
    s_units = SelectField('Únidades', choices=[('none','Ninguna'),('kV','Kilo-Vatios [kV]'),('N','Newton [N]'),('m','Metros [m]'),('mps','MetrosxSegundo [m/s]'),('mpss','MetrosxSegundos2  [m/s2]'),('kg','Kilogramo')])
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

# Creación / Edición de los campos especificos, el JSON
class update_part_json(FlaskForm):
    part_id = IntegerField('id de la parte a editar', validators=[DataRequired('Es necesario qu parte editar')])
    json_pack = TextAreaField('json_part', validators=[DataRequired('El valor es necesario validación')])
    submit_json = SubmitField('Actualizar parte...')
