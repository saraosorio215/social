from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import avatar, user


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
        query = "SELECT * FROM prof_comments WHERE profile_id = %(id)s ORDER BY prof_comments.created_at DESC;"
        return connectToMySQL("contact").query_db(query, data)

    @classmethod
    def add_procomm(cls, data):
        query = "INSERT INTO prof_comments (comment_title, comment_text, profile_id, user_id) VALUES (%(comment_title)s, %(comment_text)s, %(profile_id)s, %(user_id)s);"
        return connectToMySQL("contact").query_db(query, data)

    @classmethod
    def get_procomm_userav(cls, data):
        query = "SELECT * FROM prof_comments JOIN users ON prof_comments.user_id = users.id JOIN avatars ON avatars.id = users.avatar_id WHERE prof_comments.profile_id = %(id)s ORDER BY prof_comments.created_at DESC;"
        results = connectToMySQL("contact").query_db(query, data)
        alldata = []
        if results:
            for row in results:
                temp_users = cls(row)
                user_data = {
                    "id": row["users.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "username": row["username"],
                    "email": row["email"],
                    "password": row["password"],
                    "avatar_id": row["avatar_id"],
                    "online": row["online"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"],
                }
                avatar_data = {
                    "id": row["avatars.id"],
                    "name" : row["name"],
                    "file_path" : row["file_path"],
                    "created_at" : row["avatars.created_at"],
                    "updated_at" : row["avatars.updated_at"]
                }
                temp_users.maker = user.User(user_data)
                temp_users.creator = avatar.Avatar(avatar_data)
                alldata.append(temp_users)
        return alldata


    @classmethod
    def delete_procomm(cls, data):
        query = "DELETE FROM prof_comments WHERE id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)