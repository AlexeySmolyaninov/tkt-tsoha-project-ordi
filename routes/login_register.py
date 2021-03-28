from flask import render_template, request, redirect, session
from app import app
import services.login_register as loginRegister

@app.route("/", methods=["GET", "POST"])
def login():
  if request.method == "GET":
    if "user" in session: 
      return redirect("/profile/" + "alexsmol")
    else:
      return render_template("login.html")
  else:
    user_name = request.form["username"]
    password = request.form["password"]
    result = loginRegister.login(user_name, password)
    if result["logedIn"] == True:
      session["user"] = user_name
      return redirect("/profile/" + user_name)
    else:
      return render_template("login.html", message=result["message"]) 

@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "GET":
    return render_template("register.html")
  else:
    first_name = request.form["firstName"]
    surname = request.form["surname"]
    user_name = request.form["userName"]
    password_1 = request.form["password1"]
    password_2 = request.form["password2"]
    result = loginRegister.register(
      first_name,
      surname,
      user_name,
      password_1,
      password_2
    )
    if result["isRegistered"] == True:
      return redirect("/")
    else:
      session["user"] = user_name
      return redirect("/profile/" + user_name)

@app.route("/logout")
def logout():
  del session["user"]
  return redirect("/")
  