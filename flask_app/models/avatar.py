from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user, avatar

class Avatar():
    def __init__(self, data):
        self.id = data["id"]
        self.file_path = data["file_path"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    @classmethod
    def get_all_avatars(cls):
        query = "SELECT * FROM avatars"
        return connectToMySQL("contact").query_db(query)


    @classmethod
    def getav_by_id(cls, data):
        query = "SELECT * FROM avatars WHERE id = %(id)s;"
        result = connectToMySQL("contact").query_db(query, data)
        if result:
            return cls(result[0])