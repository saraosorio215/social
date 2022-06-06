from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import avatar, user

class Profile():
    def __init__(self, data):
        self.id = data['id']
        self.birthday = data['birthday']
        self.hometown = data['hometown']
        self.location = data['location']
        self.fav_show = data['fav_show']
        self.fav_movie = data['fav_movie']
        self.fav_quote = data['fav_quote']
        self.about_me = data['about_me']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM profiles WHERE user_id = %(id)s;"
        result = connectToMySQL("contact").query_db(query, data)
        if result:
            return cls(result[0])

    @classmethod
    def get_prof_userav(cls, data):
        query = "SELECT * FROM profiles JOIN users ON profiles.user_id = users.id JOIN avatars ON users.avatar_id = avatars.id WHERE profiles.user_id = %(id)s;"
        result = connectToMySQL("contact").query_db(query, data)
        alldata = []
        if result:
            temp_avatar = cls(result[0])
            avatar_data = {
                "id" : result[0]["avatars.id"],
                "name" : result[0]["name"],
                "file_path" : result[0]["file_path"],
                "created_at" : result[0]["avatars.created_at"],
                "updated_at" : result[0]["avatars.updated_at"]
            }
            user_data = {
                "id": result[0]["users.id"],
                "first_name": result[0]["first_name"],
                "last_name": result[0]["last_name"],
                "username": result[0]["username"],
                "email": result[0]["email"],
                "password": result[0]["password"],
                "avatar_id": result[0]["avatar_id"],
                "online": result[0]["online"],
                "created_at": result[0]["users.created_at"],
                "updated_at": result[0]["users.updated_at"]
            }
            temp_avatar.maker = avatar.Avatar(avatar_data)
            temp_avatar.creator = user.User(user_data)
            alldata.append(temp_avatar)
        return alldata

    @classmethod
    def upd_prof(cls, data):
        query = "UPDATE profiles SET birthday = %(birthday)s, hometown = %(hometown)s, location = %(location)s, fav_show = %(fav_show)s, fav_movie = %(fav_movie)s, fav_quote = %(fav_quote)s, about_me = %(about_me)s WHERE id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)

    @classmethod
    def create_prof(cls, data):
        query = "INSERT INTO profiles (birthday, hometown, location, fav_show, fav_movie, fav_quote, about_me, user_id) VALUES (%(birthday)s, %(hometown)s, %(location)s, %(fav_show)s, %(fav_movie)s, %(fav_quote)s, %(about_me)s, %(user_id)s);"
        return connectToMySQL("contact").query_db(query, data)