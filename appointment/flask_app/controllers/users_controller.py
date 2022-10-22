from flask import render_template, redirect, request,session, flash
from flask_app import app

from flask_app.models.users import User
from flask_app.models.appointments import Appointment


from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.valida_usuario(request.form):
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password'])

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario)
    
    session['user_id'] = id 
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    #verificamos que el email exista en la base de datos
    user = User.get_by_email(request.form)

    if not user : 
        flash('E-mail not found', 'login')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Incorrect password', 'login')
        return redirect('/')
    
    session['user_id'] = user.id
    return redirect('dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    #queda pendiente validar si se haya iniciado sesion o registrado

    formulario ={ "id": session['user_id']}
    
    user = User.get_by_id(formulario)

    #Enviar todas las calificaciones
    appointments = Appointment.get_all()


    return render_template('dashboard.html', user=user, appointments=appointments)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
