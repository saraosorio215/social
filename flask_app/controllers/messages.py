from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import message, user, avatar, profile
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
        current_prof = profile.Profile.get_by_id(user_data)
        return render_template("inbox.html", person=person, choices=choices, msgs=msgs, deliveries = deliveries, current_avatar = current_avatar, current_prof = current_prof)


@app.route("/unsend-msg/<int:id>")
def delete(id):
    data = {"id" : id}
    message.Message.delete_msg(data)
    return redirect("/inbox/")


@app.route("/readmsg/<int:id>")
def read_msg(id):
    data = {"id" : id}
    current_msg = message.Message.one_msg(data)
    message.Message.mark_read(data)
    user_data = {"id" : session['user_id']}
    current_user = user.User.get_one_with_av(user_data)
    sender_id = {"id": current_msg.user_id}
    msg_sender = user.User.get_one_with_av(sender_id)
    msg_data = {
        "user_id": session["user_id"],
        "recipient_id": current_msg.user_id
    }
    rev_msg_data = {
        "user_id": current_msg.user_id,
        "recipient_id": session["user_id"]
    }
    all_msgs = message.Message.all_msgs(msg_data)
    rev_all_msgs = message.Message.all_msgs(rev_msg_data)
    return render_template("viewmsg.html", current_user = current_user, current_msg = current_msg, msg_sender = msg_sender, all_msgs = all_msgs, rev_all_msgs = rev_all_msgs)

@app.route("/viewmsg/<int:id>")
def view_msg(id):
    data = {"id" : id}
    current_msg = message.Message.one_msg(data)
    user_data = {"id" : session['user_id']}
    current_user = user.User.get_one_with_av(user_data)
    sender_id = {"id": current_msg.user_id}
    msg_sender = user.User.get_one_with_av(sender_id)
    msg_data = {
        "user_id": session["user_id"],
        "recipient_id": current_msg.user_id
    }
    rev_msg_data = {
        "user_id": current_msg.user_id,
        "recipient_id": session["user_id"]
    }
    all_msgs = message.Message.all_msgs(msg_data)
    rev_all_msgs = message.Message.all_msgs(rev_msg_data)
    return render_template("viewmsg.html", current_user = current_user, current_msg = current_msg, msg_sender = msg_sender, all_msgs = all_msgs, rev_all_msgs = rev_all_msgs)


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


