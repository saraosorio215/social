from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

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
    def upd_prof(cls, data):
        query = "UPDATE profiles SET birthday = %(birthday)s, hometown = %(hometown)s, location = %(location)s, fav_show = %(fav_show)s, fav_movie = %(fav_movie)s, fav_quote = %(fav_quote)s, about_me = %(about_me)s WHERE id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)

    @classmethod
    def create_prof(cls, data):
        query = "INSERT INTO profiles (birthday, hometown, location, fav_show, fav_movie, fav_quote, about_me, user_id) VALUES (%(birthday)s, %(hometown)s, %(location)s, %(fav_show)s, %(fav_movie)s, %(fav_quote)s, %(about_me)s, %(user_id)s);"
        return connectToMySQL("contact").query_db(query, data)