from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import message, user, avatar
from flask_app.config.mysqlconnection import connectToMySQL


#*---------------------------------DISPLAY ROUTES-------------------------------------



@app.route("/inbox/")
def send():
    if "user_id" in session:
        user_data = {"id" : session['user_id']}
        person = user.User.get_by_id(user_data)
        choices = user.User.get_all()
        msgs = message.Message.get_all_inbox()
        deliveries = message.Message.get_all_outbox()
        avatar_data = {"id" : person.avatar_id}
        current_avatar = avatar.Avatar.getav_by_id(avatar_data)
        return render_template("inbox.html", person=person, choices=choices, msgs=msgs, deliveries = deliveries, current_avatar = current_avatar)


@app.route("/unsend-msg/<int:id>")
def delete(id):
    data = {"id" : id}
    message.Message.delete_msg(data)
    return redirect("/inbox/")




#*----------------------------------ACTION ROUTES-------------------------------------

@app.route("/send-msg/", methods=['POST'])
def outbox():
    data = {
        "subject" : request.form["subject"],
        "msg_text" : request.form["msg_text"],
        "user_id" : session["user_id"],
        "recipient_id" : request.form["recipient_id"]
    }
    message.Message.create_msg(data)
    return redirect("/inbox/")


