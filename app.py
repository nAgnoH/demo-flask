from datetime import timedelta
from os import path

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(seconds=30)

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form["name"]
        session.permanent = True
        if user_name:
            session["user"] = user_name
            found_user = User.query.filter_by(name=user_name).first()
            if found_user:
                session["email"] = found_user.email
            else:
                user = User(user_name, "temp@gmail.com")
                db.session.add(user)
                db.session.commit()
            flash("Login Successful!", "info")
            return redirect(url_for("user", user=user_name))
            user = User(user_name, "temp@gmail.com")
            db.session.add(user)
            db.session.commit()
            flash("Login Successful!", "info")
            return redirect(url_for("user", user=user_name))
    if "user" in session:
        name = session["user"]
        flash("Login Successful!", "info")
        return redirect(url_for("user", user=user_name))

    return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        name = session["user"]
        if request.method == "POST":
            if not request.form["email"] and request.form["name"]:
                User.query.filter_by(
                    name=name
                ).delete()  # delete user from database if email is empty
                db.session.commit()
                flash("User was deleted!")
                return redirect(url_for("logout"))
            else:
                email = request.form["email"]
                session["email"] = email
                found_user = User.query.filter_by(name=name).first()
                found_user.email = email
                db.session.commit()
                flash("Email was saved!")

        elif "email" in session:
            email = session["email"]
        return render_template("user.html")
    else:
        flash("You haven't logged in!", "info")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("Logout", "info")
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    if not path.exists("users.db"):
        db.create_all(app=app)
        print("Database created successfully!")
    app.run(debug=True)
