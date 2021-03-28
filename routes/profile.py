from flask import render_template, session, redirect
from app import app

@app.route("/profile/<string:username>")
def get_profile(username):
  if "user" in session:
    return render_template("profile.html", username=username, back_link="")
  else:
    return redirect("/")