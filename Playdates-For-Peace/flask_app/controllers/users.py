from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User

@app.route("/")
def index():
    return redirect("/login")

@app.route("/register", methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect("/")
    user_id = User.register(request.form)
    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route("/loggedin", methods=["POST"])
def loggedin():
    registered_user = User.validate_login(request.form)
    if not registered_user:
        return redirect("/login")
    session["user_id"] = registered_user.id
    return redirect("/dashboard")

@app.route("/login")
def login():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("index.html")


@app.route("/logout")
def logout():
    if "user_id" in session:
        session.pop("user_id")
    return redirect("/login")
