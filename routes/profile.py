from flask import render_template, session, redirect
from app import app

@app.route("/profile/<string:username>")
def get_profile(username):
  if "user" in session:
    return render_template("profile.html", username=username)
  else:
    return redirect("/")

@app.route("/wallet")
def wallet():
  if "user" in session:
    return render_template("wallet.html")
  else:
    return redirect("/")
