from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user, post

class Like():
    def __init__(self, data):
        self.id = data['id']
        self.post_id = data['post_id']
        self.user_id = data['user_id']

    @classmethod
    def add_like(cls, data):
        query = "INSERT INTO likes (post_id, user_id) VALUES (%(post_id)s, %(user_id)s);"
        return connectToMySQL("contact").query_db(query, data)

