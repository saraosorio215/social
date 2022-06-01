from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import post, user, avatar, like
from flask_app.config.mysqlconnection import connectToMySQL

#*---------------------------------DISPLAY ROUTES-------------------------------------



@app.route("/edit/post/<int:id>")
def edit_post(id):
    user_data = {"id" : session['user_id']}
    person = user.User.get_by_id(user_data)
    data = {"id" : id}
    info = post.Post.get_by_id(data)
    avatar_data = {"id" : person.avatar_id}
    current_avatar = avatar.Avatar.getav_by_id(avatar_data)
    return render_template("editpost.html", info = info, person=person, current_avatar = current_avatar)



@app.route("/delete/post/<int:id>")
def deleting_post(id):
    data = {"id" : id}
    post.Post.delete_post(data)
    return redirect ("/dashboard/")


@app.route("/like/post/<int:id>")
def like_post(id):
    data = {"id" : id}
    post.Post.update_likes(data)
    all_data = { 
        "post_id": id,
        "user_id": session["user_id"]
    }
    like.Like.add_like(all_data)
    return redirect("/dashboard/")


#*---------------------------------ACTION ROUTES-------------------------------------


@app.route("/new_post/", methods=['POST'])
def new_post():
    data = {
        "title" : request.form["title"],
        "content" : request.form["content"],
        "user_id" : session['user_id']
    }
    post.Post.create_post(data)
    return redirect("/dashboard/")



@app.route("/update/post/<int:id>", methods=['POST'])
def update(id):
    data = {
        "id" : id,
        "title" : request.form["title"],
        "content" : request.form["content"]
    }
    post.Post.edit_post(data)
    return redirect("/dashboard/")


