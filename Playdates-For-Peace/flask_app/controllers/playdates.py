from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.playdate import Playdate
from flask_app import app

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    registered_user = User.get_by_id({"id":session['user_id']})
    if not registered_user:
        return redirect("/logout")
    return render_template("dashboard.html", registered_user=registered_user, playdates=Playdate.get_all())

@app.route("/create")
def create_playdate():
    if "user_id" not in session:
        return redirect("/login")
    registered_user = User.get_by_id({"id":session['user_id']})
    if not registered_user:
        return redirect("/logout")
    return render_template("add-playdate.html", registered_user=registered_user)

@app.route("/create/add", methods=["POST"])
def add_playdate():
    if "user_id" not in session:
        return redirect("/login")
    if not Playdate.validate_playdate(request.form):
        return redirect("/create")
    
    data = {
        "event" : request.form["event"],
        "date" : request.form["date"],
        "address" : request.form["address"],
        "details" : request.form["details"],
        "user_id" : session["user_id"]
    }
    Playdate.create_playdate(data)
    return redirect ("/dashboard")

@app.route("/details/<int:id>")
def details(id):
    if "user_id" not in session:
        return redirect("/login")
    registered_user = User.get_by_id({"id":session['user_id']})
    if not registered_user:
        return redirect("/logout")
    return render_template("details.html", registered_user=registered_user, playdate=Playdate.get_by_id({"id":id}))

@app.route("/edit/<int:id>")
def edit_playdate(id):
    if "user_id" not in session:
        return redirect("/login")
    registered_user = User.get_by_id({"id":session['user_id']})
    if not registered_user:
        return redirect("/logout")
    return render_template("edit-playdate.html", registered_user=registered_user, playdate=Playdate.get_by_id({"id":id}))

@app.route("/edit/<int:id>", methods=["POST"])
def alter_playdate(id):
    if "user_id" not in session:
        return redirect("/login")
    if not Playdate.validate_playdate(request.form):
        return redirect(f"/edit/{id}")
    data = {
        "id" : id,
        "event" : request.form["event"],
        "date" : request.form["date"],
        "address" : request.form["address"],
        "details" : request.form["details"],
        "user_id" : session["user_id"]
    }
    Playdate.edit_playdate(data)
    return redirect(f"/edit/{id}")

@app.route("/delete/<int:id>")
def destroy_playdate(id):
    if "user_id" not in session:
        return redirect("/login")
    data = {
        "id" : id
    }
    Playdate.delete_playdate(data)
    return redirect("/dashboard")