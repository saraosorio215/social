from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user, post


class Comment():
    def __init__(self, data):
        self.id = data["id"]
        self.comment_text = data["comment_text"]
        self.post_id = data["post_id"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.like_count = data['like_count']


    @classmethod
    def add_comment(cls, data):
        query = "INSERT INTO comments (comment_text, post_id, user_id) VALUES (%(comment_text)s, %(post_id)s, %(user_id)s);"
        return connectToMySQL("contact").query_db(query, data)


    @classmethod
    def get_all_comments(cls):
        query = "SELECT * FROM comments JOIN users ON users.id = comments.user_id;"
        results = connectToMySQL("contact").query_db(query)
        comments = []
        if results:
            for row in results:
                temp_user = cls(row)
                user_data = {
                    "id" : row["users.id"],
                    "first_name" : row["first_name"],
                    "last_name" : row["last_name"],
                    "username" : row["username"],
                    "email" : row["email"],
                    "password" : row["password"],
                    "avatar_id" : row["avatar_id"],
                    "created_at" : row["users.created_at"],
                    "updated_at" : row["users.updated_at"],
                    "like_count" : row["like_count"]
                }
                temp_user.creator = user.User(user_data)
                comments.append(temp_user)
        return comments