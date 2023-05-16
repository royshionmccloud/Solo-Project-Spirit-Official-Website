from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import spirit_user
from flask_app.models import event_request


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Event_request:
    DB = 'spirit_page'

    def __init__( self, data ):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.event_date = data['event_date']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.spirit_users_id = data['spirit_users_id']
        self.admin = None
        self.yourevent = []

    @classmethod
    def get_all_event_request(cls):
        query = """
                SELECT * FROM event_request JOIN spirit_users ON event_request.spirit_users_id = spirit_users.id;
                """
        results = connectToMySQL(cls.DB).query_db(query)
        request = []
        for row in results:
            print(row)
            a_request = cls(row)
            spirit_data = {
                "id" : row["spirit_users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password": row["password"],
                "created_at" : row["spirit_users.created_at"],
                "updated_at" : row["spirit_users.updated_at"],
                "spirit_users_id" : row["spirit_users_id"]
            }
            a_request.admin = spirit_user.Spirit_user(spirit_data)
            request.append(a_request)
        return request
    
    @classmethod
    def update_request(cls, data):
        query = """
                UPDATE event_request
                SET name = %(name)s,
                location = %(location)s,
                event_date = %(event_date)s,
                details = %(details)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.DB).query_db(query, data)
    

    @classmethod
    def save_request(cls, data):
        query = """
                INSERT INTO event_request (name, location, event_date, details, spirit_users_id)
                VALUES (%(name)s, %(location)s, %(event_date)s, %(details)s, %(spirit_users_id)s);
                """
        return connectToMySQL(cls.DB).query_db(query, data)       


    @classmethod
    def get_user_one_event_request(cls,data):
        query = """
                SELECT * FROM event_request JOIN spirit_users ON event_request.spirit_users_id = spirit_users.id 
                WHERE event_request.id = %(id)s;
                """
        result = connectToMySQL(cls.DB).query_db(query,data)
        
        look_result = result[0]
        a_spirit = cls(look_result)
    
        spirit_data = {
                "id": look_result['spirit_users.id'],
                "first_name": look_result['first_name'],
                "last_name": look_result['last_name'],
                "email": look_result['email'],
                "password": look_result['password'],
                "created_at": look_result['spirit_users.created_at'],
                "updated_at": look_result['spirit_users.updated_at'],
                "spirit_users_id": look_result['spirit_users_id']
        }
        a_spirit.admin = spirit_user.Spirit_user(spirit_data)
        return a_spirit 

    
    @classmethod
    def destroy_event(cls,data):
        query = """
                DELETE FROM event_request
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.DB).query_db(query,data)
    

    @staticmethod
    def spcheck(user):
        is_valid = True
        if len(user['name']) == 0:
            flash("Event name cannot be blank. Must be at least 5 characters")
            is_valid = False
        if len(user['name']) < 5:
            flash("Event name must be at least 5 characters")
            is_valid = False
        if len(user['location']) == 0:
            flash("Location cannot be blank. Must be at least 2 characters")
            is_valid = False
        if len(user['location']) < 2:
            flash("Location must be at least 2 characters")
            is_valid = False
        # if len(user['details']) == 0:
        #     flash("Details cannot be blank. Must be at least 50 characters")
        #     is_valid = False
        # if len(user['details']) > 50:
        #     flash("Details must be at least 50 characters")
        #     is_valid = False
        if user['event_date'] == '':
            flash("Please input a date.")
            is_valid = False
        return is_valid 