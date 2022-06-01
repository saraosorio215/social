from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import avatar
bcrypt=Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User():
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.avatar_id = data["avatar_id"]
        self.online = data["online"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    @classmethod
    def create_user(cls, data):
        hash_browns = bcrypt.generate_password_hash(data["password"])
        hashed_dict = {
            "first_name" : data["first_name"],
            "last_name" : data["last_name"],
            "username" : data["username"],
            "email" : data["email"],
            "avatar_id" : data["avatar_id"],
            "password" : hash_browns
        }
        query = "INSERT INTO users (first_name, last_name, username, email, avatar_id, password) VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(avatar_id)s, %(password)s);"
        return connectToMySQL("contact").query_db(query, hashed_dict)


    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL("contact").query_db(query, data)
        if result:
            return cls(result[0])


    @classmethod
    def get_by_user(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s"
        result = connectToMySQL("contact").query_db(query, data)
        if result:
            return cls(result[0])


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("contact").query_db(query, data)
        if result:
            return cls(result[0])


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        return connectToMySQL("contact").query_db(query)

    @classmethod
    def offline(cls, data):
        query = "UPDATE users SET online = (0) WHERE id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)

    @classmethod
    def online(cls, data):
        query = "UPDATE users SET online = (1) WHERE id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)

    @classmethod
    def get_user_prof(cls, data):
        query = "SELECT * FROM users LEFT JOIN profiles ON profiles.user_id = users.id WHERE users.id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)


    @classmethod
    def get_all_with_av(cls):
        query = "SELECT * FROM users LEFT JOIN avatars ON users.avatar_id = avatars.id"
        results = connectToMySQL("contact").query_db(query)
        avatars = []
        if results:
            for row in results:
                temp_avatar = cls(row)
                avatar_data = {
                    "id" : row["avatars.id"],
                    "name" : row["name"],
                    "file_path" : row["file_path"],
                    "created_at" : row["avatars.created_at"],
                    "updated_at" : row["avatars.updated_at"]
                }
                temp_avatar.maker = avatar.Avatar(avatar_data)
                avatars.append(temp_avatar)
        return avatars



    @staticmethod
    def validate_user(data):
        is_valid=True
        if data['first_name'] == "":
            flash("Please enter a first name")
            is_valid=False
        if len(data['first_name']) < 2:
            flash("First Name must be at least 3 characters long!")
            is_valid = False
        if data['last_name'] == "":
            flash("Please enter a last name")
            is_valid=False
        if len(data['last_name']) < 2:
            flash("Last Name must be at least 3 characters long!")
            is_valid = False
        if data['username'] == "":
            flash("Please enter a username")
            is_valid = False
        if len(data['username']) < 4:
            flash("Username must be at least 5 characters long!")
            is_valid = False
        check = User.get_by_user(data)
        if check:
            flash("Username already in use!")
            is_valid = False
        if data['email'] == "":
            flash("Please enter an email")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        user = User.get_by_email(data)
        if user:
            flash("Email is already in use!")
            is_valid = False
        if data['password'] == "":
            flash("Please enter a password")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be 8 characters long")
            is_valid = False
        if data['password'] != data['conf_password']:
            flash("Passwords must match!")
            is_valid = False
        return is_valid