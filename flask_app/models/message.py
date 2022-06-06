from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user, avatar

class Message():
    def __init__(self, data):
        self.id = data["id"]
        self.subject = data["subject"]
        self.msg_text = data["msg_text"]
        self.user_id = data["user_id"]
        self.recipient_id = data["recipient_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.isRead = data["isRead"]

    
    @classmethod
    def create_msg(cls, data):
        mysql = connectToMySQL("contact")
        query = "INSERT INTO messages (subject, msg_text, user_id, recipient_id) VALUES (%(subject)s, %(msg_text)s, %(user_id)s, %(recipient_id)s);"
        return mysql.query_db(query, data)


    @classmethod
    def get_all_inbox(cls):
        query = "SELECT * FROM messages JOIN users ON users.id = messages.user_id JOIN avatars ON avatars.id = users.avatar_id;"
        results = connectToMySQL("contact").query_db(query)
        messages = []
        if results:
            for row in results:
                temp_msg = cls(row)
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
                temp_msg.maker = user.User(user_data)
                temp_msg.creator = avatar.Avatar(avatar_data)
                messages.append(temp_msg)
        return messages


    @classmethod
    def get_all_outbox(cls):
        query = "SELECT * FROM messages JOIN users ON users.id = messages.recipient_id JOIN avatars ON avatars.id = users.avatar_id;"
        results = connectToMySQL("contact").query_db(query)
        messages = []
        if results:
            for row in results:
                temp_delivery = cls(row)
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
                temp_delivery.maker = user.User(user_data)
                temp_delivery.creator = avatar.Avatar(avatar_data)
                messages.append(temp_delivery)
        return messages


    @classmethod
    def delete_msg(cls, data):
        query = "DELETE FROM messages WHERE id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)

    
    @classmethod
    def one_msg(cls, data):
        query = "SELECT * FROM messages WHERE id = %(id)s;"
        result = connectToMySQL("contact").query_db(query, data)
        if result:
            return cls(result[0])


    @classmethod
    def all_msgs(cls, data):
        query = "SELECT * FROM messages WHERE (user_id = %(user_id)s) AND (recipient_id = %(recipient_id)s);"
        return connectToMySQL("contact").query_db(query, data)


    @classmethod
    def mark_read(cls, data):
        query = "UPDATE messages SET isRead = '1' WHERE messages.id = %(id)s;"
        return connectToMySQL("contact").query_db(query, data)