from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import spirit_user
from flask_app.models import event_request


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Spirit_user:
    DB = 'spirit_page'

    def __init__( self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.yourevent = []
        self.admin = None




    @classmethod
    def save_reg_spirit_u(cls,data):
        query = "INSERT INTO spirit_users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_by_spirit_user_id(cls,data):
        query = "SELECT * FROM spirit_users WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_by_spirit_user_email(cls,data):
        query = "SELECT * FROM spirit_users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def all_spirit_user_events(cls,data):
        query = "SELECT * FROM spirit_users LEFT JOIN event_request ON spirit_users.id = event_request.spirit_users_id WHERE spirit_users.id = %(id)s;"   
        result = connectToMySQL(cls.DB).query_db(query,data)
        
        a_spirit = cls(result[0])
        for row in result:
            print(row,"*"*20)
            all_event_data = {
                "id": row["event_request.id"],
                "name": row["name"],
                "location": row["location"],
                "event_date": row["event_date"],
                "details": row["details"],
                "created_at": row["event_request.created_at"],
                "updated_at": row["event_request.updated_at"],
                "spirit_users_id": row["spirit_users_id"]
        }
            a_spirit.yourevent.append(event_request.Event_request(all_event_data))
        return a_spirit


    @staticmethod
    def validate_spirit_reg(user):
        is_valid = True 
        
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if not str.isalpha(user['first_name']):
            flash("First Name must contain alphabet characters.")
            is_valid = False
        if len(user['email']) < 2:
            flash("Email cannot be blank. At least 2 characters")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.")
            is_valid = False
        elif Spirit_user.get_by_spirit_user_email(user):
            flash("A user already exists for that email.")
            is_valid = False 
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False
        if not str.isalpha(user['last_name']):
            flash("Last Name must contain alphabet characters.")
            is_valid = False
        if len(user['email']) < 2:
            flash("Email must be at least 2 characters.")
            is_valid = False 
        if len(user['password']) < 8:
            flash("password must be 8 or greater.")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Password does not match")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_spirit_log(user):
        is_valid = True 
        if not Spirit_user.get_by_spirit_user_email(user):
            flash("Invalid email address.")
            is_valid = False
        if len(user['email']) < 2:
            flash("Email must be at least 2 characters.")
            is_valid = False
        if len(user['password']) < 8:
            flash("password must be 8 or greater.")
            is_valid = False
        return is_valid