from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import profile, user, avatar
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import date
import math
import json

#*---------------------------------DISPLAY ROUTES-------------------------------------
@app.route("/profile/<int:id>")
def user_profile(id):
    if "user_id" in session:
        user_data = {"id": session["user_id"]}
        curr_user = user.User.get_by_id(user_data)
        user_prof = profile.Profile.get_by_id(user_data)
        data = {"id": id}
        profile_user = user.User.get_by_id(data)
        curr_id = {"id": profile_user.avatar_id}
        current_avatar = avatar.Avatar.getav_by_id(curr_id)
        curr_profile = profile.Profile.get_by_id(data)
        birthday = curr_profile.birthday
        birth_date = birthday.strftime("%m/%d")
        bday = birthday.strftime("%Y")
        now = date.today().strftime("%Y")
        now = int(now)
        bday = int(bday)
        age = math.floor(now - bday)
        return render_template("profile.html", profile_user = profile_user, current_avatar = current_avatar, curr_profile = curr_profile, birth_date=birth_date, age=age, curr_user=curr_user, user_prof = user_prof)
    return redirect("/")


@app.route("/profile/setup")
def prof_setup():
    if "user_id" in session:
        data = {"id" : session["user_id"]}
        curr_user = user.User.get_by_id(data)
        return render_template("profilesetup.html", curr_user = curr_user)
    return redirect("/")


#*---------------------------------ACTION ROUTES-------------------------------------

@app.route("/create/profile/<int:id>", methods=['POST'])
def create_prof(id):
    data = {
        "birthday" : request.form["birthday"],
        "hometown" : request.form["hometown"],
        "location" : request.form["location"],
        "fav_show" : request.form["fav_show"],
        "fav_movie" : request.form["fav_movie"],
        "fav_quote" : request.form["fav_quote"],
        "about_me" : request.form["about_me"],
        "user_id" : id,
    }
    profile.Profile.create_prof(data)
    return redirect("/dashboard/")
