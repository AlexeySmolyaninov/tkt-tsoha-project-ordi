from app import app
from flask import render_template, request, redirect, session
from services.services import create_project, get_users, username_to_userid, get_projects_by_me, get_projects_to_me, get_project, get_tasks, create_task, update_task as update_task_s, update_project as update_project_s

@app.route("/servicesByMe")
def services_by_me():
  if "user" in session:
    username = session["user"]
    provider_id = username_to_userid(username)
    users = get_users(username)
    projects = get_projects_by_me(provider_id)
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
  if "user" in session:
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
  else:
    return redirect("/")

@app.route("/servicesToMe")
def services_to_me():
  if "user" in session:
    my_username = session["user"]
    my_id = username_to_userid(my_username)
    projects = get_projects_to_me(my_id)
    return render_template(
      "services_to_me.html",
      back_link = "/profile",
      projects = projects 
    )
  else:
    return redirect("/")

@app.route("/servicesByMe/projects/<int:project_id>")
def view_project(project_id):
  if "user" in session:
    project = get_project(project_id)
    tasks = get_tasks(project_id)
    return render_template(
      "project_view_for_creator.html",
      back_link="/servicesByMe",
      project = project,
      tasks = tasks
    )
  else:
    return redirect("/")

@app.route("/task", methods=["POST"])
def new_task():
  if "user" in session:
    title = request.form["title"]
    status = request.form["status"]
    project_id = request.form["project_id"]
    create_task(title, status, project_id)
    return redirect("/servicesByMe/projects/" + str(project_id))
  else:
    return redirect("/")

@app.route("/updateProject", methods=["POST"])
def update_project():
  print(request.form)
  project_id = request.form["project_id"]
  title = request.form["project"]
  description = request.form["description"]
  amount = request.form["amount"]
  update_project_s(project_id, title, description, amount)
  return redirect("/servicesByMe/projects/"+str(project_id))


@app.route("/updateTask", methods=["POST"])
def update_task():
  if "user" in session:
    project_id = request.form["project_id"]
    task_id = request.form["task_id"]
    title = request.form["task"]
    status = request.form["status"]
    update_task_s(title, status, task_id)
    return redirect("/servicesByMe/projects/"+str(project_id))
  else:
    return redirect("/")
