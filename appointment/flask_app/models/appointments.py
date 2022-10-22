from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from datetime import datetime #manipula fechas

class Appointment:
    def __init__(self, data):
        self.id=data['id']
        self.tasks=data['tasks']
        self.date=data['date']
        self.status=data['status']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id= data['user_id']
    
    @staticmethod #recibe la lista deformulario para validar los datos
    def valida_appointment(formulario):
        es_valido=True

        if formulario['tasks'] =='':
            flash('tasks no puede ser vacio', 'appointments') #flashrecoge por seccion los datos de errores
            es_valido = False 
        
        if formulario['date'] =='':
            flash('Set a date', 'appointments')
            es_valido = False
        else:
            fecha_obj = datetime.strptime(formulario['date'], '%Y-%m-%d') #transformamos un texto a formato de fecha
            hoy = datetime.now() #me da la fecha de hoy
            if hoy > fecha_obj:
                flash('Should be a future date', 'appointments')
                es_valido = False

        if formulario['status'] =='':
            flash('Status cant be empty', 'appointments')
            es_valido = False

        
        
        return es_valido

    @classmethod
    def save (cls, formulario):
        query = 'INSERT INTO appointments (tasks,date,status,user_id) VALUES (%(tasks)s,%(date)s,%(status)s,%(user_id)s)'
        result = connectToMySQL('appointments').query_db(query, formulario)
        return result 

    @classmethod 
    def get_all(cls):
        query="SELECT * FROM appointments"
        results = connectToMySQL('appointments').query_db(query) #lista de diccionarios
        appointments = []

        for appointment in results:
            appointments.append(cls(appointment)) #1

        return appointments
    
    @classmethod
    def get_by_id(cls, formulario):
        query="SELECT * FROM appointments WHERE id = %(id)s"
        result = connectToMySQL('appointments').query_db(query, formulario)
        appointment = cls(result[0])
        return appointment

    @classmethod
    def update(cls,formulario):
        query = "UPDATE appointments SET tasks=%(tasks)s, date=%(date)s, status=%(status)s, user_id=%(user_id)s WHERE id=%(id)s"
        result = connectToMySQL('appointments').query_db(query, formulario)
        return result
    
    @classmethod
    def delete(cls,formulario):
        query = "DELETE FROM appointments WHERE id = %(id)s"
        result = connectToMySQL('appointments').query_db(query, formulario)
        return result