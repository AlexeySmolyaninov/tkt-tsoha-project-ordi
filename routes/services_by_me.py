from app import app
from flask import render_template

@app.route("/servicesByMe")
def servicesByMe():
  return render_template(
    "services_by_me.html",
    back_link="/profile"
    )