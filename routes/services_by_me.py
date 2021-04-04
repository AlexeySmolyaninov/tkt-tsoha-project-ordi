from app import app
from flask import render_template, request, redirect, session
from services.services import create_project, get_users, username_to_userid, get_projects

@app.route("/servicesByMe")
def services_by_me():
  if "user" in session:
    username = session["user"]
    provider_id = username_to_userid(username)
    users = get_users(username)
    projects = get_projects(provider_id)
    return render_template(
      "services_by_me.html",
      back_link="/profile",
      users = users,
      projects = projects
    )
  else:
    return redirect("/")

@app.route("/newProject", methods=["POST"])
def create_new_project():
  title = request.form["title"]
  desc = request.form["description"]
  provider_username = session["user"]
  client = request.form["client"]
  amount = request.form["amount"]
  payed = False
  status = request.form["status"]
  display = True
  provider_id = username_to_userid(provider_username)
  create_project(title, desc, provider_id, int(client), amount, payed, status, display)
  return redirect("/servicesByMe")