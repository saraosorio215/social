from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user, like, avatar

class Post():
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.like_count = data['like_count']


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id JOIN avatars ON users.avatar_id = avatars.id ORDER BY posts.created_at DESC;"
        results = connectToMySQL("contact").query_db(query)
        posts = []
        if results:
            for row in results:
                temp_post = cls(row)
                user_data = {
                    "id" : row["users.id"],
                    "first_name" : row["first_name"],
                    "last_name" : row["last_name"],
                    "username" : row["username"],
                    "email" : row["email"],
                    "password" : row["password"],
                    "avatar_id" : row["avatar_id"],
                    "online" : row["online"],
                    "created_at" : row["users.created_at"],
                    "updated_at" : row["users.updated_at"],
                    "like_count" : row["like_count"]
                }
                avatar_data = {
                    "id": row["avatars.id"],
                    "name" : row["name"],
                    "file_path" : row["file_path"],
                    "created_at" : row["avatars.created_at"],
                    "updated_at" : row["avatars.updated_at"]
                }
                temp_post.maker = user.User(user_data)
                temp_post.creator = avatar.Avatar(avatar_data)
                posts.append(temp_post)
        return posts


    
    @classmethod
    def create_post(cls, data):
        query = "INSERT INTO posts (title, content, user_id) VALUES (%(title)s, %(content)s, %(user_id)s);"
        return connectToMySQL("contact").query_db(query, data)


    @classmethod
    def edit_post(cls, data):
        query = "UPDATE posts SET title = %(title)s, content = %(content)s WHERE id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)

    @classmethod
    def update_likes(cls, data):
        query = "UPDATE posts SET like_count = like_count + 1 WHERE id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        result = connectToMySQL("contact").query_db(query, data)
        if result:
            return cls(result[0])

    
    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)

    @classmethod
    def get_likes(cls, data):
        query = "SELECT user_id FROM likes WHERE post_id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)