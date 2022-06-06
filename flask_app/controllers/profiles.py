from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import profile, user, avatar, procomment
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import date
import math

#*---------------------------------DISPLAY ROUTES-------------------------------------
@app.route("/profile/<int:id>")
def user_profile(id):
    if "user_id" in session:
        user_data = {"id": session["user_id"]}
        curr_user = profile.Profile.get_prof_userav(user_data)
        data = {"id": id}
        curr_prof = profile.Profile.get_prof_userav(data)
        com_data = {"id" : curr_prof[0].id}
        birthday = curr_prof[0].birthday
        birth_date = birthday.strftime("%m/%d")
        age = int(date.today().strftime("%Y")) - int(birthday.strftime("%Y"))
        all_coms = procomment.Procomment.get_procomm_userav(com_data)
        return render_template("profile.html", curr_prof = curr_prof, birth_date=birth_date, age=age, curr_user=curr_user, all_coms = all_coms)
    return redirect("/")


@app.route("/profile/setup")
def prof_setup():
    if "user_id" in session:
        data = {"id" : session["user_id"]}
        curr_user = user.User.get_by_id(data)
        return render_template("profilesetup.html", curr_user = curr_user)
    return redirect("/")


@app.route("/edit/profile/")
def edit_prof():
    data = {"id": session["user_id"]}
    curr_prof = profile.Profile.get_prof_userav(data)
    return render_template("editprofile.html", curr_prof = curr_prof)


#*---------------------------------ACTION ROUTES-------------------------------------

@app.route("/create/profile/<int:id>", methods=['POST'])
def create_prof(id):
    profuser_id = int(id);
    data = {
        "birthday" : request.form["birthday"],
        "hometown" : request.form["hometown"],
        "location" : request.form["location"],
        "fav_show" : request.form["fav_show"],
        "fav_movie" : request.form["fav_movie"],
        "fav_quote" : request.form["fav_quote"],
        "about_me" : request.form["about_me"],
        "user_id" : profuser_id
    }
    profile.Profile.create_prof(data)
    return redirect("/dashboard/")

@app.route("/update/profile/<int:id>", methods=['POST'])
def update_prof(id):
    data = {
        "birthday" : request.form["birthday"],
        "hometown" : request.form["hometown"],
        "location" : request.form["location"],
        "fav_show" : request.form["fav_show"],
        "fav_movie" : request.form["fav_movie"],
        "fav_quote" : request.form["fav_quote"],
        "about_me" : request.form["about_me"],
        "id" : id
    }
    profile.Profile.upd_prof(data)
    return redirect("/dashboard/")