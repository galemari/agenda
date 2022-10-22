from flask import render_template, redirect, request,session, flash
from flask_app import app

from flask_app.models.users import User
from flask_app.models.appointments import Appointment

@app.route('/new/appointment')
def new_appointment():
    if 'user_id' not in session:
        return redirect('/')
    #queda pendiente validar si se haya iniciado sesion o registrado

    formulario ={ "id": session['user_id']}
    
    user = User.get_by_id(formulario)

    return render_template('new_appointment.html', user=user)

@app.route('/create/appointment',methods=['POST'])
def create_appointment():
    if 'user_id' not in session:
        return redirect('/')
    
    #validacion appointment
    #if not Appointment.valida_appointment(request.form):
    #   return redirect('/new/appointment')

    #Guardar appointment
    Appointment.save(request.form)

    return redirect('/dashboard')

@app.route('/edit/appointment/<int:id>')
def edit_appointment(id):
    if 'user_id' not in session:
        return redirect('/')
    #validar si se haya iniciado sesion o registrado

    formulario ={ "id": session['user_id']}
    
    user = User.get_by_id(formulario)

    #cual es el appointment que se va a editar
    formulario_appointment = {"id": id}
    appointment = Appointment.get_by_id(formulario_appointment)
    return render_template('edit_appointment.html', user=user, appointment=appointment)


@app.route('/update/appointment', methods=['POST'])
def update_appointment():
    if 'user_id' not in session:
        return redirect('/')
    
    #Validacion
    if not Appointment.valida_appointment(request.form):
        return redirect('/edit/appointment/'+request.form['id']) 
    
    Appointment.update(request.form)

    return redirect('/dashboard')

@app.route('/delete/appointment/<int:id>')
def delete_appointment(id):
    if 'user_id' not in session:
        return redirect('/')

    formulario = {"id":id}
    Appointment.delete(formulario)
    return redirect('/dashboard')
