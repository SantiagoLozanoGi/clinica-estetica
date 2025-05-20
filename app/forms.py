from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import Usuario

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')  # ✅ Nombre correcto y único
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
    fecha_hora = DateTimeField('Fecha y Hora', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    duracion_estimada = IntegerField('Duración (minutos)', default=30, validators=[DataRequired()])
    notas = TextAreaField('Notas Adicionales')
    submit = SubmitField('Agendar Cita')
    