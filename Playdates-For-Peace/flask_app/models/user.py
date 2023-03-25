from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

db = "P4P"
class User:
    def __init__(self, db_data):
        self.id = db_data["id"]
        self.first_name = db_data["first_name"]
        self.last_name = db_data["last_name"]
        self.email = db_data["email"]
        self.password = db_data["password"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]


    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data["first_name"]) < 2:
            flash("First name required. Must have at least 2 characters.", "register")
            is_valid = False
        if len(data["last_name"]) < 2:
            flash("Last name required. Must have at least 2 characters.", "register")
            is_valid = False
        if len(data["email"]) == 0:
            flash("Email is required.", "register")
            is_valid = False
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email format.", "register")
            is_valid = False
        elif User.get_by_email(data):
            flash("Email already in use, please use a different email.", "register")
            is_valid = False
        if len(data["password"]) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if data["password"] != data["confirm_password"]:
            flash("Invalid, passwords do not match.", "register")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        if not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email/password.", "login")
            return False
        if len(data["email"]) == 0:
            flash("Email required.", "login")
            return False
        if len(data["password"]) == 0:
            flash("Password required.", "login")
            return False
        registered_user = User.get_by_email(data)
        if not registered_user:
            flash("Invalid email/password.", "login")
            return False
        if not bcrypt.check_password_hash(registered_user.password, data["password"]):
            flash("Invalid email/password.", "login")
            return False
        return registered_user
    
    @classmethod
    def register(cls, data):
        hashed_data = {
            "first_name" : data["first_name"],
            "last_name" : data["last_name"],
            "email" : data["email"],
            "password" : bcrypt.generate_password_hash(data["password"]),
        }
        query = """
                INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s,NOW(), NOW());
                """
        return connectToMySQL(db).query_db(query, hashed_data)

    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False
        return cls(result[0])
