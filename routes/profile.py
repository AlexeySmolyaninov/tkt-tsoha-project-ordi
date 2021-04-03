from flask import render_template, session, redirect
from app import app

@app.route("/profile")
def get_profile():
  if "user" in session:
    username = session["user"]
    return render_template("profile.html", username=username, back_link="")
  else:
    return redirect("/")