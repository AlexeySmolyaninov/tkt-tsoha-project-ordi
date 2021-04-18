from app import app
from flask import render_template, request, redirect, session, url_for
from services.services import create_project, get_users, username_to_userid, \
  get_projects_by_me, get_projects_to_me, get_project, get_tasks, create_task, \
  update_task as update_task_s, update_project as update_project_s, \
  has_provider_rights, delete_task as delete_task_s, delete_project as delete_project_s, \
  update_project_status, has_client_rights, has_money, create_transaction, \
  hide_project as hide_project_s
from services.message import get_messages

@app.route("/servicesByMe")
def services_by_me():
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

@app.route("/servicesToMe")
def services_to_me():
  my_username = session["user"]
  my_id = username_to_userid(my_username)
  projects = get_projects_to_me(my_id)
  print(request.args)
  return render_template(
    "services_to_me.html",
    back_link = "/profile",
    projects = projects
  )

@app.route("/servicesByMe/projects/<int:project_id>")
def view_project_creator(project_id):
  if has_provider_rights(session["user_id"], project_id):
    project = get_project(project_id)
    tasks = get_tasks(project_id)
    chat_messages = get_messages(project_id)
    return render_template(
      "project_view_for_creator.html",
      back_link="/servicesByMe",
      project = project,
      tasks = tasks,
      chat_messages = chat_messages[::-1]
    )
  else:
    return redirect("/")

@app.route("/servicesToMe/projects/<int:project_id>")
def view_project_client(project_id):
  client_id = session["user_id"]
  if has_client_rights(client_id, int(project_id)):
    project = get_project(project_id)
    tasks = get_tasks(project_id)
    chat_messages = get_messages(project_id)
    message = None
    if "message" in request.args:
      message = request.args["message"]
    return render_template(
      "project_view_for_client.html",
      project = project,
      tasks = tasks,
      chat_messages = chat_messages[::-1],
      back_link = "/servicesToMe",
      message = message
    )
  else:
    redirect("/")

@app.route("/task", methods=["POST"])
def new_task():
  project_id = request.form["project_id"] 
  user_id = session["user_id"]
  if has_provider_rights(user_id, int(project_id)):
    title = request.form["title"]
    status = request.form["status"]
    create_task(title, status, project_id)
    update_project_status(project_id)
    return redirect("/servicesByMe/projects/" + str(project_id))
  else:
    return redirect("/")

@app.route("/updateProject", methods=["POST"])
def update_project():
  project_id = request.form["project_id"]
  user_id = session["user_id"]
  if has_provider_rights(user_id, int(project_id)):
    title = request.form["project"]
    description = request.form["description"]
    amount = request.form["amount"]
    update_project_s(project_id, title, description, amount)
    return redirect("/servicesByMe/projects/"+str(project_id))
  else:
    return redirect("/")


@app.route("/updateTask", methods=["POST"])
def update_task():
  project_id = request.form["project_id"]
  user_id = session["user_id"]
  if has_provider_rights(user_id, int(project_id)):
    task_id = request.form["task_id"]
    title = request.form["task"]
    status = request.form["status"]
    update_task_s(title, status, task_id)
    update_project_status(int(project_id))
    return redirect("/servicesByMe/projects/"+str(project_id))
  else:
    return redirect("/")

@app.route("/deleteTask", methods=["POST"])
def delete_task():
  project_id = request.form["project_id"]
  user_id = session["user_id"]
  if has_provider_rights(user_id, int(project_id)):
    task_id = request.form["task_id"]
    delete_task_s(int(task_id))
    update_project_status(int(project_id))
    return redirect("/servicesByMe/projects/"+str(project_id))
  else:
    return redirect("/")

@app.route("/deleteProject", methods=["POST"])
def delete_project():
  project_id = request.form["project_id"]
  user_id = session["user_id"]
  if has_provider_rights(user_id, int(project_id)):
    delete_project_s(int(project_id))
    return redirect("/servicesByMe")
  else:
    return redirect("/")

@app.route("/pay", methods=["POST"])
def pay():
  project_id = request.form["project_id"]
  client_id = session["user_id"]
  if has_client_rights(client_id, project_id):
    amount = request.form["amount"]
    provider = request.form["provider"]
    if has_money(client_id, amount):

      create_transaction(project_id, provider, client_id, int(amount))
      return redirect("/servicesToMe/projects/" + str(project_id))
    else:
      return redirect(url_for(
        "view_project_client",  project_id=str(project_id),
        message = "You don't have enough credits"
        )
      )
  else:
    return redirect("/")

@app.route("/hideProject", methods=["POST"])
def hide_project():
  project_id = request.form["project_id"]
  user_id = session["user_id"]
  if has_provider_rights(user_id, project_id):
    hide_project_s(project_id)
    return redirect("/servicesByMe")
  elif has_client_rights(user_id, project_id):
    hide_project_s(project_id)
    return redirect("/servicesToMe")
  else:
    return redirect("/")