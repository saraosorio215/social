from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash


class Procomment():
    def __init__(self,data):
        self.id = data["id"]
        self.comment_title = data["comment_title"]
        self.comment_text = data["comment_text"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.profile_id = data["profile_id"]
        self.user_id = data["user_id"]

    @classmethod
    def get_all_procomms(cls, data):
        query = "SELECT * FROM prof_comments WHERE profile_id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)

    @classmethod
    def add_procomm(cls, data):
        query = "INSERT INTO prof_comments (comment_title, comment_text, profile_id, user_id) VALUES (%(comment_title)s, %(comment_text)s, %(profile_id)s, %(user_id)s);"
        return connectToMySQL("contact").query_db(query, data)