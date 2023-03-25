from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "P4P"
class Playdate:
    def __init__(self, db_data):
        self.id = db_data["id"]
        self.event = db_data["event"]
        self.date = db_data["date"]
        self.address = db_data["address"]
        self.details = db_data["details"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]
        self.user_id = db_data["user_id"]
        self.rsvp = None
        

# VALIDATIONS
    @staticmethod
    def validate_playdate(data):
        is_valid = True
        if len(data["event"]) < 5:
            flash("Event name of playdate is required, must be at least 5 characters.", "playdate")
            is_valid = False
        if data["date"] == "":
            flash("Date & time are required, please select a date / time.", "playdate")
            is_valid = False
        if len(data["address"]) < 5:
            flash("Address of playdate is required, must be at least 5 characters.", "playdate")
            is_valid = False
        if len(data["details"]) < 5:
            flash("Details are required, must be at least 5 characters. Please give more information.", "playdate")
            is_valid = False
        return is_valid

# CREATE
    @classmethod
    def create_playdate(cls, data):
        query = """
                INSERT INTO playdates (event, date, address, details, created_at, updated_at, user_id)
                VALUES (%(event)s, %(date)s, %(address)s, %(details)s, NOW(), NOW(), %(user_id)s);
                """
        return connectToMySQL(db).query_db(query, data)

# READ
    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM playdates
                JOIN users ON playdates.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        playdates = []
        for row in results:
            this_event = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : "",
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
                
            }
            this_event.rsvp = user.User(user_data)
            playdates.append(this_event)
        return playdates

    @classmethod
    def get_by_id(cls, data):
        query = """
                SELECT * FROM playdates
                JOIN users ON playdates.user_id = users.id
                WHERE playdates.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False
        result = result[0]
        the_event = cls(result)
        user_data = {
                "id" : result["users.id"],
                "first_name" : result["first_name"],
                "last_name" : result["last_name"],
                "email" : result["email"],
                "password" : "",
                "created_at" : result["users.created_at"],
                "updated_at" : result["users.updated_at"]
            }
        the_event.rsvp = user.User(user_data)
        return the_event

    @classmethod
    def get_by_user(cls, data):
        query = """
                SELECT *
                FROM playdates
                JOIN users ON playdates.user_id = users.id
                WHERE playdates.user_id = %(user_id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        playdates = []
        for row in results:
            this_event = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : "",
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"],
            }
            this_event.rsvp = user.User(user_data)
            playdates.append(this_event)
        return playdates
    
# UPDATE
    @classmethod
    def edit_playdate(cls, data):
        query = """
                UPDATE playdates
                SET 
                event = %(event)s, 
                date = %(date)s, 
                address = %(address)s, 
                details = %(details)s,
                updated_at = NOW()
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query, data)

# DELETE
    @classmethod
    def delete_playdate(cls, data):
        query = "DELETE FROM playdates WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)