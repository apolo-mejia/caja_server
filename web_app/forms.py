from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ssid_form(FlaskForm):
    ssid = StringField('SSID',validators=[DataRequired()])
    pass_word = StringField('PassKey', validators=[DataRequired()])
    submit = SubmitField('Registrar...')

class erase_network(FlaskForm):
    ssid = StringField('SSID', validators=[DataRequired()])
    id_net = StringField('Net_id', validators=[DataRequired()])
    submit = SubmitField('Olviar Red...')

class start_measure(FlaskForm):
    sensor_mac = StringField('MAC_sensor', validators=[DataRequired()])
    submit = SubmitField('Iniciar la toma')
