from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import Usuario

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')  
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2 = PasswordField('Repetir Contraseña', validators=[DataRequired(), EqualTo('password')])
    tipo_documento = SelectField('Tipo Documento', choices=[('CC', 'Cédula'), ('CE', 'Cédula Extranjería'), ('TI', 'Tarjeta Identidad'), ('PASAPORTE', 'Pasaporte')])
    documento = StringField('Número Documento', validators=[DataRequired()])
    nombres = StringField('Nombres', validators=[DataRequired()])
    apellidos = StringField('Apellidos', validators=[DataRequired()])
    genero = SelectField('Género', choices=[('F', 'Femenino'), ('M', 'Masculino'), ('OTRO', 'Otro')])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = Usuario.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Por favor usa un nombre de usuario diferente.')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor usa un email diferente.')

class CitaForm(FlaskForm):
    procedimiento_id = SelectField('Procedimiento', coerce=int, validators=[DataRequired()])
    medico_id = SelectField('Médico', coerce=int, validators=[DataRequired()])
    # CAmbio aquí: Usar DateTimeLocalField y el formato para HTML5 datetime-local
    fecha_hora = DateTimeLocalField('Fecha y Hora', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    duracion_estimada = IntegerField('Duración (minutos)', default=30, validators=[DataRequired()])
    notas = TextAreaField('Notas Adicionales')
    
    # ... (campos adicionales para crear paciente)
    tipo_sangre = StringField('Tipo de Sangre')
    alergias = TextAreaField('Alergias')
    medicamentos_actuales = TextAreaField('Medicamentos Actuales')
    historial_estetica_previo = TextAreaField('Historial Estético Previo')
    motivo_consulta = TextAreaField('Motivo de Consulta')
    referido_por = StringField('Referido Por')

    submit = SubmitField('Agendar Cita')

    