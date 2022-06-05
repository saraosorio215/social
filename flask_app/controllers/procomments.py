from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import procomment



#*----------------------------------ACTION ROUTES-------------------------------------

@app.route("/new_procomm/", methods=["POST"])
def new_procomm():
    data = {
        "comment_title" : request.form["comment_title"],
        "comment_text" : request.form["comment_text"],
        "profile_id" : request.form["profile_id"],
        "user_id" : request.form["user_id"]
    }
    procomment.Procomment.add_procomm(data)
    return redirect("/dashboard/")
