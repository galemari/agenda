from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

class User:

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def valida_usuario(formulario):
    #formulario = DICCIONARIO con todos los names y valores que el usuario ingresa
        es_valido = True

    #Validamos que el nombre tenga al menos 3 caracteres
        if len(formulario['first_name']) < 3:
            flash('Nombre debe tener al menos 3 ')
            es_valido = False
        #Verificamos que las contraseñas coincidan
        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseñas NO coinciden', 'registro')
            es_valido = False
        
        #Revisamos que email tenga el formato correcto -> Expresiones Regulares
        if not EMAIL_REGEX.match(formulario['email']):
            flash('E-mail inválido', 'registro')
            es_valido = False
        
    #Consultamos si existe el correo electrónico
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('appointments').query_db(query, formulario)
        if len(results) >= 1:
            flash('E-mail registrado previamente', 'registro')
            es_valido = False
        
        return es_valido
    
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('appointments').query_db(query, formulario)
        return result 
    @classmethod
    def get_by_email(cls, formulario):
        query="SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('appointments').query_db(query, formulario) 
        if len(result) < 1: #significa que mi lista esta vacia y no existe ese email
            return False
        else:
            #regresa una lista con un regisro correspondiente al usuario de ese email
            user = cls(result[0])
            return user

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('appointments').query_db(query,formulario)
        user = cls(result[0])
        return user