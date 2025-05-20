from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.routes import bp
from app.models import Usuario, Persona, Paciente
from app.forms import LoginForm, RegistrationForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('procedimientos.listar'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña inválidos', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('procedimientos.listar'))
    
    return render_template('auth/login.html', title='Iniciar Sesión', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('procedimientos.listar'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Usuario(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        
        persona = Persona(
            usuario_id=user.id,
            tipo_documento=form.tipo_documento.data,
            documento=form.documento.data,
            nombres=form.nombres.data,
            apellidos=form.apellidos.data,
            genero=form.genero.data,
            telefono=form.telefono.data
        )
        db.session.add(persona)
        
        paciente = Paciente(persona_id=persona.id)
        db.session.add(paciente)
        
        db.session.commit()
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Registro', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('procedimientos.listar'))