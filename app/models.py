from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='paciente')
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    persona = db.relationship('Persona', backref='usuario', uselist=False, lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Persona(db.Model):
    __tablename__ = 'personas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True)
    tipo_documento = db.Column(db.String(10), nullable=False)
    documento = db.Column(db.String(20), unique=True, nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(10))
    fecha_nacimiento = db.Column(db.Date)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    ciudad = db.Column(db.String(50), default='Ibagué')
    departamento = db.Column(db.String(50), default='Tolima')
    foto_perfil = db.Column(db.String(255))
    medico = db.relationship('Medico', backref='persona', uselist=False, lazy=True)
    paciente = db.relationship('Paciente', backref='persona', uselist=False, lazy=True)

class Medico(db.Model):
    __tablename__ = 'medicos'
    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'), unique=True, nullable=False)
    especialidad_principal = db.Column(db.String(100), nullable=False)
    otras_especialidades = db.Column(db.Text)
    registro_medico = db.Column(db.String(50), unique=True, nullable=False)
    horario_atencion = db.Column(db.Text)
    biografia = db.Column(db.Text)
    citas = db.relationship('Cita', backref='medico', lazy=True)
    tratamientos = db.relationship('Tratamiento', backref='medico', lazy=True)

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'), unique=True, nullable=False)
    tipo_sangre = db.Column(db.String(5))
    alergias = db.Column(db.Text)
    medicamentos_actuales = db.Column(db.Text)
    historial_estetica_previo = db.Column(db.Text)
    motivo_consulta = db.Column(db.Text)
    referido_por = db.Column(db.String(100))
    citas = db.relationship('Cita', backref='paciente', lazy=True)
    pagos = db.relationship('Pago', backref='paciente', lazy=True)

class Procedimiento(db.Model):
    __tablename__ = 'procedimientos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    duracion_min = db.Column(db.Integer, default=30)
    costo_base = db.Column(db.Numeric(10, 2))
    requerimientos = db.Column(db.Text)
    contraindicaciones = db.Column(db.Text)
    cuidados_posteriores = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    citas = db.relationship('CitaProcedimiento', backref='procedimiento', lazy=True)
    tratamientos = db.relationship('TratamientoProcedimiento', backref='procedimiento', lazy=True)

class Tratamiento(db.Model):
    __tablename__ = 'tratamientos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    sesiones = db.Column(db.Integer, default=1)
    intervalo_sesiones = db.Column(db.Integer)
    costo_total = db.Column(db.Numeric(10, 2))
    medico_responsable = db.Column(db.Integer, db.ForeignKey('medicos.id'))
    citas = db.relationship('Cita', backref='tratamiento', lazy=True)
    procedimientos = db.relationship('TratamientoProcedimiento', backref='tratamiento', lazy=True)

class TratamientoProcedimiento(db.Model):
    __tablename__ = 'tratamiento_procedimientos'
    tratamiento_id = db.Column(db.Integer, db.ForeignKey('tratamientos.id'), primary_key=True)
    procedimiento_id = db.Column(db.Integer, db.ForeignKey('procedimientos.id'), primary_key=True)
    orden = db.Column(db.Integer)

class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    tratamiento_id = db.Column(db.Integer, db.ForeignKey('tratamientos.id'))
    fecha_hora = db.Column(db.DateTime, nullable=False)
    duracion_estimada = db.Column(db.Integer, default=30)
    estado = db.Column(db.String(20), default='programada')
    notas = db.Column(db.Text)
    sala = db.Column(db.String(50))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    procedimientos = db.relationship('CitaProcedimiento', backref='cita', lazy=True)
    pagos = db.relationship('Pago', backref='cita', lazy=True)

class CitaProcedimiento(db.Model):
    __tablename__ = 'cita_procedimientos'
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'), primary_key=True)
    procedimiento_id = db.Column(db.Integer, db.ForeignKey('procedimientos.id'), primary_key=True)
    observaciones = db.Column(db.Text)

class Pago(db.Model):
    __tablename__ = 'pagos'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'))
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    metodo = db.Column(db.String(20), nullable=False)
    referencia = db.Column(db.String(100))
    estado = db.Column(db.String(20), default='pendiente')
    observaciones = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

@login.user_loader
def load_user(id):
    return Usuario.query.get(int(id))