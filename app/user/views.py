from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user,logout_user, login_required
from app.user.models import User
from app.extensions import db, bcrypt


blueprint =  Blueprint("user", __name__, url_prefix="/user")

@blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        repeat_password = request.form.get("repeat_password")
        if password != repeat_password:
            flash(message="Password not match", category="register_error")
            return redirect(url_for("user.register"))
        new_user = User(username=username, password=bcrypt.generate_password_hash(password).decode("utf-8"))
        #Fill object model without constructor in model
        # new_user.username = username
        # new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("user.login"))
    return render_template("user/register.html")

@blueprint.route("/login", methods=["GET", "POST"])
def login():
    #Early return
    if request.method == "GET":
        return render_template("user/login.html")
    username = request.form.get("username")
    password = request.form.get("password")
    find_user = User.query.filter_by(username=username).first()
    if not find_user:
        flash("Username or Password not found", category="login_error")
        return  redirect(url_for("user.login"))
    if not bcrypt.check_password_hash(find_user.password, password):
        flash("Username or Password not found", category="login_error")
        return redirect(url_for("user.login"))

    login_user(find_user)
    return redirect(url_for("user.home"))

@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))

@blueprint.route("/home")
@login_required
def home():
 return render_template("home.html")

