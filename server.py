from flask import Flask
from flask_app import app
from flask_app.controllers import users, posts, messages, comments

if __name__ == "__main__":
    app.run(debug=True) 