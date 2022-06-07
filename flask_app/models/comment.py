from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user, post, avatar


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
        query = "SELECT * FROM comments JOIN users ON users.id = comments.user_id JOIN avatars ON avatars.id = users.avatar_id ORDER BY comments.created_at DESC;"
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
                    "online" : row["online"]
                }
                avatar_data = {
                    "id": row["avatars.id"],
                    "name" : row["name"],
                    "file_path" : row["file_path"],
                    "created_at" : row["avatars.created_at"],
                    "updated_at" : row["avatars.updated_at"]
                }
                temp_user.maker = user.User(user_data)
                temp_user.creator = avatar.Avatar(avatar_data)
                comments.append(temp_user)
        return comments

    @classmethod
    def add_like(cls, data):
        query = "UPDATE comments SET like_count = like_count + 1 WHERE id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)


    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)