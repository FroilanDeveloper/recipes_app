from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one(cls, data):
        query =  "SELECT * "
        query += "FROM users "
        query += "WHERE email = %(email)s;"

        result = connectToMySQL(DATABASE).query_db(query,data)

        if len(result) > 0:
            return cls(result[0])
        else:
            return None

    @classmethod
    def create(cls, data):
        query =  "INSERT into users(first_name, last_name, email, password) "
        query += "VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result

    @staticmethod
    def validate_register(data):
        isValid = True
        if data['first_name'] == "":
            flash("You must provide your first name.", "error_register_first_name" )
            isValid = False
        if len(data['first_name']) < 2:
            flash("Your first name must have at least two characters.", "error_register_first_name" )
            isValid = False
        if data['last_name'] == "":
            flash("You must provide your last name.", "error_register_last_name" )
            isValid = False
        if len(data['last_name']) < 2:
            flash("Your last name must have at least two characters.", "error_register_last_name" )
            isValid = False
        if data['email'] == "":
            flash("You must provide your email.", "error_register_email" )
            isValid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Please provide a valid email.", "error_register_email")
            isValid = False
        if data['password'] == "":
            flash("You must provide a password.", "error_register_password")
            isValid = False
        if len(data['password']) < 4:
            flash("Password must be at least 4 characters long.", "error_register_password")
            isValid = False
        if data['password_confirmation'] != data['password']:
            flash("Your password confirmationan doesn't match.", "error_register_password_confirmation")
        return isValid

    @staticmethod
    def validate_session():
        if "user_id" not in session:
            return False
        else:
            return True
