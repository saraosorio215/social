from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import message, user, avatar, comment
from flask_app.config.mysqlconnection import connectToMySQL


#*---------------------------------DISPLAY ROUTES-------------------------------------


@app.route("/like/comm/<int:id>")
def like_comm(id):
    data = {"id": id}
    comment.Comment.add_like(data)
    return redirect("/dashboard/")






#*----------------------------------ACTION ROUTES-------------------------------------


@app.route("/new-comment/", methods=["POST"])
def new_comm():
    data = {
        "comment_text" : request.form["comment_text"],
        "post_id" : request.form["post_id"],
        "user_id" : session["user_id"]
    }
    comment.Comment.add_comment(data)
    return redirect("/dashboard/")