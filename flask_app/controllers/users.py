from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, post, message, avatar, comment, profile, like
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)


#*---------------------------------DISPLAY ROUTES-------------------------------------

@app.route("/")
def index():
    if "user_id" in session:
        return redirect ("/dashboard/")
    return render_template("index.html")


@app.route("/welcome/")
def choose():
    avatars = avatar.Avatar.get_all_avatars()
    return render_template("choose.html", avatars = avatars)


@app.route("/dashboard/")
def dash():
    if "user_id" in session:
        data = {"id" : session['user_id']}
        curr_user = profile.Profile.get_prof_userav(data)
        all_posts = post.Post.get_all()
        all_comments = comment.Comment.get_all_comments()
        all_users = user.User.get_all_with_av()
        return render_template("dashboard.html", all_users = all_users, curr_user = curr_user, all_comments=all_comments, all_posts = all_posts)
    return redirect("/")

@app.route("/logout/")
def logout():
    data = {"id": session['user_id']}
    user.User.offline(data)
    session.clear()
    return redirect("/")


#*---------------------------------ACTION ROUTES-------------------------------------


@app.route("/register/", methods=['POST'])
def register():
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "username" : request.form["username"],
        "email" : request.form["email"],
        "password" : request.form["password"],
        "avatar_id" : request.form["avatar_id"],
        "conf_password" : request.form["conf_password"]
    }
    if user.User.validate_user(data):
        person = user.User.create_user(data)
        session["user_id"] = person
        return redirect("/dashboard/")
    return redirect("/welcome/")


@app.route("/login/", methods=['POST'])
def login():
    data = {
        "email": request.form["email"],
        "password" : request.form["password"]
        }
    person = user.User.get_by_email(data)
    if not person:
        flash("Invalid Login!")
        return redirect("/")
    if not bcrypt.check_password_hash(person.password, data['password']):
        flash("Invalid Login!")
        return redirect("/") 
    session["user_id"]= person.id
    data = {"id": person.id}
    user.User.online(data)
    return redirect("/dashboard/")